
class StaticChessMethods:
    @staticmethod
    def uci_to_indices(position:str):
        """
        Convert chess notation (e.g., 'E2') to grid indices.
        
        Args:
            position (str): Chess position in format like 'E2', 'a1', etc.
        
        Returns:
            tuple: (row, col) indices for the grid, or (None, None) if invalid
        """
        # Convert to uppercase and strip whitespace
        position = position.strip().upper()
        
        # Check if position is valid format (letter + number)
        if len(position) != 2:
            return None, None
        
        file_char = position[0]
        rank_char = position[1]
        
        # Validate file (A-H) and rank (1-8)
        if file_char not in 'ABCDEFGH' or rank_char not in '12345678':
            return None, None
        
        # Convert file letter to column index
        col = ord(file_char) - ord('A')
        
        # Convert rank number to row index
        row = int(rank_char) - 1
        
        return row, col

    @staticmethod
    def indices_to_uci(row, col):
        """
        Convert chess notation (e.g., 'E2') to grid indices.
        
        Args:
            position (str): Chess position in format like 'E2', 'a1', etc.
        
        Returns:
            tuple: (row, col) indices for the grid, or (None, None) if invalid
        """
        rank = row + 1
        files = "ABCDEFGH"
        file = files[col]
        uci = file + str(rank)
        return uci



