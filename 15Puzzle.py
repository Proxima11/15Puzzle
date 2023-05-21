import numpy

def init_puzzle(puzzle_board):
    b = 3
    k = 3
    for i in range(100):
        angka = numpy.random.randint(0,99)
        if angka < 25:
            if b > 0:
                puzzle_board[b][k] = puzzle_board[b-1][k]
                b-=1
                puzzle_board[b][k] = 0
        elif angka < 50:
            if b < 3:
                puzzle_board[b][k] = puzzle_board[b+1][k]
                b+=1
                puzzle_board[b][k] = 0
        elif angka < 75:
            if k > 0:
                puzzle_board[b][k] = puzzle_board[b][k-1]
                k-=1
                puzzle_board[b][k] = 0
        elif angka < 100:
            if k < 3:
                puzzle_board[b][k] = puzzle_board[b][k+1]
                k+=1
                puzzle_board[b][k] = 0
    return puzzle_board

def solve_puzzle(puzzle_board, cur_score, goal = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]], iter = 0, store_board = [], store_value = [], past_board = []):
    while iter <= 1000:
        #buat clone board
        temp_board = copy_board(puzzle_board)
        past_board.append(copy_board(temp_board))
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
        
        #simpan board dan score
        for i in range(len(score)):
                store_board.append(swap_board[i])
                store_value.append(score[i])

        #cek max score
        change = False
        index = -1
        for i in range(len(score)):
            if score[i] > cur_score and swap_board[i] not in past_board:
                cur_score = score[i]
                puzzle_board = swap_board[i]
                change = True
                index = i
        
        #cek selesai
        if cur_score == 16:
            print("Solution Found")
            print("board akhir : ", puzzle_board)
            return
        
        #keluarkan isi board sekarang
        if change:
            store_board.pop(len(store_board)-len(swap_board)+index)
            store_value.pop(len(store_value)-len(score)+index)

        #local maximum
        if not change:
            temp = [] 
            temp_index = []
            #cari nilai sama
            second_best = -1
            for i in range(len(store_value)):
                if store_value[i] == cur_score and store_board[i] not in past_board:
                    temp.append(store_board[i])
                    temp_index.append(i)
                elif store_value[i] > second_best and store_board[i] not in past_board:
                    second_best = store_value[i]
            if len(temp) == 0:
                cur_score = second_best
                for i in range(len(store_value)):
                    if store_value[i] == second_best and store_board[i] not in past_board:
                        temp.append(store_board[i])
                        temp_index.append(i)
            
            if len(store_board) == 0:
                print("Solution not found (local maximum)")
                return
            
            #random (stochastic hill climbing)
            get_random = numpy.random.randint(len(temp))
            puzzle_board = copy_board(temp[get_random])
            store_board.pop(temp_index[get_random])
            store_value.pop(temp_index[get_random])
        print("board = ", puzzle_board)
        print("current score = ", cur_score)
        iter += 1
    print("Solution not found (iter max)")

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
    return matched
            

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
    

puzzle_board = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]


puzzle_board = init_puzzle(puzzle_board)
score = heuristic(puzzle_board, [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])
print("board awal : ", puzzle_board)
solve_puzzle(puzzle_board, score)