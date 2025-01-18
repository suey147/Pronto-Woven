# Implementation documentation

## Code Structure
```
woven_monopoly/
|-- doc                            # Documentations
|-- src/
    |-- game.py                    # Main script to run the game
    |-- board.json                 # 
    |-- rolls.json                 # 
    |-- property.json              # 
|-- tests/
    |-- test_game.py               # Unit and integration tests
|-- board.json                     # JSON file defining the game bo ard
|-- rolls_1.json                   # JSON file defining dice rolls 1
|-- rolls_2.json                   # JSON file defining dice rolls 2
```

## Key Modules and Functions
A class diagrams can be found [here][doc/Architecture.pdf].
### Game
Manages the overall game flow. Manages the board, players, dice rolls, game actions, and determines the winner.
### Player
Represents a player in the game.
### Board
The Board class represents the layout of the game board, including all properties. 
### Property
Represents a property on the board.
### Actions
Defines the actions a player can take during their turn in the game, such as paying rent, buying properties, and passing GO.

## Design Rationale
### Aim
The primary goal of this project is to create a simplified version of Monopoly that is easy to use, modify, and test. Key design considerations include:
1. **Modularity:**
   - Classes like `Game`, `Player`, `Board`, and `Property` encapsulate specific responsibilities.
   - JSON files are used for dynamic configuration, allowing users to customize the board and dice rolls.
2. **Extensibility**
    - The architecture is designed for future expansion. By separating actions into their own class, additional gameplay mechanics can be added effortlessly without disrupting the core logic.
4. **Ease of Use:**
   - The game automates most actions, requiring minimal user input.
   - Logs are kept for debugging and performance review.

## Data File Formats
1. board
```[
  {
    "name": "GO",
    "type": "go"
  },
  {
    "name": "Mediterranean Avenue",
    "price": 60,
    "colour": "brown",
    "type": "property"
  }
]
```

2. rolls
```
[4, 6, 3, 2, 5]
 ```

## Error Handling
* File Not Found: If `board.json` or `rolls.json` is missing, an appropriate error message will be displayed. Example: `Error: Board file 'board.json' does not exist.`
* Malformed JSON: If the JSON files are invalid, the program will display a parsing error. Example: `Invalid property structure in board file`.
* Invalid Data: If required fields are missing in the JSON files, the program will raise an exception with specific details.

## Future Enhancements
* Add a graphical interface to improve user experience.
* Enhance error messages with suggestions for fixing issues.
* Introduce configurable rules for custom games.

## Assumptions
* Rent and cost of property are the same
