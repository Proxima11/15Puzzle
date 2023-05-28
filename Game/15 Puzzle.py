import pygame
import random
import time
import numpy


pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("15 PUZZLE")

tileImage = []
board = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]]
movement = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]

# menu variables
index1 = random.randint(0,15)
index2 = random.randint(0,15)

while index1 == index2:
    index2 = random.randint(0,15)

expand = True
count = 0
scaleX = 0
scaleY = 0

# game variables
mouse_x = 0
mouse_y = 0
delay = 0.3
last = 0

hoverSolve = False
hoverReset = False
hoverShuffle = False

# mode variables
mainMenu = True
startGame = False
gameover = False

# menu bg
menuBg = pygame.image.load("mainMenuBg.png").convert_alpha()
gameTitle = pygame.image.load("gameTitle.png").convert_alpha()
startButton = pygame.image.load("startButton.png").convert_alpha()

# tile images
full = pygame.image.load("full.png").convert_alpha() #isi path sendiri
for i in range (1,17):
    tileImage.append(pygame.image.load(f"tile{i}.png").convert_alpha()) #isi path sendiri

# ingame images
inGameBg = pygame.image.load("backgroundGame.png").convert_alpha()
header = pygame.image.load("headerGame.png").convert_alpha()
solveUnhover = pygame.image.load("solveUnhover.png").convert_alpha()
solveHover = pygame.image.load("solveHover.png").convert_alpha()
resetUnhover = pygame.image.load("resetUnhover.png").convert_alpha()
resetHover = pygame.image.load("resetHover.png").convert_alpha()
shuffleUnhover = pygame.image.load("shuffleUnhover.png").convert_alpha()
shuffleHover = pygame.image.load("shuffleHover.png").convert_alpha()

def drawMenu():
    screen.blit(menuBg, (0,0))
    animateTile()
    screen.blit(gameTitle, (0,0))
    animateText()

def animateTile():
    image1 = pygame.transform.rotate(tileImage[index1], 20)
    screen.blit(image1, (40,40))
    image2 = pygame.transform.rotate(tileImage[index2], -30)
    screen.blit(image2, (400,330))

def animateText():
    global expand, count, scaleX, scaleY

    if expand:
        scaleX+=0.9
        scaleY+=0.1
    else:
        scaleX-=0.9
        scaleY-=0.1
    
    count+=1

    if count==20:
        if expand: expand = False
        else : expand = True
        count = 0

    title = pygame.transform.scale(startButton, (startButton.get_width()+scaleX, startButton.get_height()+scaleY))
    screen.blit(title, (110 ,550))

# draw ingame backgrounds
def drawGame():
    screen.blit(inGameBg, (0,0))
    screen.blit(header, (0,0))

    drawIcons()

# draw ingame action icons
def drawIcons():
    if hoverSolve:
        screen.blit(solveHover, (337,48))
    else:
        screen.blit(solveUnhover, (337,50))

    if hoverReset:
        screen.blit(resetHover, (415,50))
    else:
        screen.blit(resetUnhover, (415,50))

    if hoverShuffle:
        screen.blit(shuffleHover, (499,50))
    else:
        screen.blit(shuffleUnhover, (499,50))

# draw tile
def drawTile():
    #screen.blit(full, (0,0))
    y = 175
    for i in range(0,4):
        x = 44
        for j in range (0,4):
            index = board[i][j]
            if index is not None:
                screen.blit(tileImage[index-1], (x,y))
            x+=133
        y+=130

# search empty and enable movement
def search():
    for i in range (0,4):
        for j in range (0,4):
            if board[i][j] == 16:
                return [i,j]

def enableMovement():

    # look for empty spot
    index = search()

    # reset movement
    for i in range(0,4):
        for j in range(0,4):
            movement[i][j]=None

    # enable right
    if index[1] > 0:
        movement[index[0]][index[1]-1] = "right"
    # enable left
    if index[1] < 3:
        movement[index[0]][index[1]+1] = "left"
    # enable down
    if index[0] > 0:
        movement[index[0]-1][index[1]] = "down"
    # enable up
    if index[0] < 3:
        movement[index[0]+1][index[1]] = "up"

# movement
def moveRight():
    
    # check movement availability
    right = False
    for i in range(0,4):
        for j in range(0,4):
            if movement[i][j] == "right":
                right = True
                break
    if right:
        index = search()
        currentX = 44 + ((index[1]-1) * 133)
        currentY = 175 + ((index[0]) * 130)
        tileNum = board[index[0]][index[1]-1]-1
        newX = currentX + 133
        while currentX != newX:
            #screen.blit(tileImage[15], (currentX,currentY))
            animationRight(tileNum, currentX, currentY)
            currentX+=0.5
        screen.blit(tileImage[15], (currentX-0.5, currentY))

        temp = board[index[0]][index[1]]
        board[index[0]][index[1]] = board[index[0]][index[1]-1]
        board[index[0]][index[1]-1] = temp

