#WhileH
#-----------------------------------------
from Tkinter import *
import random

def aiMove():
    boardReset(canvas.data.snake,canvas.data.snakeSize,canvas.data.board)
    bestMove = canvas.data.ERROR
    if(canvas.data.isGameOver == False):
        if(boardRefresh(canvas.data.food,canvas.data.snake,canvas.data.board)):
            bestMove = getSafeMove()
        else:
            bestMove = followTail()
        if(bestMove == canvas.data.ERROR):
            bestMove = anyMove()
        if(bestMove != canvas.data.ERROR):
            makeMove(bestMove)
        else: gameOver()
        if (canvas.data.snakeSize == ((canvas.data.ROW-2)*(canvas.data.COL-2)-1)):
            win()
        redrawAll()
    delay = 1
    canvas.after(delay,aiMove);
#################################################################################################################
def anyMove():
    bestMove = canvas.data.ERROR
    minimum = canvas.data.SNAKE
    boardReset(canvas.data.snake,canvas.data.snakeSize,canvas.data.board)
    boardRefresh(canvas.data.food,canvas.data.snake,canvas.data.board)
    for i in xrange(4):
        if(isMovePossible(canvas.data.snake[canvas.data.HEAD],canvas.data.move[i]) and minimum>canvas.data.board[canvas.data.snake[canvas.data.HEAD]+canvas.data.move[i]]):
            minimum = canvas.data.board[canvas.data.snake[canvas.data.HEAD]+canvas.data.move[i]]
            bestMove = canvas.data.move[i]
    return bestMove

def testMove():
    kagebunshinnojyutsu()
    boardReset(canvas.data.vsnake,canvas.data.vsnakeSize,canvas.data.vboard)
    flag = False
    while not flag:
        boardRefresh(canvas.data.food,canvas.data.vsnake,canvas.data.vboard)
        move = chooseShortestSafeMove(canvas.data.vsnake,canvas.data.vboard)
        shiftArray(canvas.data.vsnake,canvas.data.vsnakeSize)
        canvas.data.vsnake[canvas.data.HEAD] +=move
        if(canvas.data.vsnake[canvas.data.HEAD] == canvas.data.food):
            canvas.data.vsnakeSize+=1
            boardReset(canvas.data.vsnake,canvas.data.vsnakeSize,canvas.data.vboard)
            canvas.data.vboard[canvas.data.food] = canvas.data.SNAKE
            flag = True
        else:
            canvas.data.board[canvas.data.snake[canvas.data.HEAD]] = canvas.data.SNAKE
            canvas.data.board[canvas.data.snake[canvas.data.snakeSize]] = canvas.data.UNDEFINED

def getSafeMove():
    safeMove = canvas.data.ERROR
    testMove()
    if(canFollowTail()):
        safeMove = chooseShortestSafeMove(canvas.data.snake,canvas.data.board)
    else:
        safeMove = followTail()
    return safeMove

def kagebunshinnojyutsu():
    canvas.data.vsnakeSize = canvas.data.snakeSize
    canvas.data.vsnake = canvas.data.snake[:]
    boardReset(canvas.data.vsnake,canvas.data.vsnakeSize,canvas.data.vboard)

def canFollowTail():
    canvas.data.vboard[canvas.data.vsnake[canvas.data.vsnakeSize-1]] = canvas.data.FOOD
    canvas.data.vboard[canvas.data.food] = canvas.data.SNAKE
    result = boardRefresh(canvas.data.vsnake[canvas.data.vsnakeSize-1],canvas.data.vsnake,canvas.data.vboard)
    for i in xrange(4):
        if(isMovePossible(canvas.data.vsnake[canvas.data.HEAD],canvas.data.move[i]) and (canvas.data.vsnake[canvas.data.HEAD]+canvas.data.move[i] == canvas.data.vsnake[canvas.data.vsnakeSize-1]) and canvas.data.vsnakeSize>3):
            result = False
    return result

def followTail():
    kagebunshinnojyutsu()
    canvas.data.vboard[canvas.data.vsnake[canvas.data.vsnakeSize-1]] = canvas.data.FOOD
    canvas.data.vboard[canvas.data.food] = canvas.data.SNAKE
    boardRefresh(canvas.data.vsnake[canvas.data.vsnakeSize-1],canvas.data.vsnake,canvas.data.vboard)
    #canvas.data.vboard[canvas.data.vsnake[]canvas.data.vsnakeSize-1]] = canvas.data.SNAKE
    return chooseLongestSafeMove(canvas.data.vsnake,canvas.data.vboard)

