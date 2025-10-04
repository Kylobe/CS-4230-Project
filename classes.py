from abc import ABC

class Board:
    def __init__(self):
        self.board = []
        for _ in range(8):
            self.board.append([None, None, None, None, None, None, None, None])
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                cur_rank = 8 - i
                cur_file = j + 1
                cur_piece = None
                if cur_rank == 7 or cur_rank == 8:
                    color = "BLACK"
                elif cur_rank == 1 or cur_rank == 2:
                    color = "WHITE"
                if cur_rank == 1 or cur_rank == 8:
                    if cur_file == 1 or cur_file == 8:
                        cur_piece = Rook(color, self, cur_rank, cur_file)
                    elif cur_file == 2 or cur_file == 7:
                        cur_piece = Knight(color, self, cur_rank, cur_file)
                    elif cur_file == 3 or cur_file == 6:
                        cur_piece = Bishop(color, self, cur_rank, cur_file)
                    elif cur_file == 4:
                        cur_piece = Queen(color, self, cur_rank, cur_file)
                    elif cur_file == 5:
                        cur_piece = King(color, self, cur_rank, cur_file)
                if cur_rank == 2 or cur_rank == 7:
                    cur_piece = Pawn(color, self, cur_rank, cur_file)
                self.board[8 - cur_rank][cur_file - 1] = cur_piece
        self.color_to_move = "WHITE"

    def get_square(self, rank, file):
        rank_index = 8 - rank
        file_index = file - 1
        return self.board[rank_index][file_index]

    def get_legal_moves(self):
        legal_moves = []
        for rank in self.board:
            for square in rank:
                if isinstance(square, PieceABC):
                    legal_moves += square.get_legal_moves()
        return legal_moves

    def __str__(self):
        return_str = ""
        files = "ABCDEFGH"
        for i, rank in enumerate(self.board):
            return_str += f"{8 - i}    "
            for piece in rank:
                if isinstance(piece, PieceABC):
                    return_str += str(piece)
                else:
                    return_str += "*"
                return_str += " "
            return_str += "\n"
        return_str += "\n     "
        for char in files:
            return_str += char + " "
        return return_str

class PieceABC(ABC):
    def __init__(self, color: str, board: Board, rank: int, file: int):
        self.color: str = color
        self.board: Board = board
        self.rank: int = rank
        self.file: int = file

    def get_legal_moves(self) -> list[str]:
        pass

    def __str__(self):
        pass

class King(PieceABC):
    def __init__(self, color: str, board: Board, rank: int, file: int):
        super().__init__(color, board, rank, file)

    def get_legal_moves(self):
        if self.color == "WHITE":
            pass

    def __str__(self):
        if self.color == "WHITE":
            return "K"
        else:
            return "k"

class Queen(PieceABC):
    def __init__(self, color: str, board: Board, rank: int, file: int):
        super().__init__(color, board, rank, file)

    def get_legal_moves(self):
        if self.color == "WHITE":
            pass

    def __str__(self):
        if self.color == "WHITE":
            return "Q"
        else:
            return "q"

class Rook(PieceABC):
    def __init__(self, color: str, board: Board, rank: int, file: int):
        super().__init__(color, board, rank, file)

    def get_legal_moves(self):
        if self.color == "WHITE":
            pass

    def __str__(self):
        if self.color == "WHITE":
            return "R"
        else:
            return "r"

class Bishop(PieceABC):
    def __init__(self, color: str, board: Board, rank: int, file: int):
        super().__init__(color, board, rank, file)

    def get_legal_moves(self):
        if self.color == "WHITE":
            pass

    def __str__(self):
        if self.color == "WHITE":
            return "B"
        else:
            return "b"

class Knight(PieceABC):
    def __init__(self, color: str, board: Board, rank: int, file: int):
        super().__init__(color, board, rank, file)

    def get_legal_moves(self):
        if self.color == "WHITE":
            pass

    def __str__(self):
        if self.color == "WHITE":
            return "N"
        else:
            return "n"

class Pawn(PieceABC):
    def __init__(self, color: str, board: Board, rank: int, file: int):
        super().__init__(color, board, rank, file)

    def get_legal_moves(self):
        legal_moves = []
        forward_offset = 0
        if self.color == "WHITE":
            forward_offset = 1
            if self.rank == 1:
                double_move_square = self.board.get_square(self.rank + 2 * forward_offset, self.file)
                if double_move_square is None:
                    legal_moves.append(((self.rank, self.file), (self.rank + 2 * forward_offset, self.file)))
        elif self.color == "BLACK":
            forward_offset = -1
            if self.rank == 7:
                double_move_square = self.board.get_square(self.rank + 2 * forward_offset, self.file)
                if double_move_square is None:
                    legal_moves.append(((self.rank, self.file), (self.rank + 2 * forward_offset, self.file)))
        forward_square = self.board.get_square(self.rank + forward_offset, self.file)
        if forward_square is None:
            legal_moves.append(((self.rank, self.file), (self.rank + forward_offset, self.file)))
        right_diagnol_square = None
        if self.file <= 7:
            right_diagnol_square = self.board.get_square(self.rank + forward_offset, self.file + 1)
        if isinstance(right_diagnol_square, PieceABC) and right_diagnol_square.color != self.color:
            legal_moves.append(((self.rank, self.file), (self.rank + forward_offset, self.file + 1)))
        left_diagnol_square = None
        if self.file >= 2:
            left_diagnol_square = self.board.get_square(self.rank + forward_offset, self.file - 1)
        if isinstance(left_diagnol_square, PieceABC) and left_diagnol_square.color != self.color:
            legal_moves.append(((self.rank, self.file), (self.rank + forward_offset, self.file - 1)))
        return legal_moves


    def __str__(self):
        if self.color == "WHITE":
            return "P"
        else:
            return "p"

