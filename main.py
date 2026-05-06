from board import Board

def main():
    chess_board = Board()
    
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
            print("\nExiting game.")
            break

if __name__ == "__main__":
    main()