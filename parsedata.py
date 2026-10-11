
import boardclaude
import board
import os
import numpy as np
import random

class parseData(object):
    def __init__(self, directory):
        self.directory = directory
        self.data = [] # many [position, result] pairs
        self.result = 1
        self.boardSize = 19

    def shuffle(self):
        return random.shuffle(self.data)

    def getList(self, file):
        f = open(file)
        for i in range(14):
            if i == 8:
                x = f.readline()
                if(x[3] == 'W'):
                    self.result = -1
                else:
                    self.result = 1
            f.readline()
        s = f.read()
        a = s.split("[")
        moves = []
        for i in a:
            if len(i) == 0:
                continue
            moves.append(i[:2])
        del moves[-1]
        del moves[0]
        moves2 = []
        for i in moves:
            moves2.append([ord(i[0]) - 97, ord(i[1]) - 97])
        return moves2

    def getList2(self, file):
        f = open(file, 'r', errors = 'ignore')
        s = f.read()
        a = s.split("RE[")
        del a[0]
        s = a[0]
        if(s[0] == 'W'):
            self.result = -1
        else:
            self.result = 1
        a = s.split("[")
        moves = []
        for i in range(4, len(a)):
            st = a[i][:2]
            row = ord(st[0]) - 97
            col = ord(st[1]) - 97
            temp = row
            row = 18-col
            col = temp
            moves.append([row, col])
        return moves

    def addData(self, moves):
        # feature planes
        # position black 1
        # position white 2
        # player move (always balck, will reflect white and black)
        # ko positions, but these may not generalize
        # result
        b = boardclaude.boardclaude(self.boardSize, self.result)
        # only perform inference as "black"

        
        ctr = 0
        for move in moves:
            b.move(move)
            if ctr < 3:
                ctr+=1
                continue
            if b.color == 1:
                blackhistory = b.blackHistory
                whitehistory = b.whiteHistory
                blackLiberty = b.blackLibertyHistory
                whiteLiberty = b.whiteLibertyHistory
            else:
                blackhistory = b.whiteHistory
                whitehistory = b.blackHistory
                blackLiberty = b.whiteLibertyHistory
                whiteLiberty = b.blackLibertyHistory



        array = [blackhistory[0], blackLiberty[0], whitehistory[0], whiteLiberty[0]]
        arrayflip = [np.fliplr(blackhistory[0]), np.fliplr(blackLiberty[0]), np.fliplr(whitehistory[0]), np.fliplr(whiteLiberty[0])]
        array = np.stack(array, axis = 2)
        arrayflip = np.stack(arrayflip, axis = 2)
        array1 = np.rot90(array, 1)
        array2 = np.rot90(array, 2)
        array3 = np.rot90(array, 3)
        array4 = np.rot90(arrayflip, 1)
        array5 = np.rot90(arrayflip, 2)
        array6 = np.rot90(arrayflip, 3)
        self.data.append([array, self.result])
        self.data.append([array1, self.result])
        self.data.append([array2, self.result])
        self.data.append([array3, self.result])
        self.data.append([array4, self.result])
        self.data.append([array5, self.result])
        self.data.append([array6, self.result])
        self.data.append([arrayflip, self.result])

    def parseAll(self):
        i = 1
        for file in os.listdir(self.directory):
            if(i == 1000):
                break
            print(i)
            file = file.decode("utf-8")
            file = "/Users/ray/cnn/9d/" + file
            l = self.getList2(file)
            self.addData(l)
            i+=1