# Copyright Hugh Perkins 2015 hughperkins at gmail
#
# This Source Code Form is subject to the terms of the Mozilla Public License, 
# v. 2.0. If a copy of the MPL was not distributed with this file, You can 
# obtain one at http://mozilla.org/MPL/2.0/.

import Bag2d

# represents a string of contiguous pieces of one color on the board
# including we have a list of all its liberties, and therefore their count
class GoString(object):
    def __init__(self, boardSize, color ):
        self.boardSize = boardSize
        self.color = color
        self.liberties = Bag2d.Bag2d(boardSize)
        self.pieces = Bag2d.Bag2d(boardSize)

    def getPiece( self, index ):
        return self.pieces[index] #returns index of placed piece
    
    def getLiberty( self, index ):
        return self.liberties[index] #returns index of liberty piece

    def insertPiece( self, combo ):
        self.pieces.insert( combo ) # inserts piece into piece board

    def numPieces(self):
        return self.pieces.size() # returns number of pieces

    def removeLiberty( self, combo ):
        self.liberties.erase( combo ) # erases liberty from liberty board

    def numLiberties(self):
        return self.liberties.size() # returns number of liberties

    def insertLiberty( self, combo ):
         self.liberties.insert( combo ) # inserts liberty into liberty board
    
    def copyLibertiesFrom( self, source ):
        for libertyPos in source.liberties.pieces: # copies liberties from another liberty board
            self.liberties.insert( libertyPos )

    def __str__(self):
        result = "GoString[ pieces=" + str(self.pieces) + " liberties=" + str(self.liberties) + " ]" # prints liberties in a string
        return result