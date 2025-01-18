class Player:
    """
    The Player class represents a player in the game. Each player has a balance,
    a current position on the board, and a list of properties they own. The class 
    provides methods to move the player, manage the player's balance, and track 
    the properties they own.
    """
    def __init__(self, name) -> None:
        """
        Initializes a new player with the given name, sets the initial balance, 
        position, and an empty list for owned properties.

        Args:
            name (str): The name of the player.
        """
        self.name = name
        self._balance = 16
        self._current_position = 0
        self._owned_properties = []
    def move(self, steps, board_size):
        """
        Moves the player by the given number of steps. If the player passes the 
        "GO" square, their position is adjusted accordingly.

        Args:
            steps (int): The number of steps to move the player.
            board_size (int): The total number of spaces on the board.

        Returns:
            int: The player's new position after moving.
        """
        # check if pass go
        if self.check_pass_go(steps, board_size):
            self._current_position = self._current_position+steps-board_size
        else:
            self._current_position += steps # Move forward by steps
        return self._current_position
    def check_pass_go(self,  steps, board_size):
        """
        Checks whether the player has passed the "GO" during their move.

        Args:
            steps (int): The number of steps the player intends to move.
            board_size (int): The total number of spaces on the board.

        Returns:
            bool: True if the player passes "GO", False otherwise.
        """
        if self._current_position+steps>=board_size:
            return True
        return False
    def pay(self, amount):
        """
        Deducts the specified amount from the player's balance to pay rent or other expenses.

        Args:
            amount (int): The amount to be deducted from the player's balance.
        """
        self._balance -= amount
    def receive(self, amount):
        """
        Increases the player's balance by the specified amount, typically when receiving rent.

        Args:
            amount (int): The amount to be added to the player's balance.
        """
        self._balance += amount
    def buy_property(self, property):
        """
        Deducts the price of the property from the player's balance and adds the property to the 
        player's list of owned properties.

        Args:
            property (Property): The property to be purchased by the player.
        """
        self._balance -= property._price    # Deduct price from balance
        self._owned_properties.append(property) # Add property to owned list
    def get_balance(self):
        """
        Returns the current balance of the player.

        Returns:
            int: The player's current balance.
        """
        return self._balance
    def get_current_position(self):
        """
        Returns the player's current position on the board.

        Returns:
            int: The index of the player's current position on the board.
        """
        return self._current_position
