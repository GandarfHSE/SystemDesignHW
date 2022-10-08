import copy
from enum import Enum


WIN = 1
LOSE = -1
NOT_FINISHED = 0


class ResultData:
    x: 0
    y: 0
    result: NOT_FINISHED

    def __init__(self, res, x, y):
        self.x = x
        self.y = y
        self.result = res

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.result == other.result


class Game:
    steps = [(0, 1), (1, 1), (1, 0), (1, -1),
             (-1, 0), (-1, -1), (-1, 0), (-1, 1)]

    def __init__(self, sz, win_cnt):
        self.cur = {
            'x': [],
            'o': []
        }
        self.n = sz
        self.win_count = win_cnt

    def __is_in_field(self, x, y):
        return 1 <= x <= self.n and 1 <= y <= self.n

    def __try_expand(self, steps_cnt, x, y, dx, dy, sign):
        if steps_cnt == 0:
            return True
        return self.__is_in_field(x + dx, y + dy) and self.cur[sign].count((x + dx, y + dy)) == 1 and self.__try_expand(steps_cnt - 1, x + dx, y + dy, dx, dy, sign)

    def is_square_free(self, x, y):
        if not self.__is_in_field(x, y):
            return False

        for sign in self.cur:
            if self.cur[sign].count((x, y)):
                return False

        return True

    def is_tie(self):
        for x in range(1, self.n + 1):
            for y in range(1, self.n + 1):
                if self.is_square_free(x, y):
                    return False
        return True

    def get_score(self):
        for sign in self.cur:
            for square in self.cur[sign]:
                for step in self.steps:
                    if self.__try_expand(self.win_count - 1, square[0], square[1], step[0], step[1], sign):
                        return WIN if sign == 'x' else LOSE

        return NOT_FINISHED

    def is_game_finished(self):
        return self.get_score() != NOT_FINISHED or self.is_tie()

    def current_sign(self):
        x_squares = len(self.cur.get('x', []))
        o_squares = len(self.cur.get('o', []))

        if x_squares == o_squares:
            return 'x'
        else:
            return 'o'

    def make_a_move(self, new_x, new_y):
        if not self.is_square_free(new_x, new_y):
            return False

        self.cur[self.current_sign()].append((new_x, new_y))
        return True

    def get_field(self):
        field = [['.' for i in range(self.n)] for j in range(self.n)]
        for sign in self.cur:
            for square in self.cur[sign]:
                field[square[1] - 1][square[0] - 1] = sign.upper()

        return field


def find_move(game, depth):
    if game.is_game_finished():
        return ResultData(game.get_score(), 0, 0)

    mn_val, mx_val = 100, -100
    mn_x, mx_x = 0, 0
    mn_y, mx_y = 0, 0

    for x in range(1, game.n + 1):
        for y in range(1, game.n + 1):
            if mn_val == LOSE and mx_val == WIN:
                break

            if game.is_square_free(x, y):
                new_game = copy.deepcopy(game)
                new_game.make_a_move(x, y)

                score = new_game.get_score()
                res = ResultData(score, x, y)
                if score == NOT_FINISHED and depth != 0:
                    res = find_move(new_game, depth - 1)

                if mn_val > res.result:
                    mn_val = res.result
                    mn_x = x
                    mn_y = y

                if mx_val < res.result:
                    mx_val = res.result
                    mx_x = x
                    mx_y = y

    if game.current_sign() == 'x':
        return ResultData(mx_val, mx_x, mx_y)
    else:
        return ResultData(mn_val, mn_x, mn_y)


def print_field(game):
    field = game.get_field()
    for i in field:
        for j in i:
            print(j, end='')
        print()
    print()
    print()


def make_a_move(game, depth):
    res = find_move(game, depth)
    game.make_a_move(res.x, res.y)
    print("Computer made a move: ", res.x, res.y)
    print()
    print_field(game)
