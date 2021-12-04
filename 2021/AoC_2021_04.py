#!/usr/bin/python

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
            self.PuzzleData.append(r.strip())

        tFile.close()


    def PartA(self):
        if self.Results == None:
            self.OurSub.Bingo.ParseRawPuzzleData(self.PuzzleData);
            self.Results = self.OurSub.Bingo.RunGame()

        return self.Results[0]

    def PartB(self):
        if self.Results == None:
            self.OurSub.Bingo.ParseRawPuzzleData(self.PuzzleData);
            self.Results = self.OurSub.Bingo.RunGame()

        return self.Results[1]


if __name__== "__main__":

    AoC_Puzzle = AoC_2021( u'_inputs/2021_04_Data', UseSample=False, Verbosity=1)

    print(AoC_Puzzle.PartA()) # 60368
    print(AoC_Puzzle.PartB()) # 17435