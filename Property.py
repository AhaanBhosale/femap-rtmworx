import re
from Ply import Ply

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
                            ply.Material = parts[2].strip()
                            
                            # Add to property plies
                            prop.Plies.append(ply)
                    
                    # Add property to output list
                    properties.append(prop)

        return properties