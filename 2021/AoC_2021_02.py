#!/usr/bin/python

#=========================================================================================
# Day Class
#=========================================================================================
class AoC_2021_DEC02():

    PuzzleData = None
    CurPos = None

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
            [cmd, dist] = tIn.strip().split(' ')
            self.PuzzleData.append([cmd, int(dist)])
                
        tFile.close()


    #------------------------------------------------------------------------------
    # --- Day 2: Dive! ---
    #------------------------------------------------------------------------------
    def PartA_MoveSub(self):
        self.CurPos = [0, 0]
    
        for tData in self.PuzzleData:
            if tData[0] == 'forward':
                self.CurPos[0] += tData[1]
            elif tData[0] == 'down':
                self.CurPos[1] += tData[1]
            elif tData[0] == 'up':
                self.CurPos[1] -= tData[1]

        return self.CurPos[0] * self.CurPos[1]


    #------------------------------------------------------------------------------
    # --- Part Two ---
    #------------------------------------------------------------------------------
    def PartB_AimAndMoveSub(self, win_size=3):
        self.CurPos = [0, 0, 0]

        for tData in self.PuzzleData:

            if tData[0] == 'forward':
                self.CurPos[0] += tData[1]
                self.CurPos[1] += self.CurPos[2] * tData[1]
                
            elif tData[0] == 'down':
                self.CurPos[2] += tData[1]
                
            elif tData[0] == 'up':
                self.CurPos[2] -= tData[1]

        return self.CurPos[0] * self.CurPos[1]



if __name__== "__main__":

    AoC_Puzzle = AoC_2021_DEC02( u'_inputs/2021_02_Data', UseSample=False)

    print(AoC_Puzzle.PartA_MoveSub()) # 1938402
    print(AoC_Puzzle.PartB_AimAndMoveSub()) # 1947878632