from classes import Board

def main():
    my_board = Board()
    my_board.set_square(6, 4, "king", "BLACK")
    print(my_board)
    print(my_board.get_square(6, 4).get_legal_moves())

if __name__ == "__main__":
    main()
