import GoBoard
import numpy as np

boardSize = 19
board = GoBoard.GoBoard(boardSize)
board.applyMove('b', (1,1))
print(board.board)