def animationRight(tileNum, x, y):
    screen.blit(tileImage[15], ((x-0.5),y))
    screen.blit(tileImage[tileNum], (x, y))
    pygame.display.update()

def moveLeft():

    # check movement availability
    left = False
    for i in range(0,4):
        for j in range(0,4):
            if movement[i][j] == "left":
                left = True
                break
    if left:
        index = search()

        currentX = 44 + ((index[1]+1) * 133)
        currentY = 175 + ((index[0]) * 130)
        tileNum = board[index[0]][index[1]+1]-1
        newX = currentX - 133
        while currentX != newX:
            animationLeft(tileNum, currentX, currentY)
            currentX-=0.5
        screen.blit(tileImage[15], (currentX+0.5, currentY))

        temp = board[index[0]][index[1]]
        board[index[0]][index[1]] = board[index[0]][index[1]+1]
        board[index[0]][index[1]+1] = temp

def animationLeft(tileNum, x, y):
    screen.blit(tileImage[15], ((x+0.5),y))
    screen.blit(tileImage[tileNum], (x, y))
    pygame.display.update()

def moveDown():

    # check movement availability
    down = False
    for i in range(0,4):
        for j in range(0,4):
            if movement[i][j] == "down":
                down = True
                break
    if down:
        index = search()

        currentX = 44 + ((index[1]) * 133)
        currentY = 175 + ((index[0]-1) * 130)
        tileNum = board[index[0]-1][index[1]]-1
        newY = currentY + 130
        while currentY != newY:
            animationDown(tileNum, currentX, currentY)
            currentY+=0.5
        screen.blit(tileImage[15], (currentX, currentY-0.5))

        temp = board[index[0]][index[1]]
        board[index[0]][index[1]] = board[index[0]-1][index[1]]
        board[index[0]-1][index[1]] = temp

def animationDown(tileNum, x, y):
    screen.blit(tileImage[15], (x,(y-0.5)))
    screen.blit(tileImage[tileNum], (x, y))
    pygame.display.update()

def moveUp():

    # check movement availability
    up = False
    for i in range(0,4):
        for j in range(0,4):
            if movement[i][j] == "up":
                up = True
                break
    if up:
        index = search()

        currentX = 44 + ((index[1]) * 133)
        currentY = 175 + ((index[0]+1) * 130)
        tileNum = board[index[0]+1][index[1]]-1
        newY = currentY - 130
        while currentY != newY:
            animationUp(tileNum, currentX, currentY)
            currentY-=0.5
        screen.blit(tileImage[15], (currentX, currentY+0.5))

        temp = board[index[0]][index[1]]
        board[index[0]][index[1]] = board[index[0]+1][index[1]]
        board[index[0]+1][index[1]] = temp

def animationUp(tileNum, x, y):
    screen.blit(tileImage[15], (x,(y+0.5)))
    screen.blit(tileImage[tileNum], (x, y))
    pygame.display.update()



# GENERATE BOARD =======================================================================================================
def count_inversions(arr):
    count = 0
    kosong = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j] and arr[i] != kosong and arr[j] != kosong:
                count += 1
    return count

# cek posisi kosong dari bawah
def findEmptyPosition(besar,arr):
    for i in range(besar-1,-1,-1):
        for j in range(besar-1,-1,-1):
            if(arr[i][j] == 0):
                return (besar-i)

def random_board(besar):
    arr=[]
    size=besar*besar
    while len(arr) <= size:
        if len(arr) == size:
            break
        r = random.randint(0,(size-1))
        if r not in arr:
            arr.append(r)
    arr=[[arr[0],arr[1],arr[2],arr[3]],[arr[4],arr[5],arr[6],arr[7]],[arr[8],arr[9],arr[10],arr[11]],[arr[12],arr[13],arr[14],arr[15]]]
    return arr

