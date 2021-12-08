#!/usr/bin/python
import numpy as np

from AoC_Utils import debug
from AoC_2021_Submarine import Submarine

from AoC_2021_SegmentedDisplay import *

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


        for tDat in tFile:
            tSignals, tOutputs = tDat.strip().split('|')

            self.PuzzleData.append([[i.strip() for i in tSignals.split()], [i.strip() for i in tOutputs.split()]] )

        tFile.close()


    def PartA(self):

        knownOuts = 0
        for tRow in self.PuzzleData:

            for tOut in tRow[1]:
                tSeg = SevenSeg(tOut)
                if tSeg.SegKnown:
                    knownOuts += 1

        return knownOuts

    def PartB(self):

        tOutSum = 0
        for tRow in self.PuzzleData:
            #print('\n\n')
            tDisp = DigitDisplay(tRow)

            tDisp.PrintSimpleDisplay()
            tDisp.DecodeDisplay()
            
            tOutSum += tDisp.DecodeOutput()


        return tOutSum


if __name__== "__main__":

    AoC_Puzzle = AoC_2021( u'_inputs/2021_08_Data', UseSample=False, Verbosity=1)

    print(AoC_Puzzle.PartA()) # 390
    print(AoC_Puzzle.PartB()) # 1011785
