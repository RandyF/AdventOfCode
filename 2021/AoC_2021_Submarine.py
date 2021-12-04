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



class Submarine():
    Verbosity = None
    CurPos = None
    
    Bingo = None

    def __init__(self, Verbosity=0):
        self.Verbosity = Verbosity
        debug('Creating AoC Submarine...', DebugLevel=DBG_MINOR_START, Verbosity=self.Verbosity )

        self.Bingo = BingoSubsystem(Verbosity = self.Verbosity)

        self.ResetPosition()
        debug('AoC Submarine Created.', DebugLevel=DBG_MINOR, Verbosity=self.Verbosity )


    def ResetPosition(self):
        self.CurPos = [0, 0, 0]

    #------------------------------------------------------------------------------
    # --- Day 2: Dive! ---
    # --- Part Two ---
    #------------------------------------------------------------------------------
    def AimAndMoveSub(self, PuzzleData):

        for tData in PuzzleData:

            if tData[0] == 'forward':
                self.CurPos[0] += tData[1]
                self.CurPos[1] += self.CurPos[2] * tData[1]
                
            elif tData[0] == 'down':
                self.CurPos[2] += tData[1]
                
            elif tData[0] == 'up':
                self.CurPos[2] -= tData[1]

        return self.CurPos[0] * self.CurPos[1]


    #------------------------------------------------------------------------------
    # --- Day 3: Binary Diagnostic ---
    #------------------------------------------------------------------------------
    def _RunBinaryDiagnostic(self, DiagData):

        debug('Calculating Binary Diagnostic...', DebugLevel=DBG_MINOR_START, Verbosity=self.Verbosity )
        tDiagBits = len(DiagData[0])

        tDiagCnt = [0] * tDiagBits

        for tData in DiagData:
            for tBit in range(tDiagBits):
                if tData[tBit] == '1':
                    tDiagCnt[tBit] += 1

        tMajority = ceil(len(DiagData)/2)

        tRet = ''
        for tBit in range(tDiagBits):
            if tDiagCnt[tBit] >= tMajority:
                tRet += '1'
            else:
                tRet += '0'

        Gamma = (tRet, int(tRet, 2))
        debug('Gamma Rate is %s [%d]' % Gamma, DebugLevel=DBG_MINOR_DETAIL, Verbosity=self.Verbosity )

        tRet = tRet.replace('1','x').replace('0','1').replace('x','0')

        Epsilon = (tRet, int(tRet, 2))
        debug('Epsilon Rate is %s [%d]' % Epsilon, DebugLevel=DBG_MINOR_DETAIL, Verbosity=self.Verbosity )

        return [Gamma, Epsilon]


    def CalculatePowerConsumption(self, PuzzleData):
        [Gamma, Epsilon] = self._RunBinaryDiagnostic(PuzzleData)

        PowerCons = Gamma[1] * Epsilon[1]
        debug('Power Consumption Rate is %d' % PowerCons, DebugLevel=1, Verbosity=self.Verbosity )
        
        return [PowerCons, Gamma, Epsilon]


    #------------------------------------------------------------------------------
    # --- Day 3: Binary Diagnostic ---
    # --- Part Two ---
    #------------------------------------------------------------------------------
    def _DiagSearch(self, DiagData, GammaNotEpsilon = True):
        tBits = len(DiagData[0])
        searchList = DiagData

        for tPos in range(tBits):
            tNextList = []
            [Gamma, Epsilon] = self._RunBinaryDiagnostic(searchList)
            
            if GammaNotEpsilon:
                tMask = Gamma[0]
            else:
                tMask = Epsilon[0]
            
            for tData in searchList:
                if tData[tPos] == tMask[tPos]:
                    tNextList.append(tData)

            searchList = tNextList
            
            if len(searchList) == 1:
                break

        return [searchList[0], int(searchList[0], 2)]


    def CalculateLifeSupportRating(self, PuzzleData ):

        O2GenRating = self._DiagSearch(PuzzleData, GammaNotEpsilon = 1)
        C02ScrubRating = self._DiagSearch(PuzzleData, GammaNotEpsilon = 0)

        LifeSupportRating = O2GenRating[1] * C02ScrubRating[1]
        debug('Life Support Rating is %d' % LifeSupportRating, DebugLevel=1, Verbosity=self.Verbosity )
        
        return [LifeSupportRating, O2GenRating, C02ScrubRating]
