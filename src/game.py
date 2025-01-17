import json
import argparse
import os
from board import Board
from player import Player

class Game:
    def __init__(self, board_file_name, dice_file_name, players) -> None:
        self._players = self.set_player(players)
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
        """Load the dice rolls from rolls.json

        Args:
            dice_file_name (str): name of the rolls file

        Returns:
            list: list of dice 
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
            if player.get_balance()<=0:
                return True
        return False
    def determine_winner(self):
        """Determine the winners with the highest balance."""
        # Find the maximum balance among players
        max_balance = max(player.get_balance() for player in self._players)
        # Find all players with the maximum balance
        winners = [player.name for player in self._players if player.get_balance() == max_balance]
        return winners

    def declare_winner(self):
        """ Print out the winner and balance of all players
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
        """perform action in each turn

        Args:
            steps (int): number of rolls

        Raises:
            ValueError: invalide number of steps
        """
        if (steps<=0):
            raise ValueError(f"Rolls {steps} is out of bounds.")
        # Roll the dice and reach new position
        action = f"\n{self._current_player.name}'s turn! Rolling dice: {steps} \n"
        player = self._current_player
        pass_go = player.check_pass_go(steps, self._board.get_board_len())
        previous_position = player.get_current_position()
        new_position = player.move(steps, self._board.get_board_len())
        landed_property = self._board.get_property(new_position)
        action += f"{player.name} moves from {previous_position} to {new_position} ({landed_property.name})\n"
        # Get $1 if pass Go
        if pass_go:
            player.receive(1)
            action += f"{player.name} passes GO and earns $1! New balance: ${player.get_balance()}\n"
        # Check if landed on Go
        if landed_property.type == "go":
            return
        # Check if the property has owner
        elif landed_property.is_owned():
            # tenant pay rent
            rent = landed_property.get_rent()
            # owner receive rent
            owner = landed_property.get_owner()
            # check if the owner own all property of same colour
            property_set = self._board.get_property_set(landed_property.get_colour())
            if all(p.get_owner() == owner for p in property_set):
                rent *= 2
            owner.receive(rent)
            player.pay(rent)
            action += f"{player.name} pays ${rent} rent to {owner.name} for landing on {landed_property.name}.\n"
            action += f"{player.name}'s new balance: ${player.get_balance()}\n"
            action += f"{owner.name}'s new balance: ${owner.get_balance()}\n"
        else:
            # Buy property if not owned by anyone
            player.buy_property(landed_property)
            landed_property.set_owner(self._current_player)
            action += f"{player.name} buys {landed_property.name} for ${landed_property.get_price()}. Remaining balance: ${player.get_balance()}\n"
        # Record turn
        self._turns.append({
            "player": self._current_player.name,
            "roll": steps,
            "balance": self._current_player.get_balance(),
            "position": landed_property.name,
            "action": action
        })
    def start_game(self):
        """ start the monopoly game
        """
        # start at Go
        self._current_player = self._players[0]
        self._current_turn = 0
        # check anyone bankrupt
        while self.check_bankrupt() is not True:
            self.play_turn(self._dice[self._current_turn])
            self._current_turn += 1
            self._current_player= self._players[self._current_turn%4]
        self.declare_winner()
        self.records_turns()
    def records_turns(self):
        """save the actions of each turns in txt 
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