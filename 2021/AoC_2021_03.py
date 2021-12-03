#!/usr/bin/python

from AoC_Utils import debug
from AoC_2021_Submarine import Submarine

#=========================================================================================
# Day Class
#=========================================================================================
class AoC_2021_DEC03():
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

        for tIn in tFile:
            tBits = tIn.strip()
            self.PuzzleData.append(tBits)

        tFile.close()


    def PartA(self):
        return self.OurSub.CalculatePowerConsumption(self.PuzzleData)

    def PartB(self):
        return self.OurSub.CalculateLifeSupportRating(self.PuzzleData)


if __name__== "__main__":

    AoC_Puzzle = AoC_2021_DEC03( u'_inputs/2021_03_Data', UseSample=False, Verbosity=1)

    print(AoC_Puzzle.PartA()) # 1540244
    print(AoC_Puzzle.PartB()) # 4203981