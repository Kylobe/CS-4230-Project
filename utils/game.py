"""
Controls the main game flow.
"""
from .board import Board
from .move_validator import MoveValidator
from .check_detector import CheckDetector

class Game:
    """
    Controls the chess game.
    
    Manages:
    - Turn alternation between players
    - Move input and validation
    - Check detection
    - Game over conditions
    """
    
    def __init__(self):
        """
        Initialize a new chess game.
        
        Sets up the board, validators, and game state.
        """
        self.board = Board()

        self.move_validator = MoveValidator(self.board)
        self.current_player = 'white'
        self.game_over = False
    
    def start(self):
        """
        Start the game and run the main game loop.
        
        Displays the board, prompts for moves, and loops until one king is captured.
        """
        print("Welcome to Chess!")
        print("Enter moves like: E2 (initial position) E4 (source destination)")
        print("The game ends when a king is captured.")
        print("White = Uppercase letters, Black = Lowercase letters.")
        print("White plays first.")
        print()
        
        # Display initial board
        print(self.board.display())
        
        # Main game loop
        while not self.game_over:
            self.play_turn()
    
    def play_turn(self):
        """        
        Cycles one turn. Checks for check, prompts for move, validates it, executes it, and switches players.
        """
        # Check if current player's king is in check
        check = CheckDetector.is_in_check(self.current_player, self.board.grid)
        legal_moves = self.move_validator.generate_valid_moves(self.current_player)
        # If there are no legal moves, end the game
        if len(legal_moves) == 0:
            # Declare victory by check mate
            if check:
                victor = "white" if self.current_player == "black" else "black"
                print(f"\n{victor.capitalize()} won with check mate!")
            # Declare Draw
            else:
                print(f"\n{self.current_player.capitalize()} has no legal moves, game ends in a draw!")
            self.game_over = True
            return

        if check:
            print(f"\n{self.current_player.capitalize()} is in check!")
        
        # Prompt for move
        print(f"\n{self.current_player.capitalize()}'s move: ", end="")
        move_input = input().strip()
        
        # Parse the move input
        source, destination = self.parse_move(move_input)
        
        if source is None:
            print("Invalid move format. Use format like: E2 E4")
            return
        
        # Validate the move
        is_valid, error_message = self.move_validator.is_valid_move(source, destination, self.current_player)
        
        if not is_valid:
            print(f"Illegal move: {error_message}")
            return
        
        # Execute the move
        new_state, captured_piece = self.board.move_piece(source, destination)

        self.board.set_grid(new_state)
        
        # Check if a king was captured
        if captured_piece and captured_piece.piece_type == 'king':
            print(self.board.display())
            print(f"\n{self.current_player.capitalize()} wins! {captured_piece.color.capitalize()} king has been captured!")
            self.game_over = True
            return
        
        # Display the board after the move
        print()
        print(self.board.display())
        
        # Report any captures
        if captured_piece:
            print(f"\n{self.current_player.capitalize()} captured {captured_piece.color}'s {captured_piece.piece_type}!")
        
        # Switch to the other player
        self.current_player = 'black' if self.current_player == 'white' else 'white'
    
    def parse_move(self, move_input):
        """
        Parse user input into source and destination positions.
        
        Accepts formats like:
        - "E2 E4" (with space)
        - "E2-E4" (with dash)
        - "e2 e4" (lowercase)
        - "e2, e4" (comma+space)
        - "e2,e4" (comma)
        
        Args:
            move_input (str): The user's move input
        
        Returns:
            tuple: (source, destination) as strings, or (None, None) if invalid
        """
        parts = None
        
        move_input = move_input.strip()

        if ', ' in move_input:
            parts = move_input.split(', ')
        elif ',' in move_input:
            parts = move_input.split(',')
        elif '-' in move_input:
            parts = move_input.split('-')
        elif ' ' in move_input:
            parts = move_input.split()
        else:
            return None, None

        if len(parts) != 2:
            return None, None
        
        source = parts[0].strip().upper()
        destination = parts[1].strip().upper()
        
        return source, destination