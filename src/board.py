from src.property import Property

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
        return self._positions[position]