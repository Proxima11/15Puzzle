import numpy

def init_puzzle(puzzle_board):
    pass

def solve_puzzle(puzzle_board, goal = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]):
    #buat clone board
    temp_board = copy_board(puzzle_board)
    #cek posisi tukar
    row, col = find_blank(temp_board)
    #batas tukar
    swap_board = []
    if (row-1) >= 0:
        swap_board.append(swap(temp_board, row, col, row-1, col))
    if (row+1) <= 3:
        swap_board.append(swap(temp_board, row, col, row+1, col))
    if (col-1) >= 0:
        swap_board.append(swap(temp_board, row, col, row, col-1))
    if (col+1) <= 3:
        swap_board.append(swap(temp_board, row, col, row, col+1))
    #best score heuristic (percent)
    print(swap_board)
    score = []
    for i in swap_board:
        score.append(heuristic(i, goal))
    print(score)
    #loop lagi

def find_blank(puzzle_board):
    for i in range(4):
        for j in range(4):
            if puzzle_board[i][j] == 0:
                return i,j
            
def heuristic(puzzle_board, goal):
    matched = 0
    for i in range(len(puzzle_board)):
        for j in range(len(puzzle_board[i])):
            if puzzle_board[i][j] == goal[i][j]:
                matched += 1
    return matched/16*100
            

def copy_board(puzzle_board):
    new_board = []
    for i in range(4):
        row = []
        for j in range(4):
            row.append(puzzle_board[i][j])
        new_board.append(row)
    return new_board

def swap(puzzle_board, row, col, row_swap, col_swap):
    puzzle_board[row][col], puzzle_board[row_swap][col_swap] = puzzle_board[row_swap][col_swap], puzzle_board[row][col]
    return puzzle_board
    

puzzle_board = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,0,15]]

# puzzle_board = init_puzzle(puzzle_board)
solve_puzzle(puzzle_board)