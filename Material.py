class Material:

    # Attributes:
    def __init__(self):

        self.Name = ""
        self.Vf = 0.0  # Fiber volume fraction
        self.K11 = 0.0  # Permeability in 1 direction
        self.K22 = 0.0  # Permeability in 2 direction

    # Read materials from abaqus input file and return a list of Material objects
    @staticmethod
    def read_materials(file_path):

        # Intialize output
        materials = []

        # Open the file and read lines
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Process each line
            lines_list = list(lines)
            xi = 0
            while xi < len(lines_list):

                # Get current line
                line = lines_list[xi]
                
                #Check for material definition line
                if line.strip().upper().startswith('*MATERIAL,'):
                    
                    # Get material name from the line
                    material_name = line.split('=')[1].strip()

                    # Ensure it is of the correct type
                    # Advance to next line since material type is defined there
                    xi += 1
                    line = lines_list[xi]
                    if not 'LAMINA' in line.strip().upper():
                        xi += 1
                        continue  # Skip non-orthotropic materials
                    
                    # Read material properties until the next asterisk line
                    for xj in range(xi + 1, len(lines_list)):

                        # Get current line within material definitions
                        line = lines_list[xj]

                        # If there is a new asterisk line, break
                        # Also realign xi to continue from here
                        if line.startswith('*'):
                            xi = xj - 1
                            break

                        # Split line and create Material object
                        parts = line.strip().split(',')
                        if len(parts) >= 2:
                            material = Material()
                            material.Name = material_name
                            material.K11 = float(parts[0])
                            material.K22 = float(parts[1])
                            material.Vf = float(parts[3])

                    # Append material to output list
                    materials.append(material)

                # Increment counter
                xi += 1

        return materials