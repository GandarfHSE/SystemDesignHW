import copy
from enum import Enum

class ResultData:
    def __init__(self, res, x, y):
        self.x = x
        self.y = y
        self.result = res

class Score(Enum):
    'WIN' = 1
    'LOSE' = -1
    'NOT_FINISHED' = 0

class Game:
    steps = [(0, 1), (1, 1), (1, 0), (1, -1), (-1, 0), (-1, -1), (-1, 0), (-1, 1)]

    def __init__(self, sz, win_cnt):
        self.cur_x = []
        self.cur_o = []
        self.n = sz
        self.win_count = win_cnt
        self.move_x = True

    def __is_in_field(self, x, y):
        return x >= 1 and y >= 1 and x <= self.n and y <= self.n

    def __try_expand_x(self, steps_cnt, x, y, dx, dy):
        if steps_cnt == 0:
            return True
        else:
            return self.__is_in_field(x + dx, y + dy) and self.cur_x.count((x + dx, y + dy)) == 1 and self.__try_expand_x(steps_cnt - 1, x + dx, y + dy, dx, dy)

    def __try_expand_o(self, steps_cnt, x, y, dx, dy):
        if steps_cnt == 0:
            return True
        else:
            return self.__is_in_field(x + dx, y + dy) and self.cur_o.count((x + dx, y + dy)) == 1 and self.__try_expand_o(steps_cnt - 1, x + dx, y + dy, dx, dy)

    def is_square_free(self, x, y):
        return self.cur_x.count((x, y)) == 0 and self.cur_o.count((x, y)) == 0 and self.__is_in_field(x, y)

    def is_tie(self):
        for x in range(1, self.n + 1):
            for y in range(1, self.n + 1):
                if self.is_square_free(x, y):
                    return False
        return True

    def get_score(self):
        for sq in self.cur_x:
            for d in self.steps:
                if self.__try_expand_x(self.win_count - 1, sq[0], sq[1], d[0], d[1]):
                    return Score.WIN

        for sq in self.cur_o:
            for d in self.steps:
                if self.__try_expand_o(self.win_count - 1, sq[0], sq[1], d[0], d[1]):
                    return Score.LOSE

        return Score.NOT_FINISHED

    def is_game_finished(self):
        return self.get_score() != Score.NOT_FINISHED or self.is_tie()

    def make_a_move(self, new_x, new_y):
        if self.is_square_free(new_x, new_y):
            if self.move_x:
                self.cur_x.append((new_x, new_y))
                self.move_x = False
            else:
                self.cur_o.append((new_x, new_y))
                self.move_x = True
            return True
        else:
            return False

    def get_field(self):
        field = [['.' for i in range(self.n)] for j in range(self.n)]
        for sq in self.cur_x:
            field[sq[1] - 1][sq[0] - 1] = 'X'
        for sq in self.cur_o:
            field[sq[1] - 1][sq[0] - 1] = 'O'

        return field


def find_move(game, depth):
    if game.is_game_finished():
        return ResultData(game.get_score(), 0, 0)
    
    mn_val, mx_val = 100, -100
    mn_x, mx_x = 0, 0
    mn_y, mx_y = 0, 0

    for x in range(1, game.n + 1):
        for y in range(1, game.n + 1):
            if mn_val == Score.LOSE and mx_val == Score.WIN:
                break

            if game.is_square_free(x, y):
                new_game = copy.deepcopy(game)
                new_game.make_a_move(x, y)

                score = new_game.get_score()
                res = Result(score, x, y)
                if score == 0 and depth != 0:
                    res = find_move(new_game, depth - 1)
                
                if mn_val > res.result:
                    mn_val = res.result
                    mn_x = x
                    mn_y = y
                
                if mx_val < res.result:
                    mx_val = res.result
                    mx_x = x
                    mx_y = y
    
    if game.move_x:
        return (mx_val, mx_x, mx_y)
    else:
        return (mn_val, mn_x, mn_y)

def print_field(game):
    field = game.get_field()
    for i in field:
        for j in i:
            print(j, end = '')
        print("\n", end = '')
    print("\n")

def make_a_move(game, depth):
    res = find_move(game, depth)
    game.make_a_move(res.x, res.y)
    print("Computer made a move: ", res.x, res.y, "\n")
    print_field(game)
