import pytest
from game import Game

@pytest.fixture
def game():
    """Initialize game with test files
    """
    return Game("test_board.json", "test_dice.json")
