from property import Property

class Board:
    """
    The Board class represents the layout of the game board, including all properties, 
    their types, and positions.
    """
    def __init__(self, positions) -> None:
        """
        Initializes the board with a list of positions and creates Property objects 
        for each position. This method is called when the board data is loaded.

        Args:
            positions (list): List of dictionaries containing board data, with each 
                               dictionary representing a property (name, type, price, etc.).
        """
        self._positions = []
        # Create Property objects for each position
        for i,position in enumerate(positions):
            name = position["name"]
            property_type = position["type"]
            # For "go" type properties, price and color are not applicable
            if property_type == "go":
                price = None
                colour = None
            else:
                price = position["price"]
                colour =  position["colour"]
            # Create a new Property object and append to the positions list
            new_property = Property(name, price, colour, property_type, i)
            self._positions.append(new_property)
    def get_property(self, position):
        """
        Retrieves the property at the specified position index on the board.

        Args:
            position (int): The index of the property on the board.

        Returns:
            Property: The Property object located at the given position.

        Raises:
            ValueError: If the board data is invalid (empty).
            IndexError: If the position is out of bounds.
        """
        if not self._positions:
            raise ValueError("Board data is invalid.")
        if position < 0 or position >= len(self._positions):
            raise IndexError(f"Position {position} is out of bounds. Board size: {len(self._positions)}")
        return self._positions[position]
    def get_board_len(self):
        """
        Retrieves the length of the board, which is the number of properties on the board.

        Returns:
            int: The number of spaces on the board (length of the positions list).

        Raises:
            ValueError: If the board data is invalid or has an invalid size.
        """
        if not self._positions:
            raise ValueError("Board data is invalid.")
        if len(self._positions)<=0:
            raise ValueError(f"Board size: {len(self._positions)} is invalid")
        return len(self._positions)
    def get_property_set(self, colour):
        """
        Retrieves all properties on the board that share the specified colour.

        Args:
            colour (str): The desired colour of the property set.

        Returns:
            list[Property]: A list of Property objects that have the specified colour.
        """
        property_set = []
        # Loop through all properties on the board and collect those with matching colour
        for position in self._positions:
            if colour == position.get_colour():
                property_set.append(position)
        return property_set