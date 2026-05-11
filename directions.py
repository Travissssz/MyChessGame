from constant import NOT_A_FILE, NOT_H_FILE

class Direction:
    def __init__(self):
        self = self 
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
    

