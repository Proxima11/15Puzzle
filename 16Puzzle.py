import numpy

def init_puzzle():
    pass

def solve_puzzle(puzzle_board):
    #buat clone board
    temp_board = copy_board(puzzle_board)
    #cek posisi tukar
    row, col = find_blank(temp_board)
    #batas tukar
    swap_board = []
    if (row-1) >= 0:
        swap_board.append(swap_board(puzzle_board, row, col, row-1, col))
    if (row+1) <= 2:
        swap_board.append(swap_board(puzzle_board, row, col, row+1, col))
    if (col-1) >= 0:
        swap_board.append(swap_board(puzzle_board, row, col, row, col-1))
    if (col+1) <= 2:
        swap_board.append(swap_board(puzzle_board, row, col, row, col+1))
    #best score heuristic
    
    #loop lagi

def find_blank(puzzle_board):
    for i in range(4):
        for j in range(4):
            if puzzle_board[i][j] == 0:
                return i,j
            
def heuristic(puzzle_board):
    pass

def copy_board(puzzle_board):
    new_board = []
    for i in range(4):
        row = []
        for j in range(4):
            row.append(puzzle_board[i][j])
        new_board.append(row)
    return new_board

def swap_board(puzzle_board, row, col, row_swap, col_swap):
    puzzle_board[row][col], puzzle_board[row_swap][col_swap] = puzzle_board[row_swap][col_swap], puzzle_board[row][col]
    return puzzle_board
    

puzzle_board = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]

puzzle_board = init_puzzle(puzzle_board)
solve_puzzle(puzzle_board)