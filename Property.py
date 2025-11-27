import re
from Ply import Ply
import math
import Material

class Property:
    # Attributes:
    def __init__(self):

        self.Elset = None
        self.Plies = None

    # Read properties from abaqus input file and return a list of Property objects
    @staticmethod
    def read_properties(file_path, materials_list, elements_list):

        # Initialize output
        properties = []

        # Open the file and read lines
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Process each line
            lines_iter = iter(lines)
            for line in lines_iter:

                # Check for ply definition line
                if line.strip().upper().startswith('*SHELL SECTION,'):

                    # Get the element set name from the line
                    elset_name_match = re.search(r'ELSET\s*=\s*([^,\s]+)', line, re.IGNORECASE)
                    if elset_name_match:
                        elset_name = elset_name_match.group(1)
                    else:
                        raise ValueError("ELSET not found in SHELL SECTION line.")
                    
                    # Create Property object and initialise plies list
                    prop = Property()
                    prop.Plies = []
                    
                    # Find all elements in this elset and assign to property
                    elset_elements = [elem for elem in elements_list if elem.Elset_Name == elset_name]
                    prop.Elset = elset_elements
                    
                    # Read ply definitions until the next asterisk line
                    # The ply definition line is already skipped
                    for line in lines_iter:
                        if line.startswith('*'):
                            break
                        parts = line.strip().split(',')
                        if len(parts) >= 4:
                            ply = Ply()
                            ply.Thickness = float(parts[0])
                            ply.Angle = float(parts[3])
                            ply.Elset_Name = elset_name

                            # Find material by name
                            material_name = parts[2].strip()
                            mat = [m for m in materials_list if m.Name == material_name]
                            if not mat:
                                raise ValueError(f"Material '{material_name}' not found for ply.")
                            ply.Material = mat[0]
                            
                            # Add to property plies
                            prop.Plies.append(ply)
                    
                    # Add property to output list
                    properties.append(prop)

        return properties
    
    # Compute propoerty plies into a single effective property
    def compute_effective_property(self):

        # Intialize some arrays
        ts = []
        k11s = []
        k22s = []
        vfs = []

        # Iterate through plies and compute effective rotated property
        for ply in self.Plies:

            # Transform the permeability values based on the ply angle
            rad = math.radians(ply.Angle)
            mat = ply.Material
            k11 = mat.K11
            k22 = mat.K22
            k11_transformed = (k11 * (math.cos(rad))**2 + k22 * (math.sin(rad))**2)
            k22_transformed = (k11 * (math.sin(rad))**2 + k22 * (math.cos(rad))**2)

            # Append material propeorties to global arrays
            ts.append(ply.Thickness)
            vfs.append(mat.Vf)
            k11s.append(k11_transformed)
            k22s.append(k22_transformed)

        # Compute total thickness
        total_thickness = sum(ts)

        # Compute weighted average properties
        if total_thickness > 0:
            weighted_k11 = sum(k * t for k, t in zip(k11s, ts)) / total_thickness
            weighted_k22 = sum(k * t for k, t in zip(k22s, ts)) / total_thickness
            weighted_vf = sum(v * t for v, t in zip(vfs, ts)) / total_thickness
        else:
            weighted_k11 = 0.0
            weighted_k22 = 0.0
            weighted_vf = 0.0

        # Create new material
        effective_material = Material.Material()
        effective_material.K11 = weighted_k11
        effective_material.K22 = weighted_k22
        effective_material.Vf = weighted_vf

        # Create new ply to hold effective property
        effective_ply = Ply()
        effective_ply.Thickness = total_thickness
        effective_ply.Material = effective_material

        # Create new property to hold effective ply
        effective_property = Property()
        effective_property.Elset = self.Elset
        effective_property.Plies = [effective_ply]

        return effective_property
    
    # Write property information to SALT file
    def write_salt_property(self, file):

        # Compute effective property
        effective_property = self.compute_effective_property()
        elems = effective_property.Elset

        # Create a surface in RTM Worx for each element in the elset
        for elem in elems:

            # Get the four corner coordinates of the element
            # Convert to m for SALT
            x1 = elem.Nodes[0].X / 1000.0
            y1 = elem.Nodes[0].Y / 1000.0
            z1 = elem.Nodes[0].Z / 1000.0
            x2 = elem.Nodes[1].X / 1000.0
            y2 = elem.Nodes[1].Y / 1000.0
            z2 = elem.Nodes[1].Z / 1000.0
            x3 = elem.Nodes[2].X / 1000.0
            y3 = elem.Nodes[2].Y / 1000.0
            z3 = elem.Nodes[2].Z / 1000.0

            # For four noded elements
            if len(elem.Nodes) == 4:
                x4 = elem.Nodes[3].X / 1000.0
                y4 = elem.Nodes[3].Y / 1000.0
                z4 = elem.Nodes[3].Z / 1000.0

                # Create the key points
                points_content = f"""
                var point1 = solver::KptAdd({x1}, {y1}, {z1});
                var point2 = solver::KptAdd({x2}, {y2}, {z2});
                var point3 = solver::KptAdd({x3}, {y3}, {z3});
                var point4 = solver::KptAdd({x4}, {y4}, {z4});
                """

                # Create the curves
                curves_content = f"""
                var curve1 = solver::CrvAdd(point1, point2);
                var curve2 = solver::CrvAdd(point2, point3);
                var curve3 = solver::CrvAdd(point3, point4);
                var curve4 = solver::CrvAdd(point4, point1);
                """

                # Create the surface
                surface_content = f"""
                var surface = solver::SrfAdd(curve1, curve2, curve3, curve4);
                """
            else:

                # For three noded elements, create a triangular surface
                points_content = f"""
                var point1 = solver::KptAdd({x1}, {y1}, {z1});
                var point2 = solver::KptAdd({x2}, {y2}, {z2});
                var point3 = solver::KptAdd({x3}, {y3}, {z3});
                """

                # Create the curves
                curves_content = f"""
                var curve1 = solver::CrvAdd(point1, point2);
                var curve2 = solver::CrvAdd(point2, point3);
                var curve3 = solver::CrvAdd(point3, point1);
                """

                # Create the surface
                surface_content = f"""
                var surface = solver::SrfAdd(curve1, curve2, curve3);
                """
                
            # Set the surface properties
            properties_content = f"""
            solver::SrfSetProps(surface, {{
                propId = "RTM Thin Shell";
                H = {effective_property.Plies[0].Thickness / 1000.0};
                Vf = {effective_property.Plies[0].Material.Vf};
                phi = 0.0;
                k11 = {effective_property.Plies[0].Material.K11};
                k22 = {effective_property.Plies[0].Material.K22};
                r1x = 1; r1y = 0; r1z = 0;
            }});
            """

            # Write all contents to the file
            file.write("\n")
            file.write("{")
            file.write("\n")
            file.write(points_content)
            file.write(curves_content)
            file.write(surface_content)
            file.write(properties_content)
            file.write("\n")
            file.write("}")
            file.write("\n")

            
            