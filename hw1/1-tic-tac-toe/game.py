import copy

class Game:
    dd = [(0, 1), (1, 1), (1, 0), (1, -1), (-1, 0), (-1, -1), (-1, 0), (-1, 1)]

    def __init__(self, sz, row_sz):
        self.cur_x = []
        self.cur_o = []
        self.n = sz
        self.row_n = row_sz
        self.move_x = True

    def __is_in_field(self, x, y):
        return x >= 1 and y >= 1 and x <= self.n and y <= self.n

    def __try_expand_x(self, rem, x, y, dx, dy):
        if rem == 0:
            return True
        else:
            return self.__is_in_field(x + dx, y + dy) and self.cur_x.count((x + dx, y + dy)) == 1 and self.__try_expand_x(rem - 1, x + dx, y + dy, dx, dy)

    def __try_expand_o(self, rem, x, y, dx, dy):
        if rem == 0:
            return True
        else:
            return self.__is_in_field(x + dx, y + dy) and self.cur_o.count((x + dx, y + dy)) == 1 and self.__try_expand_o(rem - 1, x + dx, y + dy, dx, dy)

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
            for d in self.dd:
                if self.__try_expand_x(self.row_n - 1, sq[0], sq[1], d[0], d[1]):
                    return 1

        for sq in self.cur_o:
            for d in self.dd:
                if self.__try_expand_o(self.row_n - 1, sq[0], sq[1], d[0], d[1]):
                    return -1

        return 0

    def is_game_finished(self):
        return self.get_score() != 0 or self.is_tie()

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
        return (game.get_score(), 0, 0)
    
    mn_val = 100
    mn_x = 0
    mn_y = 0
    mx_val = -100
    mx_x = 0
    mx_y = 0

    for x in range(1, game.n + 1):
        for y in range(1, game.n + 1):
            if mn_val == -1 and mx_val == 1:
                break

            if game.is_square_free(x, y):
                new_game = copy.deepcopy(game)
                new_game.make_a_move(x, y)

                score = new_game.get_score()
                res = (score, x, y)
                if score == 0 and depth != 0:
                    res = find_move(new_game, depth - 1)
                
                #if depth == 5:
                #    print(x, y, res)
                
                if mn_val > res[0]:
                    mn_val = res[0]
                    mn_x = x
                    mn_y = y
                
                if mx_val < res[0]:
                    mx_val = res[0]
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
    game.make_a_move(res[1], res[2])
    print("Computer made a move: ", res[1], res[2], "\n")
    print_field(game)