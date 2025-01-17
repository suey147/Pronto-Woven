import json

class Game:
    def __init__(self, board_file_name, dice_file_name) -> None:
        self._players = self.set_player(["Peter", "Billy", "Charlotte", "Sweedal"])
        self._board = self.get_board(board_file_name)
        self._dice = self.get_dice(dice_file_name)
        self._current_player = None
        self._current_turn = 0
        self._turns = []
    
    def get_board(self, board_file_name):
        pass
    def get_dice(self, dice_file_name):
        pass
    def get_player(self):
        pass
    def check_bankrupt(self):
        pass
    def declare_winner(self):
        pass
    def play_turn(self):
        pass
    def start_game(self):
        pass