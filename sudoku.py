from globals import easy_board, evil_board

# handles the inputs for the program and outputs the initial and solved states
# of the puzzle to the console  
def main():
    board_type = input("Which board would you like to solve (easy, evil, custom)? ")
    while (board_type != "easy" and board_type != "evil" and board_type != "custom"):
        board_type = input("Invalid board. Enter either easy, evil, or custom: ")
    if board_type == "easy":
        board = easy_board
    elif board_type == "evil":
        board = evil_board
    else:
        board = custom_board()
        if not valid_board(board):
            print("Unsolvable custom board")
            return
    print("Initial Board:")
    print_board(board)
    print("Solving...")
    solve(board)
    print("\nSolved Board:")
    print_board(board)

# helper for the inputs for a custom board
def custom_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    print("Enter 9 consecutive integers for each row. 0's represent blank squares (e.g., \"104006032\").")
    for i in range(1, 10):
        row = input(f"Row {i}: ")
        while (not row.isdigit() or len(row) != 9):
            if (not row.isdigit()):
                row = input(f"Invalid row (non-integer input). Row {i}: ")
            else:
                row = input(f"Invalid row (row length not 9). Row {i}: ")
        for j in range (0,9):
            board[i - 1][j] = int(row[j])
    return board

# determines if the given board is a valid board to solve
def valid_board(board):
    for i in range(9):
        row = {}
        column = {}
        box = {}
        for j in range(9):
            if board[i][j] in row and board[i][j] != 0:
                return False
            row[board[i][j]] = 1
            if board[j][i] in column and board[j][i] != 0:
                return False
            column[board[j][i]] = 1
            row_box = 3 * (i // 3) + j // 3
            column_box = 3 * (i % 3) + j % 3
            if board[row_box][column_box] in box and board[row_box][column_box] != 0:
                return False
            box[board[row_box][column_box]] = 1
    return True

# main runner method in the program
#   1. Finds the next empty square (if none, board is solved)
#   2. Finds a valid number for that square (if none, backtracks and sets past squares to new numbers)
#   3. Sets the valid number into the board
#   4. Repeat recursively to find all empty squares.
def solve(board):
    find = next_square(board)
    if not find:
        return True
    else:
        y, x = find

    # check all possible numbers
    for i in range(1,10):
        if valid_number(board, i, (y, x)):

            # set valid number if found
            board[y][x] = i
            
            # recursively attempt to implement new numbers
            if solve(board):
                return True
            board[y][x] = 0
    return False

# returns a pair of the index of the next empty square in the puzzle
# returns None if there is no more
def next_square(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None

# checks if the given number is valid for the given position
# returns True if so and False if not
def valid_number(board, num, pos):

    # check if num is already in the column
    for i in range(9):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
        
    # check if num is already in the row
    for i in range(9):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    # check if num is already in the box
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False
    return True

# prints the current state of the board
def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("---------------------")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("| ", end = "")
            if board[i][j] != 0:
                print(str(board[i][j]) + " ", end = "")
            else:
                print("_ ", end = "")
            if j == 8:
                print("")

if __name__ == "__main__":
    main()