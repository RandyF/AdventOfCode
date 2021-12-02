from Advent2019_IntCode_DEC13 import ADV19_IntcodeComputer
from math import floor
from random import randint
import networkx as nx

class ADV19_RepairDroid(object):

    def __init__(self, lIntCode = [], lArgs=[], lInitPosition=[0, 0], iVerbosity = 0, iICVerbosity = 0):
        self.SetVerbosity(iVerbosity)
        if self.Verbosity >= 1: print( "[ROBOT] Initializing Puzzle Robot")
        
        self.Position = lInitPosition[:]

        
        self.ICComp = ADV19_IntcodeComputer(sIntcodeProg=lIntCode, lArgs=lArgs, iVerbosity=iICVerbosity)
        if self.Verbosity >= 1: print( "[ROBOT] Waiting to Start")


    def RunSequence(self):
        if self.Verbosity >= 1: print( "[ROBOT] Restarting Program Sequence")
        self.ICComp.RestartProgram()



    #==============================================================================================
    # DECEMBER15 REPAIR FUNCTIONS
    #==============================================================================================
 


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
                        strArr += 'D'    
                else:
                    tPan = self.PanelArray[iY][iX]
                    tPan = tPan % 10
                    if tPan == 0:
                        strArr += ' '   
                    elif tPan == 1:
                        strArr += '.'   
                    elif tPan == 2:
                        strArr += 'O'   
                    elif tPan == 3:
                        strArr += '#'   
                    else:
                        strArr += '{' + str(tPan) + '}'   
        
            strArr += '|\n'
        strArr += ' ' * iOffset + '+' + '-'*iW + '+'

        return strArr

    def PrintPanelArray(self, lArray = [], bShowBot=True):
        print( self.strPanelArray(lArray = [], bShowBot=True)) 


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
        

    def MoveRobot(self, iMoveDir = 0):
        #north (1), south (2), west (3), and east (4)
        if self.Verbosity >= 2: print( "[ROBOT] Moving Robot from ", self.Position)
        
        self.ICComp.AppendStdIn([iMoveDir])
        self.ICComp.Continue()
        
        iStatusCode = self.ICComp.StdOut[-1]
        print("[ROBOT] Returned Status Code", iStatusCode)
        bMoved = False
        if iStatusCode != 0: bMoved = True
        
        if iMoveDir == 1:
            if iStatusCode == 0:
                self.PanelArray[ self.Position[1]-1 ][ self.Position[0] ] = 3
            else:
                self.PanelArray[ self.Position[1] ][ self.Position[0] ] = iStatusCode
                self.Position[1] -= 1
                
        elif iMoveDir == 2:
            if iStatusCode == 0:
                self.PanelArray[ self.Position[1]+1 ][ self.Position[0] ] = 3
            else:
                self.PanelArray[ self.Position[1] ][ self.Position[0] ] = iStatusCode
                self.Position[1] += 1
                
        elif iMoveDir == 3:
            if iStatusCode == 0:
                self.PanelArray[ self.Position[1] ][ self.Position[0]+1 ] = 3
            else:
                self.PanelArray[ self.Position[1] ][ self.Position[0] ] = iStatusCode
                self.Position[0] += 1
                
        elif iMoveDir == 4:
            if iStatusCode == 0:
                self.PanelArray[ self.Position[1] ][ self.Position[0]-1 ] = 3
            else:
                self.PanelArray[ self.Position[1] ][ self.Position[0] ] = iStatusCode
                self.Position[0] -= 1
                
        else:
            pass
        

        if self.Verbosity >= 2: print( "   Robot @ ", self.Position)

        return bMoved


    def GetLocInfo(self, lPos = []):
        if lPos == []: lPos = self.Position
        #north (1), south (2), west (3), and east (4)
        tlLoc = [999, 0, 0, 0, 0]
        tlLoc[0] = self.PanelArray[ lPos[1] ][ lPos[0] ]
        tlLoc[1] = self.PanelArray[ lPos[1]-1 ][ lPos[0] ]
        tlLoc[2] = self.PanelArray[ lPos[1]+1 ][ lPos[0] ]
        tlLoc[3] = self.PanelArray[ lPos[1] ][ lPos[0]+1 ]
        tlLoc[4] = self.PanelArray[ lPos[1] ][ lPos[0]-1 ]
        return tlLoc


    def RunMappingSequence(self):
        if self.Verbosity >= 1: print( "[ROBOT] Running Mapping Sequence")
        
        #self.PanelArray = [[0,0],[0,0]]
        self.PanelArray = self.HaxBlankCanvas(50)
   
        self.ICComp.RestartProgram()        

        lPath = []
        curDir = 1
        while True:

            print("[ROBOT] Moving", curDir)
            bMoved = self.MoveRobot(curDir)

            lLoc = self.GetLocInfo()
            print(lLoc)
            #north (1), south (2), west (3), and east (4)
            
            if lLoc[1] == 0:
                curDir = 1
            elif lLoc[3] == 0:
                curDir = 3
            elif lLoc[2] == 0:
                curDir = 2
            elif lLoc[4] == 0:
                curDir = 4
            else:
                curDir = randint(1,4)
            
            

            print( curDir )            
            if self.Verbosity >= 4: self.PrintPanelArray() 
            input()


       
        
        return self.strPanelArray()
        
        
    def Cheated(self):
        territory = set()
        oxygen = None
        x, y = 0, 0

        while not oxygen:
            iMoveDir = randint(1, 4)
            self.ICComp.AppendStdIn([iMoveDir])
            self.ICComp.Continue()
            iStatusCode = self.ICComp.StdOut[-1]

            #  hit a wall
            if iStatusCode == 0:
                #print("wall")
                continue
            # found oxygen
            if iStatusCode == 2:
                #print("oxy")
                oxygen = (x, y)
            # found open space
            #print("moving")
            territory.add((x, y))
            if iMoveDir == 1:
                x -= 1
            elif iMoveDir == 2:
                x += 1
            elif iMoveDir == 3:
                y -= 1
            elif iMoveDir == 4:
                y += 1       
                
        G = nx.Graph()
        G.add_node((0, 0))
        # build up graph edges
        for (x1, y1) in territory:
            for (x2, y2) in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
                i, j = (x1 + x2, y1 + y2)
                if (i, j) in territory:
                    G.add_edge((x1, y1), (i, j))

        print("path:", len(nx.shortest_path(G, (0, 0), oxygen)))  # part 1
        print("flood:", nx.eccentricity(G, v=oxygen) + 1)  # part 2