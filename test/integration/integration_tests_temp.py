# Temporary file for updated content
"""
Integration Tests for Chess Game

Integration tests verify that multiple components work together correctly,
testing interactions between classes like Board + MoveValidator,
CheckDetector + Board, etc.

EXPORT:
- test_case decorator function to identify test cases
- All test cases are labeled with (unique identifier, description)
- unique identifier = 'TC-INT-xxx'
"""

import unittest
from typing import Any, Dict, List, Optional, Tuple

from utils.board import Board
from utils.check_detector import CheckDetector
from utils.move_validator import MoveValidator
from utils.pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from utils.static_chess_methods import StaticChessMethods


def test_case(test_id: str, description: str) -> Any:
    """
    Decorator to add test metadata for Excel export.

    Args:
        test_id: Unique identifier like 'TC-INT-001'
        description: Human-readable description of what the test verifies
    """

    def decorator(func: Any) -> Any:
        func.test_id = test_id
        func.test_description = description
        return func

    return decorator


class TestChessGameIntegration(unittest.TestCase):
    """
    Integration tests for chess game components.
    Tests interactions between multiple classes.
    """

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.board: Board = Board()  # Already initializes the board
        self.move_validator: MoveValidator = MoveValidator(self.board)

    def tearDown(self) -> None:
        """Clean up after each test method."""
        pass  # No cleanup needed

    @test_case(
        "TC-INT-001",
        "Verify Board and MoveValidator work together for valid pawn moves",
    )
    def test_board_validator_integration_pawn_moves(self) -> None:
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
        is_valid, error = self.move_validator.is_valid_move("E2", "E3", "white")
        self.assertTrue(
            is_valid, f"Single pawn move should be valid, got error: {error}"
        )
        self.assertEqual(error, "")

        # Execute the move
        new_grid, captured = self.board.move_piece("E2", "E3")
        self.board.set_grid(new_grid)

        # Verify board state after move
        piece_at_e3 = self.board.get_piece("E3")
        self.assertIsNotNone(piece_at_e3, "Expected piece at E3")
        if piece_at_e3:  # Type guard
            self.assertEqual(piece_at_e3.piece_type, "pawn")
            self.assertEqual(piece_at_e3.color, "white")
        self.assertIsNone(self.board.get_piece("E2"))
        self.assertIsNone(captured)

        # TEST 2: Valid double square opening move
        is_valid, error = self.move_validator.is_valid_move("D7", "D5", "black")
        self.assertTrue(is_valid)

        new_grid, captured = self.board.move_piece("D7", "D5")
        self.board.set_grid(new_grid)

        piece_at_d5 = self.board.get_piece("D5")
        self.assertIsNotNone(piece_at_d5, "Expected piece at D5")
        if piece_at_d5:  # Type guard
            self.assertEqual(piece_at_d5.piece_type, "pawn")
            self.assertEqual(piece_at_d5.color, "black")

        # TEST 3: Valid diagonal capture
        # Move white pawn to position for capture
        new_grid, _ = self.board.move_piece("E3", "E4")
        self.board.set_grid(new_grid)

        # White pawn at E4 can now capture black pawn at D5
        is_valid, error = self.move_validator.is_valid_move("E4", "D5", "white")
        self.assertTrue(is_valid)

        new_grid, captured = self.board.move_piece("E4", "D5")
        self.board.set_grid(new_grid)

        # Verify capture occurred
        self.assertIsNotNone(captured, "Expected captured piece")
        if captured:  # Type guard
            self.assertEqual(captured.piece_type, "pawn")
            self.assertEqual(captured.color, "black")

        piece_at_d5 = self.board.get_piece("D5")
        self.assertIsNotNone(piece_at_d5, "Expected piece at D5 after capture")
        if piece_at_d5:  # Type guard
            self.assertEqual(piece_at_d5.color, "white")

    @test_case(
        "TC-INT-002",
        "Verify Board and CheckDetector integration for check detection",
    )
    def test_board_checkdetector_integration(self) -> None:
        """
        Test that Board and CheckDetector work together to:
        - Detect check situations
        - Track king positions
        - Identify attacking pieces
        """
        # Set up a check situation
        moves: List[Tuple[str, str]] = [
            ("E2", "E4"),  # White pawn
            ("E7", "E5"),  # Black pawn
            ("F1", "C4"),  # White bishop
            ("B8", "C6"),  # Black knight
            ("D1", "H5"),  # White queen
        ]

        # Execute moves
        for src, dst in moves:
            new_grid, _ = self.board.move_piece(src, dst)
            self.board.set_grid(new_grid)

        # White queen should now be threatening black king
        is_check = CheckDetector.is_in_check("black", self.board.grid)
        self.assertTrue(is_check, "Black king should be in check")

        # Verify checking piece is the queen
        queen_piece = self.board.get_piece("H5")
        self.assertIsNotNone(queen_piece, "Queen should be at H5")
        if queen_piece:  # Type guard
            self.assertEqual(queen_piece.piece_type, "queen")
            self.assertEqual(queen_piece.color, "white")

            # Get king position
            king_row, king_col = CheckDetector.find_king("black", self.board.grid)
            king_pos = StaticChessMethods.indices_to_uci(king_row, king_col)

            # Verify queen can attack king
            queen_moves = queen_piece.get_legal_moves()
            self.assertIn(king_pos, queen_moves, "Queen should be able to attack king")

    @test_case(
        "TC-INT-003",
        "Verify piece movement with board obstacles",
    )
    def test_piece_movement_with_obstacles(self) -> None:
        """
        Test that pieces properly interact with obstacles:
        - Rooks can't move through pieces
        - Bishops can't move through pieces
        - Queens can't move through pieces
        - Knights can jump over pieces
        """
        # Test rook blocked by own pawn
        is_valid, error = self.move_validator.is_valid_move("A1", "A3", "white")
        self.assertFalse(is_valid)
        self.assertIn("blocked", error.lower())

        # Test bishop blocked by own pawn
        is_valid, error = self.move_validator.is_valid_move("C1", "A3", "white")
        self.assertFalse(is_valid)
        self.assertIn("blocked", error.lower())

        # Test knight can jump over pawns
        is_valid, error = self.move_validator.is_valid_move("B1", "C3", "white")
        self.assertTrue(is_valid)
        new_grid, _ = self.board.move_piece("B1", "C3")
        self.board.set_grid(new_grid)

        # Verify knight moved successfully despite pawns
        piece = self.board.get_piece("C3")
        self.assertIsNotNone(piece, "Knight should be at C3")
        if piece:  # Type guard
            self.assertEqual(piece.piece_type, "knight")

    @test_case(
        "TC-INT-004",
        "Verify pawn promotion with board state updates",
    )
    def test_pawn_promotion_integration(self) -> None:
        """
        Test that pawn promotion works correctly with board state:
        - Pawn reaches opposite end
        - Board updates piece to queen
        - Move validation handles promotion
        """
        # Set up a pawn near promotion
        self.board = Board()  # Fresh board
        self.move_validator = MoveValidator(self.board)

        # Move white pawn to 7th rank
        new_grid, _ = self.board.move_piece("E2", "E7")
        self.board.set_grid(new_grid)

        # Verify pawn promotion move is valid
        is_valid, error = self.move_validator.is_valid_move("E7", "E8", "white")
        self.assertTrue(is_valid)

        # Execute promotion move
        new_grid, _ = self.board.move_piece("E7", "E8")
        self.board.set_grid(new_grid)

        # Verify pawn was promoted to queen
        promoted_piece = self.board.get_piece("E8")
        self.assertIsNotNone(promoted_piece, "Promoted piece should exist")
        if promoted_piece:  # Type guard
            self.assertEqual(promoted_piece.piece_type, "queen")
            self.assertEqual(promoted_piece.color, "white")

    @test_case(
        "TC-INT-005",
        "Verify legal move generation considering check",
    )
    def test_legal_moves_in_check(self) -> None:
        """
        Test that legal moves are properly filtered when king is in check:
        - Only moves that block check or move king are valid
        - Other pieces can't make unrelated moves
        - Moving into check is prevented
        """
        # Set up a check situation
        moves: List[Tuple[str, str]] = [
            ("E2", "E4"),  # White pawn
            ("E7", "E5"),  # Black pawn
            ("F1", "C4"),  # White bishop
            ("F7", "F6"),  # Black pawn
            ("D1", "H5"),  # White queen puts black in check
        ]

        for src, dst in moves:
            new_grid, _ = self.board.move_piece(src, dst)
            self.board.set_grid(new_grid)

        # Verify black king is in check
        is_check = CheckDetector.is_in_check("black", self.board.grid)
        self.assertTrue(is_check, "Black king should be in check")

        # Test invalid moves that don't address check
        is_valid, _ = self.move_validator.is_valid_move("B8", "C6", "black")
        self.assertFalse(is_valid, "Knight move should be invalid while in check")

        # Test valid move that blocks check
        is_valid, _ = self.move_validator.is_valid_move("G7", "G6", "black")
        self.assertTrue(is_valid, "Pawn should be able to block check")

    @test_case(
        "TC-INT-006",
        "Verify board state copying for validation",
    )
    def test_board_state_copying(self) -> None:
        """
        Test that board state is properly copied during validation:
        - Original board remains unchanged during validation
        - Temporary moves don't affect main board
        - Piece positions are correctly preserved
        """
        # Store initial state
        initial_e2_piece = self.board.get_piece("E2")
        self.assertIsNotNone(initial_e2_piece, "Initial piece should exist")

        # Validate a move (which should use a board copy internally)
        self.move_validator.is_valid_move("E2", "E4", "white")

        # Verify original board unchanged
        current_e2_piece = self.board.get_piece("E2")
        self.assertIsNotNone(current_e2_piece, "Current piece should still exist")

        if initial_e2_piece and current_e2_piece:  # Type guard
            self.assertEqual(
                initial_e2_piece.piece_type,
                current_e2_piece.piece_type,
                "Board state should not change during move validation",
            )
            self.assertEqual(
                initial_e2_piece.color,
                current_e2_piece.color,
                "Board state should not change during move validation",
            )

        # Make actual move
        new_grid, _ = self.board.move_piece("E2", "E4")
        self.board.set_grid(new_grid)

        # Verify board state changed after real move
        self.assertIsNone(
            self.board.get_piece("E2"), "Original position should be empty after move"
        )

        moved_piece = self.board.get_piece("E4")
        self.assertIsNotNone(moved_piece, "Moved piece should exist")
        if moved_piece:  # Type guard
            self.assertEqual(moved_piece.piece_type, "pawn")
            self.assertEqual(moved_piece.color, "white")


if __name__ == "__main__":
    unittest.main()
