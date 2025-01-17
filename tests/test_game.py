from game import Game
import pytest

@pytest.fixture
def game():
    """Initialize game with test files
    """
    return Game("tests/test_board.json", "tests/test_rolls.json", ["Peter", "Billy", "Charlotte", "Sweedal"])
# Test Game initialization
def test_game_initialization(game):
    assert len(game._players) == 4
    assert [player.name for player in game._players] == ["Peter", "Billy", "Charlotte", "Sweedal"]
    assert all(player._balance == 16 for player in game._players)
    assert all(player._current_position == 0 for player in game._players)
    assert game._board.get_board_len() > 0
    assert game._current_turn == 0
    assert game._dice

def test_board_load(game):
    """ Verify board is loaded correctly from JSON
    """
    assert game._board._positions[0].name == "GO"
    assert game._board._positions[-1].name == "Massizim"
def test_dice_load(game):
    """Test that dice rolls are loaded correctly."""
    assert game._dice ==  [1,2,3,4,5,6]
# Test player
def test_player_initialization(game):
    """Test player initialization attributes."""
    player = game._players[0]
    assert player.name == "Peter"
    assert player._balance == 16
    assert player._current_position == 0
    assert not player._owned_properties
def test_player_movement(game):
    """Test player movement on dice roll."""
    game._current_player = game._players[0]
    game.play_turn(2)  # Assume roll of 2
    assert game._current_player._current_position == 2
def test_passing_go(game):
    """Test passing GO and receiving $1."""
    game._current_player = game._players[0]
    player = game._current_player
    player._current_position = 8  # Assume board has 9 positions
    game.play_turn(1)
    assert player._current_position == 0  # Board wraps back to Go
    assert player._balance == 17  # +1 for passing GO
def test_bankruptcy(game):
    """Test bankruptcy condition."""
    player = game._players[0]
    game._current_player = player
    player._balance = 1
    game.play_turn(1)  # Assume rent owed > balance
    assert player._balance <= 0
    assert game.check_bankrupt() == True
# Test property
def test_rent_payment(game):
    """Test rent payment to property owner."""
    player1 = game._players[0]
    player2 = game._players[1]
    game._current_player = player1
    game.play_turn(1)  # Player1 buys property at position 1
    game._current_player = player2
    game.play_turn(1)  # Player2 lands on position 1
    assert player2._balance == 15  # $16 - $1 rent
    assert player1._balance == 16  # Rent collected
def test_buy_property(game):
    """Test property purchase."""
    player = game._players[0]
    game._current_player = player
    game.play_turn(1)  # Lands on position 1 (property)
    assert player._balance == 15  # $16 - $1
    # check ownership
    assert game._board.get_property(1).get_owner().name == player.name
    assert len(player._owned_properties) == 1
def test_double_rent(game):
    """Test double rent when owning all properties of a color."""
    player = game._players[0]
    game._current_player = player
    # All Brown properties
    property1 = game._board.get_property(1)
    property2 = game._board.get_property(2)
    player._owned_properties = [property1, property2]
    property1.set_owner(player)
    property2.set_owner(player)
    # Another player lands on a Brown property
    game._current_player = game._players[1]
    game.play_turn(1)
    assert player._balance == 18  # Rent = 2x for full ownership
# Turn
def test_player_turn_roation(game):
    """Test correct turn rotation."""
    game.play_turn(1)
    assert game._current_player.name == "Billy"
    game.play_turn(2)  # Billy's turn
    assert game._current_player.name == "Charlotte"
def test_roll(game):
    """Test dice roll's impact on player movement."""
    player = game._players[0]
    game._current_player = player
    initial_position = player._current_position
    game.play_turn(3)
    assert player._current_position == (initial_position + 3) % game._board.get_board_len()
# Winning Condition
def test_winning_condition(game):
    """Test game ends when a player is bankrupt and determine the winner."""
    game._players[1]._balance = 0  # Billy is bankrupt
    winner = game.check_bankrupt()
    assert winner.name == "Peter"  # Assume Peter has the highest balance
def test_tie_breaker(game):
    """Test tie-breaking rules when two players have the same balance."""
    game._players[0]._balance = 20
    game._players[1]._balance = 20
    winners = game.determine_winner()
    assert len(winners) == 2
    assert [winner.name for winner in winners] == ["Peter", "Billy"]
# Edge Cases
@pytest.fixture
def mock_game(mock_board, mock_dice):
    """Create a mock game with mocked board and dice."""
    game = Game("tests/test_board.json", "tests/test_rolls.json", ["Peter", "Billy", "Charlotte", "Sweedal"])
    game._board = mock_board
    game._dice = mock_dice
    return game
@pytest.fixture
def mock_board():
    """Mock board data."""
    return [
        {"name": "GO", "type": "go"},
        {"name": "The Burvale", "price": 1, "colour": "Brown", "type": "property"},
        {"name": "Fast Kebabs", "price": 1, "colour": "Brown", "type": "property"},
        {"name": "Massizim", "price": 4, "colour": "Blue", "type": "property"},
    ]
@pytest.fixture
def mock_dice():
    """Mock dice rolls."""
    return [1, 3, 5, 2, 6, 4]

def test_invalid_json_files(mock_game):
    """Test behavior when the board data is invalid."""
    mock_game._board = []
    with pytest.raises(ValueError, match="Board data is invalid."):
        mock_game._board.get_property(0)
def test_empty_dice_rolls(mock_game):
    """Test behavior when dice rolls file is empty."""
    mock_game._dice = []
    with pytest.raises(ValueError, match="No dice rolls provided."):
        mock_game.play_turn()
def test_invalid_dice(game):
    """Test invalid negative dice rolls."""
    game._dice = [-3, 2, 5]  # Replace dice rolls with invalid values
    game._current_player = game._players[0]
    with pytest.raises(ValueError):
        game.play_turn(game._dice[0])
def test_wraps_board(game):
    """Test player wraps around to the start of the board."""
    player = game._players[0]
    game._current_player = player
    player._current_position = game._board.get_board_len() - 1  # Last position
    game.play_turn(2)  # Move past last position
    assert player._current_position == 1  # Wrap around