from constant import *
from directions import Direction

class MoveGen:
    def __init__(self):
        self.directions = Direction()
        self.knight_moves = self._precompute_knights()
        self.king_moves = self._precompute_king()
    
    #for debug 
    def get_indices_from_bitboard(self, bitboard):
        return [i for i in range(64) if (bitboard & (1 << i)) != 0]
    
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
        print(f"Knight moves bitboard: {self.get_indices_from_bitboard(self.knight_moves[knight_pos] &~ friendly_pos)}")
        return self.knight_moves[knight_pos] &~ friendly_pos
    
    def get_valid_king_moves(self, king_pos, friendly_pos):
        print(f"King moves bitboard: {self.get_indices_from_bitboard(self.king_moves[king_pos] &~ friendly_pos)}")
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
                print("here2")
                move |= (pawn_pos >> 16) & ~occupied_pos 
        print(f"Pawn moves bitboard: {self.get_indices_from_bitboard(move)}")
        return move
    
    def get_valid_pawn_attacks(self, pawn_pos, enemy_pos, is_white):
        move = 0
        if is_white:
            move |= (pawn_pos << 9) & enemy_pos & NOT_A_FILE
            move |= (pawn_pos << 7) & enemy_pos & NOT_H_FILE
        else:
            move |= (pawn_pos >> 7) & enemy_pos & NOT_A_FILE
            move |= (pawn_pos >> 9) & enemy_pos & NOT_H_FILE
        print(f"Pawn attacks bitboard: {self.get_indices_from_bitboard(move)}")
        return move
    
    def get_valid_rook_moves(self, rook_pos, occupied_pos, friendly_pos):
        print(f"Rook moves bitboard: {self.get_indices_from_bitboard((self.directions.check_north(rook_pos, occupied_pos) | self.directions.check_south(rook_pos, occupied_pos) | self.directions.check_east(rook_pos, occupied_pos) | self.directions.check_west(rook_pos, occupied_pos)) &~ friendly_pos)}")
        return (self.directions.check_north(rook_pos, occupied_pos) | 
                self.directions.check_south(rook_pos, occupied_pos) | 
                self.directions.check_east(rook_pos, occupied_pos) | 
                self.directions.check_west(rook_pos, occupied_pos)) & ~friendly_pos

    def get_valid_bishop_moves(self, bishop_pos, occupied_pos, friendly_pos):
        print(f"Bishop moves bitboard: {self.get_indices_from_bitboard((self.directions.check_north_east(bishop_pos, occupied_pos) | self.directions.check_north_west(bishop_pos, occupied_pos) | self.directions.check_south_east(bishop_pos, occupied_pos) | self.directions.check_south_west(bishop_pos, occupied_pos)) &~ friendly_pos)}")
        return (self.directions.check_north_east(bishop_pos, occupied_pos) | 
                self.directions.check_north_west(bishop_pos, occupied_pos) | 
                self.directions.check_south_east(bishop_pos, occupied_pos) | 
                self.directions.check_south_west(bishop_pos, occupied_pos)) &~ friendly_pos
    
    def get_valid_queen_moves(self, queen_pos, occupied_pos, friendly_pos):
        print(f"Queen moves bitboard: {self.get_indices_from_bitboard((self.get_valid_bishop_moves(queen_pos, occupied_pos, friendly_pos) | self.get_valid_rook_moves(queen_pos, occupied_pos, friendly_pos)) &~ friendly_pos)}")
        return (self.get_valid_bishop_moves(queen_pos, occupied_pos, friendly_pos) | 
                self.get_valid_rook_moves(queen_pos, occupied_pos, friendly_pos))
