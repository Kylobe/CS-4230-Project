"""
Unit Tests for Chess Game

Unit tests verify individual components in isolation, testing single methods and classes without dependencies.

EXPORT:
- test_case decorator function to identify test cases
- All test cases are labeled with (unique identifier, description)
- unique identifier = 'TC-UNIT-xxx'

An example is given to make the export run cleanly.
"""
import unittest

from utils.pieces import Pawn, Knight, Bishop, Rook, Queen, King, Piece
from utils.board import Board
from utils.check_detector import CheckDetector
from utils.static_chess_methods import StaticChessMethods


def test_case(test_id, description):
    """
    Decorator to add test metadata for Excel export.
    
    Args:
        test_id: Unique identifier like 'TC-UNIT-001'
        description: Human-readable description of what the test verifies
    """
    def decorator(func):
        func.test_id = test_id
        func.test_description = description
        return func
    return decorator


class TestChessGameUnit(unittest.TestCase):
    """
    Unit tests for individual chess game components.
    Tests single methods and classes in isolation.
    """
    
    # HELPER FUNCTIONS
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.empty_grid = [[None for _ in range(8)] for _ in range(8)]
        
    def tearDown(self):
        """Clean up after each test method."""
        self.empty_grid = None
    
    # TEST CASES
    @test_case('TC-UNIT-001', 'Verify UCI to indices conversion for all valid positions')
    def test_uci_to_indices_conversion(self):
        """
        Test StaticChessMethods.uci_to_indices() method:
        - Converts chess notation to grid indices correctly
        - Handles uppercase and lowercase input
        - Returns None for invalid input
        
        This is a complete unit test with all attributes for Excel export:
        - test_id: TC-UNIT-001
        - description: Verify UCI to indices conversion
        - Tests specific method in isolation
        - Includes multiple assertions for thorough coverage
        """
        # TEST 1: Corner positions
        row, col = StaticChessMethods.uci_to_indices('A1')
        self.assertEqual((row, col), (0, 0), "A1 should map to (0, 0)")
        
        row, col = StaticChessMethods.uci_to_indices('H1')
        self.assertEqual((row, col), (0, 7), "H1 should map to (0, 7)")
        
        row, col = StaticChessMethods.uci_to_indices('A8')
        self.assertEqual((row, col), (7, 0), "A8 should map to (7, 0)")
        
        row, col = StaticChessMethods.uci_to_indices('H8')
        self.assertEqual((row, col), (7, 7), "H8 should map to (7, 7)")
        
        # TEST 2: Center positions
        row, col = StaticChessMethods.uci_to_indices('E4')
        self.assertEqual((row, col), (3, 4), "E4 should map to (3, 4)")
        
        row, col = StaticChessMethods.uci_to_indices('D5')
        self.assertEqual((row, col), (4, 3), "D5 should map to (4, 3)")
        
        # TEST 3: Lowercase input (should handle case-insensitivity)
        row, col = StaticChessMethods.uci_to_indices('e4')
        self.assertEqual((row, col), (3, 4), "Lowercase e4 should work")
        
        # TEST 4: Invalid input
        row, col = StaticChessMethods.uci_to_indices('Z9')
        self.assertEqual((row, col), (None, None), "Invalid position should return None")
        
        row, col = StaticChessMethods.uci_to_indices('Invalid')
        self.assertEqual((row, col), (None, None), "Invalid format should return None")
        
        row, col = StaticChessMethods.uci_to_indices('')
        self.assertEqual((row, col), (None, None), "Empty string should return None")

    @test_case('TC-UNIT-002', 'Verify indices to UCI conversion for all valid positions')
    def test_indices_to_uci_conversion(self):
        """
        Test StaticChessMethods.indices_to_uci() method:
        - Converts grid indices to chess notation correctly
        - Handles all board positions
        """
        # Corner positions
        uci = StaticChessMethods.indices_to_uci(0, 0)
        self.assertEqual(uci, 'A1')
        
        uci = StaticChessMethods.indices_to_uci(0, 7)
        self.assertEqual(uci, 'H1')
        
        uci = StaticChessMethods.indices_to_uci(7, 0)
        self.assertEqual(uci, 'A8')
        
        uci = StaticChessMethods.indices_to_uci(7, 7)
        self.assertEqual(uci, 'H8')
        
        # Center positions
        uci = StaticChessMethods.indices_to_uci(3, 4)
        self.assertEqual(uci, 'E4')
        
        uci = StaticChessMethods.indices_to_uci(4, 3)
        self.assertEqual(uci, 'D5')
        
        # Round-trip conversion
        for row in range(8):
            for col in range(8):
                uci = StaticChessMethods.indices_to_uci(row, col)
                back_row, back_col = StaticChessMethods.uci_to_indices(uci)
                self.assertEqual((row, col), (back_row, back_col))
    
    @test_case('TC-UNIT-003', 'Verify white pawn legal moves from starting position')
    def test_white_pawn_legal_moves_starting(self):
        """
        Test Pawn.get_legal_moves() for white pawn at starting position:
        - Can move one square forward
        - Can move two squares forward from start
        - Cannot move if blocked
        - Can capture diagonally
        """
        # Place white pawn at E2 (starting position)
        grid = [[None for _ in range(8)] for _ in range(8)]
        pawn = Pawn('white', 1, 4, grid)
        grid[1][4] = pawn
        
        # From starting position, can move 1 or 2 squares
        legal_moves = pawn.get_legal_moves()
        self.assertIn('E3', legal_moves)
        self.assertIn('E4', legal_moves)
        self.assertEqual(len(legal_moves), 2)
        
        # If blocked, cannot move
        grid[2][4] = Pawn('black', 2, 4, grid)  # Block at E3
        legal_moves = pawn.get_legal_moves()
        self.assertEqual(len(legal_moves), 0)
        
        # Can capture diagonally
        grid[2][4] = None  # Clear E3
        grid[2][3] = Pawn('black', 2, 3, grid)  # Enemy at D3
        grid[2][5] = Pawn('black', 2, 5, grid)  # Enemy at F3
        
        legal_moves = pawn.get_legal_moves()
        self.assertIn('D3', legal_moves)
        self.assertIn('F3', legal_moves)
        self.assertIn('E3', legal_moves)
        self.assertIn('E4', legal_moves)
    
    @test_case('TC-UNIT-004', 'Verify black pawn legal moves from starting position')
    def test_black_pawn_legal_moves_starting(self):
        """
        Test Pawn.get_legal_moves() for black pawn at starting position:
        - Moves in opposite direction from white
        - Can move one or two squares from start
        """
        # Place black pawn at E7
        grid = [[None for _ in range(8)] for _ in range(8)]
        pawn = Pawn('black', 6, 4, grid)
        grid[6][4] = pawn
        
        legal_moves = pawn.get_legal_moves()
        self.assertIn('E6', legal_moves)
        self.assertIn('E5', legal_moves)
        self.assertEqual(len(legal_moves), 2)
    
    @test_case('TC-UNIT-005', 'Verify pawn cannot move backward')
    def test_pawn_cannot_move_backward(self):
        """
        Test that pawns cannot move backward:
        - White pawns only move up
        - Black pawns only move down
        """
        # White pawn at E4 (middle of board)
        grid = [[None for _ in range(8)] for _ in range(8)]
        pawn = Pawn('white', 3, 4, grid)
        grid[3][4] = pawn
        
        legal_moves = pawn.get_legal_moves()
        
        # Should only include E5, not E3
        self.assertIn('E5', legal_moves)
        self.assertNotIn('E3', legal_moves)
    
    @test_case('TC-UNIT-006', 'Verify knight legal moves in L-shape pattern')
    def test_knight_legal_moves_pattern(self):
        """
        Test Knight.get_legal_moves() for L-shaped movement:
        - All 8 possible L-shaped moves
        - Moves within board boundaries
        - Can jump over pieces
        """
        # Place knight at E4 (center, has all 8 possible moves)
        grid = [[None for _ in range(8)] for _ in range(8)]
        knight = Knight('white', 3, 4, grid)
        grid[3][4] = knight
        
        legal_moves = knight.get_legal_moves()
        
        # All 8 L-shaped moves from E4
        expected_moves = ['D6', 'F6', 'C5', 'G5', 'C3', 'G3', 'D2', 'F2']
        
        for move in expected_moves:
            self.assertIn(move, legal_moves)
        
        self.assertEqual(len(legal_moves), 8)
    
    @test_case('TC-UNIT-007', 'Verify knight moves from corner have limited options')
    def test_knight_corner_moves(self):
        """
        Test that knight in corner has only 2 possible moves.
        """
        # Place knight at A1 (corner)
        grid = [[None for _ in range(8)] for _ in range(8)]
        knight = Knight('white', 0, 0, grid)
        grid[0][0] = knight
        
        legal_moves = knight.get_legal_moves()
        
        # From A1, can only move to B3 and C2
        self.assertIn('B3', legal_moves)
        self.assertIn('C2', legal_moves)
        self.assertEqual(len(legal_moves), 2)
    
    @test_case('TC-UNIT-008', 'Verify rook legal moves along ranks and files')
    def test_rook_legal_moves_straight_lines(self):
        """
        Test Rook.get_legal_moves() for straight line movement:
        - Moves along ranks (horizontal)
        - Moves along files (vertical)
        - Stops at board edges
        - Stops at pieces
        """
        # Place rook at D4 (center)
        grid = [[None for _ in range(8)] for _ in range(8)]
        rook = Rook('white', 3, 3, grid)
        grid[3][3] = rook
        
        legal_moves = rook.get_legal_moves()
        
        # Should have 14 moves (7 horizontal + 7 vertical)
        self.assertEqual(len(legal_moves), 14)
        
        # Check specific moves
        self.assertIn('D1', legal_moves)  # Vertical down
        self.assertIn('D8', legal_moves)  # Vertical up
        self.assertIn('A4', legal_moves)  # Horizontal left
        self.assertIn('H4', legal_moves)  # Horizontal right
    
    @test_case('TC-UNIT-009', 'Verify rook stops at blocking pieces')
    def test_rook_blocked_by_pieces(self):
        """
        Test that rook movement stops at pieces:
        - Stops before friendly pieces
        - Can capture enemy pieces (stops at capture)
        """
        grid = [[None for _ in range(8)] for _ in range(8)]
        rook = Rook('white', 3, 3, grid)
        grid[3][3] = rook
        
        # Place friendly piece at D6
        grid[5][3] = Pawn('white', 5, 3, grid)
        
        # Place enemy piece at D2
        grid[1][3] = Pawn('black', 1, 3, grid)
        
        legal_moves = rook.get_legal_moves()
        
        # Can move to D5 but not D6 (blocked by friendly)
        self.assertIn('D5', legal_moves)
        self.assertNotIn('D6', legal_moves)
        self.assertNotIn('D7', legal_moves)
        
        # Can capture at D2 but not beyond
        self.assertIn('D2', legal_moves)
        self.assertNotIn('D1', legal_moves)
    
    @test_case('TC-UNIT-010', 'Verify bishop legal moves along diagonals')
    def test_bishop_legal_moves_diagonals(self):
        """
        Test Bishop.get_legal_moves() for diagonal movement:
        - Moves along all 4 diagonals
        - Stops at board edges
        """
        # Place bishop at D4 (center)
        grid = [[None for _ in range(8)] for _ in range(8)]
        bishop = Bishop('white', 3, 3, grid)
        grid[3][3] = bishop
        
        legal_moves = bishop.get_legal_moves()
        
        # Check diagonal moves
        self.assertIn('A1', legal_moves)  # Down-left diagonal
        self.assertIn('G7', legal_moves)  # Up-right diagonal
        self.assertIn('A7', legal_moves)  # Up-left diagonal
        self.assertIn('G1', legal_moves)  # Down-right diagonal
        
        # Should have 13 moves (diagonals from center)
        self.assertEqual(len(legal_moves), 13)
    
    @test_case('TC-UNIT-011', 'Verify queen combines rook and bishop movement')
    def test_queen_legal_moves_combination(self):
        """
        Test Queen.get_legal_moves() combines rook and bishop patterns:
        - Moves along ranks and files (like rook)
        - Moves along diagonals (like bishop)
        """
        # Place queen at D4 (center)
        grid = [[None for _ in range(8)] for _ in range(8)]
        queen = Queen('white', 3, 3, grid)
        grid[3][3] = queen
        
        legal_moves = queen.get_legal_moves()
        
        # Queen should have 27 moves from center (14 like rook + 13 like bishop)
        self.assertEqual(len(legal_moves), 27)
        
        # Check rook-like moves
        self.assertIn('D1', legal_moves)
        self.assertIn('A4', legal_moves)
        
        # Check bishop-like moves
        self.assertIn('A1', legal_moves)
        self.assertIn('G7', legal_moves)
    
    @test_case('TC-UNIT-012', 'Verify king legal moves one square in any direction')
    def test_king_legal_moves_one_square(self):
        """
        Test King.get_legal_moves() for one-square movement:
        - Can move one square in 8 directions
        - Cannot move off board
        """
        # Place king at E4 (center, has all 8 moves)
        grid = [[None for _ in range(8)] for _ in range(8)]
        king = King('white', 3, 4, grid)
        grid[3][4] = king
        
        legal_moves = king.get_legal_moves()
        
        # All 8 adjacent squares
        expected_moves = ['D4', 'F4', 'E3', 'E5', 'D3', 'D5', 'F3', 'F5']
        
        for move in expected_moves:
            self.assertIn(move, legal_moves)
        
        self.assertEqual(len(legal_moves), 8)
    
    @test_case('TC-UNIT-013', 'Verify king in corner has limited moves')
    def test_king_corner_moves(self):
        """
        Test that king in corner has only 3 possible moves.
        """
        # Place king at A1
        grid = [[None for _ in range(8)] for _ in range(8)]
        king = King('white', 0, 0, grid)
        grid[0][0] = king
        
        legal_moves = king.get_legal_moves()
        
        # From A1, can move to A2, B1, B2
        self.assertIn('A2', legal_moves)
        self.assertIn('B1', legal_moves)
        self.assertIn('B2', legal_moves)
        self.assertEqual(len(legal_moves), 3)
    
    @test_case('TC-UNIT-014', 'Verify piece string representation uses correct notation')
    def test_piece_string_representation(self):
        """
        Test that Piece.__str__() returns correct notation:
        - Uppercase for white pieces
        - Lowercase for black pieces
        - Correct letter for each piece type
        """
        grid = [[None for _ in range(8)] for _ in range(8)]
        
        # White pieces
        self.assertEqual(str(King('white', 0, 0, grid)), 'K')
        self.assertEqual(str(Queen('white', 0, 0, grid)), 'Q')
        self.assertEqual(str(Rook('white', 0, 0, grid)), 'R')
        self.assertEqual(str(Bishop('white', 0, 0, grid)), 'B')
        self.assertEqual(str(Knight('white', 0, 0, grid)), 'N')
        self.assertEqual(str(Pawn('white', 0, 0, grid)), 'P')
        
        # Black pieces
        self.assertEqual(str(King('black', 0, 0, grid)), 'k')
        self.assertEqual(str(Queen('black', 0, 0, grid)), 'q')
        self.assertEqual(str(Rook('black', 0, 0, grid)), 'r')
        self.assertEqual(str(Bishop('black', 0, 0, grid)), 'b')
        self.assertEqual(str(Knight('black', 0, 0, grid)), 'n')
        self.assertEqual(str(Pawn('black', 0, 0, grid)), 'p')
    
    @test_case('TC-UNIT-015', 'Verify CheckDetector finds king position correctly')
    def test_check_detector_find_king(self):
        """
        Test CheckDetector.find_king() method:
        - Finds white king position
        - Finds black king position
        - Returns None if king not found
        """
        grid = [[None for _ in range(8)] for _ in range(8)]
        
        # Place white king at E1
        white_king = King('white', 0, 4, grid)
        grid[0][4] = white_king
        
        # Place black king at E8
        black_king = King('black', 7, 4, grid)
        grid[7][4] = black_king
        
        # Find white king
        row, col = CheckDetector.find_king('white', grid)
        self.assertEqual((row, col), (0, 4))
        
        # Find black king
        row, col = CheckDetector.find_king('black', grid)
        self.assertEqual((row, col), (7, 4))
        
        # Test when king doesn't exist
        empty_grid = [[None for _ in range(8)] for _ in range(8)]
        row, col = CheckDetector.find_king('white', empty_grid)
        self.assertEqual((row, col), (None, None))
    
    @test_case('TC-UNIT-016', 'Verify Board.position_to_indices() handles all inputs')
    def test_board_position_to_indices(self):
        """
        Test Board.position_to_indices() method:
        - Converts valid positions correctly
        - Handles invalid positions
        - Case-insensitive
        """
        board = Board()
        
        # Valid positions
        row, col = board.position_to_indices('E4')
        self.assertEqual((row, col), (3, 4))
        
        row, col = board.position_to_indices('a1')
        self.assertEqual((row, col), (0, 0))
        
        # Invalid positions
        row, col = board.position_to_indices('Z9')
        self.assertEqual((row, col), (None, None))
        
        row, col = board.position_to_indices('E')
        self.assertEqual((row, col), (None, None))
    
    @test_case('TC-UNIT-017', 'Verify Board.get_piece() returns correct piece or None')
    def test_board_get_piece(self):
        """
        Test Board.get_piece() method:
        - Returns piece at valid position
        - Returns None for empty square
        - Returns None for invalid position
        """
        board = Board()
        
        # Get piece at starting position
        piece = board.get_piece('E2')
        self.assertIsNotNone(piece)
        self.assertEqual(piece.piece_type, 'pawn')
        self.assertEqual(piece.color, 'white')
        
        # Get empty square
        piece = board.get_piece('E4')
        self.assertIsNone(piece)
        
        # Invalid position
        piece = board.get_piece('Z9')
        self.assertIsNone(piece)
    
    @test_case('TC-UNIT-018', 'Verify piece copy() method creates independent copy')
    def test_piece_copy_method(self):
        """
        Test that Piece.copy() creates an independent copy:
        - Copy has same attributes
        - Modifying copy doesn't affect original
        """
        grid = [[None for _ in range(8)] for _ in range(8)]
        original = Pawn('white', 1, 4, grid)
        grid[1][4] = original
        
        copy = original.copy()
        
        self.assertEqual(copy.color, original.color)
        self.assertEqual(copy.row, original.row)
        self.assertEqual(copy.col, original.col)
        self.assertEqual(copy.piece_type, original.piece_type)
        
        self.assertIsNot(copy, original)
        copy.set_row_col(3, 4)
        
        self.assertEqual(original.row, 1)
        self.assertEqual(original.col, 4)


if __name__ == '__main__':
    unittest.main()