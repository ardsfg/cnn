import numpy as np
import math

class boardclaude(object):
    def __init__( self, boardSize, result) :
        self.result = result
        self.boardSize = boardSize
        self.head = [[[y,x] for x in range(boardSize)] for y in range(boardSize)] # directed graph
        self.boardBlack = [[0 for x in range(boardSize)] for y in range(boardSize)] # state of board
        self.boardWhite = [[0 for x in range(boardSize)] for y in range(boardSize)] # state of board
        self.board =  [[0 for x in range(boardSize)] for y in range(boardSize)] # state of board
        self.history = [None, None, None] # short history
        self.whiteHistory = [None, None, None]
        self.blackHistory = [None, None, None]
        self.whiteLibertyHistory = [None, None, None]
        self.blackLibertyHistory = [None, None, None]
        self.groupLiberty = [[set() for x in range(boardSize)] for y in range(boardSize)]
        self.numLibertyBlack = [[0 for x in range(boardSize)] for y in range(boardSize)]
        self.numLibertyWhite = [[0 for x in range(boardSize)] for y in range(boardSize)]
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

    def neighbors(self, row, col):
        # in-bounds up/down/left/right points
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            r, c = row + dr, col + dc
            if 0 <= r < self.boardSize and 0 <= c < self.boardSize:
                yield r, c

    def join(self, x, y):
        # x, y are [row, col] of two touching stones of the same color
        xhead = self.head[x[0]][x[1]]
        yhead = self.head[y[0]][y[1]]

        if(xhead == yhead): # already the same group, nothing to merge
            return

        # the head with the smaller index becomes the sink
        if(xhead[0] * self.boardSize + xhead[1] > yhead[0] * self.boardSize + yhead[1]):
            xhead, yhead = yhead, xhead

        # merge liberties into the sink
        self.groupLiberty[xhead[0]][xhead[1]] |= self.groupLiberty[yhead[0]][yhead[1]]
        self.groupLiberty[yhead[0]][yhead[1]] = set()

        # re-point every stone of the absorbed group at the sink
        for stone in self.group[yhead[0]][yhead[1]]:
            self.head[stone[0]][stone[1]] = xhead
            self.group[xhead[0]][xhead[1]].append(stone)
        self.group[yhead[0]][yhead[1]] = []

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

    def erase(self, h):
        # remove the whole group whose sink is h = [row, col]
        stones = self.group[h[0]][h[1]]
        captured = self.board[h[0]][h[1]] # color being removed

        # 1. clear the stones and reset their bookkeeping
        for [r, c] in stones:
            self.board[r][c] = 0
            self.boardBlack[r][c] = 0
            self.boardWhite[r][c] = 0
            self.head[r][c] = [r, c]
            self.group[r][c] = []
            self.groupLiberty[r][c] = set()

        # 2. every point we just emptied is a new liberty for the surrounding enemy groups
        for [r, c] in stones:
            for nr, nc in self.neighbors(r, c):
                if(self.board[nr][nc] == -captured):
                    [a, b] = self.head[nr][nc]
                    self.groupLiberty[a][b].add(r * self.boardSize + c)

        self.last_capture += len(stones)

    def move(self, loc):
        # loc = self.parseLocation(place)
        row = loc[0]
        col = loc[1]
        color = self.color
        self.last_capture = 0

        self.board[row][col] = color
        if(color == 1):
            self.boardBlack[row][col] = 1
        else:
            self.boardWhite[row][col] = 1

        # the new stone starts as a group of its own
        self.head[row][col] = [row, col]
        self.group[row][col] = [[row, col]]
        self.groupLiberty[row][col] = set()

        # update liberties around the new stone
        updateLiberty = set()
        for r, c in self.neighbors(row, col):
            if(self.board[r][c] == 0):
                self.groupLiberty[row][col].add(r * self.boardSize + c) # new stone gains a liberty
                if(self.color == 1):
                    self.numLibertyBlack[row][col]+=1
                else:
                    self.numLibertyWhite[row][col]+=1
            else:
                [a, b] = self.head[r][c]
                self.groupLiberty[a][b].discard(row * self.boardSize + col) # neighbor loses this point
                updateLiberty.add(a*self.boardSize + b)

        for item in updateLiberty:
            [a,b] = self.head[math.floor(item / self.boardSize)][item % self.boardSize]
            if self.board[a][b] == 1:
                for stone in self.group[a][b]:
                    self.numLibertyBlack[stone[0]][stone[1]]-=1
            else:
                for stone in self.group[a][b]:
                    self.numLibertyWhite[stone[0]][stone[1]]-=1
                
                

        # merge with friendly neighbors
        for r, c in self.neighbors(row, col):
            if(self.board[r][c] == color):
                self.join([row, col], [r, c])

        # capture enemy neighbors that have no liberties left
        for r, c in self.neighbors(row, col):
            if(self.board[r][c] == -color):
                [a, b] = self.head[r][c]
                if(len(self.groupLiberty[a][b]) == 0):
                    self.erase([a, b])

        self.color *= -1

        # keep a copy of the board, not a reference to the list we keep mutating
        self.history.pop(0)
        self.history.append([line[:] for line in self.board])
        self.whiteHistory.pop(0)
        self.whiteHistory.append([line[:] for line in self.boardWhite])
        self.blackHistory.pop(0)
        self.blackHistory.append([line[:] for line in self.boardBlack])
        self.whiteLibertyHistory.pop(0)
        self.whiteLibertyHistory.append([line[:] for line in self.numLibertyWhite])
        self.blackLibertyHistory.pop(0)
        self.blackLibertyHistory.append([line[:] for line in self.numLibertyBlack])
