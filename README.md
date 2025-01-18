# Pronto Woven Monopoly

## Setup Requirements
### Dependencies
* Python 3.8 or higher
* No external libraries are required for core functionality. Testing may use `pytest`.

### How to run
1. Install Python if you haven't
2. Clone the repository or download the project to your local directory
```
git clone https://github.com/suey147/Pronto-Woven.git
```
3. Run the game
```
python .\src\game.py .\board.json .\rolls_1.json
```
You can modify the board layout by providing a new board JSON or new rolls with a new rolls JSON. Simply replace the file with your file path.

## Environment Configuration
* Ensure `board.json` and `rolls.json` are placed in the root directory
* The `board.json` and `rolls.json` files must follow the expected format

## Testing Details
Unit tests for key functions are included in the tests/ directory. Run the tests using:
`python -m pytest tests/test_game.py `