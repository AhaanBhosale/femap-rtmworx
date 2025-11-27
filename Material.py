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
            lines_iter = iter(lines)
            for line in lines_iter:
                
                #Check for material definition line
                if line.strip().upper().startswith('*MATERIAL,'):
                    
                    # Get material name from the line
                    material_name = line.split('=')[1].strip()

                    # Ensure it is of the correct type
                    line = next(lines_iter)
                    if not 'LAMINA' in line.strip().upper():
                        continue  # Skip non-orthotropic materials
                    
                    # Read material properties until the next asterisk line
                    for line in lines_iter:
                        if line.startswith('*'):
                            break
                        parts = line.strip().split(',')
                        if len(parts) >= 2:
                            material = Material()
                            material.Name = material_name
                            material.K11 = float(parts[0])
                            material.K22 = float(parts[1])
                            material.Vf = float(parts[3])

                    
                    # Append material to output list
                    materials.append((material_name, material))

        return materials
    

# Debugging
file_dir = "C:\\Users\\AhaanBhosalePontisEn\\Documents\\Pontis\\Pontis INTERNAL - Documents\\Engineering Tools en Technology\\Flow Simulation - RTMWorx\\Scripting\\FEMAP to RTMWorx\\FEMAP Files\\Surface with Property.inp"
Material.read_materials(file_dir)