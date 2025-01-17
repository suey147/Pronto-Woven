import pytest
import sys
import os
print("sys.path:", sys.path)
print("Current directory:", os.getcwd())
from src.game import Game
@pytest.fixture
def new_game():
    """Initialize game with test files
    """
    return Game("tests/test_board.json", "tests/test_rolls.json")
# Test Game initialization
def test_game_initialization(new_game):
    assert len(new_game._players) == 4
    assert new_game._players[0].name == "Peter"
    assert new_game._players[0]._balance == 16
    assert new_game._board._positions[0].name == "GO"
def test_board_load(new_game):
    pass
def test_dice_load(new_game):
    pass
def test_initial_game_state(new_game):
    pass
# Test player
def test_player_balance(new_game):
    pass
def test_player_position(new_game):
    pass
def test_pass_go(new_game):
    pass
def test_bankruptcy(new_game):
    pass
# Test property
def test_rent_payment(new_game):
    pass
def test_rent_receive(new_game):
    pass
def test_buy_property(new_game):
    pass
def test_ownership(new_game):
    pass
# Turn
def test_player_turn_roation(new_game):
    pass
def test_roll(new_game):
    pass
# Winning Condition
def test_bankruptcy(new_game):
    pass
def test_tie_breaker(new_game):
    pass
# Edge Cases
def invalid_json_files(game):
    pass
def empty_dice_rolls(game):
    pass
def invalide_dice_rolls(game):
    pass
def wraps_board(game):
    pass