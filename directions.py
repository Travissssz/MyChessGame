from constant import NOT_A_FILE, NOT_H_FILE

class Direction:
    def __init__(self):
        pass 
    
    def check_north(self, moving_piece_pos, occupied_pos):
        prop = ~occupied_pos
        gen = moving_piece_pos
        gen |= (gen << 8) & prop
        prop &= (prop << 8)  
        gen |= (gen << 16) & prop
        prop &= (prop << 16)
        gen |= (gen << 32) & prop
        # Extra shift North to include the blocking piece (capture square)
        full_ray = gen | (gen << 8)
        return (full_ray & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF
    
    def check_south(self, moving_piece_pos, occupied_pos):
        prop = ~occupied_pos
        gen = moving_piece_pos
        gen |= (gen >> 8) & prop
        prop &= (prop >> 8)
        gen |= (gen >> 16) & prop
        prop &= (prop >> 16)
        gen |= (gen >> 32) & prop
        # Extra shift South to include the blocking piece
        full_ray = gen | (gen >> 8)
        return (full_ray & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF

    def check_east(self, moving_piece_pos, occupied_pos):
        # East is right (<< 1). Mask NOT_H_FILE to prevent wrapping to A-file.
        prop = ~occupied_pos & NOT_A_FILE
        gen = moving_piece_pos
        gen |= (gen << 1) & prop
        prop &= (prop << 1)
        gen |= (gen << 2) & prop
        prop &= (prop << 2)
        gen |= (gen << 4) & prop
        # Extra shift East (with boundary check)
        full_ray = gen | ((gen & NOT_H_FILE) << 1)
        return (full_ray & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF
    
    def check_west(self, moving_piece_pos, occupied_pos):
        # West is left (>> 1). Mask NOT_A_FILE to prevent wrapping to H-file.
        prop = ~occupied_pos & NOT_A_FILE
        gen = moving_piece_pos
        gen |= (gen >> 1) & prop
        prop &= (prop >> 1)
        gen |= (gen >> 2) & prop
        prop &= (prop >> 2)
        gen |= (gen >> 4) & prop
        # Extra shift West (with boundary check)
        full_ray = gen | ((gen & NOT_A_FILE) >> 1)
        return (full_ray & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF
    # --- DIAGONAL DIRECTIONS ---

    def check_north_east(self, moving_piece_pos, occupied_pos):
        # North-East is Up-Right (<< 9). Mask NOT_H_FILE.
        prop = ~occupied_pos & NOT_H_FILE
        gen = moving_piece_pos
        gen |= (gen << 9) & prop
        prop &= (prop << 9)
        gen |= (gen << 18) & prop
        prop &= (prop << 18)
        gen |= (gen << 36) & prop
        full_ray = gen | ((gen & NOT_H_FILE) << 9)
        return (full_ray & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF
    
    def check_north_west(self, moving_piece_pos, occupied_pos):
        # North-West is Up-Left (<< 7). Mask NOT_A_FILE.
        prop = ~occupied_pos & NOT_A_FILE
        gen = moving_piece_pos
        gen |= (gen << 7) & prop
        prop &= (prop << 7)
        gen |= (gen << 14) & prop
        prop &= (prop << 14)
        gen |= (gen << 28) & prop
        full_ray = gen | ((gen & NOT_A_FILE) << 7)
        return (full_ray & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF
    
    def check_south_east(self, moving_piece_pos, occupied_pos):
        # South-East is Down-Right (>> 7). Mask NOT_H_FILE.
        prop = ~occupied_pos & NOT_H_FILE
        gen = moving_piece_pos
        gen |= (gen >> 7) & prop
        prop &= (prop >> 7)
        gen |= (gen >> 14) & prop
        prop &= (prop >> 14)
        gen |= (gen >> 28) & prop
        full_ray = gen | ((gen & NOT_H_FILE) >> 7)
        return (full_ray & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF
    
    def check_south_west(self, moving_piece_pos, occupied_pos):
        # South-West is Down-Left (>> 9). Mask NOT_A_FILE.
        prop = ~occupied_pos & NOT_A_FILE
        gen = moving_piece_pos
        gen |= (gen >> 9) & prop
        prop &= (prop >> 9)
        gen |= (gen >> 18) & prop
        prop &= (prop >> 18)
        gen |= (gen >> 36) & prop
        full_ray = gen | ((gen & NOT_A_FILE) >> 9)
        return (full_ray & ~moving_piece_pos) & 0xFFFFFFFFFFFFFFFF