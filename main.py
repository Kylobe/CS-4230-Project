from classes import Board

def main():
    my_board = Board()
    my_board.set_square(4, 4, "queen", "BLACK")
    print(my_board)
    print(my_board.get_square(4, 4).get_legal_moves())

if __name__ == "__main__":
    main()



