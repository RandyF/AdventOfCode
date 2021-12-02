from Advent2019_IntCode_DEC13 import ADV19_IntcodeComputer
from math import floor

class ADV19_PuzzleRobot(object):

    def __init__(self, lIntCode = [], lArgs=[], lInitPosition=[0, 0], iInitHeading=0, iVerbosity = 0, iICVerbosity = 0):
        self.SetVerbosity(iVerbosity)
        if self.Verbosity >= 1: print( "[ROBOT] Initializing Puzzle Robot")
        
        self.Position = lInitPosition[:]
        self.Heading = 0 # Clockwise from 0=Up
        
        self.ICComp = ADV19_IntcodeComputer(sIntcodeProg=lIntCode, lArgs=lArgs, iVerbosity=iICVerbosity)
        if self.Verbosity >= 1: print( "[ROBOT] Waiting to Start")


    def RunSequence(self):
        if self.Verbosity >= 1: print( "[ROBOT] Restarting Program Sequence")
        self.ICComp.RestartProgram()



    #==============================================================================================
    # DECEMBER11 PAINTING FUNCTIONS
    #==============================================================================================
 

    def MoveRobot(self, iMoveCmd):
        if self.Verbosity >= 2: print( "[ROBOT] Moving Robot from ", self.Position, self.Heading)
        
        if iMoveCmd == 0:
            self.Heading = (self.Heading - 1) % 4 
        elif iMoveCmd == 1:
            self.Heading = (self.Heading + 1) % 4 

        if self.Heading == 0:
            self.Position[1] -= 1 
        elif self.Heading == 1:
            self.Position[0] += 1 
        elif self.Heading == 2:
            self.Position[1] += 1 
        elif self.Heading == 3:
            self.Position[0] -= 1

        if      self.Position[1] < 0 or self.Position[1] > len(self.PanelArray)-1 \
            or  self.Position[0] < 0 or self.Position[0] > len(self.PanelArray[0])-1:
            self.ExpandCanvas()

        if self.Verbosity >= 2: print( "   Moved Robot to ", self.Position, self.Heading)


    def SetVerbosity(self, iVerbosity=1):
        self.Verbosity = iVerbosity        
        if self.Verbosity > 0: print( "[ROBOT] Robot Verbosity now %d" % self.Verbosity)


    def strPanelArray(self, lArray = [], bShowBot=True, iOffset = 0):
        if lArray == []:
            lArr = self.PanelArray
        else:
            lArr = lArray
        iH = len(lArr)
        iW = len(lArr[0])
        
        if self.Verbosity >= 4: print( "[ROBOT] Panel Size is %d rows, %d columns" % (iH, iW) )
        
        strArr = ' ' * iOffset
        
        strArr += '+' + '-'*iW + '+\n'
        for iY in range(iH):
            strArr += ' ' * iOffset + '|'

            for iX in range(iW):
                
                if [iX,iY] == self.Position and bShowBot:
                    if self.Heading == 0:
                        strArr += '^'
                    elif self.Heading == 1:
                        strArr += '>'
                    elif self.Heading == 2:
                        strArr += 'v'
                    elif self.Heading == 3:
                        strArr += '<'
                    else:
                        strArr += 'X'    
                else:
                    tPan = self.PanelArray[iY][iX]
                    tPan = tPan % 10
                    if tPan == 0:
                        strArr += ' '   
                    elif tPan == 1:
                        strArr += '#'   
                    else:
                        strArr += '{' + str(tPan) + '}'   
        
            strArr += '|\n'
        strArr += ' ' * iOffset + '+' + '-'*iW + '+'

        return strArr

    def PrintPanelArray(self, lArray = [], bShowBot=True):
        print( self.strPanelArray(lArray = [], bShowBot=True)) 


    def GetPanelColor(self, lPosition=[0,0]):
        if self.Verbosity >= 2: print( "[ROBOT] Getting Panel Color @ ", lPosition)
        tColor = self.PanelArray[lPosition[1]][lPosition[0]]
        tColor = tColor % 10
        if self.Verbosity >= 2: print( "     Color is ", tColor)
        return tColor


    def ExpandCanvas(self):
        if self.Verbosity >= 2: print( "[ROBOT] Expanding Panel Array") 
        if self.Verbosity >= 5: self.PrintPanelArray()
        
        oldH = len(self.PanelArray)
        oldW = len(self.PanelArray[0])
        oldX = self.Position[0]
        oldY = self.Position[1]
        #print( "Old Position: [%d, %d]   Old Size:  [%d, %d]" % (oldX, oldY, oldH, oldW) ) 

        tNewPanels = []

        if oldX < 0:
            #print("PREPEND COL")
            for tRow in self.PanelArray:
                tNewPanels.append( [0] + tRow[:] )
            self.Position[0] = oldX + 1
                
        elif oldX > oldW-1:
            #print("APPEND COL")
            for tRow in self.PanelArray:
                tNewPanels.append( tRow[:] + [0] )
            
        elif oldY < 0:
            #print("PREPEND ROW")
            
            tNewPanels.append( [0] * oldW )
            for tRow in self.PanelArray:
                tNewPanels.append( tRow )

            self.Position[1] = oldY + 1
         
        elif oldY > oldH-1:
            #print("APPEND ROW")
            tNewPanels = self.PanelArray[:]
            tNewPanels.append( [0] * oldW )


        self.PanelArray = tNewPanels
        if self.Verbosity >= 5: self.PrintPanelArray()
      
        

    def HaxBlankCanvas(self, iSize=120):
        tCanvas = []
        for iY in range(iSize):
            tRow = []
            for iX in range(iSize):
                tRow.append(0)
            tCanvas.append(tRow)
            
        self.Position = [ floor(iSize/2),floor(iSize/2) ]
        
        return tCanvas       
        
            

    def RunPaintSequence(self, iStartColor = 0):
        if self.Verbosity >= 1: print( "[ROBOT] Running Paint Sequence")
        
        self.PanelArray = [[0,0],[0,0]]
        #self.PanelArray = self.HaxBlankCanvas(150)
        self.PanelArray[self.Position[1]][self.Position[0]] = iStartColor 
        
        self.ICComp.RestartProgram()        

        if self.Verbosity >= 4: self.PrintPanelArray()        

        while self.ICComp.MachineState != 99:
        
            if self.Verbosity >= 2: print( "\n\n[ROBOT] SEQUENCE STEP")
            
            tColor = self.GetPanelColor( self.Position )
            
            self.ICComp.AppendStdIn([tColor])
            self.ICComp.Continue()
            
            tPaintColor, tMoveCmd = self.ICComp.StdOut[-2:]
            if self.Verbosity >= 2: print( "[ROBOT] Paint with %d, Move %d " % (tPaintColor, tMoveCmd) )
             
            self.PanelArray[self.Position[1]][self.Position[0]] = tPaintColor + 10

            self.MoveRobot(tMoveCmd)

            if self.Verbosity >= 4: self.PrintPanelArray()
            if self.Verbosity >= 4: input()
            
        if self.Verbosity >= 1: self.PrintPanelArray()

        iPainted = 0
        for iRow in self.PanelArray:
            for iPanel in iRow:
                if iPanel >= 10: iPainted += 1
        
        return iPainted, self.strPanelArray()