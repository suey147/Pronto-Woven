class Property:
    def __init__(self, name, price, color, property_type, index) -> None:
        self.name = name
        self._price = price
        self._rent = price
        self._color = color
        self.type = property_type
        self._index = index
        self._owner = None
    def is_owned(self):
        """ check if this property is owned
        Returns:
            boolean: True if is owned
        """
        return True if self._owner is not None else False
    def get_rent(self):
        """getter method of rent

        Returns:
            int: amount of rent
        """
        return self._rent
    def get_owner(self):
        """getter method of owner

        Returns:
            Player: player that owned the property
        """
        return self._owner
    def set_owner(self, player):
        """setter method of owner

        Args:
            player (Player): player that own the property
        """
        self._owner = player
    def get_colour(self):
        """getter method of colour

        Returns:
            str: colour of the property
        """
        return self._color
    