# Chess Game

A console-based chess program that allows two players to play chess with move validation and check detection. This is a simplified "dumb" version of chess.

## Description

This chess program implements a fully functional two-player chess game in the terminal. Players take turns entering moves, and the program validates moves according to chess rules, detects check situations, and ends the game when a king is captured.

The game displays an 8x8 chess board with pieces represented by letters (uppercase for white, lowercase for black). The board is labeled with standard chess notation: files A-H (columns) and ranks 1-8 (rows).

## Directory
- [Component Descriptions](#component-descriptions)
- [How to Run](#how-to-run)
  - [Windows](#windows)
  - [Mac/Linux](#maclinux)
- [How to Play](#how-to-play)
- [Game Limitations](#game-limitations-dumb-chess-rules)
- [Example Board Display](#example-board-display)
- [Testing](#testing)
- [Requirements](#requirements)

## Component Descriptions

### pieces.py
Defines the `Piece` abstract base class which contains common functionality between different types of chess pieces.

Defines the child classes of Piece: `Pawn`, `Rook`, `Knight`, `Bishop`, `Queen`, and `King`

**Responsibilities:**
- Stores piece color (white or black)
- Stores piece row (0-7)
- Stores piece column (0-7)
- Stores a two dimensional 8x8 grid of pieces and null objects that represents the board state
- Provides a list of uci positions it can attack
- Provides string representation for display
- Uses uppercase letters for white pieces (K, Q, R, B, N, P)
- Uses lowercase letters for black pieces (k, q, r, b, n, p)
- Knight is represented as 'n' or 'N' to avoid confusion with king

### board.py
Defines the `Board` class which manages the chess board and piece positions.

**Responsibilities:**
- Maintains an 8x8 grid of pieces
- Sets up the initial chess position with all pieces in standard starting locations
- Displays the board in a text-based grid format with rank and file labels
- Converts chess notation (like "E2") to array indices and vice versa
- Immutably moves pieces from one position to another 
- Handles pawn promotion (automatically promotes pawns to queens when reaching the opposite end)
- Manages piece captures

### move_validator.py
Defines the `MoveValidator` class which validates chess moves according to piece movement rules.

**Responsibilities:**
- Generates a list of valid moves based on what each piece sees, and whether or not that move puts their king in check.
- Checks if the correct player owns the piece being moved
- Prevents capturing your own pieces
- Implements specific movement rules for each piece type:
  - Pawns: Move forward one square (or two from starting position), capture diagonally
  - Rooks: Move horizontally or vertically any distance
  - Knights: Move in L-shape (2 squares in one direction, 1 perpendicular), can jump over pieces
  - Bishops: Move diagonally any distance
  - Queens: Move like rooks or bishops
  - Kings: Move one square in any direction
- Checks if paths are clear for pieces that cannot jump (rooks, bishops, queens)

### check_detector.py
Defines the `CheckDetector` class which detects when a king is in check.

**Responsibilities:**
- Locates kings on the board
- Determines if a king is under attack by any enemy piece
- Scans all enemy pieces to see if any can legally move to the king's position
- Reports check status at the beginning of each turn

### static_chess_methods.py

Defines the `StaticChessMethods` class which implements common chess needs.

**Responsibilities:**
- Converts uci positions to grid indices
- Converts grid indices to uci positions

### game.py
Defines the `Game` class which controls the main game flow.

**Responsibilities:**
- Manages turn alternation between white and black players
- Prompts players for their moves
- Parses move input in various formats (space-separated, dash-separated, comma-separated)
- Validates moves using the MoveValidator
- Executes valid moves on the board
- Detects check situations before each turn
- Handles piece captures and reports them
- Detects game over condition (when a king is captured)
- Displays the board after each move

## How to Run

1. Navigate to the project directory in your terminal
2. Run the game:
    ### Windows

    1. Navigate to the project directory
    2. Double-click `ChessGame.exe` or run from Command Prompt:
      ```cmd
      ChessGame.exe
      ```

    ### Mac/Linux

    1. Navigate to the project directory in Terminal
    2. Make the file executable (first time only):
      ```bash
      chmod +x ChessGame-Linux
      ```
    3. Run the game:
      ```bash
      ./ChessGame-Linux
      ```

## How to Play

1. The game starts with the standard chess position displayed
2. White moves first
3. Enter moves in the format: `E2 E4` (source position, then destination position)
   - Accepted formats: `E2 E4`, `E2-E4`, `E2,E4`, or `E2, E4`
   - Case insensitive (e2 e4 works the same as E2 E4)
4. The program will validate your move and display an error if illegal
5. After a valid move, the updated board is displayed
6. If a piece is captured, the program reports it
7. If a king is in check, the program reports it at the start of that player's turn
8. Players alternate turns until one king is captured
9. The game ends when a player no longer has legal moves, the winner is announced if that player is also in check. Otherwise its a draw

## Game Limitations (Dumb Chess Rules)

This is a simplified version of chess with the following limitations:

### Not Implemented
- **Castling**: Not allowed
- **En passant**: Pawn captures en passant are not implemented

### Simplified Rules
- **Pawn promotion**: Pawns automatically promote to queens when reaching the opposite end (no choice of piece)

## Example Board Display

```
    A   B   C   D   E   F   G   H
  ---------------------------------
  ---------------------------------
8 | r | n | b | q | k | b | n | r |
  ---------------------------------
7 | p | p | p | p | p | p | p | p |
  ---------------------------------
6 |   |   |   |   |   |   |   |   |
  ---------------------------------
5 |   |   |   |   |   |   |   |   |
  ---------------------------------
4 |   |   |   |   |   |   |   |   |
  ---------------------------------
3 |   |   |   |   |   |   |   |   |
  ---------------------------------
2 | P | P | P | P | P | P | P | P |
  ---------------------------------
1 | R | N | B | Q | K | B | N | R |
  ---------------------------------
  ---------------------------------
    A   B   C   D   E   F   G   H
```

## Testing

This project includes a comprehensive test suite with 46 test cases covering all aspects of the chess game. Tests are organized into three categories: **Unit Tests**, **Integration Tests**, and **System Tests**.

## Installation

Before running the tests, install the required dependencies:

```bash
pip install -r requirements.txt
```

**Required packages:**
- `openpyxl` - For generating Excel test reports

### Test Categories

#### 1. Unit Tests
Unit tests verify individual components in isolation, testing single methods and classes without dependencies.

**Coverage:**
- Static method conversions (UCI notation ↔ grid indices)
- Individual piece movement patterns (Pawn, Knight, Bishop, Rook, Queen, King)
- Piece string representation
- CheckDetector helper methods
- Board utility methods
- Piece copying functionality

**Example:** `TC-UNIT-001` verifies that chess notation like "E4" correctly converts to grid indices (3, 4).

#### 2. Integration Tests
Integration tests verify that multiple components work together correctly, testing interactions between classes.

**Coverage:**
- Board + MoveValidator integration
- Board + CheckDetector integration
- Piece movement with board obstacles
- Pawn promotion with board state
- Legal move generation considering check
- Board state copying for validation

**Example:** `TC-INT-001` verifies that Board and MoveValidator work together to handle pawn moves, including validation, execution, and state updates.

#### 3. System Tests
System tests verify complete game workflows from start to finish, testing end-to-end scenarios.

**Coverage:**
- Game initialization and board setup
- Complete move sequences
- Turn alternation
- Piece captures
- Check detection
- Pawn promotion
- Game ending conditions (checkmate, stalemate, king capture)
- Move input parsing (all supported formats)
- Illegal move rejection
- Board state persistence

**Example:** `TC-SYS-003` verifies a standard opening move sequence, ensuring pieces move correctly and the board state updates properly.

### How to Run Tests

#### Run All Tests with Excel Export
This executes all test suites and generates a detailed Excel report:

```bash
python -m test.test
```

**Output:**
- Console summary with pass/fail statistics
- Excel report saved to `test/export/chess_test_results_YYYYMMDD_HHMMSS.xlsx`
- Exit code 0 for success, 1 for failures

#### Run Specific Test Suite
```bash
# Run only system tests
python -m unittest test.system.system_tests

# Run only integration tests
python -m unittest test.integration.integration_tests

# Run only unit tests
python -m unittest test.unit.unit_tests
```

#### Run Individual Test
```bash
# Run a specific test method
python -m unittest test.system.system_tests.TestChessGameSystem.test_game_initialization
```

### Test Case Format

Each test case follows a consistent format with metadata for Excel export:

```python
@test_case('TC-UNIT-001', 'Description of what this test verifies')
def test_method_name(self):
    """
    Detailed docstring explaining:
    - What component/method is being tested
    - Test setup and preconditions
    - Expected results
    - Any edge cases covered
    """
    # Arrange: Set up test data
    test_object = SomeClass()
    
    # Act: Execute the method being tested
    result = test_object.method_to_test()
    
    # Assert: Verify expected behavior
    self.assertEqual(result, expected_value)
    self.assertTrue(condition)
```

**Test Case ID Convention:**
- `TC-SYS-XXX` - System tests (complete workflows)
- `TC-INT-XXX` - Integration tests (component interactions)  
- `TC-UNIT-XXX` - Unit tests (individual methods)

Where `XXX` is a zero-padded 3-digit number (001, 002, etc.)

### Excel Report Format

The generated Excel report includes two sheets:

#### Sheet 1: Test Results
A detailed table with the following columns:

| Column | Description |
|--------|-------------|
| **Test Case ID** | Unique identifier (e.g., TC-SYS-001) |
| **Category** | SYSTEM, INTEGRATION, or UNIT |
| **Test Name** | Python method name |
| **Description** | Human-readable explanation of what's tested |
| **Result** | PASS, FAIL, ERROR, or SKIP (color-coded) |
| **Duration (s)** | Execution time in seconds |
| **Timestamp** | When the test was executed |
| **Error Message** | Full traceback for failures (if applicable) |

**Color Coding:**
- Green background = PASS
- Red background = FAIL  
- Yellow background = ERROR
- Gray background = SKIP

#### Sheet 2: Summary
Test execution statistics:
- Total tests run
- Number passed/failed/errors/skipped
- Pass rate percentage
- Execution date and time

### Finding Test Results

After running `python -m test.test`, the Excel report is saved to:

```
tests/export/chess_test_results_YYYYMMDD_HHMMSS.xlsx
```

Where `YYYYMMDD_HHMMSS` is the timestamp when tests were executed (e.g., `chess_test_results_20251002_143022.xlsx`).

**Example Console Output:**
```
Running Chess Game Tests...

======================================================================
TEST EXECUTION SUMMARY
======================================================================
Total Tests: 46
Passed: 44
Failed: 2
Errors: 0
Skipped: 0
======================================================================

Excel report saved to: tests/export/chess_test_results_20251012_143022.xlsx
```

### Adding New Tests

To add a new test case:

1. Open the appropriate test file (`unit_tests.py`, `integration_tests.py`, or `system_tests.py`)
2. Add a new test method to the test class
3. Use the `@test_case` decorator with a unique ID and description
4. Follow the Arrange-Act-Assert pattern
5. Run `test.py` to include it in the Excel report

**Example:**
```python
@test_case('TC-UNIT-019', 'Verify rook cannot jump over pieces')
def test_rook_cannot_jump(self):
    """Test that rook movement is blocked by intervening pieces."""
    # Test implementation here
    pass
```

### Troubleshooting Tests

**Import Errors:**
- Ensure you're running from the project root directory
- Verify all `__init__.py` files exist in test directories

**Excel Not Generated:**
- Install openpyxl: `pip install -r requirements.txt`
- Check write permissions for `test/export/` directory

**Module Not Found:**
```bash
python -m test.test
```

## Requirements

- Python 3.7+
- openpyxl (for test report generation)

See `requirements.txt` for complete dependency list.