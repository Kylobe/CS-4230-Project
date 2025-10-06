"""
Validates chess moves according to piece movement rules.

Defines the MoveValidator class which checks if a move is legal based on the piece type, board state, and chess rules.
"""

class MoveValidator:
    """
    Validates chess moves.
    
    Checks if moves are legal based on:
    - Piece movement patterns
    - Path obstruction
    - Capture rules
    
    Does NOT check for check/checkmate or prevent self-check.
    Check detection is done in ./check_detector.py.
    """
    
    def __init__(self, board):
        """
        Initialize the validator with a reference to the board.
        
        Args:
            board (Board): The chess board to validate moves on
        """
        self.board = board
    
    def is_valid_move(self, source, destination, current_player):
        """
        Check if a move is valid.
        
        Args:
            source (str): Starting position like 'E2'
            destination (str): Ending position like 'E4'
            current_player (str): 'white' or 'black'
        
        Returns:
            tuple: (is_valid, error_message)
                   is_valid is True if move is legal, False otherwise
                   error_message explains why move is invalid
        """
        # Convert positions to indices
        source_row, source_col = self.board.position_to_indices(source)
        dest_row, dest_col = self.board.position_to_indices(destination)
        
        # Check if positions are valid
        if source_row is None or dest_row is None:
            return False, "Invalid position format"
        
        # Get the piece at source
        piece = self.board.get_piece(source)
        
        # Check if there's a piece at source
        if piece is None:
            return False, "No piece at source position"
        
        # Check if it's the correct player's piece
        if piece.color != current_player:
            return False, "That's not your piece"
        
        # Check if source and destination are the same
        if source_row == dest_row and source_col == dest_col:
            return False, "Source and destination are the same"
        
        # Get destination piece (if any)
        dest_piece = self.board.get_piece(destination)
        
        # Check if trying to capture own piece
        if dest_piece and dest_piece.color == current_player:
            return False, "Cannot capture your own piece"
        
        # Validate move based on piece type
        if piece.piece_type == 'pawn':
            return self.validate_pawn_move(source_row, source_col, dest_row, dest_col, piece.color, dest_piece)
        elif piece.piece_type == 'rook':
            return self.validate_rook_move(source_row, source_col, dest_row, dest_col)
        elif piece.piece_type == 'knight':
            return self.validate_knight_move(source_row, source_col, dest_row, dest_col)
        elif piece.piece_type == 'bishop':
            return self.validate_bishop_move(source_row, source_col, dest_row, dest_col)
        elif piece.piece_type == 'queen':
            return self.validate_queen_move(source_row, source_col, dest_row, dest_col)
        elif piece.piece_type == 'king':
            return self.validate_king_move(source_row, source_col, dest_row, dest_col)
        
        return False, "Unknown piece type"
    
    def validate_pawn_move(self, source_row, source_col, dest_row, dest_col, color, dest_piece):
        """
        Validate pawn movement.
        
        Pawns move forward one square (or two from starting position)
        and capture diagonally forward.
        
        Args:
            source_row, source_col: Starting position indices
            dest_row, dest_col: Ending position indices
            color: 'white' or 'black'
            dest_piece: Piece at destination (None if empty)
        
        Returns:
            tuple: (is_valid, error_message)
        """
        # Determine direction based on color
        # White pawns move up (increasing row), black pawns move down (decreasing row)
        direction = 1 if color == 'white' else -1
        starting_row = 1 if color == 'white' else 6
        
        row_diff = dest_row - source_row
        col_diff = abs(dest_col - source_col)
        
        # Moving forward (no capture)
        if col_diff == 0:
            # Check if destination is empty
            if dest_piece is not None:
                return False, "Pawn cannot capture forward"
            
            # One square forward
            if row_diff == direction:
                return True, ""
            
            # Two squares forward from starting position
            if row_diff == 2 * direction and source_row == starting_row:
                # Check if path is clear
                middle_row = source_row + direction
                if self.board.grid[middle_row][source_col] is None:
                    return True, ""
                else:
                    return False, "Path is blocked"
            
            return False, "Invalid pawn move"
        
        # Diagonal capture
        elif col_diff == 1 and row_diff == direction:
            if dest_piece is not None:
                return True, ""
            else:
                return False, "Pawn can only move diagonally to capture"
        
        return False, "Invalid pawn move"
    
    def validate_rook_move(self, source_row, source_col, dest_row, dest_col):
        """
        Validate rook movement.
        
        Rooks move horizontally or vertically any number of squares.
        
        Args:
            source_row, source_col: Starting position indices
            dest_row, dest_col: Ending position indices
        
        Returns:
            tuple: (is_valid, error_message)
        """
        # Rook moves either horizontally or vertically, not both
        if source_row != dest_row and source_col != dest_col:
            return False, "Rook must move horizontally or vertically"
        
        # Check if path is clear
        if not self.is_path_clear(source_row, source_col, dest_row, dest_col):
            return False, "Path is blocked"
        
        return True, ""
    
    def validate_knight_move(self, source_row, source_col, dest_row, dest_col):
        """
        Validate knight movement.
        
        Knights move in an L-shape: 2 squares in one direction, 1 in perpendicular.
        Knights can jump over pieces.
        
        Args:
            source_row, source_col: Starting position indices
            dest_row, dest_col: Ending position indices
        
        Returns:
            tuple: (is_valid, error_message)
        """
        row_diff = abs(dest_row - source_row)
        col_diff = abs(dest_col - source_col)
        
        # Valid knight moves: (2,1) or (1,2)
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return True, ""
        
        return False, "Invalid knight move (must be L-shaped)"
    
    def validate_bishop_move(self, source_row, source_col, dest_row, dest_col):
        """
        Validate bishop movement.
        
        Bishops move diagonally any number of squares.
        
        Args:
            source_row, source_col: Starting position indices
            dest_row, dest_col: Ending position indices
        
        Returns:
            tuple: (is_valid, error_message)
        """
        row_diff = abs(dest_row - source_row)
        col_diff = abs(dest_col - source_col)
        
        # Bishop must move diagonally (same distance in both directions)
        if row_diff != col_diff:
            return False, "Bishop must move diagonally"
        
        # Check if path is clear
        if not self.is_path_clear(source_row, source_col, dest_row, dest_col):
            return False, "Path is blocked"
        
        return True, ""
    
    def validate_queen_move(self, source_row, source_col, dest_row, dest_col):
        """
        Validate queen movement.
        
        Queens move like rooks or bishops (horizontal, vertical, or diagonal).
        
        Args:
            source_row, source_col: Starting position indices
            dest_row, dest_col: Ending position indices
        
        Returns:
            tuple: (is_valid, error_message)
        """
        row_diff = abs(dest_row - source_row)
        col_diff = abs(dest_col - source_col)
        
        # Queen moves horizontally, vertically, or diagonally
        is_horizontal_vertical = (source_row == dest_row or source_col == dest_col)
        is_diagonal = (row_diff == col_diff)
        
        if not (is_horizontal_vertical or is_diagonal):
            return False, "Queen must move horizontally, vertically, or diagonally"
        
        # Check if path is clear
        if not self.is_path_clear(source_row, source_col, dest_row, dest_col):
            return False, "Path is blocked"
        
        return True, ""
    
    def validate_king_move(self, source_row, source_col, dest_row, dest_col):
        """
        Validate king movement.
        
        Kings move one square in any direction.
        
        Args:
            source_row, source_col: Starting position indices
            dest_row, dest_col: Ending position indices
        
        Returns:
            tuple: (is_valid, error_message)
        """
        row_diff = abs(dest_row - source_row)
        col_diff = abs(dest_col - source_col)
        
        # King moves one square in any direction
        if row_diff <= 1 and col_diff <= 1:
            return True, ""
        
        return False, "King can only move one square"
    
    def is_path_clear(self, source_row, source_col, dest_row, dest_col):
        """
        Check if the path between source and destination is clear.
        
        Used for rooks, bishops, and queens (pieces that can't jump).
        Knights don't use this since they can jump.
        
        Args:
            source_row, source_col: Starting position indices
            dest_row, dest_col: Ending position indices
        
        Returns:
            bool: True if path is clear, False if blocked
        """
        # Determine direction of movement
        row_step = 0 if source_row == dest_row else (1 if dest_row > source_row else -1)
        col_step = 0 if source_col == dest_col else (1 if dest_col > source_col else -1)
        
        # Start checking from the square after source
        current_row = source_row + row_step
        current_col = source_col + col_step
        
        # Check each square along the path (not including destination)
        while current_row != dest_row or current_col != dest_col:
            if self.board.grid[current_row][current_col] is not None:
                return False
            current_row += row_step
            current_col += col_step
        
        return True