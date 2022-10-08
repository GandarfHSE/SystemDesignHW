from game import Game, find_move, ResultData, NOT_FINISHED, LOSE, WIN, print_field


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
    assert game._Game__try_expand(0, 1, 1, 1, 1, 'x') == True
    assert game._Game__try_expand(0, 1, 1, 1, 1, 'o') == True

    game.make_a_move(1, 1)
    game.make_a_move(2, 1)
    game.make_a_move(1, 2)

    assert game._Game__try_expand(1, 1, 1, 0, 1, 'x') == True
    assert game._Game__try_expand(1, 1, 1, 1, 1, 'x') == False
    assert game._Game__try_expand(1, 1, 1, 1, 0, 'x') == False
    assert game._Game__try_expand(1, 1, 2, 0, 1, 'x') == False
    assert game._Game__try_expand(1, 1, 1, 1, 0, 'o') == True
    assert game._Game__try_expand(1, 2, 1, 1, 0, 'o') == False


def test_score_check():
    game = Game(3, 3)
    assert game.get_score() == NOT_FINISHED

    game.make_a_move(2, 2)
    game.make_a_move(1, 2)
    game.make_a_move(1, 1)

    assert game.get_score() == NOT_FINISHED

    game.make_a_move(2, 1)
    game.make_a_move(3, 3)

    assert game.get_score() == WIN


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
    assert find_move(game, 1) == ResultData(WIN, 3, 3)

    game = Game(3, 3)
    game.make_a_move(3, 1)
    game.make_a_move(2, 2)
    game.make_a_move(1, 3)
    game.make_a_move(1, 1)
    game.make_a_move(2, 3)
    assert find_move(game, 1) == ResultData(LOSE, 3, 3)
