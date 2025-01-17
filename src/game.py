import json
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
        winner = None
        print("Results")
        for player in self._players:
            # finish space that player on
            finish_space = self._board.get_property(player.get_current_position()).name
            print(player.name+" end up with: $"+str(player.get_balance())+" at "+ finish_space + "\n")
        
        print("The Winner is "+ ''.join(self.determine_winner()))
    def play_turn(self, steps):
        """ perform action in each turn
        """
        # Roll the dice and reach new position
        pass_go = self._current_player.check_pass_go(steps, self._board.get_board_len())
        new_position = self._current_player.move(steps, self._board.get_board_len())
        if pass_go:
            self._current_player.receive(1)
        landed_property = self._board.get_property(new_position)
        # Check if landed on Go
        if landed_property.type == "go":
            action = "Laned on GO"
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
            self._current_player.pay(rent)
            action = f"{self._current_player.name} paid rent to {owner.name}"
        else:
            # Buy property if not owned by anyone
            self._current_player.buy_property(landed_property)
            landed_property.set_owner(self._current_player)
            action = f"Bought {landed_property.name}"
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
        with open("records.txt", "w") as file:
            file.write("Game Turns:\n")
            file.write("-"*20+"\n")
            for i, turn in enumerate(self._turns):
                file.write(
                    f"Turn {i}: Player: {turn['player']}, "
                    f"Roll: {turn['roll']}, Position: {turn['position']}, "
                    f"Balance: ${turn['balance']}, Position: {turn['action']}\n"
                )
newGame = Game("./board.json", "./rolls_1.json", ["Peter", "Billy", "Charlotte", "Sweedal"])
newGame.start_game()