from .Node import Node

class Element:

    # Attributes:
    def __init__(self, nodes=None):
        self._nodes = None  # List of Node objects
        self.Nodes = nodes if nodes is not None else []

        @property
        def nodes(self):
            return self._nodes
        
        @nodes.setter
        def nodes(self, value):
            if isinstance(value, Node):
                self._nodes = [value]
            elif isinstance(value, list):
                if not all(isinstance(item, Node) for item in value):
                    raise TypeError("All items must be Node objects")
                self._nodes = value
            else:
                raise TypeError("Must be Node or list of Nodes")