# syarat solved
# besar = genap
# blank di genap + inversi = ganjil
# blank di ganjil + inversi = genap
def generate_board(besar):
    arr=random_board(besar)
    bykinversi = count_inversions(arr)
    posisikosong = findEmptyPosition(besar,arr)
    #jika genap genap dan ganjil ganjil maka kerja terus, harus salah satu ganjil yg lain genap atau kebalikan
    while((posisikosong%2 == 0 and bykinversi%2 == 0) and (posisikosong%2 != 0 and bykinversi%2 != 0) ):
        arr=random_board(besar)
        bykinversi = count_inversions(arr)
        posisikosong=findEmptyPosition(besar,arr)
        if((posisikosong%2 == 0 and bykinversi%2 == 1) or (posisikosong%2 == 1 and bykinversi%2 == 0) ):
            break
    return arr
   

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
# AI SOLVER ============================================================================================================

def solve_puzzle(puzzle_board, cur_score, goal = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]], iter = 0, store_board = [], store_value = [], past_board = []):
    while iter <= 5000:
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
                if swap_board[i] not in past_board:
                    store_board.append(swap_board[i])
                    store_value.append(score[i])

        #cek max score
        change = False
        index = -1
        for i in range(len(score)):
            if score[i] > cur_score:
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
                if store_value[i] == cur_score:
                    temp.append(store_board[i])
                    temp_index.append(i)
                elif store_value[i] > second_best:
                    second_best = store_value[i]
            if len(temp) == 0:
                cur_score = second_best
                for i in range(len(store_value)):
                    if store_value[i] == second_best:
                        temp.append(store_board[i])
                        temp_index.append(i)
            
            if len(store_board) == 0:
                print("Solution not found (local maximum)")
                return
            
            #random (stochastic hill climbing)
            get_random = numpy.random.randint(abs(len(temp)))
            puzzle_board = copy_board(temp[get_random])
            store_board.pop(temp_index[get_random])
            store_value.pop(temp_index[get_random])
        # print("board = ", puzzle_board)
        # print("current score = ", cur_score)
        # print("iter = ",iter)
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

# # start game
# for i in range(20):
#     besarboard = 4
#     goal = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
#     puzzle_board = generate_board(besarboard)
#     # puzzle_board=[[5, 11, 8, 12], [3, 6, 13, 2], [4, 15, 7, 9], [14, 10, 0, 1]]
#     score = heuristic(puzzle_board, goal)
#     print("board awal : ", puzzle_board)
#     solve_puzzle(puzzle_board, score)

puzzle_board = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
puzzle_board = init_puzzle(puzzle_board)
score = heuristic(puzzle_board, [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])
print("board awal : ", puzzle_board)
board = puzzle_board
for i in range (0,4):
        for j in range (0,4):
            if board[i][j] == 0:
                board[i][j] = 16
# solve_puzzle(puzzle_board, score)

# hill climbing 
# A*

# A* = hill climbing tapi inefisien ;v




run = True

#game play
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
    cclock = clock.tick(FPS)

    if mainMenu:
        drawMenu()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if click[0] and mouse_x >= 0 and mouse_y >= 0:
            mainMenu = False
            startGame = True

    elif startGame:

        # time variables
        now = time.time()

        # draw bg and tiles
        drawGame()
        drawTile()
        
        # get keyboard input and enable movement
        key = pygame.key.get_pressed()
        enableMovement()

        if key[pygame.K_RIGHT] and ((now-last) > delay):
            last = now
            moveRight()
        elif key[pygame.K_LEFT] and ((now-last) > delay):
            last = now
            moveLeft()
        elif key[pygame.K_UP] and ((now-last) > delay):
            last = now
            moveUp()
        elif key[pygame.K_DOWN] and ((now-last) > delay):
            last = now
            moveDown()

        # get mouse input
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if (mouse_x >= 337 and mouse_x <= 337 + solveHover.get_width()) and (mouse_y >= 50 and mouse_y <= 50 + solveHover.get_height()):
            hoverSolve = True
        else:
            hoverSolve = False

        if (mouse_x >= 415 and mouse_x <= 415 + resetHover.get_width()) and (mouse_y >= 50 and mouse_y <= 50 + resetHover.get_height()):
            hoverReset = True
        else:
            hoverReset = False

        if (mouse_x >= 499 and mouse_x <= 499 + shuffleHover.get_width()) and (mouse_y >= 50 and mouse_y <= 50 + shuffleHover.get_height()):
            hoverShuffle = True
        else:
            hoverShuffle = False

        # enable button
        click = pygame.mouse.get_pressed()

        if click[0] and hoverSolve and ((now-last) > delay):
            last = now
            print("Solve")

        if click[0] and hoverReset and ((now-last) > delay):
            last = now
            print("Reset")
            
        if click[0] and hoverShuffle and ((now-last) > delay):
            last = now
            print("Shuffle")


    elif gameover:
        pass

    pygame.display.update()

pygame.quit()