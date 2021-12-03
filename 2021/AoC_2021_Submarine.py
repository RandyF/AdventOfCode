from AoC_Utils import *
from math import ceil

class Submarine():
    Verbosity = None
    CurPos = None

    def __init__(self, Verbosity=0):
        self.Verbosity = Verbosity
        debug('Creating AoC Submarine...', DebugLevel=DBG_MINOR_START, Verbosity=self.Verbosity )

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
