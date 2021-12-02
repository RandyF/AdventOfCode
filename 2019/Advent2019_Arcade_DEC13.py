from Advent2019_IntCode_DEC13 import ADV19_IntcodeComputer
from math import floor
from os import system


class ADV19_ArcadeCabinet(object):

    def __init__(self, lIntCode = [], lArgs=[], iVerbosity = 0, iICVerbosity = 0):
        self.SetVerbosity(iVerbosity)
        if self.Verbosity >= 1: print( "[ARCADE] Initializing Arcade Cabinet")
        
        self.ScreenSize = [1,1]
        self.Screen = []
        self.StdOutIdx = 0
        
        self.ICComp = ADV19_IntcodeComputer(sIntcodeProg=lIntCode, lArgs=lArgs, iVerbosity=iICVerbosity)
        if self.Verbosity >= 1: print( "[ARCADE] Waiting to Start")

    def SetVerbosity(self, iVerbosity=1):
        self.Verbosity = iVerbosity        
        if self.Verbosity > 0: print( "[ARCADE] Arcade Verbosity now %d" % self.Verbosity)

    def RestartGame(self):
        if self.Verbosity >= 1: print( "[ARCADE] Restarting Game")
        self.BlocksRemain = 0
        self.Score = 0

        self.ICComp.RestartProgram()

        
        self.ScreenSize = [1,1]
        iIdx = 0
        while iIdx < len(self.ICComp.StdOut):
            tPx = self.ICComp.StdOut[iIdx:iIdx+3]
            #print(tPx)
            if tPx[0] + 1 > self.ScreenSize[0]: self.ScreenSize[0] = tPx[0] + 1
            if tPx[1] + 1 > self.ScreenSize[1]: self.ScreenSize[1] = tPx[1] + 1
            
            iIdx += 3

        if self.Verbosity >= 1: print("[ARCADE]  Screen Size is ", self.ScreenSize )
        self.BlankScreen()
        self.ParseScreen()

        self.GameLoop()
        return self.BlocksRemain

    def AddCredits(self):
        self.ICComp.IntcodeMEM[0] = 2


    def BlankScreen(self):
        self.Screen = []
        for _ in range(self.ScreenSize[1]):
            tRow = []
            for _ in range(self.ScreenSize[0]):
                tRow.append(0)
            self.Screen.append(tRow)


    def ParseScreen(self):

        while self.StdOutIdx < len(self.ICComp.StdOut):
            tPx = self.ICComp.StdOut[self.StdOutIdx:self.StdOutIdx+3]

            if tPx[2] == 0 and self.Screen[tPx[1]][tPx[0]] == 2: self.BlocksRemain -= 1
 
            if tPx[2] == 2: self.BlocksRemain += 1
            if tPx[2] == 4: self.BallLoc = tPx[0:2]
            if tPx[2] == 3: self.PaddleLoc = tPx[0:2]

            if tPx[0] == -1:
                self.Score = tPx[2]
            else:
                self.Screen[tPx[1]][tPx[0]] = tPx[2]

            
            self.StdOutIdx += 3


    def DrawScreen(self):
        system('cls')
        print("SCORE: ", self.Score)
        for tCIdx in range(self.ScreenSize[1]):
            for tRIdx in range(self.ScreenSize[0]):
                
                tChr = self.Screen[tCIdx][tRIdx]
                
                if tChr == 0:
                    print(' ', end='')
                elif tChr == 1:
                    print('#', end='')
                elif tChr == 2:
                    print('=', end='')
                elif tChr == 3:
                    print('_', end='')
                elif tChr == 4:
                    print('o', end='')              
                
            print()
        if self.Verbosity >= 2: print("Ball   @ ", self.BallLoc)
        if self.Verbosity >= 2: print("Paddle @ ", self.PaddleLoc)
            

    def GameLoop(self):
    
        while self.BlocksRemain > 0 and self.ICComp.MachineState != 99:
            if self.Verbosity >= 2: print( "[ARCADE] %d Blocks Remaining" % self.BlocksRemain)
            
            if self.Verbosity >= 1: self.DrawScreen()
            
            iJoyDir = 0
            if (self.BallLoc[0] - self.PaddleLoc[0]) < 0: iJoyDir = -1
            if (self.BallLoc[0] - self.PaddleLoc[0]) > 0: iJoyDir = 1
            
            self.ICComp.AppendStdIn([iJoyDir])
            self.ICComp.Continue()
            self.ParseScreen()

            
            if self.Verbosity >= 2: input()
            
        return(self.Score)
