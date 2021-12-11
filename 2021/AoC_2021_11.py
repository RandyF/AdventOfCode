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

        tArr = []
        for tRow in tFile:
            tArr.append( [int(i) for i in [*tRow.strip()]] )

        self.PuzzleData = np.array( tArr, dtype=np.uint8)
        self.ArrSize = self.PuzzleData.shape


        tFile.close()


    ArrSize = None
    OctosA = None

    def _MakeFlashAdder(self, Source):
        tAdder= np.zeros( self.ArrSize, dtype=np.uint8 )

        yMin = max( Source[0] - 1, 0)
        yMax = min( Source[0] + 2, self.ArrSize[0])
        xMin = max( Source[1] - 1, 0)
        xMax = min( Source[1] + 2, self.ArrSize[1])

        #print( Source, yMin, yMax, xMin, xMax )

        tAdder[yMin:yMax, xMin:xMax] += 1

        return tAdder

    def _OctoStep(self):
        HasFlashed = np.zeros( self.ArrSize, dtype=bool )

        StepFlashes = 0
        #---------------------------------------------------------
        # Add one First
        #---------------------------------------------------------

        #print(self.OctosA)

        tOnes = np.ones( self.ArrSize, dtype=np.uint8 )
   
        self.OctosA = np.add( self.OctosA, tOnes)

        #---------------------------------------------------------
        # Flash until stopped flashing.
        #---------------------------------------------------------
        tNines = np.ones( self.ArrSize, dtype=np.uint8 ) * 9

        #print('PREFLASH')
        #print(self.OctosA)


        cycleFlashes = 999
        while(cycleFlashes > 0):
            cycleFlashes = 0
            #print("\nCYCLEFLASH")
            tFlash = np.greater( self.OctosA, tNines )
            
            tNewFlash = np.logical_and(  tFlash, np.logical_not(HasFlashed) )


            #print("NEWFLASH")
            #print(tNewFlash)

            tFlashIdx = np.transpose(np.transpose( np.argwhere(tNewFlash == True )) )
            cycleFlashes += len(tFlashIdx)

            for tFl in tFlashIdx:

                self.OctosA = np.add( self.OctosA, self._MakeFlashAdder( tFl ) )
                #print('FLASH @ ', tFl)
                #print( self.OctosA )

            HasFlashed = np.logical_or( HasFlashed, tNewFlash )

            StepFlashes += cycleFlashes

        AllFlashed = np.array_equal( HasFlashed, np.ones( self.ArrSize, dtype=bool ) )        

        #print("Before Clearing > 9")
        #print(self.OctosA)

        self.OctosA = np.multiply( self.OctosA, (self.OctosA < 10).astype(np.uint8) )

        #print("POSTFLASH")
        #print(self.OctosA, StepFlashes)

        return StepFlashes, AllFlashed


    def PartA(self):
        self.OctosA = self.PuzzleData

        total = 0
        for x in range(100):
            #print('===========================  STEP %d =============================' % (x+1) )
            Flashes, AllFlashed = self._OctoStep()
            total += Flashes
            #input()
            
        return total


    def PartB(self):
        self.OctosA = self.PuzzleData

        tStep = 0
        AllFlashed = False
        while not AllFlashed:
            tStep += 1
            #print('===========================  STEP %d =============================' % (x+1) )
            Flashes, AllFlashed = self._OctoStep()
            
        return tStep


if __name__== "__main__":

    AoC_Puzzle = AoC_2021( u'_inputs/2021_11_Data', UseSample=False, Verbosity=1)

    print(AoC_Puzzle.PartA()) # 1793
    print(AoC_Puzzle.PartB()) # 247
