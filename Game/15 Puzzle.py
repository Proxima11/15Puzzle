import pygame
import random
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