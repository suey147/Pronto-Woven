class Property:
    """
    The Property class represents a property on the game board. Each property has
    a name, price, rent value, color, type, index on the board, and an owner (if any).
    This class allows the game to check if the property is owned, get rent and price values,
    and manage ownership.
    """
    def __init__(self, name, price, color, property_type, index) -> None:
        """
        Initializes a new property with the specified details.

        Args:
            name (str): The name of the property.
            price (int): The purchase price of the property.
            color (str): The color of the property (used for groups of properties).
            property_type (str): The type of the property (e.g., "go").
            index (int): The position of the property on the board (its index).
        """
        self.name = name
        self._price = price
        self._rent = price
        self._color = color
        self.type = property_type
        self._index = index
        self._owner = None
    def is_owned(self):
        """
        Checks if this property has an owner.

        Returns:
            bool: True if the property has an owner, False otherwise.
        """
        return True if self._owner is not None else False
    def get_rent(self):
        """
        Getter for the rent value of the property.

        Returns:
            int: The amount of rent that needs to be paid for this property.
        """
        return self._rent
    def get_price(self):
        """
        Getter for the price of the property.

        Returns:
            int: The purchase price of the property.
        """
        return self._price
    def get_owner(self):
        """
        Getter for the owner of the property.

        Returns:
            Player: The player who owns this property. Returns None if no owner.
        """
        return self._owner
    def set_owner(self, player):
        """
        Sets the owner of the property.

        Args:
            player (Player): The player who is purchasing the property.
        """
        self._owner = player
    def get_colour(self):
        """
        Getter for the color of the property, used to group similar properties.

        Returns:
            str: The color group of the property.
        """
        return self._color
    