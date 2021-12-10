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

        for tRow in tFile:
            self.PuzzleData.append( [*tRow.strip()] )

        tFile.close()


    def PartA(self):
        A, B = self.OurSub.NavSystem.LoadAndSyntaxCheck(self.PuzzleData)
        return A


    def PartB(self):
        A, B = self.OurSub.NavSystem.LoadAndSyntaxCheck(self.PuzzleData)
        return B

if __name__== "__main__":

    AoC_Puzzle = AoC_2021( u'_inputs/2021_10_Data', UseSample=False, Verbosity=1)

    print(AoC_Puzzle.PartA()) # 344193
    print(AoC_Puzzle.PartB()) # 3241238967
