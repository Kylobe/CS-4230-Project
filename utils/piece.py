"""
Represents a single chess piece with its type and color.

Defines the Piece class which encapsulates the data for a chess piece 
including its type (king, queen, etc.) and color (white or black).
"""

class Piece:
    """
    Represents a chess piece.
    
    Attributes:
        piece_type (str): Type of piece ('king', 'queen', 'rook', 'bishop', 'knight', 'pawn')
        color (str): Color of piece ('white' or 'black')
    """
    
    def __init__(self, piece_type, color):
        """
        Initialize a chess piece.
        
        Args:
            piece_type (str): The type of chess piece
            color (str): The color of the piece ('white' or 'black')
        """
        self.piece_type = piece_type
        self.color = color
    
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