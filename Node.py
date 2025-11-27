
class Node:

    # Attributes:
    def __init__(self, x=0, y=0, z=0):
        # Coordinates (validated to be numeric)
        self._x = None
        self._y = None
        self._z = None
        
        self.X = x
        self.Y = y
        self.Z = z
    
    @property
    def X(self):
        return self._x
    
    @X.setter
    def X(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"X coordinate must be numeric, got {type(value).__name__}")
        self._x = value
    
    @property
    def Y(self):
        return self._y
    
    @Y.setter
    def Y(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Y coordinate must be numeric, got {type(value).__name__}")
        self._y = value
    
    @property
    def Z(self):
        return self._z
    
    @Z.setter
    def Z(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Z coordinate must be numeric, got {type(value).__name__}")
        self._z = value