'''
Created on 21 Oct 2013

@author: mariaz
'''
import unittest
from collections import namedtuple


class Game(object):

    BOARD_SIZE = 3
    WHITE_PLAYER = 1
    BLACK_PLAYER = 2
    
    def __init__(self):
        self._currentPlayer = Game.WHITE_PLAYER
        self._board = {}
    
    def current_player(self):
        return self._currentPlayer

    def placeStone(self, location):
        self._board[location] = self._currentPlayer
        self._currentPlayer = Game.BLACK_PLAYER

    
    def isWhite(self, location):
        return self._board.get(location) == Game.WHITE_PLAYER

    
    def isEmpty(self, location):
        return not self._board.has_key(location)

    
    def placeTiles(self, slots):
        for slot in slots:
            self._board[slot.location] = slot.player

    
    def isBlack(self, location):
        return self._board.get(location) == Game.BLACK_PLAYER

    
    def moveFromTo(self, fromLocation, toLocation):
        self._board[toLocation] = self._board.get(fromLocation)
        del self._board[fromLocation]
        pass

    def isFullRowOfColor(self, rowNum, color):
        slots = self._board.iteritems()
        whiteSlotsInRow = [1 for location, player in slots if player == color and location.row == rowNum]
        return sum(whiteSlotsInRow) == Game.BOARD_SIZE

    def isFullColumnOfColor(self, columnNum, color):
        slots = self._board.iteritems()
        blackSlotsInColumn = [1 for (location, player) in slots if player == color and location.column == columnNum]
        return sum(blackSlotsInColumn) == Game.BOARD_SIZE

    def isWhiteRow(self, rowNum):
        return self.isFullRowOfColor(rowNum, Game.WHITE_PLAYER)
    

    def isFirstDiagonalForPlayer(self, color):
        slots = self._board.iteritems()
        sorted_player_locations = sorted([location for (location, player) in slots if player == color])
        diagonals = [[(0,0), (1,1), (2,2)], [(0, 2), (1, 1), (2, 0)]]
        return sorted_player_locations in diagonals
    
    
    def winner(self):
        for player in [Game.WHITE_PLAYER, Game.BLACK_PLAYER]:
            for i in range(3):
                if(self.isFullRowOfColor(i, player) or self.isFullColumnOfColor(i, player)):
                    return player
            if self.isFirstDiagonalForPlayer(player):
                return player
        return None

    
    
    

    
    
    
    
Location = namedtuple('Location', 'row column')
Slot = namedtuple('Slot', 'location player')

class Test(unittest.TestCase):
    def testNewBoardIsEmpty(self):
        game = Game()
        allLocations = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        for location in allLocations:
            self.assertTrue(game.isEmpty(Location(*location)), "Every tile should be empty at the beginning")
