#!/usr/bin/python
import numpy as np

from AoC_Utils import debug
from AoC_2021_Submarine import Submarine


#=========================================================================================
# Day Class
#=========================================================================================
class AoC_2021():
    Verbosity = None
    PuzzleData = None
    OurSub = None

    #------------------------------------------------------------------------------
    # Initialize Puzzle Day
    #------------------------------------------------------------------------------
    def __init__(self, FileBase, UseSample=False, Verbosity=0):
        self.Verbosity = Verbosity
        self.PuzzleData = []
        self.OurSub = Submarine(Verbosity=Verbosity)
        
        if FileBase != None:
            self.ReadAndParsePuzzleData(FileBase, UseSample)


    #------------------------------------------------------------------------------
    # Read Puzzle Data and do any simple parsing
    #------------------------------------------------------------------------------
    def ReadAndParsePuzzleData(self, FileBase, UseSample=False):

        tFileName = FileBase

        if UseSample:
            tFileName += '_Sample'

        tFile = open('%s.txt' % tFileName, 'r')

        self.PuzzleData = [int(i) for i in tFile.read().strip().split(',')]

        tFile.close()


    def CalcCrabFuel(self, Part):
        maxDist = max(self.PuzzleData)
        posArr = [0] * (maxDist + 1)
        for crab in self.PuzzleData:
            posArr[crab] += 1

        leastFuelPos = -1
        leastFuel = 2**32
        for targetPos in range(len(posArr)+1):

            fuelUsed = 0
            for chkPos in range(len(posArr)):
                if Part == 1:
                    fuelUsed += abs(chkPos - targetPos) * posArr[chkPos]
                if Part == 2:
                    fuelUsed += sum( [*range(abs(chkPos - targetPos)+1)]) * posArr[chkPos]

            if fuelUsed < leastFuel:
                leastFuelPos = targetPos
                leastFuel = fuelUsed

        return [leastFuelPos, leastFuel]


    def PartA(self):
        return self.CalcCrabFuel(1)

    def PartB(self):
        return self.CalcCrabFuel(2)


if __name__== "__main__":

    AoC_Puzzle = AoC_2021( u'_inputs/2021_07_Data', UseSample=False, Verbosity=1)

    print(AoC_Puzzle.PartA()) # 344138
    print(AoC_Puzzle.PartB()) # 94862124
