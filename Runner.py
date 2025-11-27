import re

class Runner:

    # Attributes
    def __init__(self):
        self.Elements = []
        self.Diameter = 0.0

    # Read runner properties from abaqus input file
    @staticmethod
    def read_runner(file_path, elements_list):

        # Initialize output
        runners = []

        # Open the file and read lines
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Process each line
            lines_list = list(lines)
            xi = 0
            while xi < len(lines_list):

                # Get current line
                line = lines_list[xi]

                # Check for beam section. Also get the element sets involved
                if line.strip().upper().startswith('*BEAM SECTION,'):
                    
                    # Get the element set name from the line
                    elset_name_match = re.search(r'ELSET\s*=\s*([^,\s]+)', line, re.IGNORECASE)
                    if elset_name_match:
                        elset_name = elset_name_match.group(1)
                    else:
                        raise ValueError("ELSET not found in BEAM SECTION line.")

                    # Find all elements in this elset and assign to runner
                    runner = Runner()
                    elset_elements = [elem for elem in elements_list if elem.Elset_Name == elset_name]
                    runner.Elements = elset_elements

                    # Incmrement counter, since next line has diameter info
                    xi += 1
                    line = lines_list[xi]
                    runner.Diameter = 2 * float(line.strip())

                    # Add to output list
                    runners.append(runner)

                # Increment counter
                xi += 1

        return runners
    
    # Method to write runner info to SALT file
    def write_salt(self, file):

        # Iterate through each runner element
        for elem in self.Elements:

            # Get the two coordinates of the element
            # Convert to m for SALT
            x1 = elem.Nodes[0].X / 1000.0
            y1 = elem.Nodes[0].Y / 1000.0
            z1 = elem.Nodes[0].Z / 1000.0
            x2 = elem.Nodes[1].X / 1000.0
            y2 = elem.Nodes[1].Y / 1000.0
            z2 = elem.Nodes[1].Z / 1000.0

            # Create the key points
            points_content = f"""
            var point1 = solver::KptAdd({x1}, {y1}, {z1});
            var point2 = solver::KptAdd({x2}, {y2}, {z2});
            """

            # Create the curves
            curves_content = f"""
            var curve1 = solver::CrvAdd(point1, point2);
            """

            # Assign the circular runner property
            property_content = f"""
            solver::CrvSetProps(curve1, {{
                propId = "Circular Runner";
                D = {self.Diameter / 1000.0};
            }});
            """

            # Write content to the file
            file.write("\n")
            file.write("{")
            file.write("\n")
            file.write(points_content)
            file.write(curves_content)
            file.write(property_content)
            file.write("\n")
            file.write("}")
            file.write("\n")