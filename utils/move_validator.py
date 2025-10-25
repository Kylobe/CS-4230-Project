"""
Validates chess moves according to piece movement rules.

Defines the MoveValidator class which checks if a move is legal based on the piece type, board state, and chess rules.
"""
from .board import Board
from .check_detector import CheckDetector

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
        self.board : Board = board

    def generate_valid_moves(self, current_player):
        legal_moves = []
        king_in_check_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if not piece is None and piece.color == current_player:
                    for potential_move in piece.get_legal_moves():
                        new_grid, _ = self.board.move_piece(piece.get_uci_pos(), potential_move)
                        if not CheckDetector.is_in_check(current_player, new_grid):
                            legal_moves.append(piece.get_uci_pos() + " " + potential_move)
                        else:
                            king_in_check_moves.append(piece.get_uci_pos() + " " + potential_move)
        return legal_moves, king_in_check_moves
    
    def is_valid_move(self, source: str, destination: str, current_player: str):
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
        
        legal_moves, king_in_check_moves = self.generate_valid_moves(current_player)

        potential_move = source + " " + destination

        if potential_move in legal_moves:
            return True, ""

        if potential_move in king_in_check_moves:
            return False, "Can't put your king in jeopardy"

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

        # Check if trying to move through another piece
        if self._path_is_blocked(piece, source_row, source_col, dest_row, dest_col):
            return False, "That path is blocked"
        
        return False, "Unknown piece type"
    
    def _path_is_blocked(self, piece, source_row, source_col, dest_row, dest_col):
        """Checks whether there's a piece on the path `piece` wants to travel along.

        If `piece` is a knight, this method always returns `False`.

        Returns:
            bool: `True` if the action is invalid (i.e., the path is blocked);
            `False` otherwise.
        """
        piece_type = piece.piece_type

        # Let knights jump over pieces
        if piece_type == "knight":
            return False

        # Find direction of movement
        row_dir = 0 if (dest_row == source_row) else ((dest_row - source_row) // abs(dest_row - source_row))
        col_dir = 0 if (dest_col == source_col) else ((dest_col - source_col) // abs(dest_col - source_col))

        # Check each square in the path
        curr_row, curr_col = source_row + row_dir, source_col + col_dir
        while (curr_row, curr_col) != (dest_row, dest_col):
            if self.board.grid[curr_row][curr_col] is not None:
                return True
            curr_row += row_dir
            curr_col += col_dir

        return False