def chooseShortestSafeMove(snake,board):
    bestMove = canvas.data.ERROR
    minimum = canvas.data.SNAKE
    for i in xrange(4):
        if(isMovePossible(snake[canvas.data.HEAD],canvas.data.move[i]) and minimum>board[snake[canvas.data.HEAD]+canvas.data.move[i]]):
            minimum = board[snake[canvas.data.HEAD]+canvas.data.move[i]]
            bestMove = canvas.data.move[i]
    return bestMove

def chooseLongestSafeMove(snake,board):
    bestMove = canvas.data.ERROR
    maximum = -1
    for i in xrange(4):
        if(isMovePossible(snake[canvas.data.HEAD],canvas.data.move[i]) and maximum<board[snake[canvas.data.HEAD]+canvas.data.move[i]] and board[snake[canvas.data.HEAD]+canvas.data.move[i]] < canvas.data.UNDEFINED):
            maximum = board[snake[canvas.data.HEAD]+canvas.data.move[i]]
            bestMove = canvas.data.move[i]
    return bestMove

def boardRefresh(food,snake,board):
    queue = []
    queue.append(food)
    inqueue = [0] * canvas.data.FIELDSIZE
    found = False
    while len(queue)!=0:
        idx = queue.pop(0)
        if inqueue[idx] == 1: continue
        inqueue[idx] = 1
        for i in xrange(4):
            if isMovePossible(idx, canvas.data.move[i]):
                if idx + canvas.data.move[i] == snake[canvas.data.HEAD]:
                    found = True
                if board[idx+canvas.data.move[i]] < canvas.data.SNAKE:
                    if board[idx+canvas.data.move[i]] > board[idx]+1:
                        board[idx+canvas.data.move[i]] = board[idx] + 1
                    if inqueue[idx+canvas.data.move[i]] == 0:
                        queue.append(idx+canvas.data.move[i])

    return found

def boardReset(snake,size,board):
    for i in xrange(canvas.data.FIELDSIZE):
        if (i == canvas.data.food):
            board[i] = canvas.data.FOOD
        elif (isCellFree(i,size,snake)):
            board[i] = canvas.data.UNDEFINED
        else:
            board[i] = canvas.data.SNAKE

def makeMove(move):
    shiftArray(canvas.data.snake,canvas.data.snakeSize)
    canvas.data.snake[canvas.data.HEAD] +=move
    if(canvas.data.snake[canvas.data.HEAD] == canvas.data.food):
        canvas.data.board[canvas.data.snake[canvas.data.HEAD]] = canvas.data.SNAKE
        canvas.data.snakeSize+=1
        canvas.data.score+=1
        if(canvas.data.snakeSize<canvas.data.FIELDSIZE): placeFood()
    else:
        canvas.data.board[canvas.data.snake[canvas.data.HEAD]] = canvas.data.SNAKE
        canvas.data.board[canvas.data.snake[canvas.data.snakeSize]] = canvas.data.UNDEFINED

def shiftArray(arr, size):
    for i in xrange(size, 0, -1):
        arr[i] = arr[i-1]

def isMovePossible(idx, move):
    flag = False
    if move == canvas.data.LEFT:
        flag = True if idx%canvas.data.WIDTH > 1 else False
    elif move == canvas.data.RIGHT:
        flag = True if idx%canvas.data.WIDTH < (canvas.data.WIDTH-2) else False
    elif move == canvas.data.UP:
        flag = True if idx > (2*canvas.data.WIDTH-1) else False
    elif move == canvas.data.DOWN:
        flag = True if idx < (canvas.data.FIELDSIZE-2*canvas.data.WIDTH) else False
    return flag

def isCellFree(i,size,snake):
    return not (i in snake[:size])

def placeFood():
    cellfree = False
    while not cellfree:
        w = random.randint(1,canvas.data.ROW-2)
        h = random.randint(1,canvas.data.COL-2)
        food = w*canvas.data.WIDTH+h
        cellfree = isCellFree(food,canvas.data.snakeSize,canvas.data.snake)
    canvas.data.food = food
    canvas.data.board[food] = canvas.data.FOOD

