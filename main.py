from classes import Board

def main():
    my_board = Board()
    print(my_board)
    print(my_board.get_square(8, 2).get_legal_moves())

if __name__ == "__main__":
    main()



