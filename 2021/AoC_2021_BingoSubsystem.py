from AoC_Utils import *
from math import ceil

import numpy as np

class BingoBoard():
    BoardName = None

    Verbosity = None
    
    BoardArray = None
    GameMarks = None
    
    LastDraw = None
    
    HasWon = None
    
    def __init__(self, RawArray, BoardName = None, Verbosity=0):
        self.Verbosity = Verbosity
        debug('Creating Bingo Board...', DebugLevel=DBG_MINOR_START, Verbosity=self.Verbosity )

        self.ParsePuzzleArray(RawArray)
        GameMarks = np.zeros( (5,5), dtype=bool )
        LastDraw = -1
        HasWon = False

        self.BoardName = BoardName

        debug('Bingo Board Created.', DebugLevel=DBG_MINOR, Verbosity=self.Verbosity )


    def ParsePuzzleArray(self, RawArray):
        if len(RawArray) != 5:
            raise Exception('NOT ENOUGH DATA FOR A BINGO BOARD')

        tScrub = []
        for r in RawArray:
            tScrub.append([int(i) for i in r.strip().split()])

        self.BoardArray = np.array(tScrub)
        
        if self.BoardArray.size != 25:
            raise Exception('Invalid Board Size!')


    def MarkNumber(self, Number):

        self.LastDraw = Number
        
        tDraw = np.ones( (5,5), dtype=np.int8 ) * int(Number)
        tCheck = np.ma.getmaskarray( np.ma.masked_equal( self.BoardArray, tDraw ) )
        self.GameMarks = np.logical_or(self.GameMarks, tCheck)

        return self.CheckBingo()


    def CheckBingo(self):

        tRowCheck = np.ones( (5), dtype=bool)
        #print(tRowCheck)
        for tRow in range(5):
            tRowDat = self.GameMarks[ tRow, : ]

            if (tRowDat == tRowCheck).all():
                debug('Got Row Bingo!', DebugLevel=DBG_FINE_DETAIL, Verbosity=self.Verbosity )
                self.HasWon = True
                return True

        tColCheck = np.ones( (5), dtype=bool)
        #print(tColCheck)
        for tCol in range(5):
            tColDat = self.GameMarks[ :, tCol ]
            #print("ColData", tColDat)

            if (tColDat == tColCheck).all():
                debug('Got Column Bingo!', DebugLevel=DBG_FINE_DETAIL, Verbosity=self.Verbosity )
                self.HasWon = True
                return True

        return False


    def GetScore(self):
        tMaskedBoard = np.multiply(self.BoardArray, np.logical_not(self.GameMarks).astype(np.int8) )

        return np.sum(tMaskedBoard) * self.LastDraw


class BingoSubsystem():

    Verbosity = None

    BingoDraws = None
    BingoBoards = None

    def __init__(self, Verbosity=0):
        self.Verbosity = Verbosity
        debug('Creating Bingo Subsystem...', DebugLevel=DBG_MINOR_START, Verbosity=self.Verbosity )

        self.BingoDraws = []
        self.BingoBoards = []

        debug('Bingo Subsystem Created.', DebugLevel=DBG_MINOR, Verbosity=self.Verbosity )


    def ParseRawPuzzleData(self, RawPuzzle):

        self.BingoDraws = [int(i) for i in RawPuzzle[0].strip().split(',')];
        #print(self.BingoDraws)

        tNumPuzzles =  int((len(RawPuzzle)-1) / 6)

        for tPuz in range(tNumPuzzles):
            tBoard = BingoBoard( RawPuzzle[(tPuz * 6)+2:(tPuz * 6)+7 ], BoardName = 'Board %03d'%tPuz, Verbosity=self.Verbosity  )
            self.BingoBoards.append(tBoard)


    def RunGame(self):
        
        tWinningBoards = []
    
        if self.BingoDraws == None:
            raise Exception('Load a game first!')
    
        debug('Running Game...', DebugLevel=DBG_MAJOR, Verbosity=self.Verbosity )
    
        tWinner = None
        for tDraw in self.BingoDraws:

            debug('Drew number [%d] for %d remaining boards.' % (tDraw, len(self.BingoBoards)), DebugLevel=DBG_MAJOR_DETAIL, Verbosity=self.Verbosity )

            for tBoard in self.BingoBoards:
                
                if not tBoard.HasWon:
                    tRet = tBoard.MarkNumber(tDraw)
                    
                    if tRet:
                        debug('Got Bingo', DebugLevel=DBG_FINE_DETAIL, Verbosity=self.Verbosity )

                        tWinningBoards.append(tBoard)


        debug('   Done drawing!', DebugLevel=DBG_MAJOR, Verbosity=self.Verbosity )

        return [tWinningBoards[0].GetScore(), tWinningBoards[-1].GetScore() ]


