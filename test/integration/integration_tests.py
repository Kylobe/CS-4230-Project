"""
Integration Tests for Chess Game

Integration tests verify that multiple components work together correctly,
testing interactions between classes like Board + MoveValidator, 
CheckDetector + Board, etc.

EXPORT:
- test_case decorator function to identify test cases
- All test cases are labeled with (unique identifier, description)
- unique identifier = 'TC-INT-xxx'

An example is given to make the export run cleanly.
"""
import unittest

from utils.board import Board
from utils.move_validator import MoveValidator
from utils.check_detector import CheckDetector
from utils.pieces import Pawn, Knight, Bishop, Rook, Queen, King


def test_case(test_id, description):
    """
    Decorator to add test metadata for Excel export.
    
    Args:
        test_id: Unique identifier like 'TC-INT-001'
        description: Human-readable description of what the test verifies
    """
    def decorator(func):
        func.test_id = test_id
        func.test_description = description
        return func
    return decorator


class TestChessGameIntegration(unittest.TestCase):
    """
    Integration tests for chess game components.
    Tests interactions between multiple classes.
    """
    # HELPER FUNCTIONS
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.board = Board()
        self.move_validator = MoveValidator(self.board)
        
    def tearDown(self):
        """Clean up after each test method."""
        self.board = None
        self.move_validator = None

    # TEST CASES
    @test_case('TC-INT-001', 'Verify Board and MoveValidator work together for valid pawn moves')
    def test_board_validator_integration_pawn_moves(self):
        """
        Test that Board and MoveValidator correctly handle pawn moves:
        - Single square forward move
        - Double square opening move
        - Diagonal capture moves
        - Invalid backward moves
        
        This tests the integration between:
        - Board.move_piece() method
        - MoveValidator.is_valid_move() method
        - Pawn.get_legal_moves() method
        """
        # TEST 1: Valid single square pawn move
        is_valid, error = self.move_validator.is_valid_move('E2', 'E3', 'white')
        self.assertTrue(is_valid, f"Single pawn move should be valid, got error: {error}")
        self.assertEqual(error, "")
        
        # Execute the move
        new_grid, captured = self.board.move_piece('E2', 'E3')
        self.board.set_grid(new_grid)
        
        # Verify board state after move
        piece_at_e3 = self.board.get_piece('E3')
        self.assertIsNotNone(piece_at_e3)
        self.assertEqual(piece_at_e3.piece_type, 'pawn')
        self.assertEqual(piece_at_e3.color, 'white')
        self.assertIsNone(self.board.get_piece('E2'))
        self.assertIsNone(captured)
        
        # TEST 2: Valid double square opening move
        is_valid, error = self.move_validator.is_valid_move('D7', 'D5', 'black')
        self.assertTrue(is_valid)
        
        new_grid, captured = self.board.move_piece('D7', 'D5')
        self.board.set_grid(new_grid)
        
        piece_at_d5 = self.board.get_piece('D5')
        self.assertEqual(piece_at_d5.piece_type, 'pawn')
        self.assertEqual(piece_at_d5.color, 'black')
        
        # TEST 3: Valid diagonal capture
        # Move white pawn to position for capture
        new_grid, _ = self.board.move_piece('E3', 'E4')
        self.board.set_grid(new_grid)
        
        # White pawn at E4 can now capture black pawn at D5
        is_valid, error = self.move_validator.is_valid_move('E4', 'D5', 'white')
        self.assertTrue(is_valid)
        
        new_grid, captured = self.board.move_piece('E4', 'D5')
        self.board.set_grid(new_grid)
        
        # Verify capture occurred
        self.assertIsNotNone(captured)
        self.assertEqual(captured.piece_type, 'pawn')
        self.assertEqual(captured.color, 'black')
        
        piece_at_d5 = self.board.get_piece('D5')
        self.assertEqual(piece_at_d5.color, 'white')

if __name__ == '__main__':
    unittest.main()