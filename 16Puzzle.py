import numpy

def init_puzzle(puzzle_board):
    pass

def solve_puzzle(puzzle_board, cur_score, goal = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]], iter = 0):
    while iter <= 10000:
        #buat clone board
        temp_board = copy_board(puzzle_board)
        #cek posisi tukar
        row, col = find_blank(temp_board)
        #batas tukar
        swap_board = []
        if (row-1) >= 0:
            temp1_board = swap(temp_board,row, col, row-1,col)
            swap_board.append(temp1_board)
        if (row+1) <= 3:
            temp2_board = swap(temp_board,row, col, row+1,col)
            swap_board.append(temp2_board)
        if (col-1) >= 0:
            temp3_board = swap(temp_board, row, col, row, col-1)
            swap_board.append(temp3_board)
        if (col+1) <= 3:
            temp4_board = swap(temp_board, row, col, row, col+1)
            swap_board.append(temp4_board)
        #best score heuristic (percent)
        score = []
        for i in swap_board:
            score.append(heuristic(i, goal))
        
        #cek max score
        change = False
        for i in range(len(score)):
            if score[i] > cur_score:
                cur_score = score[i]
                puzzle_board = swap_board[i]
                change = True
        
        if cur_score == 100.0:
            print("Solution Found")
            print(puzzle_board)
            return

        #batas minimum
        if not change:
            print("mencapai batas minimum")
            return

    print("Solution not found")

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
    temp1_board = copy_board(puzzle_board)
    temp1_board[row][col], temp1_board[row_swap][col_swap] = temp1_board[row_swap][col_swap], temp1_board[row][col]
    return temp1_board
    

puzzle_board = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[0,13,14,15]]

# puzzle_board = init_puzzle(puzzle_board)
solve_puzzle(puzzle_board, 81.25)