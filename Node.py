
class Node:

    # Attributes:
    def __init__(self, x=0, y=0, z=0, id=0):

        self.x = x
        self.y = y
        self.z = z
        self.id = id

    # Read nodes from abaqus input file and return a list of Node objects
    @staticmethod
    def read_nodes(file_path):

        # Initialize output
        nodes = []

        # Open the file and read lines
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Process each line
            lines_iter = iter(lines)
            for line in lines_iter:

                # Check for node definition line
                if line.strip().upper().startswith('*NODE'):
                    
                    # Read node definitions until the next asterisk line
                    # The node definition line is already skipped
                    for line in lines_iter:
                        if line.startswith('*'):
                            break
                        parts = line.strip().split(',')
                        if len(parts) >= 4:
                            node_id = int(parts[0])
                            x = float(parts[1])
                            y = float(parts[2])
                            z = float(parts[3])
                            node = Node(x, y, z, node_id)
                            nodes.append((node_id, node))
        return nodes