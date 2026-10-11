import numpy as np
import os
import goBoard.GoBoard as GoBoard
import goBoard.GoString as GoString
import goBoard.Bag2d as Bag2d
# not using ko
result = 1 #1 = black, -1 = white

def coordinates(file):
    f = open(file)
    for i in range(14):
        if i == 9:
            x = f.readline()
            if(x[3] == 'W'):
                result = -1
                continue
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

boardsize = 19

def checkEnemyLiberty(board, pos, color):
    [row, col] = pos
    if(row < 0 or col < 0 or row >= boardsize or col >= boardsize):
        return
    if(board[row][col] == color):
        return
    

def applyMove(board, move, color):
    [row, col] = move

    checkEnemyLiberty(board, [row-1, col], color)
    checkEnemyLiberty(board, [row+1, col], color)
    checkEnemyLiberty(board, [row, col-1], color)
    checkEnemyLiberty(board, [row, col+1], color)

directory = os.fsencode("/Users/ray/cnn/data")

dataset = [] #array of [board, result]. shuffle it later

for file in os.listdir(directory):
    file = file.decode("utf-8")
    file = "/Users/ray/cnn/data/" + file
    a = parse(file)
    board = [[0] * boardsize]* boardsize
    color = 1
    for move in a:
        coord1 = ord(move[0]) - 97
        coord2 = ord(move[1]) - 97
    