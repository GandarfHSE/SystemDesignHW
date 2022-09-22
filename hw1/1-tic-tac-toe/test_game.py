from game import Game, find_move

def test_is_in_field():
    game = Game(5, 5)
    assert game._Game__is_in_field(1, 1) == True
    assert game._Game__is_in_field(0, 1) == False
    assert game._Game__is_in_field(5, 0) == False
    assert game._Game__is_in_field(5, 1) == True
    assert game._Game__is_in_field(5, 5) == True
    assert game._Game__is_in_field(5, 6) == False
    assert game._Game__is_in_field(6, 1) == False
    
def test_expanding():
    game = Game(2, 2)
    assert game._Game__try_expand_x(0, 1, 1, 1, 1) == True
    assert game._Game__try_expand_o(0, 1, 1, 1, 1) == True

    game.make_a_move(1, 1)
    game.make_a_move(2, 1)
    game.make_a_move(1, 2)

    assert game._Game__try_expand_x(1, 1, 1, 0, 1) == True
    assert game._Game__try_expand_x(1, 1, 1, 1, 1) == False
    assert game._Game__try_expand_x(1, 1, 1, 1, 0) == False
    assert game._Game__try_expand_x(1, 1, 2, 0, 1) == False
    assert game._Game__try_expand_o(1, 1, 1, 1, 0) == True
    assert game._Game__try_expand_o(1, 2, 1, 1, 0) == False

def test_score_check():
    game = Game(3, 3)
    assert game.get_score() == 0

    game.make_a_move(2, 2)
    game.make_a_move(1, 2)
    game.make_a_move(1, 1)

    assert game.get_score() == 0

    game.make_a_move(2, 1)
    game.make_a_move(3, 3)

    assert game.get_score() == 1

def test_tie():
    game = Game(2, 2)

    assert game.is_tie() == False

    game.make_a_move(1, 1)
    game.make_a_move(1, 2)

    assert game.is_tie() == False

    game.make_a_move(2, 2)
    game.make_a_move(2, 1)

    assert game.is_tie() == True

def test_get_field():
    game = Game(3, 3)
    game.make_a_move(2, 2)
    game.make_a_move(1, 1)
    game.make_a_move(3, 3)
    game.make_a_move(1, 2)
    expected = [['O', '.', '.'], ['O', 'X', '.'], ['.', '.', 'X']]
    assert expected == game.get_field()

def test_get_move():
    game = Game(3, 3)
    game.make_a_move(1, 1)
    game.make_a_move(1, 2)
    game.make_a_move(2, 2)
    game.make_a_move(2, 1)
    assert find_move(game, 1) == (1, 3, 3)

    game = Game(3, 3)
    game.make_a_move(3, 1)
    game.make_a_move(2, 2)
    game.make_a_move(1, 3)
    game.make_a_move(1, 1)
    game.make_a_move(2, 3)
    assert find_move(game, 1) == (-1, 3, 3)