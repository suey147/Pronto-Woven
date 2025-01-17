import json
from src.board import Board
from src.player import Player

class Game:
    def __init__(self, board_file_name, dice_file_name) -> None:
        self._players = self.set_player(["Peter", "Billy", "Charlotte", "Sweedal"])
        self._board = self.get_board(board_file_name)
        self._dice = self.get_dice(dice_file_name)
        self._current_player = None
        self._current_turn = 0
        self._turns = []
    def get_board(self, board_file_name):
        """Load the board layout from board.json
        
        Args:
            board_file_name (str): name of the board layout file

        Returns:
            list: list of property 
        """
        with open(board_file_name) as file:
            board_data = json.load(file)
        new_board = Board(board_data)
        return new_board

    def get_dice(self, dice_file_name):
        """Load the dice rolls from rolls.json

        Args:
            dice_file_name (str): name of the rolls file

        Returns:
            list: list of dice 
        """
        with open(dice_file_name) as file:
            dice_data = json.load(file)
        return dice_data
    def set_player(self, players_name):
        """set players

        Args:
            players_name (str): name of the player

        Returns:
            List<Player>: list of Players
        """
        players = []
        for player_name in players_name:
            new_player = Player(player_name)
            players.append(new_player)
        return players
    def check_bankrupt(self):
        """check players balance to check bankrupt

        Returns:
            boolean: True if someone bankrupt
        """
        for player in self._players:
            if player.get_balance()<0:
                return True
        return False
    def declare_winner(self):
        """ Print out the winner and balance of all players
        """
        winner = None
        print("Results")
        for player in self._players:
            # finish space that player on
            finish_space = self._board.get_property(player.get_current_position()).name
            print(player.name+" end up with: $"+str(player.get_balance())+" at "+ finish_space + "\n")
            # find the winner
            if winner is None or winner.get_balance()<player.get_balance():
                winner = player
        print("The Winner is "+ winner.name)
    def play_turn(self):
        """ perform action in each turn
        """
        # Roll the dice and reach new position
        steps = self._dice[self._current_turn]
        new_position = self._current_player.move(steps, self._board.get_board_len())
        landed_property = self._board.get_property(new_position)
        # Check if landed on Go
        if landed_property.type == "go":
            return
        # Check if the property has owner
        elif landed_property.is_owned():
            # tenant pay rent
            rent = landed_property.get_rent()
            # owner receive rent
            owner = landed_property.get_owner()
            owner.receive(rent)
            self._current_player.pay(rent)
        else:
            # Buy property if not owned by anyone
            self._current_player.buy_property(landed_property)
            landed_property.set_owner(self._current_player)
    def start_game(self):
        """ start the monopoly game
        """
        # start at Go
        self._current_player = self._players[0]
        self._current_turn = 0
        # check anyone bankrupt
        while self.check_bankrupt() is not True:
            self.play_turn()
            self._current_turn += 1
            self._current_player= self._players[self._current_turn%4]
newGame = Game("./board.json", "./rolls_1.json")
newGame.start_game()