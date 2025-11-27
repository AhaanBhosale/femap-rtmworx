import re

class Ply:

    # Attributes:
    def __init__(self, name="", id=0):

        self.Material = None
        self.Angle = 0.0
        self.Thickness = 0.0
        self.Elset_Name = ""

    #  Create array of ply objects from abaqus input file
    @staticmethod
    def read_plies(file_path):

        # Initialize output
        plies = []

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
                            ply.Material = parts[2].strip()
                            
                            # Append ply to output list
                            plies.append((elset_name, ply))

        return plies
    
# Debugging
file_dir = "C:\\Users\\AhaanBhosalePontisEn\\Documents\\Pontis\\Pontis INTERNAL - Documents\\Engineering Tools en Technology\\Flow Simulation - RTMWorx\\Scripting\\FEMAP to RTMWorx\\FEMAP Files\\Surface with Property.inp"
Ply.read_plies(file_dir)
