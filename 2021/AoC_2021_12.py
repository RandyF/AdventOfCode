#!/usr/bin/python
import numpy as np

from AoC_Utils import *
from AoC_2021_Submarine import Submarine


class Cave():
    Verbosity = None

    Name = ''
    IsBig = None
    Visitied = False
    Exits = None

    def __init__(self, InitStr, Verbosity=0):
        self.Verbosity = Verbosity

        self.Name = InitStr[0]
        debug('Creating Cave %s...' % self.Name, DebugLevel=DBG_MINOR_START, Verbosity=self.Verbosity )

        if self.Name == self.Name.lower():
            self.IsBig = False
        else:
            self.IsBig = True
        
        self.Visitied = False

        self.Exits = []
        self.AddExit(InitStr)

    def AddExit(self, InitStr):
        if InitStr[1] not in self.Exits:
            debug('Adding Exit %s to %s...' % (InitStr[1], InitStr[0]), DebugLevel=DBG_MINOR, Verbosity=self.Verbosity )
            self.Exits.append(InitStr[1] )

    def __str__(self) -> str:
        return '[%s] Big:%u Visit:%u exits:%s' % (self.Name, self.IsBig, self.Visitied, self.Exits) 


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
            self.PuzzleData.append( tRow.strip().split('-') )

        tFile.close()


    def CreateCaveDict(self):
        self.Caves = {}

        for tRow in self.PuzzleData:
            #print('\n\n', tRow, self.Caves.keys())

            if tRow[0] not in self.Caves.keys():
                self.Caves[tRow[0]] = Cave(tRow)
            else:
                self.Caves[tRow[0]].AddExit(tRow)

            if tRow[1] not in self.Caves.keys():
                self.Caves[tRow[1]] = Cave([tRow[1], tRow[0]])
            else:
                self.Caves[tRow[1]].AddExit([tRow[1], tRow[0]])

        print('\n\n CAVE SYSTEM =================')
        for tCave in self.Caves.keys():
            print(self.Caves[tCave])

    def FindMultiSmall(self, Path):

        for tCave in Path:
            if tCave == tCave.lower():
                if Path.count(tCave) > 1:
                    return tCave

        return None




    def ExtendPaths(self, Paths, SmallVisits=1):

        #print('\n\n EXTENDING PATHS =================')

        #for tPath in Paths:
        #    print(tPath)

        tExtended = 0
        tNewPaths = []
        for tPath in Paths:
            #print("chk ex", tPath)
            if tPath[-1] == 'end':
                #print('Saving Traversed Path', tPath)
                tNewPaths.append(tPath)
            else:
                #print('\nExtending Path', tPath)
                
                for tExit in self.Caves[tPath[-1]].Exits:
                    #print('Eval Exit', tExit)

                    tOkToExtend = False

                    if tExit == 'start':
                        #print('   Not Extending back to start')
                        tOkToExtend = False
                    elif tExit == 'end':
                        #print('   Adding End!')
                        tOkToExtend = True

                    elif tExit != tExit.lower():
                        #print('Got a large cave', tExit)
                        tOkToExtend = True
                    
                    elif tExit == tExit.lower():
                        tSmlVisits = tPath.count(tExit)
                        MultiSmall = self.FindMultiSmall(tPath)

                        #print('Got a small cave %s that appears %d [MultiSmall=%s] {%d}' % ( tExit, tSmlVisits, MultiSmall, SmallVisits ) )
                        
                        if tSmlVisits == 0:
                            #print('   Never Seen!')
                            tOkToExtend = True
                        
                        elif tSmlVisits < SmallVisits:

                            if tExit != MultiSmall and tSmlVisits > 0:
                                if MultiSmall == None:
                                    #print('   We are now multismall!')
                                    tOkToExtend = True
                                else:
                                    #print('   Already Been to %s, and we are not MultiSmall!' % tExit)
                                    tOkToExtend = False

                            elif tSmlVisits < SmallVisits and tExit == MultiSmall:
                                #print('   We are MultiSmall, and we still can visit again')
                                tOkToExtend = True


                            else:
                                #print('    HMM?')
                                tOkToExtend = False


                    else:
                        print('Why?', tExit)



                    if tOkToExtend:
                        #print('Adding %s to path...' % tExit)
                        tNewPath = tPath + [tExit]
                        tNewPaths.append(tNewPath)
                        tExtended += 1

            #print('DONE EVALING PATH!\n')

        print("Extended %d Paths from Step:" % tExtended)
        #for tPath in tNewPaths:
        #    print(tPath)

        return tNewPaths, tExtended

    def PermutePaths(self, SmallVisits=1):
        Paths = []
        print('\n\n PERMUTING PATHS =================')

        print('Seeding Paths with [start]')
        for tExit in self.Caves['start'].Exits:
            tNewPath = ['start', tExit]
            Paths.append(tNewPath)

        tExtended = 2**32
        while(tExtended > 0):
            tNewPaths, tExtended = self.ExtendPaths(Paths, SmallVisits)
            #input()
            Paths = tNewPaths

        return len(Paths)

    def PartA(self):
        self.CreateCaveDict()
        return self.PermutePaths(SmallVisits=1)




    def PartB(self):
        self.CreateCaveDict()
        return self.PermutePaths(SmallVisits=2)


if __name__== "__main__":

    AoC_Puzzle = AoC_2021( u'_inputs/2021_12_Data', UseSample=False, Verbosity=1)

    print(AoC_Puzzle.PartA()) # 3298
    print(AoC_Puzzle.PartB()) # 93572
