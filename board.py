from constant import *

class Board: 
    def __init__(self, board_size = 64):
        self.board_size = board_size
        self.white_pawns = WHITE_PAWNS_START
        self.white_rooks = WHITE_ROOKS_START
        self.white_knights = WHITE_KNIGHTS_START
        self.white_bishops = WHITE_BISHOPS_START
        self.white_queen = WHITE_QUEEN_START
        self.white_king = WHITE_KING_START

        self.black_pawns = BLACK_PAWNS_START
        self.black_rooks = BLACK_ROOKS_START
        self.black_knights = BLACK_KNIGHTS_START
        self.black_bishops = BLACK_BISHOPS_START
        self.black_queen = BLACK_QUEEN_START
        self.black_king = BLACK_KING_START

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