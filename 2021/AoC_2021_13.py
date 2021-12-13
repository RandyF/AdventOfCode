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
        self.PuzzleFolds = []
        self.OurSub = Submarine(Verbosity=Verbosity)
        
        if FileBase != None:
            self.ReadAndParsePuzzleData(FileBase, UseSample)

    PuzzleFolds = None

    #------------------------------------------------------------------------------
    # Read Puzzle Data and do any simple parsing
    #------------------------------------------------------------------------------
    def ReadAndParsePuzzleData(self, FileBase, UseSample=False):

        tFileName = FileBase

        if UseSample:
            tFileName += '_Sample'

        tFile = open('%s.txt' % tFileName, 'r')

        yMax, xMax = 0, 0
        tPuzzDots = []
        for tRow in tFile:

            if len(tRow.strip().split(',')) > 1:
                tDot = [int(x) for x in tRow.strip().split(',') ] 

                yMax = max(tDot[1], yMax )            
                xMax = max(tDot[0], xMax )            

                tPuzzDots.append( (tDot[1], tDot[0]) )

        
            elif tRow.strip().split(' ')[0] == 'fold':
                tFoldDir, tFoldNum = tRow.strip().split(' ')[2].split('=')
                self.PuzzleFolds.append( [tFoldDir, int(tFoldNum) ]  )

        tFile.close()

        #print(yMax, xMax, tPuzzDots)

        self.PuzzleData = np.zeros( (yMax+1, xMax+1), dtype=np.uint8 )

        for tDot in tPuzzDots:
            self.PuzzleData[tDot] = 1

        #print(self.PuzzleData)
        #print(self.PuzzleFolds)


    def FoldPage(self, Page, FoldLine):
        #print('\nInput')
        #print(Page, FoldLine, Page.shape )

        if FoldLine[0] == 'y':
            tTop = Page[0:FoldLine[1],:]
            tBot = Page[FoldLine[1]+1:,:]

            #print('Top')
            #print(tTop, tTop.shape)
            #print('Bottom')
            #print(tBot, tBot.shape)

            tTopSizeY, tTopSizeX = tTop.shape
            tBotSizeY, tFoldSizeX = tBot.shape
            
            #print(tTopSizeY, tBotSizeY)
            if tTopSizeY < tBotSizeY:
                tStack = np.zeros( (tBotSizeY - tTopSizeY, tTopSizeX), dtype=np.uint8 )

                tTop = np.vstack( (tStack, tTop) )
                #print('New Top')
                #print(tTop, tTop.shape)

            elif tTopSizeY > tBotSizeY:
                tStack = np.zeros( (tTopSizeY - tBotSizeY, tTopSizeX), dtype=np.uint8 )

                tBot = np.vstack( (tBot, tStack) )
                #print('New Bottom')
                #print(tBot, tBot.shape)

            tFlipped = np.flip(tBot, 0)

            #print('tBot Flipped')
            #print(tFlipped, tFlipped.shape)

            tFolded = np.add( tTop, tFlipped )

        elif FoldLine[0] == 'x':
            tLeft = Page[:,0:FoldLine[1]]
            tRight = Page[:,FoldLine[1]+1:]

            #print('tLeft')
            #print(tLeft, tLeft.shape)
            #print('tRight')
            #print(tRight, tRight.shape)


            tLeftSizeY, tLeftSizeX = tLeft.shape
            tRightSizeY, tRightSizeX = tRight.shape
            
            #print(tLeftSizeX, tRightSizeX)
            if tLeftSizeX < tRightSizeX:
                tStack = np.zeros( (tLeftSizeY, tRightSizeX - tLeftSizeX), dtype=np.uint8 )

                tLeft = np.hstack( (tStack, tLeft) )
                #print('New Left')
                #print(tLeft, tLeft.shape)

            elif tLeftSizeX > tRightSizeX:
                tStack = np.zeros( (tLeftSizeY, tLeftSizeX - tRightSizeX ), dtype=np.uint8 )

                tRight = np.hstack( (tRight, tStack) )
                #print('New Right')
                #print(tRight, tRight.shape)

            tFlipped = np.flip(tRight, 1)

            #print('tRight Flipped')
            #print(tFlipped, tFlipped.shape)

            tFolded = np.add( tLeft, tFlipped )



        else:
            raise Exception('bork')


        #print('Folded')
        #print(tFolded, tFolded.shape)

        return tFolded.astype(bool).astype(np.uint8)


    def PartA(self):

        tCurPage = self.FoldPage( self.PuzzleData, self.PuzzleFolds[0])
        return tCurPage.sum()


    def PartB(self):

        tCurPage = self.PuzzleData
        
        for tCurFold in self.PuzzleFolds:
            tCurPage = self.FoldPage( tCurPage, tCurFold)

        tStr = ''
        yMax, xMax = tCurPage.shape
        for y in range(yMax):
            for x in range(xMax):
                if tCurPage[y, x] == 1:
                    tStr += '#'
                else:
                    tStr += ' '
            tStr += '\n'

        return tStr


    def Test(self):

        tTest = [ \
                [1, 0, 0, 0, 0], \
                [0, 1, 0, 0, 0], \
                [0, 0, 1, 0, 0], \
                [0, 0, 0, 1, 0], \
                [1, 0, 0, 0, 1], \
                [0, 1, 0, 0, 0], \
                [0, 0, 1, 0, 0], \
                [0, 0, 0, 1, 0], \
                [0, 0, 0, 0, 1] \
                ]

        tTest = np.array(tTest)

        print(tTest, tTest.shape)

        self.FoldPage( tTest, ['x', 3])


if __name__== "__main__":

    AoC_Puzzle = AoC_2021( u'_inputs/2021_13_Data', UseSample=False, Verbosity=1)

    print(AoC_Puzzle.PartA()) # 763
    print(AoC_Puzzle.PartB()) # RHALRCRA
