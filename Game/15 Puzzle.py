import pygame
import time

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

delay = 0.3
last = 0

# tile images
full = pygame.image.load("16Puzzle/16Puzzle/Game/full.png").convert_alpha() #isi path sendiri
for i in range (1,17):
    tileImage.append(pygame.image.load(f"16Puzzle/16Puzzle/Game/tile{i}.png").convert_alpha()) #isi path sendiri

    

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

run = True
menu = True
play = False
gameover = False

#game play
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
    cclock = clock.tick(FPS)

    drawTile()
    enableMovement()

    key = pygame.key.get_pressed()

    now = time.time()

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
    

    pygame.display.update()

pygame.quit()