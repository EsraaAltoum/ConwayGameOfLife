
import random


class GameBoard:
  def __init__(self, height=5, width=5):
    #definiing the gameboard
    self.width= width
    self.height= height
    #this is the gameboard we will initialize it as a grid of zeros (all dead)
    self.board = []

    #start the game with a randomized grid
  def randomStart(self):
    #each cell is assigned dead or alive using a the random.randint() function
    self.board = [[random.randint(0,1) for i in range(self.width)] for j in range(self.height)]

    #start the game with a specific grid (as a .txt file)
  def specificStart(self, gridFile):
    #open file and read rows
    with open(gridFile) as fp:
        lines = fp.readlines()
        self.height = int(lines.pop(0))
        self.width = int(lines.pop(0))

        if len(lines) != self.height:
            #error height mismatch
            pass

        line_count = 0
        for line in lines:
            row = [int(i) for i in line.strip()]
            if len(row) != self.width:
                #error width mismatch
                pass

            self.board.append(row)
            line_count += 1

        
    #create the state of the board at the next tick from the state at the current tick.
  def nextTick(self):
    next_board = [[0 for i in range(self.width)] for i in range(self.height)]
    #access cell
    for r in range(self.height):
      # print()
      # self.printBoard()
      # print()
      for c in range(self.width):
        life_count = 0
        #accounting for edge cases 
        isTop = r == 0
        isBottom = r == self.height-1
        isLeft = c == 0
        isRight = c == self.width-1
        #topleftcorner
        if isTop and isLeft:
          life_count = self.board[r+1][c] + self.board[r][c+1] + self.board[r+1][c+1]
        
        #toprightcorner
        elif isTop and isRight:
          life_count = self.board[r+1][c] + self.board[r][c-1] + self.board[r+1][c-1]
        
        #topedge
        elif isTop and not isLeft and not isRight:
          life_count = self.board[r][c-1] + self.board[r][c+1] + sum(self.board[r+1][c-1:c+2])
        
        #bottomleftcorner
        elif isBottom and isLeft:
          life_count = self.board[r-1][c] + self.board[r][c+1] + self.board[r-1][c+1]
        
        #bottomrightcorner
        elif isBottom and isRight:
          life_count = self.board[r-1][c] + self.board[r][c-1] + self.board[r-1][c-1]

        #bottomedge
        elif isBottom and not isLeft and not isRight:
          life_count = self.board[r][c-1] + self.board[r][c+1] + sum(self.board[r-1][c-1:c+2])

        elif isLeft and not isTop and not isBottom:
          life_count = sum(self.board[r-1][c:c+2]) + sum(self.board[r+1][c:c+2]) + self.board[r][c+1]
        
        elif isRight and not isTop and not isBottom:
          life_count = sum(self.board[r-1][c-1:c+1]) + sum(self.board[r+1][c-1:c+1]) + self.board[r][c-1]

        #normal
        else:
          life_count = sum(self.board[r-1][c-1:c+2]) + sum(self.board[r+1][c-1:c+2]) + self.board[r][c-1] + self.board[r][c+1]
        # if r == 0:
        #   print(r, c, "\n", isTop, isBottom, isLeft, isRight, life_count)
        #checking against rules
        if self.board[r][c] and life_count < 2:
            next_board[r][c] = 0
        
        if self.board[r][c] and 2 <= life_count <= 3:
            next_board[r][c] = 1
        
        if self.board[r][c] and life_count > 3:
            next_board[r][c] = 0
            
        if not self.board[r][c] and life_count == 3:
            next_board[r][c] = 1

    self.board = next_board
    
    
  def printBoard(self):
      for i in range(self.height):
        for j in range(self.width):
            print(self.board[i][j], end="")
        print()
      print()
  
	#main function for running the game
def main():
  print("Welcome to Conway's Game of Life, select one of the two following options\n1. Random Start\n2.Specific start\n")

  game_type = input("Enter you selection: ")

  if int(game_type) == 1:
    h = input("enter board height: ")
    w = input("enter board width: ")
    gb = GameBoard(int(h), int(w))
    gb.randomStart()

  elif int(game_type) == 2:
    fpath = input("please enter path to the file containing the specific grid: ")
    gb = GameBoard()
    gb.specificStart(fpath)

  gb.printBoard()

  while True:
    next_c = input("press X to exit, press enter to see the next generation: ")
    if next_c == 'X' or next_c == 'x':
      break
    gb.nextTick()
    gb.printBoard()

    
###############################
main()
    