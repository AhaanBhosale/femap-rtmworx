import re

class Element:

    # Attributes:
    def __init__(self, nodes=None, id=0, elset_name =""):

        self.Nodes = nodes if nodes is not None else []
        self.Id = id
        self.Elset_Name = elset_name

    # Read elements from abaqus input file and return a list of Element objects
    @staticmethod
    def read_elements(file_path, nodes_list):

        # Initialize output
        elements = []

        # Convert nodes_list to a dictionary for easy access
        nodes_list = dict(nodes_list)

        # Open the file and read lines
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Process each line
            lines_list = list(lines)
            xi = 0
            while xi < len(lines_list):

                # Current line
                line = lines_list[xi]

                # Check for element definition line
                if line.strip().upper().startswith('*ELEMENT,'):
                    
                    # Extract ELSET name from the element definition line
                    elset_match = re.search(r'ELSET\s*=\s*([^,\s]+)', line, re.IGNORECASE)
                    if elset_match:
                        elset_name = elset_match.group(1)
                    else:
                        raise ValueError(f"ELSET not found in ELEMENT line: {line.strip()}")
                        
                    
                    # Read element definitions until the next asterisk line
                    # The element definition line is already skipped
                    for xj in range(xi + 1, len(lines_list)):

                        # Current line within element definitions
                        line = lines_list[xj]

                        # If there is a new asterisk line, break
                        # Also realign xi to continue from here
                        if line.startswith('*'):
                            xi = xj - 1
                            break

                        # Split line and create Element object
                        parts = line.strip().split(',')
                        if len(parts) >= 2:
                            element_id = int(parts[0])
                            node_ids = [int(nid) for nid in parts[1:]]
                            element_nodes = [nodes_list[nid] for nid in node_ids if nid in nodes_list]
                            element = Element(element_nodes, element_id, elset_name)
                            elements.append(element)
                
                # Increment counter
                xi += 1
                
        return elements