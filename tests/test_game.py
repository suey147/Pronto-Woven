import pytest
from game import Game

@pytest.fixture
def game():
    """Initialize game with test files
    """
    return Game("test_board.json", "test_dice.json")

# Test Game initialization
def test_game_initialization(game):
    pass
def test_board_load(game):
    pass
def test_dice_load(game):
    pass
def test_initial_game_state(game):
    pass
# Test player
def test_player_balance(game):
    pass
def test_player_position(game):
    pass
def test_pass_go(game):
    pass
def test_bankruptcy(game):
    pass
# Test property
def test_rent_payment(game):
    pass
def test_rent_receive(game):
    pass
def test_buy_property(game):
    pass
def test_ownership(game):
    pass
# Turn
def test_player_turn_roation(game):
    pass
def test_roll(game):
    pass
# Winning Condition
def test_bankruptcy(game):
    pass
def test_tie_breaker(game):
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