#         self.assertEqual("...\n...\n...", game.humanRepresenation(), "New boards should be empty")
        
    def testFirstPlayerIsWhite(self):
        game = Game()
        self.assertEqual(game.current_player(), Game.WHITE_PLAYER, "First player should be white")
        
    def testSecondPlayerIsBlack(self):
        game = Game()
        game.placeStone(Location(1,1))
        self.assertEqual(game.current_player(), Game.BLACK_PLAYER, "Second player should be black")
        
    def testValidFirstMovePlacesATile(self):
        game = Game()
        game.placeStone(Location(1,1))
        self.assertTrue(game.isWhite(Location(1,1)), "Middle should be white now")
        self.assertFalse(game.isEmpty(Location(1,1)), "Middle shouldn't be empty")
        
    def testSettingUpABoardInParticularState(self):
        game = Game()
        game.placeTiles([Slot(Location(0,0), Game.WHITE_PLAYER),
                         Slot(Location(1,1), Game.BLACK_PLAYER),
                         Slot(Location(2,2), Game.WHITE_PLAYER) 
                         ])
        self.assertTrue(game.isWhite(Location(0,0)), "Bottom left corner should be white")
        self.assertTrue(game.isBlack(Location(1,1)), "Middle should be black")
        self.assertTrue(game.isWhite(Location(2,2)), "Top right corner should be white")
        
    def testEmptyBoardHasNoWhiteNorBlackPiece(self):
        game = Game()
        self.assertFalse(game.isWhite(Location(1,1)), "Should be empty - not white")
        self.assertFalse(game.isBlack(Location(1,1)), "Should be empty - not black")
    
    def testMakingMoveBetweenSlots(self):
        game = Game()
        game.placeTiles([Slot(Location(0,0), Game.WHITE_PLAYER),
                         Slot(Location(1,1), Game.BLACK_PLAYER),
                         Slot(Location(2,2), Game.WHITE_PLAYER),
                         Slot(Location(0,1), Game.BLACK_PLAYER),
                         Slot(Location(1,2), Game.WHITE_PLAYER),
                         Slot(Location(2,0), Game.BLACK_PLAYER),
                         ])
        
        game.moveFromTo(Location(2,2), Location(2,1))
        self.assertTrue(game.isEmpty(Location(2,2)), "Departing slot should be empty")
        self.assertTrue(game.isWhite(Location(2,1)), "Arrival slot should be white")
    
    def testEmptyBoardHasNoWinner(self):
        game = Game()
        self.assertEqual(game.winner(), None, "Nobody should be winning at the start")    
    
    def testFirstRowIsWhite(self):
        game = Game()
        game.placeTiles([Slot(Location(0,0), Game.WHITE_PLAYER),
                         Slot(Location(0,1), Game.WHITE_PLAYER),
                         Slot(Location(0,2), Game.WHITE_PLAYER),
                         Slot(Location(1,0), Game.BLACK_PLAYER),
                         Slot(Location(1,2), Game.BLACK_PLAYER),
                         Slot(Location(2,1), Game.BLACK_PLAYER),
                         ])
        self.assertTrue(game.isWhiteRow(0), "Row 0 should be white")
        
    
    def testWinnerIsWhite(self):
        game = Game()
        game.placeTiles([Slot(Location(0,0), Game.WHITE_PLAYER),
                         Slot(Location(0,1), Game.WHITE_PLAYER),
                         Slot(Location(0,2), Game.WHITE_PLAYER),
                         Slot(Location(1,0), Game.BLACK_PLAYER),
                         Slot(Location(1,2), Game.BLACK_PLAYER),
                         Slot(Location(2,1), Game.BLACK_PLAYER),
                         ])
        self.assertEqual(game.winner(), Game.WHITE_PLAYER, "Winner should be white")
    
    def testWinnerIsBlackByTakingTheFirstColumn(self):
        game = Game()
        game.placeTiles([Slot(Location(1,0), Game.WHITE_PLAYER),
                         Slot(Location(1,2), Game.WHITE_PLAYER),
                         Slot(Location(2,1), Game.WHITE_PLAYER),
                         Slot(Location(0,0), Game.BLACK_PLAYER),
                         Slot(Location(1,0), Game.BLACK_PLAYER),
                         Slot(Location(2,0), Game.BLACK_PLAYER),
                         ])
        self.assertEqual(game.winner(), Game.BLACK_PLAYER, "Column 0 is black")
        
    def testWinnerIsBlackByTakingTheSouthEastDiagonal(self):
        game = Game()
        game.placeTiles([Slot(Location(1,0), Game.WHITE_PLAYER),
                         Slot(Location(1,2), Game.WHITE_PLAYER),
                         Slot(Location(2,1), Game.WHITE_PLAYER),
                         Slot(Location(0,0), Game.BLACK_PLAYER),
                         Slot(Location(1,1), Game.BLACK_PLAYER),
                         Slot(Location(2,2), Game.BLACK_PLAYER),
                         ])
        self.assertEqual(game.winner(), Game.BLACK_PLAYER, "Diagonal is black")
        
                     
    def testWinnerIsBlackByTakingTheNorthEastDiagonal(self):
        game = Game()
        game.placeTiles([Slot(Location(1,0), Game.WHITE_PLAYER),
                         Slot(Location(1,2), Game.WHITE_PLAYER),
                         Slot(Location(2,1), Game.WHITE_PLAYER),
                         Slot(Location(0,2), Game.BLACK_PLAYER),
                         Slot(Location(1,1), Game.BLACK_PLAYER),
                         Slot(Location(2,0), Game.BLACK_PLAYER),
                         ])
        self.assertEqual(game.winner(), Game.BLACK_PLAYER, "Diagonal is black")


if __name__ == "__main__":
    unittest.main()