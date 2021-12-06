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

        self.PuzzleData = np.array( [int(i) for i in tFile.read().strip().split(',')], dtype=np.uint8)

        tFile.close()


    def LanternfishGrowth(self, RunDays):

        FishPop = []
        for i in range(9):
            count = np.count_nonzero(self.PuzzleData == i)
            FishPop.append(count)

        for i in range(RunDays):
            #print('\n\n DAWN OF A NEW DAY')
            #print("start", FishPop)
            NewFish = FishPop[0]
            FishPop = FishPop[1:] + [NewFish]
            FishPop[6] += NewFish

        return sum(FishPop)


    def PartA(self):
        return self.LanternfishGrowth(80)


    def PartB(self):
        return self.LanternfishGrowth(256)


if __name__== "__main__":

    AoC_Puzzle = AoC_2021( u'_inputs/2021_06_Data', UseSample=False, Verbosity=1)

    print(AoC_Puzzle.PartA()) # 386586
    print(AoC_Puzzle.PartB()) # 1732821262171