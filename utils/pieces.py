from abc import ABC, abstractmethod
from .static_chess_methods import StaticChessMethods

class Piece(ABC):
    """
    Represents a chess piece.
    
    Attributes:
        piece_type (str): Type of piece ('king', 'queen', 'rook', 'bishop', 'knight', 'pawn')
        color (str): Color of piece ('white' or 'black')
    """
    
    def __init__(self, color, rank, file, grid):
        """
        Initialize a chess piece.
        
        Args:
            color (str): The color of the piece ('white' or 'black')
            row (int): The the index of the pieces row
            col (int): The the index of the pieces column
            board (Board): The board game object
        """
        self.color = color
        self.row = rank
        self.col = file
        self.grid = grid
    
    @property
    @abstractmethod
    def piece_type(self):
        pass

    @abstractmethod
    def get_legal_moves(self):
        pass

    def get_uci_pos(self):
        return StaticChessMethods.indices_to_uci(self.row, self.col)

    def set_row_col(self, row, col):
        self.row = row
        self.col = col

    def set_grid(self, grid):
        self.grid = grid

    @abstractmethod
    def copy(self):
        pass

    def __str__(self):
        """
        Return string representation of the piece for display.
        
        Uses uppercase letters for white pieces and lowercase for black.
        Knight is represented as 'n' to avoid confusion with king.
        
        Returns:
            str: Single character representing the piece
        """
        # Map piece types to their display characters
        piece_chars = {
            'king': 'k',
            'queen': 'q',
            'rook': 'r',
            'bishop': 'b',
            'knight': 'n',
            'pawn': 'p'
        }
        
        # Get the character for this piece type
        char = piece_chars[self.piece_type]
        
        # Return uppercase for white, lowercase for black
        return char.upper() if self.color == 'white' else char

    def __repr__(self):
        return str(self)

class Pawn(Piece):
    def __init__(self, color, row, col, grid):
        super().__init__(color, row, col, grid)

    @property
    def piece_type(self):
        return "pawn"

    def get_legal_moves(self):
        """
        Generates a list of potentially legal moves from the pawns perspective.
        Pawns move forward one square (or two from starting position)
        and capture diagonally forward.

        Returns:
            list: [uci strings]
        """
        # initalizing an empty list
        # Determine direction based on color
        # White pawns move up (increasing row), black pawns move down (decreasing row)
        legal_moves = []
        direction = 1 if self.color == "white" else -1
        starting_row = 1 if self.color == "white" else 6

        # Calculating forward rank index
        forward_rank = self.row + direction

        # check to see if a piece is blocking the pawn. Pawns can't capture forwards.
        if self.grid[forward_rank][self.col] is None:
            legal_moves.append(StaticChessMethods.indices_to_uci(forward_rank, self.col))

        # Calculating both diagnol indices
        left_col = self.col - 1
        right_col  = self.col + 1

        # Making sure indices are within the bounds of the columns
        if left_col >= 0 and left_col <= 7:
            # Checking the board to see if there is a piece on that square
            capture_piece = self.grid[forward_rank][left_col]
            if isinstance(capture_piece, Piece) and capture_piece.color != self.color:
                legal_moves.append(StaticChessMethods.indices_to_uci(forward_rank, left_col))

        if right_col >= 0 and right_col <= 7:
            capture_piece = self.grid[forward_rank][right_col]
            if isinstance(capture_piece, Piece) and capture_piece.color != self.color:
                legal_moves.append(StaticChessMethods.indices_to_uci(forward_rank, right_col))

        # Handling double move when the pawn is on its starting sqaure
        if self.row == starting_row:
            forward_rank += direction
            if self.grid[forward_rank][self.col] is None:
                legal_moves.append(StaticChessMethods.indices_to_uci(forward_rank, self.col))
        
        return legal_moves

    def copy(self):
        return Pawn(self.color, self.row, self.col, self.grid)

