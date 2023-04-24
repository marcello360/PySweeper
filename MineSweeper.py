import math
import random
import os

#Main class to hold all of the game data
class GameBoard:
    def __init__ (self, size):
        self.size = size
        self.mines = math.ceil((size * size) * .15)
        self.board = [[0 for a in range(size)] for b in range(size)]
        self.setMines()
        self.hideMines()
        self.status = 1

    #Translate function to assign characters to held values for each cell
    def symbol(self, x):
        if x == -1:
            return 'X'
        if x == 0:
            return 'O'
        if x > 108:
            return 'F'
        if x > 0 and x < 9:
            return str(x)
        else:
            return '_'
        
    #Function to display the game board
    def display(self):

        #Adds a numerical header row
        header = '  '
        for x in range(1, self.size+1):
            header = header + ' ' + str(x)
        print(header)
        print('  ' + ' _' * (self.size))
        
        #Nested for loop to create rest of the rows
        for x in range(1, self.size+1):

            #Adds a y axis to the begining of each row
            print('\r' + str(x) + ' ', end='', flush=True)

            #Calls the symbol function to fill each row with the correct symbols
            for y in range(1, self.size+1):
                print('\r' + '|' + self.symbol(self.board[x-1][y-1]), end='', flush=True)
            print('|')

    #Function to set mines to board
    def setMines(self):
        
        #Calls rng function to recieve an array of unique coordinates
        index = self.getRandom((self.size * self.size), self.mines)
        
        #places a mine at each coordinate and adds numbers around it
        for i in index:
            self.board[int(i / self.size)][(i % self.size)] = -1
            self.setNumbers(int(i / self.size), (i % self.size))

    #Function to create a random index list for the mines
    def getRandom(self, area, mines):
        out = []

        #Creates an array of usable cells to choose from
        remains = [i for i in range(area)]
        while mines > 0:

            #Generates a random index and checks if it's been used yet
            r = random.randint(0, len(remains) - 1)
            if r not in remains:
                continue

            #adds new number to the output and removes it from the usable list
            out.append(r)
            del remains[r]
            mines -= 1
        return out

    #Function to hide cells from the player
    def hideMines(self):
        for m in range(self.size):
            for n in range(self.size):
                self.board[m][n] += 100

    def reveal(self, row, col):
        if self.board[row-1][col-1] > 9:
            self.board[row-1][col-1] -= 100
            if self.board[row-1][col-1] == 0:
                for r in range(row - 1, row + 2):
                    for c in range(col - 1, col + 2):
                        if self.isValid(r-1, c-1):
                            self.reveal(r, c)

    def flag(self, row, col):
        if self.board[row-1][col-1] > 9 and self.board[row-1][col-1] < 109:
            self.board[row-1][col-1] += 100
        elif self.board[row-1][col-1] > 108:
            self.board[row-1][col-1] -= 100

    #Selects range of cells around chosen location
    def setNumbers(self, row, col):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):

                #checks if cell exists/ has a mine in it
                if self.isValid(r, c) and not self.hasMine(r, c):

                    #increases the cell value by 1
                    self.board[r][c] += 1

    #Checks if the cell contains a mine
    def hasMine(self, row, col):
        if self.board[row][col] == -1:
            return True
        else:
            return False

    #Checks if the cell is on the table
    def isValid(self, row, col):
        return row >= 0 and row < self.size and col >= 0 and col < self.size

    def countOpen(self):
        count = 0
        for m in range(self.size):
            for n in range(self.size):
                if self.board[m][n] < 9:
                    count = count + 1
        return count

    def changeStatus(self):
        for m in range(self.size):
            for n in range(self.size):
                if self.board[m][n] == -1:
                    self.status = 0; #Game lost
                elif self.countOpen() == ((self.size * self.size) - self.mines):
                    self.status = 2; #Game won

    def revealMines(self):
        for m in range(self.size):
            for n in range(self.size):
                if self.board[m][n] == 99:
                    self.board[m][n] = -1
                
    
def game():
    size = int(input('Enter width/length of game board: '))
    while size > 9 or size < 1:
        size = int(input('Please enter a number between 1 and 9: '))
    currentGame = GameBoard(size)
    error = None
    while currentGame.status == 1:
        currentGame.display()
        if error != None:
            print(error)
        choice = prompt().split(' ')
        choice.append("X")
        if len(choice) < 3:
            error = ('\nERROR! Please enter two coordinates!')
            continue
        try:
            row = int(choice[0])
            col = int(choice[1])
        except:
            error = ('\nERROR! Please enter numerical coordinates!')
            continue
        if row < 1 or row > size or col < 1 or col > size:
            error = ('\nERROR! Please enter valid coordinates in range!')
            continue
        if choice[2] == 'f':
            currentGame.flag(row, col)
        else:
            currentGame.reveal(row, col)
        currentGame.changeStatus()
        error = None
    if currentGame.status == 2:
        currentGame.display()
        print('\nCongratulations! YOU WIN!')
    else:
        currentGame.revealMines()
        currentGame.display()
        print('\nYou lost... Better luck next time!')

def prompt():
    output = '\nEnter row and col to open.\nEnter row and col followed by "f" to flag.\n'
    return input(output)

#Runs the game
game()
    
