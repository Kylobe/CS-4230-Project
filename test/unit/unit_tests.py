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
        - Converts grid indices (row, col) to chess notation correctly
        - Returns None for invalid input
        
        This is a complete unit test with all attributes for Excel export:
        - test_id: TC-UNIT-002
        - description: Verify indices to UCI conversion
        - Tests specific method in isolation
        - Includes multiple assertions for thorough coverage
        """
        # TEST 1: Corner positions
        uci = StaticChessMethods.indices_to_uci(0, 0)
        self.assertEqual(uci, "A1", "(0, 0) should map to A1")

        uci = StaticChessMethods.indices_to_uci(0, 7)
        self.assertEqual(uci, "H1", "(0, 7) should map to H1")

        uci = StaticChessMethods.indices_to_uci(7, 0)
        self.assertEqual(uci, "A8", "(7, 0) should map to A8")

        uci = StaticChessMethods.indices_to_uci(7, 7)
        self.assertEqual(uci, "H8", "(7, 7) should map to H8")

        # TEST 2: Center positions
        uci = StaticChessMethods.indices_to_uci(3, 4)
        self.assertEqual(uci, "E4", "(3, 4) should map to E4")

        uci = StaticChessMethods.indices_to_uci(4, 3)
        self.assertEqual(uci, "D5", "(4, 3) should map to D5")

        # TEST 3: Invalid input (row, col out of bounds)
        uci = StaticChessMethods.indices_to_uci(-1, 4)
        self.assertIsNone(uci, "Negative row should return None")

        uci = StaticChessMethods.indices_to_uci(3, 8)
        self.assertIsNone(uci, "Column out of bounds should return None")

        uci = StaticChessMethods.indices_to_uci(8, 8)
        self.assertIsNone(uci, "Both indices out of bounds should return None")

        # TEST 4: Invalid types (non-integers)
        uci = StaticChessMethods.indices_to_uci("e4", 3)
        self.assertIsNone(uci, "Non‐integer row should return None")

        uci = StaticChessMethods.indices_to_uci(3, None)
        self.assertIsNone(uci, "Non‐integer col should return None")


    @test_case('TC-UNIT-003', 'Verify valid move generation from Pawns')
    def test_pawn_valid_move_generation(self):
        """
        Test Pawn.get_legal_moves() method:
        - returns list of legal pawn moves
        
        This is a complete unit test with all attributes for Excel export:
        - test_id: TC-UNIT-003
        - description: Verify valid move generation from Pawns
        - Tests specific method in isolation
        - Includes multiple assertions for thorough coverage
        """
        grid = [[None for _ in range(8)] for _ in range(8)]
        #TEST 1: Pawn double move
        pawn = Pawn("white", 1, 3, grid)
        black_pawn = Pawn("black", 6, 3, grid)
        grid[1][3] = pawn
        grid[6][3] = black_pawn
        valid_moves = pawn.get_legal_moves()
        self.assertCountEqual(valid_moves, ["D3", "D4"], "White pawn should be able to move to both D3 and D4")

        valid_moves = black_pawn.get_legal_moves()
        self.assertCountEqual(valid_moves, ["D6", "D5"], "Black pawn should be able to move to both D6 and D5")
        grid[6][3] = None

        #TEST 2: Pawn blocked
        black_piece = Pawn("black", 2, 3, grid)
        grid[2][3] = black_piece
        valid_moves = pawn.get_legal_moves()
        self.assertCountEqual(valid_moves, [], "White pawn should be blocked by the black pawn on D3")

        grid[2][3] = None
        black_piece.set_row_col(3, 3)
        grid[3][3] = black_piece
        valid_moves = pawn.get_legal_moves()
        self.assertCountEqual(valid_moves, ["D3"], "White pawn should be blocked by black pawn on D4")

        #TEST 3: Diagnol capture
        grid[3][3] = None
        black_piece.set_row_col(2, 4)
        grid[2][4] = black_piece
        valid_moves = pawn.get_legal_moves()
        self.assertCountEqual(valid_moves, ["D3", "D4", "E3"], "White pawn should be able to capture black pawn on E3 and move to D3 and D4")

        grid[2][4] = None
        black_piece.set_row_col(2, 2)
        valid_moves = pawn.get_legal_moves()
        self.assertCountEqual(valid_moves, ["D3", "D4", "C3"], "White pawn should be able to capture black pawn on C3 and move to D3 and D4")

        #TEST 4: Ally on diagnol
        grid[2][4] = None
        ally_piece = Pawn("white", 2, 4, grid)
        grid[2][4] = ally_piece
        valid_moves = pawn.get_legal_moves()
        self.assertCountEqual(valid_moves, ["D3", "D4"], "White pawn shouldn't be able to capture white pawn on E3")

        grid[2][4] = None
        ally_piece.set_row_col(2, 2)
        grid[2][2] = ally_piece
        valid_moves = pawn.get_legal_moves()
        self.assertCountEqual(valid_moves, ["D3", "D4"], "White pawn shouldn't be able to capture white pawn on C3")

        #TEST 5: No double move
        grid = [[None for _ in range(8)] for _ in range(8)]
        pawn.set_grid(grid)
        pawn.set_row_col(2, 3)
        grid[2][3] = pawn
        valid_moves = pawn.get_legal_moves()
        self.assertCountEqual(valid_moves, ["D4"], "White pawn can only move one space forward")

        grid = [[None for _ in range(8)] for _ in range(8)]
        black_pawn.set_grid(grid)
        black_pawn.set_row_col(5, 3)
        valid_moves = black_pawn.get_legal_moves()
        self.assertCountEqual(valid_moves, ["D5"], "Black pawn can only move one space forward")

    @test_case('TC-UNIT-004', 'Verify valid move generation from Knights')
    def test_knight_valid_move_generation(self):
        """
        Test Knight.get_legal_moves() method:
        - returns list of legal knight moves
        
        This is a complete unit test with all attributes for Excel export:
        - test_id: TC-UNIT-004
        - description: Verify valid move generation from Knights
        - Tests specific method in isolation
        - Includes multiple assertions for thorough coverage
        """
        grid = [[None for _ in range(8)] for _ in range(8)]
        #TEST 1: Knight in the center of the board.
        knight = Knight("white", 3, 4, grid)
        grid[3][4] = knight
        valid_moves = knight.get_legal_moves()
        self.assertCountEqual(valid_moves, ["F2", "D2", "C3", "C5", "D6", "F6", "G5", "G3"])

        #TEST 2: Enemies on attack squares
        grid[1][5] = Pawn("black", 1, 5, grid)
        grid[1][3] = Pawn("black", 1, 3, grid)
        grid[2][2] = Pawn("black", 2, 2, grid)
        grid[4][2] = Pawn("black", 4, 2, grid)
        grid[5][3] = Pawn("black", 5, 3, grid)
        grid[5][5] = Pawn("black", 5, 5, grid)
        grid[4][6] = Pawn("black", 4, 5, grid)
        grid[2][6] = Pawn("black", 2, 6, grid)
        valid_moves = knight.get_legal_moves()
        self.assertCountEqual(valid_moves, ["F2", "D2", "C3", "C5", "D6", "F6", "G5", "G3"])

        #TEST 3: Allies on attack squares
        grid[1][5] = Pawn("white", 1, 5, grid)
        grid[1][3] = Pawn("white", 1, 3, grid)
        grid[2][2] = Pawn("white", 2, 2, grid)
        grid[4][2] = Pawn("white", 4, 2, grid)
        grid[5][3] = Pawn("white", 5, 3, grid)
        grid[5][5] = Pawn("white", 5, 5, grid)
        grid[4][6] = Pawn("white", 4, 5, grid)
        grid[2][6] = Pawn("white", 2, 6, grid)
        valid_moves = knight.get_legal_moves()
        self.assertCountEqual(valid_moves, [])

        #TEST 4: Knight in corners.
        grid = [[None for _ in range(8)] for _ in range(8)]
        knight.set_row_col(0, 0)
        grid[0][0] = knight
        knight.set_grid(grid)
        valid_moves = knight.get_legal_moves()
        self.assertCountEqual(valid_moves, ["B3", "C2"])
        grid[0][0] = None

        knight.set_row_col(0, 7)
        grid[0][7] = knight
        valid_moves = knight.get_legal_moves()
        self.assertCountEqual(valid_moves, ["F2", "G3"])
        grid[0][7] = None

        knight.set_row_col(7, 7)
        grid[7][7] = knight
        valid_moves = knight.get_legal_moves()
        self.assertCountEqual(valid_moves, ["G6", "F7"])
        grid[7][7] = None

        knight.set_row_col(7, 0)
        grid[7][0] = knight
        valid_moves = knight.get_legal_moves()
        self.assertCountEqual(valid_moves, ["B6", "C7"])
        grid[7][0] = None

        #TEST 5: Knight surrounded. Tests knight jump abilities
        grid = [[None for _ in range(8)] for _ in range(8)]
        knight.set_row_col(3, 4)
        grid[3][4] = knight
        knight.set_grid(grid)
        grid[2][3] = Pawn("black", 2, 3, grid)
        grid[2][4] = Pawn("black", 2, 4, grid)
        grid[2][5] = Pawn("black", 2, 5, grid)
        grid[3][5] = Pawn("black", 3, 5, grid)
        grid[4][5] = Pawn("black", 4, 5, grid)
        grid[4][4] = Pawn("black", 4, 4, grid)
        grid[4][3] = Pawn("black", 4, 3, grid)
        grid[3][3] = Pawn("black", 3, 3, grid)
        valid_moves = knight.get_legal_moves()
        self.assertCountEqual(valid_moves, ["F2", "D2", "C3", "C5", "D6", "F6", "G5", "G3"])

    @test_case('TC-UNIT-005', 'Verify valid move generation from Bishops')
    def test_bishop_valid_move_generation(self):
        """
        Test Bishop.get_legal_moves() method:
        - returns list of legal bishop moves
        
        This is a complete unit test with all attributes for Excel export:
        - test_id: TC-UNIT-005
        - description: Verify valid move generation from Bishops
        - Tests specific method in isolation
        - Includes multiple assertions for thorough coverage
        """
        grid = [[None for _ in range(8)] for _ in range(8)]
        #TEST 1: Bishop in the center of the board.
        bishop = Bishop("white", 3, 4, grid)
        grid[3][4] = bishop
        valid_moves = bishop.get_legal_moves()
        self.assertCountEqual(valid_moves, ["F3", "G2", "H1", "D3", "C2", "B1", "F5", "G6", "H7", "D5", "C6", "B7", "A8"])

        #TEST 2: Blockers
        grid[5][2] = Pawn("black", 5, 2, grid)
        grid[2][5] = Pawn("black", 2, 5, grid)
        grid[4][5] = Pawn("white", 4, 5, grid)
        grid[1][2] = Pawn("white", 1, 2, grid)
        valid_moves = bishop.get_legal_moves()
        self.assertCountEqual(valid_moves, ["F3", "D3", "D5", "C6"])

        #TEST 3: Bishop in corners.
        grid = [[None for _ in range(8)] for _ in range(8)]
        bishop.set_row_col(0, 0)
        grid[0][0] = bishop
        bishop.set_grid(grid)
        valid_moves = bishop.get_legal_moves()
        self.assertCountEqual(valid_moves, ["B2", "C3", "D4", "E5", "F6", "G7", "H8"])
        grid[0][0] = None

        bishop.set_row_col(0, 7)
        grid[0][7] = bishop
        valid_moves = bishop.get_legal_moves()
        self.assertCountEqual(valid_moves, ["G2", "F3", "E4", "D5", "C6", "B7", "A8"])
        grid[0][7] = None

        bishop.set_row_col(7, 7)
        grid[7][7] = bishop
        valid_moves = bishop.get_legal_moves()
        self.assertCountEqual(valid_moves, ["G7", "F6", "E5", "D4", "C3", "B2", "A1"])
        grid[7][7] = None

        bishop.set_row_col(7, 0)
        grid[7][0] = bishop
        valid_moves = bishop.get_legal_moves()
        self.assertCountEqual(valid_moves, ["B7", "C6", "D5", "E4", "F3", "G2", "H1"])
        grid[7][0] = None

    @test_case('TC-UNIT-006', 'Verify valid move generation from Rooks')
    def test_rook_valid_move_generation(self):
        """
        Test Rook.get_legal_moves() method:
        - returns list of legal rook moves
        
        This is a complete unit test with all attributes for Excel export:
        - test_id: TC-UNIT-006
        - description: Verify valid move generation from Rooks
        - Tests specific method in isolation
        - Includes multiple assertions for thorough coverage
        """
        grid = [[None for _ in range(8)] for _ in range(8)]
        #TEST 1: Bishop in the center of the board.
        rook = Rook("white", 3, 4, grid)
        grid[3][4] = rook
        valid_moves = rook.get_legal_moves()
        self.assertCountEqual(valid_moves, ["E1", "E2", "E3", "E5", "E6", "E7", "E8", "A4", "B4", "C4", "D4", "F4", "G4", "H4"])

        #TEST 2: Blockers
        grid[3][6] = Pawn("black", 3, 6, grid)
        grid[3][3] = Pawn("black", 3, 3, grid)
        grid[6][4] = Pawn("white", 6, 4, grid)
        grid[2][4] = Pawn("white", 2, 4, grid)
        valid_moves = rook.get_legal_moves()
        self.assertCountEqual(valid_moves, ["E5", "E6", "D4", "F4", "G4"])

        #TEST 3: Rook in corners
        grid = [[None for _ in range(8)] for _ in range(8)]
        rook.set_row_col(0, 0)
        grid[0][0] = rook
        rook.set_grid(grid)
        valid_moves = rook.get_legal_moves()
        self.assertCountEqual(valid_moves, ["A2", "A3", "A4", "A5", "A6", "A7", "A8", "B1", "C1", "D1", "E1", "F1", "G1", "H1"])
        grid[0][0] = None

        rook.set_row_col(0, 7)
        grid[0][7] = rook
        valid_moves = rook.get_legal_moves()
        self.assertCountEqual(valid_moves, ["H2", "H3", "H4", "H5", "H6", "H7", "H8", "A1", "B1", "C1", "D1", "E1", "F1", "G1"])
        grid[0][7] = None

        rook.set_row_col(7, 7)
        grid[7][7] = rook
        valid_moves = rook.get_legal_moves()
        self.assertCountEqual(valid_moves, ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "A8", "B8", "C8", "D8", "E8", "F8", "G8"])
        grid[7][7] = None

        rook.set_row_col(7, 0)
        grid[7][0] = rook
        valid_moves = rook.get_legal_moves()
        self.assertCountEqual(valid_moves, ["B8", "C8", "D8", "E8", "F8", "G8", "H8", "A1", "A2", "A3", "A4", "A5", "A6", "A7"])
        grid[7][0] = None

    @test_case('TC-UNIT-007', 'Verify valid move generation from Queens')
    def test_queen_valid_move_generation(self):
        """
        Test Queen.get_legal_moves() method:
        - returns list of legal queen moves
        
        This is a complete unit test with all attributes for Excel export:
        - test_id: TC-UNIT-007
        - description: Verify valid move generation from Queens
        - Tests specific method in isolation
        - Includes multiple assertions for thorough coverage
        """
        grid = [[None for _ in range(8)] for _ in range(8)]
        #TEST 1: Bishop in the center of the board.
        queen = Queen("white", 3, 4, grid)
        grid[3][4] = queen
        valid_moves = queen.get_legal_moves()
        self.assertCountEqual(valid_moves, ["F3", "G2", "H1", "D3", "C2", "B1", "F5", "G6", "H7", "D5", "C6", "B7", "A8", "E1", "E2", "E3", "E5", "E6", "E7", "E8", "A4", "B4", "C4", "D4", "F4", "G4", "H4"])

        #TEST 2: Blockers
        grid[3][6] = Pawn("black", 3, 6, grid)
        grid[3][3] = Pawn("black", 3, 3, grid)
        grid[6][4] = Pawn("white", 6, 4, grid)
        grid[2][4] = Pawn("white", 2, 4, grid)
        grid[5][2] = Pawn("black", 5, 2, grid)
        grid[2][5] = Pawn("black", 2, 5, grid)
        grid[4][5] = Pawn("white", 4, 5, grid)
        grid[1][2] = Pawn("white", 1, 2, grid)
        valid_moves = queen.get_legal_moves()
        self.assertCountEqual(valid_moves, ["E5", "E6", "D4", "F4", "G4", "F3", "D3", "D5", "C6"])

        #TEST 3: Queen in corners
        grid = [[None for _ in range(8)] for _ in range(8)]
        queen.set_row_col(0, 0)
        grid[0][0] = queen
        queen.set_grid(grid)
        valid_moves = queen.get_legal_moves()
        self.assertCountEqual(valid_moves, ["A2", "A3", "A4", "A5", "A6", "A7", "A8", "B1", "C1", "D1", "E1", "F1", "G1", "H1", "B2", "C3", "D4", "E5", "F6", "G7", "H8"])
        grid[0][0] = None

        queen.set_row_col(0, 7)
        grid[0][7] = queen
        valid_moves = queen.get_legal_moves()
        self.assertCountEqual(valid_moves, ["H2", "H3", "H4", "H5", "H6", "H7", "H8", "A1", "B1", "C1", "D1", "E1", "F1", "G1", "G2", "F3", "E4", "D5", "C6", "B7", "A8"])
        grid[0][7] = None

        queen.set_row_col(7, 7)
        grid[7][7] = queen
        valid_moves = queen.get_legal_moves()
        self.assertCountEqual(valid_moves, ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "A8", "B8", "C8", "D8", "E8", "F8", "G8", "G7", "F6", "E5", "D4", "C3", "B2", "A1"])
        grid[7][7] = None

        queen.set_row_col(7, 0)
        grid[7][0] = queen
        valid_moves = queen.get_legal_moves()
        self.assertCountEqual(valid_moves, ["B8", "C8", "D8", "E8", "F8", "G8", "H8", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "B7", "C6", "D5", "E4", "F3", "G2", "H1"])
        grid[7][0] = None

    @test_case('TC-UNIT-008', 'Verify valid move generation from Kings')
    def test_queen_valid_move_generation(self):
        """
        Test King.get_legal_moves() method:
        - returns list of legal king moves
        
        This is a complete unit test with all attributes for Excel export:
        - test_id: TC-UNIT-008
        - description: Verify valid move generation from Kings
        - Tests specific method in isolation
        - Includes multiple assertions for thorough coverage
        """
        grid = [[None for _ in range(8)] for _ in range(8)]
        #TEST 1: Bishop in the center of the board.
        king = King("white", 3, 4, grid)
        grid[3][4] = king
        valid_moves = king.get_legal_moves()
        self.assertCountEqual(valid_moves, ["D3", "D4", "D5", "E3", "E5", "F3", "F4", "F5"])

        #TEST 2: Blockers
        grid[2][3] = Pawn("black", 2, 3, grid)
        grid[2][4] = Pawn("white", 2, 4, grid)
        grid[2][5] = Pawn("black", 2, 5, grid)
        grid[3][3] = Pawn("white", 3, 3, grid)
        grid[3][5] = Pawn("black", 3, 5, grid)
        grid[4][3] = Pawn("white", 4, 3, grid)
        grid[4][4] = Pawn("black", 4, 4, grid)
        grid[4][5] = Pawn("white", 4, 5, grid)
        valid_moves = king.get_legal_moves()
        self.assertCountEqual(valid_moves, ["D3", "E5", "F3", "F4"])

        #TEST 3: King in corners
        grid = [[None for _ in range(8)] for _ in range(8)]
        king.set_row_col(0, 0)
        grid[0][0] = king
        king.set_grid(grid)
        valid_moves = king.get_legal_moves()
        self.assertCountEqual(valid_moves, ["A2", "B2", "B1"])
        grid[0][0] = None

        king.set_row_col(0, 7)
        grid[0][7] = king
        valid_moves = king.get_legal_moves()
        self.assertCountEqual(valid_moves, ["H2", "G2", "G1"])
        grid[0][7] = None

        king.set_row_col(7, 7)
        grid[7][7] = king
        valid_moves = king.get_legal_moves()
        self.assertCountEqual(valid_moves, ["H7", "G7", "G8"])
        grid[7][7] = None

        king.set_row_col(7, 0)
        grid[7][0] = king
        valid_moves = king.get_legal_moves()
        self.assertCountEqual(valid_moves, ["A7", "B7", "B8"])
        grid[7][0] = None

    @test_case('TC-UNIT-009', 'Verify board get_piece() method')
    def test_boards_get_piece_method(self):
        """
        Test Board.get_piece() method:
        - returns piece at a given UCI position
        
        This is a complete unit test with all attributes for Excel export:
        - test_id: TC-UNIT-009
        - description: Verify board get_piece() method
        - Tests specific method in isolation
        - Includes multiple assertions for thorough coverage
        """
        board = Board()
        #TEST 1: getting valid piece
        piece : Piece = board.get_piece("E2")
        self.assertEqual(piece.piece_type, "pawn")
        self.assertEqual(piece.color, "white")
        self.assertEqual(piece.col, 4)
        self.assertEqual(piece.row, 1)

        piece : Piece = board.get_piece("E1")
        self.assertEqual(piece.piece_type, "king")
        self.assertEqual(piece.color, "white")
        self.assertEqual(piece.col, 4)
        self.assertEqual(piece.row, 0)

        #TEST 2: valid null square
        piece = board.get_piece("E4")
        self.assertTrue(piece is None)

        #TEST 3: invalid square
        piece = board.get_piece("Z9")
        self.assertTrue(piece is None)

        #TEST 4: get corner pieces
        piece : Piece = board.get_piece("A1")
        self.assertEqual(piece.piece_type, "rook")
        self.assertEqual(piece.color, "white")
        self.assertEqual(piece.col, 0)
        self.assertEqual(piece.row, 0)

        piece : Piece = board.get_piece("H1")
        self.assertEqual(piece.piece_type, "rook")
        self.assertEqual(piece.color, "white")
        self.assertEqual(piece.col, 7)
        self.assertEqual(piece.row, 0)

        piece : Piece = board.get_piece("A8")
        self.assertEqual(piece.piece_type, "rook")
        self.assertEqual(piece.color, "black")
        self.assertEqual(piece.col, 0)
        self.assertEqual(piece.row, 7)

        piece : Piece = board.get_piece("H8")
        self.assertEqual(piece.piece_type, "rook")
        self.assertEqual(piece.color, "black")
        self.assertEqual(piece.col, 7)
        self.assertEqual(piece.row, 7)

    @test_case('TC-UNIT-010', 'Verify board move_piece() method')
    def test_boards_move_piece_method(self):
        """
        Test Board.move_piece() method:
        - returns a new_grid and a the captured piece
        
        This is a complete unit test with all attributes for Excel export:
        - test_id: TC-UNIT-010
        - description: Verify board move_piece() method
        - Tests specific method in isolation
        - Includes multiple assertions for thorough coverage
        """
        board = Board()
        #TEST 1: Verify basic pawn move
        new_grid, _ = board.move_piece("E2", "E4")
        piece : Piece = new_grid[3][4]
        self.assertEqual(piece.piece_type, "pawn")
        self.assertEqual(piece.color, "white")
        self.assertEqual(piece.col, 4)
        self.assertEqual(piece.row, 3)
        self.assertTrue(new_grid[1][4] is None)

        #TEST 2: Verify Boards Immutablity
        self.assertTrue(board.grid[3][4] is None)
        self.assertTrue(isinstance(piece, Piece))

        #TEST 3: Verify captured piece is returned
        new_grid, captured = board.move_piece("E2", "E8")
        self.assertEqual(captured.piece_type, "king")
        self.assertEqual(captured.color, "black")
        self.assertEqual(captured.col, 4)
        self.assertEqual(captured.row, 7)

        #TEST 4: Test invalid from square
        new_grid, captured = board.move_piece("E4", "E8")
        self.assertTrue(new_grid is None)
        self.assertTrue(captured is None)

        #TEST 5: Test Pawn promotion
        new_grid, captured = board.move_piece("E2", "E8")
        piece : Piece = new_grid[7][4]
        self.assertEqual(piece.piece_type, "queen")
        self.assertEqual(piece.color, "white")
        self.assertEqual(piece.col, 4)
        self.assertEqual(piece.row, 7)

    @test_case('TC-UNIT-011', 'Verify CheckDectors find_king method')
    def test_check_detector_find_king_method(self):
        """
        Test CheckDetector.find_king() method:
        - returns row, col of the selected king, or None, None if the selected king doesn't exist
        
        This is a complete unit test with all attributes for Excel export:
        - test_id: TC-UNIT-011
        - description: Verify CheckDetector find_king() method
        - Tests specific method in isolation
        - Includes multiple assertions for thorough coverage
        """
        grid = [[None for _ in range(8)] for _ in range(8)]
        grid[0][0] = King("white", 0, 0, grid)
        #TEST 1: Finding white king when it exists
        row, col = CheckDetector.find_king("white", grid)
        self.assertEqual(row, 0)
        self.assertEqual(col, 0)

        #TEST 2: Finding non existent black king
        row, col = CheckDetector.find_king("black", grid)
        self.assertTrue(row is None)
        self.assertTrue(col is None)

        #TEST 3: Test invalid input
        row, col = CheckDetector.find_king("orange", grid)
        self.assertTrue(row is None)
        self.assertTrue(col is None)

        row, col = CheckDetector.find_king("white", [[], []])
        self.assertTrue(row is None)
        self.assertTrue(col is None)

    @test_case('TC-UNIT-012', 'Verify CheckDectors is_in_check method')
    def test_check_detector_is_in_check_method(self):
        """
        Test CheckDetector.is_in_check() method:
        - returns true if the selected king is in check, false other wise
        
        This is a complete unit test with all attributes for Excel export:
        - test_id: TC-UNIT-012
        - description: Verify CheckDetector is_in_check() method
        - Tests specific method in isolation
        - Includes multiple assertions for thorough coverage
        """
        grid = [[None for _ in range(8)] for _ in range(8)]
        #TEST 1: White king not in check
        grid[0][0] = King("white", 0, 0, grid)
        self.assertFalse(CheckDetector.is_in_check("white", grid))

        #TEST 2: White king in check
        grid[0][7] = Queen("black", 0, 7, grid)
        self.assertTrue(CheckDetector.is_in_check("white", grid))

        #TEST 3: White king has enemy blocker
        grid[0][5] = Bishop("black", 0, 5, grid)
        self.assertFalse(CheckDetector.is_in_check("white", grid))

        #TEST 4: White king has ally blocker
        grid[0][5] = Queen("white", 0, 5, grid)
        self.assertFalse(CheckDetector.is_in_check("white", grid))

        #TEST 5: Black king in check but not white king
        grid[5][5] = King("black", 5, 5, grid)
        self.assertFalse(CheckDetector.is_in_check("white", grid))
        self.assertTrue(CheckDetector.is_in_check("black", grid))

if __name__ == '__main__':
    unittest.main()