class Knight(Piece):
    def __init__(self, color, row, col, grid):
        super().__init__(color, row, col, grid)

    @property
    def piece_type(self):
        return "knight"

    def get_legal_moves(self):
        """
        Generates a list of potentially legal moves from the knights perspective.
        knights move and capture in an L shape

        Returns:
            list: [uci strings]
        """

        legal_moves = []
        row_offsets = [-2, -2, -1, -1, 1, 1, 2, 2]
        col_offsets = [-1, 1, -2, 2, -2, 2, -1, 1]
        offsets = zip(row_offsets, col_offsets)
        for row_offset, col_offset in  offsets:
            cur_row = self.row + row_offset
            cur_col = self.col + col_offset
            if cur_row >= 0 and cur_col >= 0 and cur_row <= 7 and cur_col <= 7:
                capture_piece = self.grid[cur_row][cur_col]
                if (isinstance(capture_piece, Piece) and capture_piece.color != self.color) or capture_piece is None:
                    legal_moves.append(StaticChessMethods.indices_to_uci(cur_row, cur_col))

        return legal_moves

    def copy(self):
        return Knight(self.color, self.row, self.col, self.grid)

class Bishop(Piece):
    def __init__(self, color, row, col, grid):
        super().__init__(color, row, col, grid)

    @property
    def piece_type(self):
        return "bishop"

    def get_legal_moves(self):
        """
        Generates a list of potentially legal moves from the Bishops perspective.
        Bishops move and capture on the diagnol.

        Returns:
            list: [uci strings]
        """

        legal_moves = []
        forward_directions = [-1, -1, 1, 1]
        horizontal_directions = [1, -1, 1, -1]
        directions = zip(forward_directions, horizontal_directions)
        
        for forward_direction, horizontal_direction in directions:
            for i in range(1, 8):
                cur_row = self.row + i * forward_direction
                cur_col = self.col + i * horizontal_direction

                if cur_row < 0 or cur_row > 7 or cur_col < 0 or cur_col > 7:
                    break

                capture_piece = self.grid[cur_row][cur_col]
                if capture_piece is None:
                    legal_moves.append(StaticChessMethods.indices_to_uci(cur_row, cur_col))
                elif isinstance(capture_piece, Piece):
                    if capture_piece.color != self.color:
                        legal_moves.append(StaticChessMethods.indices_to_uci(cur_row, cur_col))
                    break

        return legal_moves

    def copy(self):
        return Bishop(self.color, self.row, self.col, self.grid)

class Rook(Piece):
    def __init__(self, color, row, col, grid):
        super().__init__(color, row, col, grid)

    @property
    def piece_type(self):
        return "rook"

    def get_legal_moves(self):
        """
        Generates a list of potentially legal moves from the Rooks perspective.
        Rooks move and capture on the vertical or horizontal.
        Returns:
            list: [uci strings]
        """

        legal_moves = []
        forward_directions = [-1, 1, 0, 0]
        horizontal_directions = [0, 0, -1, 1]
        directions = zip(forward_directions, horizontal_directions)
        
        for forward_direction, horizontal_direction in directions:
            for i in range(1, 8):
                cur_row = self.row + i * forward_direction
                cur_col = self.col + i * horizontal_direction

                if cur_row < 0 or cur_row > 7 or cur_col < 0 or cur_col > 7:
                    break

                capture_piece = self.grid[cur_row][cur_col]
                if capture_piece is None:
                    legal_moves.append(StaticChessMethods.indices_to_uci(cur_row, cur_col))
                elif isinstance(capture_piece, Piece):
                    if capture_piece.color != self.color:
                        legal_moves.append(StaticChessMethods.indices_to_uci(cur_row, cur_col))
                    break
        
        return legal_moves

    def copy(self):
        return Rook(self.color, self.row, self.col, self.grid)

