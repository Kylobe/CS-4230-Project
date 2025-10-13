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


if __name__ == '__main__':
    unittest.main()