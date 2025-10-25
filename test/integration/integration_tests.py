"""
Integration Tests for Chess Game

Integration tests verify that multiple components work together correctly,
testing interactions between classes like Board + MoveValidator,
CheckDetector + Board, etc.

This file includes the original test cases (001-006) and the new,
more comprehensive test cases (007-018).
"""

import unittest
from typing import Any, Optional

from utils.board import Board
from utils.check_detector import CheckDetector
from utils.move_validator import MoveValidator
from utils.pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from utils.static_chess_methods import StaticChessMethods


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

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.board: Board = Board()
        self.move_validator: MoveValidator = MoveValidator(self.board)

    def _clear_board_and_set_pieces(
        self, pieces_to_set: list[tuple[str, str, str]]
    ) -> None:
        """
        Helper to create a custom board setup for a test.

        Args:
            pieces_to_set: A list of tuples, where each tuple is
                           (uci_position, piece_type, color).
                           Example: [("E1", "king", "white"), ("E8", "king", "black")]
        """
        # Create a new empty grid
        new_grid: list[list[Piece | None]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

        # Map piece types to classes
        piece_class_map: dict[str, type[Piece]] = {
            "pawn": Pawn,
            "knight": Knight,
            "bishop": Bishop,
            "rook": Rook,
            "queen": Queen,
            "king": King,
        }

        # Place specified pieces
        for position, piece_type, color in pieces_to_set:
            row_col_tuple = StaticChessMethods.uci_to_indices(position)
            if row_col_tuple:
                row, col = row_col_tuple
                piece_class = piece_class_map.get(piece_type.lower())
                if piece_class:
                    # The grid that is being built
                    new_grid[row][col] = piece_class(color, row, col, new_grid)

        # Set the board's grid
        self.board.set_grid(new_grid)

        # Re-update the grid reference for all pieces so they point to the final grid
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece:
                    piece.set_grid(self.board.grid)

        # Re-initialize the move validator with the new board state
        self.move_validator = MoveValidator(self.board)

    @test_case(
        "TC-INT-001", "Verify Board and CheckDetector integration for check detection"
    )
    def test_board_checkdetector_integration(self) -> None:
        """
        Test that Board and CheckDetector work together to:
        - Detect check situations
        - Track king positions
        - Identify attacking pieces
        """
        # Set up a check situation
        moves: list[tuple[str, str]] = [
            ("E2", "E4"),  # White pawn
            ("F7", "F5"),  # Black pawn
            ("F1", "C4"),  # White bishop
            ("B8", "C6"),  # Black knight
            ("D1", "H5"),  # White queen
        ]

        # Execute moves
        for src, dst in moves:
            new_grid, _ = self.board.move_piece(src, dst)
            self.board.set_grid(new_grid)
            # Must re-init validator as board state has changed
            self.move_validator = MoveValidator(self.board)

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
            king_pos_tuple = CheckDetector.find_king("black", self.board.grid)
            self.assertNotEqual(king_pos_tuple, (None, None))
            king_row, king_col = king_pos_tuple
            # Use the static method from CheckDetector as it's used internally
            king_pos = CheckDetector.indices_to_position(king_row, king_col)

            # Verify queen can attack king
            queen_moves = queen_piece.get_legal_moves()
            self.assertIn(king_pos, queen_moves, "Queen should be able to attack king")

    @test_case("TC-INT-002", "Verify piece movement with board obstacles")
    def test_piece_movement_with_obstacles(self) -> None:
        """
        Test that pieces properly interact with obstacles:
        - Knights can jump over pieces
        - Rooks, bishops, and queens can't move through pieces
        """
        # Test rook blocked by own pawn
        is_valid, error = self.move_validator.is_valid_move("A1", "A3", "white")
        self.assertFalse(is_valid)
        self.assertIn("blocked", error.lower())

        # Test bishop blocked by own pawn
        is_valid, error = self.move_validator.is_valid_move("C1", "A3", "white")
        self.assertFalse(is_valid)

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

    @test_case("TC-INT-003", "Verify pawn promotion with board state updates")
    def test_pawn_promotion_integration(self) -> None:
        """
        Test that pawn promotion works correctly with board state:
        - Pawn reaches opposite end
        - Board updates piece to queen
        - Move validation handles promotion
        """
        # Set up a pawn near promotion
        self._clear_board_and_set_pieces(
            [
                ("H7", "pawn", "white"),
                ("E1", "king", "white"),
                ("E8", "king", "black"),
            ]
        )

        # Verify pawn promotion move is valid
        is_valid, error = self.move_validator.is_valid_move("H7", "H8", "white")
        self.assertTrue(is_valid, f"Promotion move should be valid, got: {error}")

        # Execute promotion move
        new_grid, _ = self.board.move_piece("H7", "H8")
        self.board.set_grid(new_grid)

        # Verify pawn was promoted to queen
        promoted_piece = self.board.get_piece("H8")
        self.assertIsNotNone(promoted_piece, "Promoted piece should exist")
        self.assertEqual(promoted_piece.piece_type, "queen")
        self.assertEqual(promoted_piece.color, "white")

    @test_case("TC-INT-004", "Verify legal move generation considering check")
    def test_legal_moves_in_check(self) -> None:
        """
        Test that legal moves are properly filtered when king is in check:
        - Only moves that block check or move king are valid
        - Other pieces can't make unrelated moves
        - Moving into check is prevented
        """
        # Set up a check situation
        moves: list[tuple[str, str]] = [
            ("E2", "E4"),  # White pawn
            ("E7", "E5"),  # Black pawn
            ("F1", "C4"),  # White bishop
            ("F7", "F6"),  # Black pawn
            ("D1", "H5"),  # White queen puts black in check
        ]

        for src, dst in moves:
            new_grid, _ = self.board.move_piece(src, dst)
            self.board.set_grid(new_grid)
            self.move_validator = MoveValidator(self.board)

        # Verify black king is in check
        is_check = CheckDetector.is_in_check("black", self.board.grid)
        self.assertTrue(is_check, "Black king should be in check")

        # Test invalid moves that don't address check
        is_valid, error = self.move_validator.is_valid_move("B8", "C6", "black")
        self.assertFalse(is_valid, "Knight move should be invalid while in check")
        self.assertEqual(error, "Can't put your king in jeopardy")

        # Test valid move that blocks check
        is_valid, error = self.move_validator.is_valid_move("G7", "G6", "black")
        self.assertTrue(is_valid, "Pawn should be able to block check")

    @test_case("TC-INT-005", "Verify board state copying for validation")
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
            self.assertIs(
                initial_e2_piece, current_e2_piece, "Piece object should be the same"
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

    @test_case("TC-INT-006", "Verify Board + MoveValidator + Pawn Integration")
    def test_board_validator_pawn_moves(self) -> None:
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

    @test_case("TC-INT-007", "Verify Board + MoveValidator + Rook Integration")
    def test_board_validator_rook_moves(self) -> None:
        """Test integration for Rook moves."""
        self._clear_board_and_set_pieces(
            [
                ("E4", "rook", "white"),
                ("E8", "king", "black"),
                ("A8", "king", "white"),
                ("E2", "pawn", "white"),  # Friendly blocker
                ("H4", "pawn", "black"),  # Enemy target
            ]
        )

        # Valid horizontal move
        is_valid, _ = self.move_validator.is_valid_move("E4", "D4", "white")
        self.assertTrue(is_valid, "Valid horizontal rook move failed")

        # Valid vertical move (blocked by friendly)
        is_valid, _ = self.move_validator.is_valid_move("E4", "E1", "white")
        self.assertFalse(is_valid, "Rook move through friendly pawn should be invalid")

        # Valid capture
        is_valid, _ = self.move_validator.is_valid_move("E4", "H4", "white")
        self.assertTrue(is_valid, "Rook capture failed")

        # Invalid diagonal move
        is_valid, _ = self.move_validator.is_valid_move("E4", "F5", "white")
        self.assertFalse(is_valid, "Invalid diagonal rook move should be invalid")

    @test_case("TC-INT-008", "Verify Board + MoveValidator + Bishop Integration")
    def test_board_validator_bishop_moves(self) -> None:
        """Test integration for Bishop moves."""
        self._clear_board_and_set_pieces(
            [
                ("E4", "bishop", "white"),
                ("E8", "king", "black"),
                ("A8", "king", "white"),
                ("C2", "pawn", "white"),  # Friendly blocker
                ("G6", "pawn", "black"),  # Enemy target
            ]
        )

        # Valid diagonal move
        is_valid, _ = self.move_validator.is_valid_move("E4", "B7", "white")
        self.assertTrue(is_valid, "Valid diagonal bishop move failed")

        # Valid move (blocked by friendly)
        is_valid, _ = self.move_validator.is_valid_move("E4", "B1", "white")
        self.assertFalse(
            is_valid, "Bishop move through friendly pawn should be invalid"
        )

        # Valid capture
        is_valid, _ = self.move_validator.is_valid_move("E4", "G6", "white")
        self.assertTrue(is_valid, "Bishop capture failed")

        # Invalid horizontal move
        is_valid, _ = self.move_validator.is_valid_move("E4", "F4", "white")
        self.assertFalse(is_valid, "Invalid horizontal bishop move should be invalid")

    @test_case("TC-INT-009", "Verify Board + MoveValidator + Knight Integration")
    def test_board_validator_knight_moves(self) -> None:
        """Test integration for Knight moves."""
        self._clear_board_and_set_pieces(
            [
                ("E4", "knight", "white"),
                ("E8", "king", "black"),
                ("A8", "king", "white"),
                ("E5", "pawn", "white"),  # Friendly piece (to jump)
                ("D6", "pawn", "white"),  # Friendly piece (to block)
                ("C5", "pawn", "black"),  # Enemy target
            ]
        )

        # Valid jump over friendly pawn
        is_valid, _ = self.move_validator.is_valid_move("E4", "F6", "white")
        self.assertTrue(is_valid, "Knight jump over friendly pawn failed")

        # Valid capture
        is_valid, _ = self.move_validator.is_valid_move("E4", "C5", "white")
        self.assertTrue(is_valid, "Knight capture failed")

        # Invalid move (blocked by friendly)
        is_valid, _ = self.move_validator.is_valid_move("E4", "D6", "white")
        self.assertFalse(is_valid, "Knight move onto friendly piece should be invalid")

    @test_case("TC-INT-010", "Verify Board + MoveValidator + Queen Integration")
    def test_board_validator_queen_moves(self) -> None:
        """Test integration for Queen moves."""
        self._clear_board_and_set_pieces(
            [
                ("E4", "queen", "white"),
                ("E8", "king", "black"),
                ("A8", "king", "white"),
                ("E5", "pawn", "white"),  # Friendly blocker (vertical)
                ("C4", "pawn", "white"),  # Friendly blocker (horizontal)
                ("C6", "pawn", "white"),  # Friendly blocker (diagonal)
                ("G6", "pawn", "black"),  # Enemy target
            ]
        )

        # Valid diagonal capture
        is_valid, _ = self.move_validator.is_valid_move("E4", "G6", "white")
        self.assertTrue(is_valid, "Queen diagonal capture failed")

        # Invalid vertical (blocked)
        is_valid, _ = self.move_validator.is_valid_move("E4", "E7", "white")
        self.assertFalse(
            is_valid, "Queen move through friendly (vertical) should be invalid"
        )

        # Invalid horizontal (blocked)
        is_valid, _ = self.move_validator.is_valid_move("E4", "B4", "white")
        self.assertFalse(
            is_valid, "Queen move through friendly (horizontal) should be invalid"
        )

        # Invalid diagonal (blocked)
        is_valid, _ = self.move_validator.is_valid_move("E4", "B7", "white")
        self.assertFalse(
            is_valid, "Queen move through friendly (diagonal) should be invalid"
        )

        # Invalid knight move
        is_valid, _ = self.move_validator.is_valid_move("E4", "F6", "white")
        self.assertFalse(is_valid, "Invalid knight move for queen should be invalid")

    @test_case("TC-INT-011", "Verify Board + MoveValidator + King Integration")
    def test_board_validator_king_moves(self) -> None:
        """Test integration for King moves (non-check)."""
        self._clear_board_and_set_pieces(
            [
                ("E4", "king", "white"),
                ("E8", "king", "black"),
                ("E5", "pawn", "white"),  # Friendly blocker
                ("D5", "pawn", "black"),  # Enemy target
            ]
        )

        # Valid move (forward)
        is_valid, _ = self.move_validator.is_valid_move("E4", "D4", "white")
        self.assertTrue(is_valid, "King move failed")

        # Valid capture
        is_valid, _ = self.move_validator.is_valid_move("E4", "D5", "white")
        self.assertTrue(is_valid, "King capture failed")

        # Invalid move (onto friendly)
        is_valid, _ = self.move_validator.is_valid_move("E4", "E5", "white")
        self.assertFalse(is_valid, "King move onto friendly piece should be invalid")

        # Invalid 2-square move
        is_valid, _ = self.move_validator.is_valid_move("E4", "E6", "white")
        self.assertFalse(is_valid, "Invalid 2-square king move should be invalid")

    @test_case("TC-INT-012", "Verify MoveValidator prevents King moving into check")
    def test_validator_prevents_king_move_into_check(self) -> None:
        """Test King cannot move onto an attacked square."""
        self._clear_board_and_set_pieces(
            [
                ("E1", "king", "white"),
                ("E8", "king", "black"),
                ("A6", "rook", "black"),
                ("H7", "rook", "black"),
            ]
        )

        # Try to move king into check from rook on A2
        is_valid, _ = self.move_validator.is_valid_move("E8", "E7", "black")
        self.assertTrue(is_valid, "Black king was put in check by a black piece")

        # Set up for tests with the white king
        self._clear_board_and_set_pieces(
            [
                ("E1", "king", "white"),
                ("A2", "rook", "black"),  # Attacks A-file, 2nd rank
                ("E8", "king", "black"),
            ]
        )
        # Try to move king into check from rook on A2
        is_valid, error = self.move_validator.is_valid_move("E1", "D2", "white")
        self.assertFalse(is_valid, "King moved into check (D2)")
        self.assertEqual(error, "Can't put your king in jeopardy")

        is_valid, error = self.move_validator.is_valid_move("E1", "E2", "white")
        self.assertFalse(is_valid, "King moved into check (E2)")
        self.assertEqual(error, "Can't put your king in jeopardy")

        is_valid, error = self.move_validator.is_valid_move("E1", "F2", "white")
        self.assertFalse(is_valid, "King moved into check (F2)")
        self.assertEqual(error, "Can't put your king in jeopardy")

    @test_case("TC-INT-013", "Verify MoveValidator prevents moving a pinned piece")
    def test_validator_prevents_pinned_piece_move(self) -> None:
        """Test a pinned piece cannot move if it exposes the King."""
        self._clear_board_and_set_pieces(
            [
                ("E1", "king", "white"),
                ("E4", "rook", "white"),  # This rook is pinned
                ("E8", "queen", "black"),  # Pinning piece
                ("A8", "king", "black"),
            ]
        )

        # The rook on E4 is pinned to the king by the black queen.
        # Moving it horizontally should be illegal.
        is_valid, error = self.move_validator.is_valid_move("E4", "C4", "white")
        self.assertFalse(is_valid, "Pinned rook moved horizontally")
        self.assertEqual(error, "Can't put your king in jeopardy")

        # Moving it vertically *along* the pin is legal (if it doesn't pass king)
        is_valid, error = self.move_validator.is_valid_move("E4", "E3", "white")
        self.assertTrue(is_valid, "Pinned rook should be able to move along pin")

    @test_case("TC-INT-014", "Verify MoveValidator allows King to move out of check")
    def test_validator_allows_king_escape_check(self) -> None:
        """Test King can move out of check."""
        self._clear_board_and_set_pieces(
            [
                ("E1", "king", "white"),
                ("B4", "bishop", "black"),  # Puts king in check
                ("E8", "king", "black"),
            ]
        )

        # Verify king is in check
        is_check = CheckDetector.is_in_check("white", self.board.grid)
        self.assertTrue(is_check, "King should be in check")

        # Test invalid move (still in check)
        is_valid, error = self.move_validator.is_valid_move("E1", "D2", "white")
        self.assertFalse(is_valid, "King move to D2 should still be in check")
        self.assertEqual(error, "Can't put your king in jeopardy")

        # Test valid move (safe square)
        is_valid, error = self.move_validator.is_valid_move("E1", "F1", "white")
        self.assertTrue(is_valid, "King should be able to escape to F1")

        # Test valid move (safe square)
        is_valid, error = self.move_validator.is_valid_move("E1", "E2", "white")
        self.assertTrue(is_valid, "King should be able to escape to E2")

    @test_case("TC-INT-015", "Verify MoveValidator + CheckDetector identify Checkmate")
    def test_validator_checkdetector_checkmate(self) -> None:
        """Test integration to identify a checkmate position."""
        # Set up Scholar's Mate
        self._clear_board_and_set_pieces(
            [
                ("E1", "king", "white"),
                ("H5", "queen", "white"),
                ("C4", "bishop", "white"),
                ("E8", "king", "black"),
                ("F7", "pawn", "black"),  # Target
                ("D8", "queen", "black"),
            ]
        )

        # Simulate the checkmating move
        new_grid, _ = self.board.move_piece("H5", "F7")
        self.board.set_grid(new_grid)
        self.move_validator = MoveValidator(self.board)

        # Verify black is in check
        is_check = CheckDetector.is_in_check("black", self.board.grid)
        self.assertTrue(is_check, "Black king should be in check")

        # Verify black has no legal moves
        legal_moves, in_check_moves = self.move_validator.generate_valid_moves("black")
        self.assertEqual(len(legal_moves), 0, "Black should have no legal moves")
        # There might be moves that *would* be legal if not for check
        # The key is that legal_moves (which are safe) is empty.

    @test_case("TC-INT-016", "Verify MoveValidator + CheckDetector identify Stalemate")
    def test_validator_checkdetector_stalemate(self) -> None:
        """Test integration to identify a stalemate position."""
        # Set up a classic stalemate
        self._clear_board_and_set_pieces(
            [
                ("A8", "king", "black"),
                ("C7", "king", "white"),
                ("B6", "queen", "white"),
            ]
        )

        # Verify black is NOT in check
        is_check = CheckDetector.is_in_check("black", self.board.grid)
        self.assertFalse(is_check, "Black king should not be in check")

        # Verify black has no legal moves
        legal_moves, _ = self.move_validator.generate_valid_moves("black")
        self.assertEqual(len(legal_moves), 0, "Black should have no legal moves")

    @test_case("TC-INT-017", "Verify Pawn Promotion can deliver check")
    def test_pawn_promotion_delivers_check(self) -> None:
        """Test that a promotion to Queen correctly triggers check."""
        self._clear_board_and_set_pieces(
            [
                ("E7", "pawn", "white"),
                ("C8", "king", "black"),
                ("A1", "king", "white"),
            ]
        )

        # Verify black is NOT in check initially
        is_check = CheckDetector.is_in_check("black", self.board.grid)
        self.assertFalse(is_check, "Black king should not be in check")

        # Execute promotion move
        new_grid, _ = self.board.move_piece("E7", "E8")
        self.board.set_grid(new_grid)
        self.move_validator = MoveValidator(self.board)

        # Verify piece is a queen
        promoted_piece = self.board.get_piece("E8")
        self.assertIsNotNone(promoted_piece)
        self.assertEqual(promoted_piece.piece_type, "queen")

        # Verify black IS in check
        is_check = CheckDetector.is_in_check("black", self.board.grid)
        self.assertTrue(is_check, "Black king should be in check after promotion")

    @test_case("TC-INT-018", "Verify MoveValidator prevents moving opponent's piece")
    def test_validator_prevents_moving_opponent_piece(self) -> None:
        """Test a player cannot move a piece of the wrong color."""
        # Use initial board setup

        # Try to move black pawn as white
        is_valid, error = self.move_validator.is_valid_move("E7", "E6", "white")
        self.assertFalse(is_valid)
        self.assertEqual(error, "That's not your piece")

        # Try to move white pawn as black
        is_valid, error = self.move_validator.is_valid_move("E2", "E3", "black")
        self.assertFalse(is_valid)
        self.assertEqual(error, "That's not your piece")


if __name__ == "__main__":
    unittest.main()
