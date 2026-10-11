import numpy as np
import math

class board(object):
    def __init__( self, boardSize, result) :
        self.result = result
        self.boardSize = boardSize
        self.head = [[[y,x] for x in range(boardSize)] for y in range(boardSize)] # directed graph
        self.boardBlack = [[0 for x in range(boardSize)] for y in range(boardSize)] # state of board
        self.boardWhite = [[0 for x in range(boardSize)] for y in range(boardSize)] # state of board
        self.board =  [[0 for x in range(boardSize)] for y in range(boardSize)] # state of board
        self.history = [None, None, None] # short history
        self.groupLiberty = [[set() for x in range(boardSize)] for y in range(boardSize)]
        self.neighbor = [[set() for x in range(boardSize)] for y in range(boardSize)]
        self.group = [[[] for x in range(boardSize)] for y in range(boardSize)] # only track for sink
        self.color = 1
        self.last_capture = 0


    def undo(self):
        l = len(self.history)-1
        del self.history[l]
        self.board = self.history[l-1]

    def row(self, x):
        return math.floor(x/self.boardSize)

    def col(self, y):
        return y%self.boardSize

    # def push(self, y):
    #     [row, col] = y # directed graph pointing to next node, but everything already points to head
    #     next = self.head[row][col]
    #     while(next != self.head[next[0]][next[1]]):
    #         next = self.head[next[0]][next[1]]

        

    def join(self, x, y):
        # coordinate, coordinate
        
        if(x[0] * self.boardSize + x[1] > y[0] * self.boardSize + y[1]):
            temp = x
            x = y 
            y = temp # x less than y
        # self.push(y) #correct
        # self.push(x) #correct
        xhead = self.head[x[0]][x[1]] #correct
        yhead = self.head[y[0]][y[1]] #correct 

        for elem in self.groupLiberty[yhead[0]][yhead[1]]:
            self.groupLiberty[xhead[0]][xhead[1]].add(elem)

        for elem in self.neighbor[yhead[0]][yhead[1]]:
            self.neighbor[xhead[0]][xhead[1]].add(elem)

        self.groupLiberty[yhead[0]][yhead[1]] = set()
        self.neighbor[yhead[0]][yhead[1]] = set()


        for stone in self.group[yhead[0]][yhead[1]]:
            if(self.head[yhead[0]][yhead[1]] == yhead):
                continue
            self.head[stone[0]][stone[1]] = xhead
            self.group[xhead[0]][xhead[1]].append(stone)
            del stone
        self.group[yhead[0]][yhead[1]] = []
        self.head[yhead[0]][yhead[1]] = self.head[xhead[0]][xhead[1]]
        
        
        

        # self.liberties[math.floor(sink / self.boardSize)][sink % self.boardSize] += self.liberties[math.floor(self.head[y] / self.boardSize)][self.head[y] % self.boardSize]
        # self.liberties[row][col] = 0
        # for stone in self.group[self.head[y]]:
        #     if(self.head[y] == self.head[stone]):
        #         break
        #     self.head[stone] = self.head[y]
        #     self.group[sink].append(stone)
        # self.group[self.head[y]] = []
        # self.head[y] = self.head[x]

    def parseLocation(place):
        row = ord(place[0])-97
        col = ord(place[1])-97
        return [row,col]

    def isKo(self, pos):
        prev = self.history[0]
        curr = pos
        [row, col] = pos
        if(prev == None or curr == None):
            return False

        for i in range(5):
            for j in range(5):
                if(row+2-i < 0 or row+2+i >= self.boardSize):
                    continue
                if(row+2-j < 0 or row+2+j >= self.boardSize):
                    continue
                [x,y] = [row + 2 - i, col + 2 - j]
                if(not curr[x][y] == prev[x][y]):
                    return False
        return True
        
    def move(self, loc):
        # loc = self.parseLocation(place)
        row = loc[0]
        col = loc[1]
        
        self.board[row][col] = self.color
        if(self.color == 1):
            self.boardBlack[row][col] = 1
        else:
            self.boardWhite[row][col] = 1


        self.group[row][col].append([row,col]) #correct
        
        if(row > 0): #correct
            self.neighbor[row][col].add((row-1)*self.boardSize + col)
            if(self.board[row-1][col] == 0):
                self.groupLiberty[row-1][col].add((row-1)*self.boardSize + col)
            else:
                # self.push([row-1,col])
                [a,b] = self.head[row-1][col]
                self.groupLiberty[a][b].remove((row-1)*self.boardSize+col)
        if(row < self.boardSize-1):
            self.neighbor[row][col].add((row+1)*self.boardSize + col)
            if(self.board[row+1][col] == 0):
                self.groupLiberty[row+1][col].add((row+1)*self.boardSize + col)
            else:
                # self.push([row+1, col])
                [a,b] = self.head[row+1][col]
                self.groupLiberty[a][b].remove((row+1) * self.boardSize + col)
        if(col > 0):
            self.neighbor[row][col].add(row*self.boardSize + col-1)
            if(self.board[row][col-1] == 0):
                self.groupLiberty[row][col].add(row*self.boardSize + col-1)
            else:
                # self.push([row, col-1])
                [a,b] = self.head[row][col-1]
                self.groupLiberty[a][b].remove(row*self.boardSize + col-1)
        if(col < self.boardSize-1):
            self.neighbor[row][col].add(row*self.boardSize + col + 1)
            if(self.board[row][col+1] == 0):
                self.groupLiberty[row][col].add(row*self.boardSize + col+1)
            else:
                # self.push([row, col+1])
                [a,b] = self.head[row][col+1]
                self.groupLiberty[a][b].remove(row*self.boardSize +col+1)#correct

