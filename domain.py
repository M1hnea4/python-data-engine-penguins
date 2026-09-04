from exceptions import InvalidAttributeError

class Penguin:
    def __init__(self, species, island, flipper_length, culmen_length, culmen_depth, body_mass, sex):
        """
        Initializes a Penguin object.
        Attributes are private (prefixed with __).
        """
        self.__species = species
        self.__island = island
        self.__flipper_length_mm = flipper_length
        self.__culmen_length_mm = culmen_length
        self.__culmen_depth_mm = culmen_depth
        self.__body_mass_g = body_mass
        self.__sex = sex

    @classmethod
    def from_dict(cls, data_dict):
        """
        Factory method to create a Penguin from a dictionary.
        """
        return cls(
            species=data_dict['species'],
            island=data_dict['island'],
            flipper_length=float(data_dict['flipper_length_mm']),
            culmen_length=float(data_dict['culmen_length_mm']),
            culmen_depth=float(data_dict['culmen_depth_mm']),
            body_mass=float(data_dict['body_mass_g']),
            sex=data_dict['sex']
        )

    @property
    def species(self):
        return self.__species

    @property
    def island(self):
        return self.__island

    @property
    def flipper_length_mm(self):
        return self.__flipper_length_mm

    @property
    def culmen_length_mm(self):
        return self.__culmen_length_mm

    @property
    def culmen_depth_mm(self):
        return self.__culmen_depth_mm

    @property
    def body_mass_g(self):
        return self.__body_mass_g

    @property
    def sex(self):
        return self.__sex

    def get_attr(self, attr_name):
        """
        Retrieves the value of a specific attribute by name.
        Uses the properties defined above.
        """
        if hasattr(self, attr_name):
            return getattr(self, attr_name)
        raise InvalidAttributeError(f"Attribute '{attr_name}' does not exist.")

    def __repr__(self):
        """
        Returns a string representation of the Penguin.
        """
        return (f"Penguin(species='{self.__species}', island='{self.__island}', "
                f"flipper={self.__flipper_length_mm})")