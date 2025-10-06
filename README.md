# Chess Game

A console-based chess program that allows two players to play chess with move validation and check detection. This is a simplified "dumb" version of chess.s

## Description

This chess program implements a fully functional two-player chess game in the terminal. Players take turns entering moves, and the program validates moves according to chess rules, detects check situations, and ends the game when a king is captured.

The game displays an 8x8 chess board with pieces represented by letters (uppercase for white, lowercase for black). The board is labeled with standard chess notation: files A-H (columns) and ranks 1-8 (rows).

## Component Descriptions

### piece.py
Defines the `Piece` class which represents individual chess pieces.

**Responsibilities:**
- Stores piece type (king, queen, rook, bishop, knight, pawn)
- Stores piece color (white or black)
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
- Moves pieces from one position to another
- Handles pawn promotion (automatically promotes pawns to queens when reaching the opposite end)
- Manages piece captures

### move_validator.py
Defines the `MoveValidator` class which validates chess moves according to piece movement rules.

**Responsibilities:**
- Validates moves based on piece type and movement patterns
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
2. Runs:

```bash
python main.py
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
9. The game ends when a king is captured, and the winner is announced

## Game Limitations (Dumb Chess Rules)

This is a simplified version of chess with the following limitations:

### Not Implemented
- **Castling**: Not allowed
- **En passant**: Pawn captures en passant are not implemented
- **Checkmate detection**: The game does not detect checkmate
- **Stalemate detection**: The game does not detect stalemate
- **Self-check prevention**: Players can move their king into check or leave their king in check (illegal in real chess)
- **Draw conditions**: No detection of threefold repetition, fifty-move rule, or insufficient material

### Simplified Rules
- **Pawn promotion**: Pawns automatically promote to queens when reaching the opposite end (no choice of piece)
- **Game ending**: The game ends when a king is actually captured, not when checkmate occurs
- **Check handling**: Check is reported but does not force the player to respond to it

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