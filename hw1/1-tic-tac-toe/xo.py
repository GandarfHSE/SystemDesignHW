from game import Game, print_field, make_a_move

def main():
    n = int(input("Enter size of field: "))
    game = None
    if n <= 5:
        game = Game(n, n)
    else:
        game = Game(n, 5)
    
    side = None
    while True:
        side = input("Choose your side (X/O): ")
        if side == "X" or side == "O":
            break
        else:
            print("Incorrect input. Enter X or O\n")

    depth = int(input("Enter computer's depth: "))

    print_field(game)
    if side == "O":
        make_a_move(game, depth)
        if game.is_game_finished():
            print("You've lost =(\n")
    
    while game.is_game_finished() == False:
        x, y = (0, 0)
        while True:
            x, y = map(int, input("Choose your move: ").split())
            if game.is_square_free(x, y):
                break
            else:
                print("Incorrect square. Try again\n")
        
        game.make_a_move(x, y)
        print_field(game)
        if game.is_game_finished():
            if game.is_tie():
                print("It's a tie!\n")
            else:
                print("Congratulations! You won\n")
            break

        make_a_move(game, depth)
        if game.is_game_finished():
            if game.is_tie():
                print("It's a tie!\n")
            else:
                print("You've lost =(\n")
            break

while True:
    main()