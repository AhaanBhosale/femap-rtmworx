
class Node:

    # Attributes:
    def __init__(self, x=0, y=0, z=0, id=0):

        self.X = x
        self.Y = y
        self.Z = z
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
            lines_list = list(lines)
            xi = 0
            while xi < len(lines_list):

                # Get current line
                line = lines_list[xi]

                # Check for node definition line
                if line.strip().upper().startswith('*NODE'):
                    
                    # Read node definitions until the next asterisk line
                    # The node definition line is already skipped
                    for xj in range(xi + 1, len(lines_list)):
                        line = lines_list[xj]

                        # If there is a new asterisk line, break
                        # Also realign xi to continue from here
                        if line.startswith('*'):
                            xi = xj - 1
                            break

                        # Split line and create Node object
                        parts = line.strip().split(',')
                        if len(parts) >= 4:
                            node_id = int(parts[0])
                            x = float(parts[1])
                            y = float(parts[2])
                            z = float(parts[3])
                            node = Node(x, y, z, node_id)
                            nodes.append((node_id, node))

                # Increment counter
                xi += 1
                
        return nodes