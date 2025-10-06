"""
Manages the chess board and piece positions.

Defines the Board class which maintains the 8x8 grid
of chess pieces, handles piece placement, movement, and board display.
"""

from .piece import Piece

class Board:
    """
    Represents the chess board.
    
    The board is an 8x8 grid where each cell can contain a Piece or None.
    Coordinates use chess notation: files A-H (columns) and ranks 1-8 (rows).
    """
    
    def __init__(self):
        """
        Initialize an 8x8 chess board.
        
        Creates an empty board and then sets up the initial chess position.
        """
        # Create 8x8 grid initialized with None (empty squares)
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_initial_position()
    
    def setup_initial_position(self):
        """
        Set up the standard starting chess position.
        
        Places all pieces in their correct starting positions.
        """
        # Set up white pieces
        # All white pieces except pawns at index 0
        self.grid[0][0] = Piece('rook', 'white')
        self.grid[0][1] = Piece('knight', 'white')
        self.grid[0][2] = Piece('bishop', 'white')
        self.grid[0][3] = Piece('queen', 'white')
        self.grid[0][4] = Piece('king', 'white')
        self.grid[0][5] = Piece('bishop', 'white')
        self.grid[0][6] = Piece('knight', 'white')
        self.grid[0][7] = Piece('rook', 'white')
        
        # Set up white pawns at index 1
        for col in range(8):
            self.grid[1][col] = Piece('pawn', 'white')
        
        # Set up black pawns at index 6
        for col in range(8):
            self.grid[6][col] = Piece('pawn', 'black')
        
        # Set up black pieces all but pawns at index 7
        self.grid[7][0] = Piece('rook', 'black')
        self.grid[7][1] = Piece('knight', 'black')
        self.grid[7][2] = Piece('bishop', 'black')
        self.grid[7][3] = Piece('queen', 'black')
        self.grid[7][4] = Piece('king', 'black')
        self.grid[7][5] = Piece('bishop', 'black')
        self.grid[7][6] = Piece('knight', 'black')
        self.grid[7][7] = Piece('rook', 'black')
    
    def display(self):
        """
        Display the chess board in a text-based grid format.
        
        Shows the board from white's perspective.
        Column labels A-H labeled at the top and bottom.
        Pieces shown with their character representations.
        """
        # Print column labels
        print("    A   B   C   D   E   F   G   H")
        print("  " + "-" * 33)
        print("  " + "-" * 33)

        # Print from top to bottom
        for rank in range(7, -1, -1):
            # Print row number
            print(f"{rank + 1} ", end="")
            
            # Print each square in the rank
            for file in range(8):
                piece = self.grid[rank][file]
                # Show piece character or empty space
                piece_char = str(piece) if piece else ' '
                print(f"| {piece_char} ", end="")
            
            print("|")
            print("  " + "-" * 33)
        
        # Print column labels
        print("  " + "-" * 33)
        print("    A   B   C   D   E   F   G   H")
    
    def position_to_indices(self, position):
        """
        Convert chess notation (e.g., 'E2') to grid indices.
        
        Args:
            position (str): Chess position in format like 'E2', 'a1', etc.
        
        Returns:
            tuple: (row, col) indices for the grid, or (None, None) if invalid
        """
        # Convert to uppercase and strip whitespace
        position = position.strip().upper()
        
        # Check if position is valid format (letter + number)
        if len(position) != 2:
            return None, None
        
        file_char = position[0]
        rank_char = position[1]
        
        # Validate file (A-H) and rank (1-8)
        if file_char not in 'ABCDEFGH' or rank_char not in '12345678':
            return None, None
        
        # Convert file letter to column index
        col = ord(file_char) - ord('A')
        
        # Convert rank number to row index
        row = int(rank_char) - 1
        
        return row, col
    
    def get_piece(self, position):
        """
        Get the piece at a given position.
        
        Args:
            position (str): Chess position like 'E2'
        
        Returns:
            Piece or None: The piece at that position, or None if empty/invalid
        """
        row, col = self.position_to_indices(position)
        if row is None:
            return None
        return self.grid[row][col]
    
    def move_piece(self, source, destination):
        """
        Move a piece from source to destination.
        
        This method physically moves the piece on the board.
        It does NOT validate if the move is legal.
        Validation will be done in a ./move_validator.py.
        
        Args:
            source (str): Starting position like 'E2'
            destination (str): Ending position like 'E4'
        
        Returns:
            Piece or None: The captured piece if any, None otherwise
        """
        source_row, source_col = self.position_to_indices(source)
        dest_row, dest_col = self.position_to_indices(destination)
        
        # Get the piece being moved
        piece = self.grid[source_row][source_col]
        
        # Get any piece being captured
        captured = self.grid[dest_row][dest_col]
        
        # Move the piece
        self.grid[dest_row][dest_col] = piece
        self.grid[source_row][source_col] = None
        
        # Handle pawn promotion (pawn reaching opposite end)
        if piece.piece_type == 'pawn':
            # White pawn reaching index 7
            if piece.color == 'white' and dest_row == 7:
                self.grid[dest_row][dest_col] = Piece('queen', 'white')
            # Black pawn reaching index 0
            elif piece.color == 'black' and dest_row == 0:
                self.grid[dest_row][dest_col] = Piece('queen', 'black')
        
        return captured