class Player:
    def __init__(self, name) -> None:
        self.name = name
        self._balance = 16
        self._current_position = 0
        self._owned_properties = []
    def move(self, steps):
        pass
    def pay(self, amount, owner):
        pass
    def buy_property(self, property):
        pass