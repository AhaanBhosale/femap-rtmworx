class Material:

    # Attributes:
    def __init__(self, name="", id=0, properties=None):

        self.Name = name
        self.Id = id
        self.Vf = 0.0  # Fiber volume fraction
        self.K11 = 0.0  # Permeability in 1 direction
        self.K22 = 0.0  # Permeability in 2 direction

        