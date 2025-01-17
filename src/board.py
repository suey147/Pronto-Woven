from property import Property

class Board:
    """ Board class to represent the board layout
    """
    def __init__(self, positions) -> None:
        self._positions = []
        for i,position in enumerate(positions):
            name = position["name"]
            property_type = position["type"]
            if property_type == "go":
                price = None
                colour = None
            else:
                price = position["price"]
                colour =  position["colour"]
            new_property = Property(name, price, colour, property_type, i)
            self._positions.append(new_property)
    def get_property(self, position):
        """Getter of property

        Args:
            position (int): position index of the property on the board
        """
        if not self._positions:
            raise ValueError("Board data is invalid.")
        if position < 0 or position >= len(self._positions):
            raise IndexError(f"Position {position} is out of bounds. Board size: {len(self._positions)}")
        return self._positions[position]
    def get_board_len(self):
        """Getter of board len

        Returns:
            Int: number of spaces on board
        """
        if not self._positions:
            raise ValueError("Board data is invalid.")
        if len(self._positions)<=0:
            raise ValueError(f"Board size: {len(self._positions)} is invalid")
        return len(self._positions)
    def get_property_set(self, colour):
        """Get same colour properties 

        Args:
            colour (string): Desired colour

        Returns:
            List<Property>: list of properties that have same colour
        """
        property_set = []
        for position in self._positions:
            if colour == position.get_colour():
                property_set.append(position)
        return property_set