"""
Detects when a king is in check.

Defines the CheckDetector class which determines if a king is under attack (in check) by any enemy piece.
"""

class CheckDetector:
    """
    Detects check situations on the board.
    
    Checks if a king is under attack by examining all enemy pieces
    to see if any can legally move to the king's position.
    """
    
    @staticmethod
    def find_king(color, grid):
        """
        Find the position of a king on the board.
        
        Args:
            color (str): 'white' or 'black'
        
        Returns:
            tuple: (row, col) of the king's position, or (None, None) if not found
        """
        for row in range(8):
            for col in range(8):
                piece = grid[row][col]
                if piece and piece.piece_type == 'king' and piece.color == color:
                    return row, col
        return None, None

    @staticmethod
    def is_in_check(color, grid):
        """
        Determine if a king of the given color is in check.
        
        A king is in check if any enemy piece can legally move to its position.
        
        Args:
            color (str): 'white' or 'black'
        
        Returns:
            bool: True if the king is in check, False otherwise
        """
        # Find the king
        king_row, king_col = CheckDetector.find_king(color, grid)
        
        # If king not found (captured), return False
        if king_row is None:
            return False
        
        # Convert king position to chess notation
        king_pos = CheckDetector.indices_to_position(king_row, king_col)
        
        # Determine enemy color
        enemy_color = 'black' if color == 'white' else 'white'
        
        # Check all squares for enemy pieces
        for row in range(8):
            for col in range(8):
                piece = grid[row][col]
                
                # Skip if square is empty or contains friendly piece
                if piece is None or piece.color != enemy_color:
                    continue
                
                piece_legal_moves = piece.get_legal_moves()

                if king_pos in piece_legal_moves:
                    return True

        return False

    @staticmethod
    def indices_to_position(row, col):
        """
        Convert grid indices to chess notation.
        
        Args:
            row (int): Row index (0-7)
            col (int): Column index (0-7)
        
        Returns:
            str: Chess position like 'E2'
        """
        file = chr(ord('A') + col)
        rank = str(row + 1)
        return file + rank