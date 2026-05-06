class Board: 
    def __init__(self, board_size = 64):
        self.board_size = board_size
    #White pieces positions
        self.white_pawns = 0X000000000000FF00
        self.white_rooks = 0x0000000000000081
        self.white_knights = 0x0000000000000042
        self.white_bishops = 0x0000000000000024
        self.white_queen = 0x0000000000000010
        self.white_king = 0x000000000000008
    #Black pieces positions
        self.black_pawns = 0x00FF000000000000
        self.black_rooks = 0x8100000000000000
        self.black_knights = 0x4200000000000000
        self.black_bishops = 0x2400000000000000
        self.black_queen = 0x1000000000000000
        self.black_king = 0x800000000000000

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
    

    def print_board(self):
        board_representation = 0 # Initialize an empty board representation
        pieces = self.define_pieces()
        
        # Loop through all the pieces in my pieces dictionary
        for piece in pieces:
            # Set all the pieces on the board representation, using bitwise OR
            board_representation |= pieces[piece]
            
        # Print the board representation using the letters for easy visualization
        for i in range(self.board_size - 1, -1, -1):
            # Check if there is a piece on the current square using bitwise AND
            if (board_representation & (1 << i)) != 0:
                # If there is a piece, find out what piece it is
                for piece in pieces:
                    if (pieces[piece] & (1 << i)) != 0:
                        print(piece, end=' ')
                        break
            else:
                print('.', end=' ')
            #Print new line after every 8 squares to represent the next rank
            if i % 8 == 0:
                print()

if __name__ == "__main__":
    chess_board = Board()
    pieces = chess_board.define_pieces()
    chess_board.print_board()