class Queen(Piece):
    def __init__(self, color, row, col, grid):
        super().__init__(color, row, col, grid)

    @property
    def piece_type(self):
        return "queen"

    def get_legal_moves(self):
        """
        Generates a list of potentially legal moves from the queens perspective.
        Queens move and capture on the vertical, horizontal, or diagnol.
        She has the combinations of the rooks and bishops moves.
        Returns:
            list: [uci strings]
        """

        legal_moves = []
        forward_directions = [-1, 1, 0, 0]
        horizontal_directions = [0, 0, -1, 1]
        directions = zip(forward_directions, horizontal_directions)
        
        for forward_direction, horizontal_direction in directions:
            for i in range(1, 8):
                cur_row = self.row + i * forward_direction
                cur_col = self.col + i * horizontal_direction

                if cur_row < 0 or cur_row > 7 or cur_col < 0 or cur_col > 7:
                    break

                capture_piece = self.grid[cur_row][cur_col]
                if capture_piece is None:
                    legal_moves.append(StaticChessMethods.indices_to_uci(cur_row, cur_col))
                elif isinstance(capture_piece, Piece):
                    if capture_piece.color != self.color:
                        legal_moves.append(StaticChessMethods.indices_to_uci(cur_row, cur_col))
                    break

        forward_directions = [-1, -1, 1, 1]
        horizontal_directions = [1, -1, 1, -1]
        directions = zip(forward_directions, horizontal_directions)
        
        for forward_direction, horizontal_direction in directions:
            for i in range(1, 8):
                cur_row = self.row + i * forward_direction
                cur_col = self.col + i * horizontal_direction

                if cur_row < 0 or cur_row > 7 or cur_col < 0 or cur_col > 7:
                    break

                capture_piece = self.grid[cur_row][cur_col]
                if capture_piece is None:
                    legal_moves.append(StaticChessMethods.indices_to_uci(cur_row, cur_col))
                elif isinstance(capture_piece, Piece):
                    if capture_piece.color != self.color:
                        legal_moves.append(StaticChessMethods.indices_to_uci(cur_row, cur_col))
                    break

        return legal_moves

    def copy(self):
        return Queen(self.color, self.row, self.col, self.grid)

class King(Piece):
    def __init__(self, color, row, col, grid):
        super().__init__(color, row, col, grid)

    @property
    def piece_type(self):
        return "king"

    def get_legal_moves(self):
        """
        Generates a list of potentially legal moves from the kings perspective.
        kings move and capture on the vertical, horizontal, or diagnol but only 1 square.

        Returns:
            list: [uci strings]
        """

        legal_moves = []
        forward_directions = [-1, 1, 0, 0]
        horizontal_directions = [0, 0, -1, 1]
        directions = zip(forward_directions, horizontal_directions)
        
        for forward_direction, horizontal_direction in directions:
            for i in range(1, 2):
                cur_row = self.row + i * forward_direction
                cur_col = self.col + i * horizontal_direction

                if cur_row < 0 or cur_row > 7 or cur_col < 0 or cur_col > 7:
                    break

                capture_piece = self.grid[cur_row][cur_col]
                if capture_piece is None:
                    legal_moves.append(StaticChessMethods.indices_to_uci(cur_row, cur_col))
                elif isinstance(capture_piece, Piece):
                    if capture_piece.color != self.color:
                        legal_moves.append(StaticChessMethods.indices_to_uci(cur_row, cur_col))
                    break

        forward_directions = [-1, -1, 1, 1]
        horizontal_directions = [1, -1, 1, -1]
        directions = zip(forward_directions, horizontal_directions)
        
        for forward_direction, horizontal_direction in directions:
            for i in range(1, 2):
                cur_row = self.row + i * forward_direction
                cur_col = self.col + i * horizontal_direction

                if cur_row < 0 or cur_row > 7 or cur_col < 0 or cur_col > 7:
                    break

                capture_piece = self.grid[cur_row][cur_col]
                if capture_piece is None:
                    legal_moves.append(StaticChessMethods.indices_to_uci(cur_row, cur_col))
                elif isinstance(capture_piece, Piece):
                    if capture_piece.color != self.color:
                        legal_moves.append(StaticChessMethods.indices_to_uci(cur_row, cur_col))
                    break

        return legal_moves

    def copy(self):
        return King(self.color, self.row, self.col, self.grid)