############# continue from here
        if(row > 0 and self.board[row][col] == self.board[row-1][col]):
            self.join([row,col], [row-1, col])
        if(row < self.boardSize-1 and self.board[row][col] == self.board[row+1][col]):
            self.join([row,col], [row+1, col])
        if(col > 0 and self.board[row][col] == self.board[row][col-1]):
            self.join([row,col], [row, col-1])
        if(col < self.boardSize-1 and self.board[row][col] == self.board[row][col+1]):
            self.join([row,col], [row, col+1]) #correct

        color = self.board[row][col]
        if(row > 0 and len(self.groupLiberty[row-1][col]) == 0):
            for stone in self.group[self.head[self.boardSize*(row-1) + col]]:
                self.board[math.floor(stone / self.boardSize)][stone % self.boardSize] = 0
                if(self.color == 1):
                    self.boardWhite[math.floor(stone / self.boardSize)][stone % self.boardSize] = 0
                else:
                    self.boardBlack[math.floor(stone / self.boardSize)][stone % self.boardSize] = 0
                self.head[stone] = stone
                [r1,c1] = [math.floor(stone / self.boardSize), stone % self.boardSize]
                if(r1 > 0):
                    if(self.board[r1-1][c1] == color):
                        update.add((r1-1)*self.boardSize + c1)
                
                if(r1 < self.boardSize -1):
                    if(self.board[r1+1][c1] == color):
                        update.add((r1+1)*self.boardSize + c1)
                
                if(c1 > 0):
                    if(self.board[r1][c1-1] == color):
                        update.add((r1)*self.boardSize + c1-1)
                
                if(c1 < self.boardSize - 1):
                    if(self.board[r1][c1+1] == color):
                        update.add((r1)*self.boardSize + c1+1)
                
            self.group[self.head[self.boardSize*(row-1) + col]] = []
            self.last_capture = 1
        if(row < self.boardSize-1 and self.liberties[math.floor(self.head[self.boardSize*(row+1) + col]/self.boardSize)][self.head[self.boardSize*(row+1) + col]%self.boardSize] == 0):
            for stone in self.group[self.head[self.boardSize*(row+1) + col]]:
                self.board[math.floor(stone / self.boardSize)][stone % self.boardSize] = 0
                self.head[stone] = stone
                [r1,c1] = [math.floor(stone / self.boardSize), stone % self.boardSize]
                if(r1 > 0):
                    if(self.board[r1-1][c1] == color):
                        update.add((r1-1)*self.boardSize + c1)
                
                if(r1 < self.boardSize -1):
                    if(self.board[r1+1][c1] == color):
                        update.add((r1+1)*self.boardSize + c1)
                
                if(c1 > 0):
                    if(self.board[r1][c1-1] == color):
                        update.add((r1)*self.boardSize + c1-1)
                
                if(c1 < self.boardSize - 1):
                    if(self.board[r1][c1+1] == color):
                        update.add((r1)*self.boardSize + c1+1)
            self.group[self.head[self.boardSize*(row+1) + col]] = []
            self.last_capture = 1
        if(col > 0 and self.liberties[math.floor(self.head[self.boardSize*(row) + col-1]/self.boardSize)][self.head[self.boardSize*(row) + col-1]%self.boardSize] == 0):
            for stone in self.group[self.head[self.boardSize*(row) + col-1]]:
                self.board[math.floor(stone / self.boardSize)][stone % self.boardSize] = 0
                self.head[stone] = stone
                [r1,c1] = [math.floor(stone / self.boardSize), stone % self.boardSize]
                if(r1 > 0):
                    if(self.board[r1-1][c1] == color):
                        update.add((r1-1)*self.boardSize + c1)
                
                if(r1 < self.boardSize -1):
                    if(self.board[r1+1][c1] == color):
                        update.add((r1+1)*self.boardSize + c1)
                
                if(c1 > 0):
                    if(self.board[r1][c1-1] == color):
                        update.add((r1)*self.boardSize + c1-1)
                
                if(c1 < self.boardSize - 1):
                    if(self.board[r1][c1+1] == color):
                        update.add((r1)*self.boardSize + c1+1)
            self.group[self.head[self.boardSize*(row) + col-1]] = []
            self.last_caputre = 1
        if(col < self.boardSize-1 and self.liberties[math.floor(self.head[self.boardSize*(row) + col+1]/self.boardSize)][self.head[self.boardSize*(row) + col+1]%self.boardSize] == 0):
            for stone in self.group[self.head[self.boardSize*(row) + col+1]]:
                self.board[math.floor(stone / self.boardSize)][stone % self.boardSize] = 0
                self.head[stone] = stone
                [r1,c1] = [math.floor(stone / self.boardSize), stone % self.boardSize]
                if(r1 > 0):
                    if(self.board[r1-1][c1] == color):
                        update.add((r1-1)*self.boardSize + c1)
                
                if(r1 < self.boardSize -1):
                    if(self.board[r1+1][c1] == color):
                        update.add((r1+1)*self.boardSize + c1)
                
                if(c1 > 0):
                    if(self.board[r1][c1-1] == color):
                        update.add((r1)*self.boardSize + c1-1)
                
                if(c1 < self.boardSize - 1):
                    if(self.board[r1][c1+1] == color):
                        update.add((r1)*self.boardSize + c1+1)
            self.group[self.head[self.boardSize*(row) + col+1]] = []
            self.last_capture = 1
        self.color *= -1
        for item in update:
            self.push(item)
            self.liberties[math.floor(self.head[item]/self.boardSize)][self.head[item] % self.boardSize] += 1

        for i in range(2):
            self.history[i] = self.history[i+1]
        del self.history[2]
        self.history.append(self.board)
        # print(self.board)
        # print(self.group)
        # print(self.head)