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
        pass
    def get_rent(self):
        pass
    def get_owner(self):
        pass
    def set_owner(self):
        pass