def keyPressed(event):
    if(event.char == 'r'):
        init()
    if(canvas.data.isGameOver == False):
        if (event.keysym == "Up"):
            makeMove(canvas.data.move[2])
        elif (event.keysym == "Down"):
            makeMove(canvas.data.move[3])
        elif (event.keysym == "Left"):
            makeMove(canvas.data.move[0])
        elif (event.keysym == "Right"):
            makeMove(canvas.data.move[1])
    redrawAll()

def redrawAll():
    canvas.delete(ALL)
    drawSnakeBoard()
    canvas.create_text(305,290,text = "score: "+str(canvas.data.score),font=("Helvetice",12,"bold"))
    if (canvas.data.isGameOver == True):
        canvas.create_text(305, 155, text="Game Over!", font=("Helvetica", 32, "bold"))
    if(canvas.data.isWin == True):
        canvas.create_text(305,155, text="Win!",font=("Helvetica",32,"bold"))

def drawSnakeBoard():
    snakeBoard = canvas.data.board
    for i in xrange(len(snakeBoard)):
        row = i/canvas.data.WIDTH
        col = i%canvas.data.WIDTH
        width = canvas.data.WIDTH
        if(row>0 and row<canvas.data.ROW-1 and col>0 and col<width-1):
            drawSnakeCell(snakeBoard,i)

def gameOver():
    canvas.data.isGameOver = True

def win():
    canvas.data.isWin = True

def init():
    canvas.data.isGameOver = False
    canvas.data.isWin = False
    # move the snake one step forward in the given direction.    canvas.data.snakeDcol = -1
    loadSnakeBoard()
    redrawAll()

def drawSnakeCell(snakeBoard,idx):
    margin = 5
    cellSize = 30
    row = idx/canvas.data.WIDTH
    col = idx%canvas.data.WIDTH
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize
    #snake = canvas.data.snake
    canvas.create_rectangle(left, top, right, bottom, fill="white")
    if (idx == canvas.data.snake[canvas.data.HEAD]):
        canvas.create_oval(left,top,right,bottom,fill="orange")
    elif (snakeBoard[idx] == canvas.data.SNAKE):
        # draw part of the snake body
        canvas.create_oval(left, top, right, bottom, fill="blue")
    elif(snakeBoard[idx] == canvas.data.FOOD):
        canvas.create_oval(left, top, right, bottom, fill="green")

def loadSnakeBoard():
    canvas.data.ROW = 10
    canvas.data.COL = 20
    canvas.data.FIELDSIZE = canvas.data.ROW*canvas.data.COL
    canvas.data.WIDTH = canvas.data.COL
    canvas.data.LEFT = -1
    canvas.data.RIGHT = 1
    canvas.data.UP = -canvas.data.WIDTH
    canvas.data.DOWN = canvas.data.WIDTH
    canvas.data.FOOD = 0
    canvas.data.ERROR = -1111
    canvas.data.move = [canvas.data.LEFT,canvas.data.RIGHT,canvas.data.UP,canvas.data.DOWN]
    canvas.data.UNDEFINED = (canvas.data.ROW+1)*(canvas.data.COL+1)
    canvas.data.HEAD = 0
    canvas.data.SNAKE = 2*canvas.data.UNDEFINED
    canvas.data.food = 3*canvas.data.WIDTH+3 #position
    canvas.data.score = 1
    canvas.data.snake = [0]*(canvas.data.FIELDSIZE+1)#snake position
    canvas.data.board = [0]*canvas.data.FIELDSIZE  #board
    canvas.data.snakeSize = 1
    canvas.data.snake[canvas.data.HEAD] = 1*canvas.data.WIDTH+1
    canvas.data.vsnake = [0]*(canvas.data.FIELDSIZE+1)#snake position
    canvas.data.vboard = [0]*canvas.data.FIELDSIZE  #board
    canvas.data.vsnakeSize = 1
    canvas.data.vsnake[canvas.data.HEAD] = 1*canvas.data.WIDTH+1
    boardReset(canvas.data.snake,canvas.data.snakeSize,canvas.data.board)
    boardReset(canvas.data.vsnake,canvas.data.vsnakeSize,canvas.data.vboard)

def run():
    # create the root and the canvas
    global canvas
    root = Tk()
    canvas = Canvas(root, width=30*(20)+5*2, height=30*(10)+5*2)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    init()
    # set up events
    #root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    aiMove()
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()
