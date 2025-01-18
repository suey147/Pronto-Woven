import json
import argparse
import os
from board import Board
from player import Player
from actions import Actions

class Game:
    """
    Represents a Monopoly game. Manages the board, players, dice rolls, game actions, and determines the winner.
    """
    def __init__(self, board_file_name, dice_file_name, players) -> None:
        """
        Initializes the game with the provided board layout, dice rolls, and players.
        
        Args:
            board_file_name (str): The file name containing the board layout (e.g., 'board.json').
            dice_file_name (str): The file name containing the dice roll values (e.g., 'rolls.json').
            players (list): A list of player names to be included in the game.
        """
        self._players = self.set_player(players)
        self._board = self.get_board(board_file_name)
        self._dice = self.get_dice(dice_file_name)
        self._current_player = None
        self._current_turn = 0
        self._turns = []
        self._game_actions = Actions()
    def get_board(self, board_file_name):
        """
        Loads the board layout from the specified JSON file and validates its structure.
        
        Args:
            board_file_name (str): The file name containing the board layout (e.g., 'board.json').
        
        Returns:
            Board: A Board object representing the game board.
        
        Raises:
            FileNotFoundError: If the board file does not exist.
            ValueError: If the board file contains invalid data or structure.
        """
        try:
            if not os.path.exists(board_file_name):
                raise FileNotFoundError(f"Board file '{board_file_name}' does not exist.")
            with open(board_file_name) as file:
                board_data = json.load(file)
            
            # Validate board structure
            for prop in board_data:
                if not all(key in prop for key in ("name", "type")):
                    raise ValueError(f"Invalid property structure in board file: {prop}")
                
            if len(board_data)>0:
                new_board = Board(board_data)
            else:
                raise ValueError("Board data is invalid.")
            
            return new_board
        except Exception as e:
            raise ValueError(f"Error loading board file: {e}")

    def get_dice(self, dice_file_name):
        """
        Loads the dice rolls from the specified JSON file and validates its structure.
        
        Args:
            dice_file_name (str): The file name containing the dice roll values (e.g., 'rolls.json').
        
        Returns:
            list: A list of integers representing the dice rolls for each turn.
        
        Raises:
            FileNotFoundError: If the dice file does not exist.
            ValueError: If the dice file is not structured correctly.
        """
        try:
            if not os.path.exists(dice_file_name):
                raise FileNotFoundError(f"Rolls file '{dice_file_name}' does not exist.")
            
            with open(dice_file_name) as file:
                dice_data = json.load(file)
            
            # Validate rolls structure
            if not isinstance(dice_data, list) or not all(isinstance(roll, int) for roll in dice_data):
                raise ValueError("Rolls file must contain a list of integers.")
            
            return dice_data
        except Exception as e:
            raise ValueError(f"Error loading rolls file: {e}")
    def set_player(self, players_name):
        """
        Initializes players from the provided list of player names.
        
        Args:
            players_name (list): A list of player names (strings).
        
        Returns:
            list[Player]: A list of Player instances created from the provided names.
        """
        players = []
        for player_name in players_name:
            new_player = Player(player_name)
            players.append(new_player)
        return players
    def check_bankrupt(self):
        """
        Checks if any player is bankrupt (balance is less than or equal to zero).
        
        Returns:
            bool: True if any player is bankrupt, otherwise False.
        """
        for player in self._players:
            if player.get_balance()<=0:
                return True
        return False
    def determine_winner(self):
        """
        Determines the winner(s) based on the highest balance among the players.
        
        Returns:
            list[str]: A list of player names who have the highest balance.
        """
        # Find the maximum balance among players
        max_balance = max(player.get_balance() for player in self._players)
        # Find all players with the maximum balance
        winners = [player.name for player in self._players if player.get_balance() == max_balance]
        return winners

    def declare_winner(self):
        """
        Declares the winner(s) and prints the final balance and properties owned by each player.
        It also writes the game records to a file.
        """
        print("Results \n")
        print("-"*40+"\n")
        for player in self._players:
            # finish space that player on
            finish_space = self._board.get_property(player.get_current_position()).name
            print(player.name+" end up with: $"+str(player.get_balance())+" at "+ finish_space + "\n")
        
        print("The Winner is "+ ''.join(self.determine_winner()))
        print("Details of each turns has saved at records.txt")
    def play_turn(self, steps):
        """
        Simulates a player's turn, including rolling the dice, moving, paying rent, and potentially buying a property.
        
        Args:
            steps (int): The number of steps the player moves based on the dice roll.
        
        Raises:
            ValueError: If the number of steps is invalid (less than or equal to zero).
        """
        if (steps<=0):
            raise ValueError(f"Rolls {steps} is out of bounds.")
        # Prepare the action message
        action = f"\n{self._current_player.name}'s turn! Rolling dice: {steps} \n"
        player = self._current_player
        previous_position = player.get_current_position()
        action += self._game_actions.pass_go(player, steps, self._board.get_board_len())
        new_position = player.move(steps, self._board.get_board_len())
        landed_property = self._board.get_property(new_position)
        action += f"{player.name} moves from {previous_position} to {new_position} ({landed_property.name})\n"
        # Perform actions based on the property type
        if landed_property.type != "go":
            action += self._game_actions.rent(player, landed_property, self._board)
            action += self._game_actions.buy_property(player, landed_property)
            # add more actions if needed
        # Record turn
        self._turns.append({
            "player": self._current_player.name,
            "roll": steps,
            "balance": self._current_player.get_balance(),
            "position": landed_property.name,
            "action": action
        })
    def start_game(self):
        """
        Starts the game by initializing the first player and looping through turns until a player is bankrupt.
        Once the game is over, it declares the winner and records the turn details.
        """
        # start at Go
        self._current_player = self._players[0]
        self._current_turn = 0
        # Loop through turns until a player is bankrupt
        while self.check_bankrupt() is not True:
            self.play_turn(self._dice[self._current_turn])
            self._current_turn += 1
            self._current_player= self._players[self._current_turn%4]
        self.declare_winner()
        self.records_turns()
    def records_turns(self):
        """
        Saves the details of each turn (including player actions, rolls, and balances) to a text file.
        
        Returns:
            None
        """
        with open("records.txt", "w") as file:
            file.write("Game Turns:\n")
            file.write("-"*20+"\n")
            for i, turn in enumerate(self._turns):
                file.write(
                    f"Turn {i}: Player: {turn['player']}, "
                    f"Roll: {turn['roll']}, Position: {turn['position']}, "
                    f"Balance: ${turn['balance']}, Position: {turn['action']}\n"
                )
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pronto Woven Monopoly Game")
    parser.add_argument("board_file", type=str, help="Path to the board JSON file")
    parser.add_argument("rolls_file", type=str, help="Path to the rolls JSON file")
    args = parser.parse_args()

    try:
        # Initialize and play the game
        players = ["Peter", "Billy", "Charlotte", "Sweedal"]
        game = Game(args.board_file, args.rolls_file, players)
        game.start_game()
    except Exception as e:
        print(f"Error: {e}")