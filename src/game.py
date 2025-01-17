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
        with open(board_file_name) as file:
            board_data = json.load(file)
        new_board = Board(board_data)
        return new_board
    def get_dice(self, dice_file_name):
        with open(dice_file_name) as file:
            dice_data = json.load(file)
        return dice_data
    def get_player(self):
        pass
    def set_player(self, players_name):
        pass
    def check_bankrupt(self):
        pass
    def declare_winner(self):
        pass
    def play_turn(self):
        pass
    def start_game(self):
        pass