class Board: 
    def __init__(self, board_size = 64):
        self.board_size = board_size
    #White pieces positions
        self.white_pawns = 0X000000000000FF00
        self.white_rooks = 0x0000000000000081
        self.white_knights = 0x0000000000000042
        self.white_bishops = 0x0000000000000024
        self.white_queen = 0x000000000000008
        self.white_king = 0x0000000000000010
    #Black pieces positions
        self.black_pawns = 0x00FF000000000000
        self.black_rooks = 0x8100000000000000
        self.black_knights = 0x4200000000000000
        self.black_bishops = 0x2400000000000000
        self.black_queen = 0x800000000000000
        self.black_king = 0x1000000000000000

    def define_pieces(self):
        pieces = {'P': self.white_pawns, 
                  'R': self.white_rooks, 
                  'N': self.white_knights, 
                  'B': self.white_bishops, 
                  'Q': self.white_queen, 
                  'K': self.white_king,
                  'p': self.black_pawns, 
                  'r': self.black_rooks, 
                  'n': self.black_knights, 
                  'b': self.black_bishops, 
                  'q': self.black_queen,
                  'k': self.black_king}
        return pieces
    
    def move_piece(self, start_idx, end_idx):
        #Get the bitmask for the starting and ending positions
        start_mask = 1 << start_idx
        end_mask = 1 << end_idx
        move_mask = start_mask | end_mask

        board_representation = self.get_board_representation()
        pieces = self.define_pieces()

        #Check if there is a piece at the starting position
        if(board_representation & start_mask) == 0:
            print("No piece at the starting position.")
            return
        #If there is a piece at the starting position
        else:
            #Find the piece that is being moved
            for piece, position in pieces.items():
                if (position & start_mask) != 0:
                    moved_piece = piece
                    break
            #Update the bits of the moving piece
            if moved_piece == "P": self.white_pawns ^= move_mask
            elif moved_piece == "R": self.white_rooks ^= move_mask
            elif moved_piece == "N": self.white_knights ^= move_mask
            elif moved_piece == "B": self.white_bishops ^= move_mask
            elif moved_piece == "Q": self.white_queen ^= move_mask
            elif moved_piece == "K": self.white_king ^= move_mask
            elif moved_piece == "p": self.black_pawns ^= move_mask
            elif moved_piece == "r": self.black_rooks ^= move_mask
            elif moved_piece == "n": self.black_knights ^= move_mask
            elif moved_piece == "b": self.black_bishops ^= move_mask
            elif moved_piece == "q": self.black_queen ^= move_mask
            elif moved_piece == "k": self.black_king ^= move_mask
        
            capture_mask = ~end_mask
            if moved_piece.isupper(): # If the moved piece is white, check for black pieces at the ending position
                self.black_pawns &= capture_mask
                self.black_rooks &= capture_mask
                self.black_knights &= capture_mask
                self.black_bishops &= capture_mask
                self.black_queen &= capture_mask
                self.black_king &= capture_mask
            else: # If the moved piece is black, check for white pieces at the ending position
                self.white_pawns &= capture_mask
                self.white_rooks &= capture_mask
                self.white_knights &= capture_mask
                self.white_bishops &= capture_mask
                self.white_queen &= capture_mask
                self.white_king &= capture_mask
    
    def get_board_representation(self):
        board_representation = 0 # Initialize an empty board representation
        pieces = self.define_pieces()
        # Loop through all the pieces in my pieces dictionary
        for piece in pieces:
            # Set all the pieces on the board representation, using bitwise OR
            board_representation |= pieces[piece]
        
        return board_representation

    def print_board(self):
        board_representation = self.get_board_representation()
        pieces = self.define_pieces()

        print("\n  a b c d e f g h") # Header for orientation
        for rank in range(7, -1, -1):
            line = f"{rank + 1} " # Side label (Rank number)
            for file in range(8):
                # Standard LERF mapping: index = rank * 8 + file
                i = rank * 8 + file
                square_bit = 1 << i
                
                if (board_representation & square_bit) != 0:
                    for char, bb in pieces.items():
                        if (bb & square_bit) != 0:
                            line += char + " "
                            break
                else:
                    line += ". "
            print(line)

if __name__ == "__main__":
    chess_board = Board()
    
    # Interactive Sandbox Loop
    while True:
        chess_board.print_board()
        print("\nEnter indices (e.g., White Pawn a2 to a4 is 8 to 24)")
        try:
            start = int(input("Start Index: "))
            end = int(input("End Index: "))
            chess_board.move_piece(start, end)
        except ValueError:
            print("Please enter valid numbers.")
        except KeyboardInterrupt:
            break
