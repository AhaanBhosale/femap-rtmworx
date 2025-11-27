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
            lines_iter = iter(lines)
            for line in lines_iter:

                # Check for element definition line
                if line.strip().upper().startswith('*ELEMENT,'):
                    
                    # Extract ELSET name from the element definition line
                    import re
                    elset_match = re.search(r'ELSET\s*=\s*([^,\s]+)', line, re.IGNORECASE)
                    elset_name = elset_match.group(1) if elset_match else ""
                    
                    # Read element definitions until the next asterisk line
                    # The element definition line is already skipped
                    for line in lines_iter:
                        if line.startswith('*'):
                            break
                        parts = line.strip().split(',')
                        if len(parts) >= 2:
                            element_id = int(parts[0])
                            node_ids = [int(nid) for nid in parts[1:]]
                            element_nodes = [nodes_list[nid] for nid in node_ids if nid in nodes_list]
                            element = Element(element_nodes, element_id, elset_name)
                            elements.append(element)
        return elements