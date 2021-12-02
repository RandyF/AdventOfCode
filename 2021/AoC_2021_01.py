#!/usr/bin/python

#=========================================================================================
# Day Class
#=========================================================================================
class AoC_2021_DEC01():

    PuzzleData = None

    #------------------------------------------------------------------------------
    # Initialize Puzzle Day
    #------------------------------------------------------------------------------
    def __init__(self, FileBase, UseSample=False):
        self.PuzzleData = []
        
        if FileBase != None:
            self.ReadAndParsePuzzleData(FileBase, UseSample=False)


    #------------------------------------------------------------------------------
    # Read Puzzle Data and do any simple parsing
    #------------------------------------------------------------------------------
    def ReadAndParsePuzzleData(self, FileBase, UseSample=False):

        tFileName = FileBase
        if UseSample:
            tFileName += '_Sample'

        tFile = open('%s.txt' % tFileName, 'r')

        for tIn in tFile:
            tDat = int(tIn.strip())
        
            self.PuzzleData.append(tDat)
        
        tFile.close()


    #------------------------------------------------------------------------------
    # --- Day 1: Sonar Sweep ---
    #------------------------------------------------------------------------------
    def PartA_SonarSweep(self):
        last = 2**32
        cnt = 0

        for tDat in self.PuzzleData:

            if tDat > last:
                cnt += 1

            last = tDat
        
        return cnt


    #------------------------------------------------------------------------------
    # --- Part Two ---
    #------------------------------------------------------------------------------
    def PartB_WindowedSweep(self, win_size=3):
        last = 2**32
        cnt = 0
        pos = 0

        while pos < (len(self.PuzzleData)-win_size+1):
            rdg = sum(self.PuzzleData[pos:pos+win_size])

            if rdg > last:
                cnt += 1

            last = rdg
            pos += 1
            
        return cnt



if __name__== "__main__":

    AoC_Puzzle = AoC_2021_DEC01( u'_inputs/2021_01_Data', UseSample=False)

    print(AoC_Puzzle.PartA_SonarSweep()) # 1195
    print(AoC_Puzzle.PartB_WindowedSweep()) # 1235