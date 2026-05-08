from constant import *

class MoveGen:
    def __init__(self):
        self.knight_moves = self._precompute_knights()
        self.king_moves = self._precompute_king()
    
    def _precompute_knights(self):
        #Moves the knight can take
        table = []
        for i in range(64):
            knight_pos = 1 << i
            move = 0
            move |= (knight_pos << 17) & NOT_A_FILE
            move |= (knight_pos << 15) & NOT_H_FILE
            move |= (knight_pos << 10) & NOT_AB_FILE
            move |= (knight_pos << 6)  & NOT_GH_FILE
            move |= (knight_pos >> 17) & NOT_H_FILE
            move |= (knight_pos >> 15) & NOT_A_FILE
            move |= (knight_pos >> 10) & NOT_GH_FILE
            move |= (knight_pos >> 6)  & NOT_AB_FILE
            table.append(move)
        return table
    
    def _precompute_king(self):
        #moves the king can take
        table = []
        for i in range(64):
            king_pos = 1 << i
            move = 0
            #King wanna move up but can't when its on row 8
            move |= (king_pos << 8) & ~RANK_8
            #Move down but cannot when its on row 0
            move |= (king_pos >> 8) & ~RANK_1
            #Move right but cannot when its column h
            move |= (king_pos << 1) & NOT_A_FILE
            #move left but cannot when its column a
            move |= (king_pos >> 1) & NOT_H_FILE
            #Move NE but cannot when its at h8
            move |= (king_pos << 9) & NOT_A_FILE
            #Move NW but cannot when its at a8
            move |= (king_pos << 7) & NOT_H_FILE
            #Move SE but cannot when its at h1
            move |= (king_pos >> 7) & NOT_A_FILE
            #Move SW but cannot when its at a1
            move |= (king_pos >> 9) & NOT_H_FILE
            table.append(move)
        return table

    def get_valid_knight_moves(self, knight_pos, friendly_pos):
        return self.knight_moves[knight_pos] &~ friendly_pos
    
    def get_valid_king_moves(self, king_pos, friendly_pos):
        return self.king_moves[king_pos] &~ friendly_pos

    def get_valid_pawn_moves(self, pawn_pos, occupied_pos, is_white):
        move = 0
        if is_white:
            #pawns first move can be 2 steps forward
            one_step = (pawn_pos << 8) & ~occupied_pos
            move |= one_step
            if one_step and (pawn_pos & RANK_2):
                move |= (pawn_pos << 16) & ~occupied_pos
        #black pawns first move can be 2 steps forward
        else:
            one_step = (pawn_pos >> 8) & ~occupied_pos
            move |= one_step
            if one_step and (pawn_pos & RANK_7):
                move |= (pawn_pos >> 16) & ~occupied_pos 
        return move
    
    def get_valid_pawn_attacks(self, pawn_pos, enemy_pos, is_white):
        move = 0
        if is_white:
            move |= (pawn_pos << 9) & enemy_pos & NOT_A_FILE
            move |= (pawn_pos << 7) & enemy_pos & NOT_H_FILE
        else:
            move |= (pawn_pos >> 7) & enemy_pos & NOT_A_FILE
            move |= (pawn_pos >> 9) & enemy_pos & NOT_H_FILE
        return move

    #Using Kogge's method to generate sliding piece moves
    def check_north(self, moving_piece_pos, occupied_pos):
        propogate = ~occupied_pos
        gen = moving_piece_pos

        gen |= (gen << 8) & propogate
        propogate2 = propogate & (propogate << 8)
        gen |= (gen << 16) & propogate2
        propogate4 = propogate2 & (propogate2 << 16)
        gen |= (gen << 32) & propogate4

        return (gen & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF
    
    def check_south(self, moving_piece_pos, occupied_pos):
        propogate = ~occupied_pos
        gen = moving_piece_pos

        gen |= (gen >> 8) & propogate
        propogate2 = propogate & (propogate >> 8)
        gen |= (gen >> 16) & propogate2
        propogate4 = propogate2 & (propogate2 >> 16)
        gen |= (gen >> 32) & propogate4

        return (gen & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF

    def check_east(self, moving_piece_pos, occupied_pos):
        propogate = ~occupied_pos & NOT_H_FILE
        gen = moving_piece_pos

        gen |= (gen << 1) & propogate
        propogate2 = propogate & (propogate << 1)
        gen |= (gen << 2) & propogate2
        propogate4 = propogate2 & (propogate2 << 2)
        gen |= (gen << 4) & propogate4

        return (gen & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF
    
    def check_west(self, moving_piece_pos, occupied_pos):
        propogate = ~occupied_pos & NOT_A_FILE
        gen = moving_piece_pos

        gen |= (gen >> 1) & propogate
        propogate2 = propogate & (propogate >> 1)
        gen |= (gen >> 2) & propogate2
        propogate4 = propogate2 & (propogate2 >> 2)
        gen |= (gen >> 4) & propogate4

        return (gen & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF

    def check_north_east(self, moving_piece_pos, occupied_pos):
        propogate = ~occupied_pos & NOT_A_FILE
        gen = moving_piece_pos

        gen |= (gen << 9) & propogate
        propogate2 = propogate & (propogate << 9)
        gen |= (gen << 18) & propogate2
        propogate4 = propogate2 & (propogate2 << 18)
        gen |= (gen << 36) & propogate4

        return (gen & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF
    
    def check_north_west(self, moving_piece_pos, occupied_pos):
        propogate = ~occupied_pos & NOT_H_FILE
        gen = moving_piece_pos

        gen |= (gen << 7) & propogate
        propogate2 = propogate & (propogate << 7)
        gen |= (gen << 14) & propogate2
        propogate4 = propogate2 & (propogate2 << 14)
        gen |= (gen << 28) & propogate4

        return (gen & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF
    
    def check_south_east(self, moving_piece_pos, occupied_pos):
        propogate = ~occupied_pos & NOT_A_FILE
        gen = moving_piece_pos

        gen |= (gen >> 7) & propogate
        propogate2 = propogate & (propogate >> 7)
        gen |= (gen >> 14) & propogate2
        propogate4 = propogate2 & (propogate2 >> 14)
        gen |= (gen >> 28) & propogate4

        return (gen & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF
    
    def check_south_west(self, moving_piece_pos, occupied_pos):
        propogate = ~occupied_pos & NOT_H_FILE
        gen = moving_piece_pos

        gen |= (gen >> 9) & propogate
        propogate2 = propogate & (propogate >> 9)
        gen |= (gen >> 18) & propogate2
        propogate4 = propogate2 & (propogate2 >> 18)
        gen |= (gen >> 36) & propogate4

        return (gen & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF
    
    def get_valid_rook_moves(self, rook_pos, occupied_pos, friendly_pos):
        return (self.check_north(rook_pos, occupied_pos) | 
                self.check_south(rook_pos, occupied_pos) | 
                self.check_east(rook_pos, occupied_pos) | 
                self.check_west(rook_pos, occupied_pos)) &~ friendly_pos

    def get_valid_bishop_moves(self, bishop_pos, occupied_pos, friendly_pos):
        return (self.check_north_east(bishop_pos, occupied_pos) | 
                self.check_north_west(bishop_pos, occupied_pos) | 
                self.check_south_east(bishop_pos, occupied_pos) | 
                self.check_south_west(bishop_pos, occupied_pos)) &~ friendly_pos
    
    def get_valid_queen_moves(self, queen_pos, occupied_pos, friendly_pos):
        return (self.get_valid_bishop_moves(queen_pos, occupied_pos, friendly_pos) | 
                self.get_valid_rook_moves(queen_pos, occupied_pos, friendly_pos))

        