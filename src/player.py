class Player:
    def __init__(self, name) -> None:
        self.name = name
        self._balance = 16
        self._current_position = 0
        self._owned_properties = []
    def move(self, steps, board_size):
        """move the player to new position

        Args:
            steps (int): number of steps to move
            board_size (int): number of spaces on the board

        Returns:
            int: new position
        """
        # check if pass go
        if self._current_position+steps>=board_size:
            self._current_position = self._current_position+steps-board_size
        else:
            self._current_position += steps
        return self._current_position
    def pay(self, amount):
        """pay rent and update balance

        Args:
            amount (int): rent to be paid
        """
        self._balance -= amount
    def receive(self, amount):
        """receive rent and update balance

        Args:
            amount (int): amount to be received
        """
        self._balance += amount
    def buy_property(self, property):
        """pay to buy property. update balance and owned properties list

        Args:
            property (Property): property to be ourchased
        """
        self._balance -= property._price
        self._owned_properties.append(property)