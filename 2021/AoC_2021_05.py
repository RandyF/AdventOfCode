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
    
    Results = None

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

        for r in tFile:
            [p1,ignore,p2] = r.strip().split()
            p1 = [int(i) for i in p1.split(',')]
            p2 = [int(i) for i in p2.split(',')]

            self.PuzzleData.append(np.array( (p1, p2)))

        tFile.close()


    def PartA(self):
        return self.OurSub.DetectThermalVentLines(self.PuzzleData, OnlyHV=True)

    def PartB(self):
        return self.OurSub.DetectThermalVentLines(self.PuzzleData)


if __name__== "__main__":

    AoC_Puzzle = AoC_2021( u'_inputs/2021_05_Data', UseSample=False, Verbosity=1)

    print(AoC_Puzzle.PartA()) # 5124
    print(AoC_Puzzle.PartB()) # 19771