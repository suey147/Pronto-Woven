# Implementation documentation

## Code Structure
```
woven_monopoly/
|-- doc                            # Documentations
|-- src/
    |-- game.py                    # Main script to run the game
    |-- board.py                 
    |-- rolls.py                 
    |-- property.py
    |-- actions.py               
|-- tests/
    |-- test_game.py               # Unit and integration tests
|-- board
    |-- board.json                     # JSON file defining the game board
|-- rolls
    |-- rolls_1.json                   # JSON file defining dice rolls 1
    |-- rolls_2.json                   # JSON file defining dice rolls 2
```

## Key Modules and Functions
A class diagrams can be found here.
### Game
Manages the overall game flow.
1. Attributes
* players: List[Player]: A list of all players in the game.
* board: Board: The game board, which contains properties and associated rules.
* dice: List[int]: Pre-determined dice rolls used during the game.
* current_player: Player: The player whose turn is currently active.
* current_turn: int: The current turn number in the game.
* turns: List[str]: A log of all turns, storing records for later review.
2. Methods
* __init__(boardFileName: str, diceFileName: str): Initializes the game by loading the board and dice rolls from the provided files. Sets up initial states for players and turns.
* get_board(board_file_name: str): Loads the game board from a JSON file. Validates the board structure and properties.
* set_players(players_name: str): Initializes the players with their starting positions and initial money.
* get_dice(dice_file_name: str): Loads the dice rolls from a JSON file. Ensures the dice rolls match the expected format.
* check_bankrupt(): Checks if any player has gone bankrupt.
* determine_winner(): Compares the remaining money of all players. Declares the winner based on the highest balance.
* start_game(): Initializes the game loop and processes player turns until a winner is determined.
* play_turn(steps: int): Executes a turn for the current player based on dice roll results.
Handles movement, property purchases, rent payments, and passing GO.
* records_turns(): Logs the details of each turn (e.g., player actions, property transactions) for review or debugging.
* declare_winner(): Outputs the winner and their final score once the game ends.

### Player
Represents a player in the game.
1. Attributes
* name: The player's name.
* current_position: Current position on the board.
* balance: Player’s available money.
* owned_properties: List of properties owned by the player.
2. Methods
* move(steps, board_size): Updates the player’s position on the board.
* check_pass_go(steps, board_size): Check if the player pass Go
* pay(amount): Handles pay rent.
* receive(amount): Handles receive rent.
* buy_property(property): Handles buy properties.
* determine_winner(): Identifies the winner based on remaining money.
* get_balance(): Get player balance.
* get_current_position(): Get player current position.

### Board
1. Attributes
* positions: A list of all property positions on the board.
2. Methods
* __init__(positions):Initializes the board with the provided list of properties.
* get_property(position): Property: Retrieves a property at a specific position on the board.
* get_board_len(): Returns the total number of positions on the board.
* get_property_set(colour): Returns all properties of a given color (used to determine if a player owns a full set).

### Property
Represents a property on the board.
1. Attributes
* name: The name of the property.
* price: The purchase price of the property.
* rent: The rent a player must pay when landing on this property.
* color: The color group of the property. Can be None for special properties like "GO"
* type: The type of property (property | go)
* owner: The current owner of the property. Defaults to None if unowned.
2. Methods
* __init__(name, price, color, type, index): Constructor to initialize a property with its attributes. The owner is set to None initially.
* is_owned(): Checks if the property is owned.
* get_rent(): Returns the rent amount for this property.
* get_price(): Returns the purchase price of the property.
* set_owner(player): Assigns ownership of the property to a specific player.
* get_owner():Returns the current owner of the property.
* get_colour():Returns the color of the property.

## Design Rationale
### Aim
The primary goal of this project is to create a simplified version of Monopoly that is easy to use, modify, and test. Key design considerations include:
1. **Modularity:**
   - Classes like `Game`, `Player`, `Board`, and `Property` encapsulate specific responsibilities.
   - JSON files are used for dynamic configuration, allowing users to customize the board and dice rolls.
2. **Ease of Use:**
   - The game automates most actions, requiring minimal user input.
   - Logs are kept for debugging and performance review.

## Data File Formats
1. board
```[
  {
    "name": "GO",
    "price": 0,
    "rent": 0,
    "color": null,
    "type": "start",
    "index": 0
  },
  {
    "name": "Mediterranean Avenue",
    "price": 60,
    "rent": 2,
    "color": "brown",
    "type": "property",
    "index": 1
  }
]
```

2. rolls
``` [4, 6, 3, 2, 5] ```

## Error Handling
* File Not Found: If `board.json` or `rolls.json` is missing, an appropriate error message will be displayed. Example: `Error: Board file 'board.json' does not exist.`
* Malformed JSON: If the JSON files are invalid, the program will display a parsing error. Example: `Invalid property structure in board file`.
* Invalid Data: If required fields are missing in the JSON files, the program will raise an exception with specific details.

## Future Enhancements
* Add a graphical interface to improve user experience.
* Enhance error messages with suggestions for fixing issues.
* Introduce configurable rules for custom games.