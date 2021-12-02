from math import floor, pi, gcd, log
from cmath import polar
from sys import maxsize, exit
from time import time
from itertools import permutations
from copy import deepcopy
from datetime import date, datetime

from Advent2019_IntCode_DEC13 import ADV19_IntcodeComputer
from Advent2019_Robot_DEC11 import ADV19_PuzzleRobot
from Advent2019_Arcade_DEC13 import ADV19_ArcadeCabinet
from Advent2019_RepairDroid_DEC15 import ADV19_RepairDroid

class OrbitalObject(object):

    def __init__(self, sName = 'UNCHARTED', oParent = None):
        self.Name = sName
        self.Parent = oParent

    def OrbitPath(self):
        lPath = []
        tParent = self.Parent
        while tParent != None:
            lPath.append(tParent.Name)
            tParent = tParent.Parent
        return lPath

    def CountOrbits(self):
        return len(self.OrbitPath())

        

class ADVENT2019(object):

    Verbosity = 0

    def __init__(self, iVerbosity = 0):
        self.Verbosity = iVerbosity
        if self.Verbosity > 0 : print("Initialized ADVENT2019!")

        
    #==============================================================================================
    # DECEMBER01
    #==============================================================================================
    
    def CalcFuelForMass(self, iMass = 0):
        #Fuel required to launch a given module is based on its mass. Specifically,
        #to find the fuel required for a module, take its mass, divide by three,
        #round down, and subtract 2.
        tFuel = floor( iMass / 3 ) - 2
        if self.Verbosity == 201901: print("      Fuel Required for %d is %d." % ( iMass, tFuel ) )
        return tFuel

    
    def CalcTyranyFuelForMass(self, iMass = 0 ):
        #[F]or each module mass, calculate its fuel and add it to the total. Then,
        #treat the fuel amount you just calculated as the input mass and repeat the
        #process, continuing until a fuel requirement is zero or negative.    
        if self.Verbosity == 201901: print("   Calculating Tyranical Fuel for Mass %d... " % iMass )
        tReq = self.CalcFuelForMass(iMass)
        
        if tReq > 0:
            if self.Verbosity == 201901: print("         But this fuel needs fuel!")
            tReq += self.CalcTyranyFuelForMass( tReq )
        else:
            if self.Verbosity == 201901: print("         No More Fuel Requred!")
            tReq = 0
            
        return tReq

    
    def DEC01A_TV(self, iMass = 0):
        if self.Verbosity == 201901: print("\nDEC01A Single Mass Test Vector")
        tFuel = self.CalcFuelForMass(iMass)
        if self.Verbosity == 201901: print("   ** Fuel Requred: %d **" % tFuel)
        return tFuel
        
        
    def DEC01A(self, lModules = []):
        #The Fuel Counter-Upper needs to know the total fuel requirement. To find it,
        #individually calculate the fuel needed for the mass of each module
        #(your puzzle input), then add together all the fuel values.
        if self.Verbosity == 201901: print("\nDEC01A Puzzle Computation")
        iFuelRequired = 0
        for iMod in lModules:
            iFuelRequired += self.CalcFuelForMass( iMod )
        if self.Verbosity == 201901: print(" ** Total Fuel Required is %d **" % iFuelRequired)
        return iFuelRequired
        

    def DEC01B_TV(self, iMass = 0):
        if self.Verbosity == 201901: print("\nDEC01B Single Mass Test Vector")
        tFuel = self.CalcTyranyFuelForMass(iMass)
        if self.Verbosity == 201901: print("  Tyrannty Fuel Requred: %d" % tFuel)
        return tFuel        


    def DEC01B(self, lModules = []):
        #What is the sum of the fuel requirements for all of the modules on your
        #spacecraft when also taking into account the mass of the added fuel?
        if self.Verbosity == 201901: print("\nDEC01B Puzzle Computation")
        iFuelRequired = 0
        for iMod in lModules:
            iFuelRequired += self.CalcTyranyFuelForMass( iMod )
        if self.Verbosity == 201901: print(" ** Tyrannical Fuel Required is %d **" % iFuelRequired)
        return iFuelRequired


    #==============================================================================================
    # DECEMBER02
    #==============================================================================================

    def RunIntcode( self, IntCode = [], lArgs = [], iVerbosity = 0 ):
        ICComp = ADV19_IntcodeComputer(IntCode, lArgs=lArgs, iVerbosity=iVerbosity)
        ICComp.RestartProgram()
        #ICComp.PrintIncodeMEM()
        
        
    def DEC02A_TV(self, IntCode = [], iVerbosity = 0):
        if self.Verbosity == 201902: print("\nDEC02A Test Vectors")
        self.RunIntcode(IntCode=IntCode, iVerbosity=iVerbosity)


    def DEC02A(self, IntCode = [], iNoun = 12, iVerb = 2, iVerbosity = 0):
        #Once you have a working computer, the first step is to restore the gravity 
        #assist program (your puzzle input) to the "1202 program alarm" state it had
        #just before the last computer caught fire. To do this, before running the
        #program, replace position 1 with the value 12 and replace position 2 with the
        #value 2. What value is left at position 0 after the program halts?
        if self.Verbosity == 201902: print("\nDEC02A Puzzle Calculation N=%d V=%d" %( iNoun, iVerb ))
        ICComp = ADV19_IntcodeComputer(IntCode, iVerbosity=iVerbosity)
        ICComp.IntcodeMEM[1] = iNoun
        ICComp.IntcodeMEM[2] = iVerb       
        ICComp.RestartProgram()

        return ICComp.IntcodeMEM[0]
        
        
    def DEC02B(self, IntCode = [], iTarget = 19690720, iVerbosity = 0):
        #"With terminology out of the way, we're ready to proceed. To complete the
        #gravity assist, you need to determine what pair of inputs produces the output 19690720."

        #The inputs should still be provided to the program by replacing the values at
        #addresses 1 and 2, just like before. In this program, the value placed in address 1
        #is called the noun, and the value placed in address 2 is called the verb. Each of
        #the two input values will be between 0 and 99, inclusive.

        #Once the program has halted, its output is available at address 0, also just like
        #before. Each time you try a pair of inputs, make sure you first reset the computer's
        #memory to the values in the program (your puzzle input) - in other words, don't reuse
        #memory from a previous attempt.

        #Find the input noun and verb that cause the program to produce the output 19690720.
        #What is 100 * noun + verb? (For example, if noun=12 and verb=2, the answer would be 1202.)
        
        for tNoun in range(100):
            for tVerb in range(100):
                if self.Verbosity == 201902: print("Checking Noun = %d and Verb = %d... " % (tNoun, tVerb), end='')
                tResult = self.DEC02A(IntCode, iNoun = tNoun, iVerb = tVerb)
                if tResult == iTarget:
                    if self.Verbosity == 201902: print(" got %d, our Target!" % tResult)
                    iSolution = 100 * tNoun + tVerb
                    return iSolution
                else:
                    if self.Verbosity == 201902: print(" got %d" % tResult)
                
        print("Could Not Find Solution!  Poor Dead Elves.")
        return -1
        

    #==============================================================================================
    # DECEMBER03
    #==============================================================================================
            
    def DistanceManhattan(self, Point):
        #Because the wires are on a grid, use the Manhattan distance for this measurement.
        return abs(Point[0]) + abs(Point[1])

 
    def GenWire( self, WireString ):
        #Opening the front panel reveals a jumble of wires. Specifically, two wires are
        #connected to a central port and extend outward on a grid. You trace the path
        #each wire takes as it leaves the central port, one wire per line of text (your
        #puzzle input).
        tWire = []
        tdWire = {}  
        
        lWireSegments = WireString.split(',')
        
        tCurPoint = [0,0]
        tCurMeta = [0,0, 0, 0]

        for tSeg in lWireSegments:

            tDir = tSeg[0]
            tLen = int(tSeg[1:])

            for tPoint in range(tLen):

                if tDir == 'R':
                    tCurPoint[1] += 1
                elif tDir == 'U':
                    tCurPoint[0] += 1
                elif tDir == 'L':
                    tCurPoint[1] -= 1
                elif tDir == 'D':
                    tCurPoint[0] -= 1
                else:
                    print("Invalid Direction!")
     
                tCurMeta[0] = tCurPoint[0]
                tCurMeta[1] = tCurPoint[1]
                tCurMeta[2] += 1
                tCurMeta[3] = self.DistanceManhattan(tCurPoint)

                taCurPoint = tCurPoint[:]
                tWire.append(taCurPoint)
                tdWire[str(taCurPoint)] = tCurMeta[:]

        if self.Verbosity == 201903: print( "Wire String: [%s...%s] has %d points." % (WireString[:17], WireString[-17:], len(tWire)) )
        #print( "Wire Points: ", tWire )
        #print( "\ndict: ", tdWire )
        #print( "\nkeys: ", tdWire.keys() )
        return tWire, tdWire

    def ProcessMatches( self, dWirePointsA = {}, dWirePointsB = {} ):
        #The wires twist and turn, but the two wires occasionally cross paths. To fix
        #the circuit, you need to find the intersection point closest to the central port. 
        lsMatches = set(dWirePointsA.keys()).intersection(dWirePointsB.keys())

        if self.Verbosity == 201903: print("Match Points: ", len(lsMatches))
        #if self.Verbosity == 201903: print(lsMatches)
        
        lMatchA = []
        lMatchB = []

        minSteps = maxsize
        minDist = maxsize
        for ptMatch in lsMatches:
            #print(dWirePointsA[ptMatch], dWirePointsB[ptMatch], end='')

            if dWirePointsA[ptMatch][3] < minDist:
                minDist = dWirePointsA[ptMatch][3]
            #print(dWirePointsA[ptMatch][0], dWirePointsA[ptMatch][1], dWirePointsA[ptMatch][2], dWirePointsB[ptMatch][2], dWirePointsA[ptMatch][2] + dWirePointsB[ptMatch][2])

            tStepTot = dWirePointsA[ptMatch][2] + dWirePointsB[ptMatch][2]
            if tStepTot < minSteps:
                minSteps = tStepTot    
                
        if self.Verbosity == 201903: print( "Minimum Distance: %d    Minimum Signal Steps: %d" % (minDist, minSteps) )
        
        return minDist, minSteps
        
                
    def DEC03(self, sWireA = '', sWireB = '' ):
        t0 = time()
        [lWireA, dWireA] = self.GenWire(sWireA)
        [lWireB, dWireB] = self.GenWire(sWireB)
        t1 = time()
        
        [minDist, minSteps] = self.ProcessMatches( dWireA, dWireB )
        
        return minDist, minSteps, (t1 - t0) * 100 
    

    #==============================================================================================
    # DECEMBER04
    #==============================================================================================
    # Your puzzle input is still 156218-652527.

    sDupes = ['00', '11', '22', '33', '44', '55', '66', '77', '88', '99']

    def CheckValidPassA(self, iPass):
        # It is a six-digit number.
        # The value is within the range given in your puzzle input.
        # Two adjacent digits are the same (like 22 in 122345).
        # Going from left to right, the digits never decrease; they only ever increase or stay
        # the same (like 111123 or 135679).
        # 111111 meets these criteria (double 11, never decreases).
        # 223450 does not meet these criteria (decreasing pair of digits 50).
        # 123789 does not meet these criteria (no double).
        sPass = str(iPass)

        if len(sPass) != 6: return False

        bDupeValid = False
        for dupe in self.sDupes:
            #print sPass, dupe
            if dupe in sPass:
                #print "Got a Dupe", dupe
                bDupeValid = True

        if not bDupeValid: return False      

        return int(sPass[0]) <= int(sPass[1]) <= int(sPass[2]) <= int(sPass[3]) <= int(sPass[4]) <= int(sPass[5])

    def CheckValidPassB(self, iPass):
        # An Elf just remembered one more important detail: the two adjacent matching
        # digits are not part of a larger group of matching digits.

        # Given this additional criterion, but still ignoring the range rule, the
        # following are now true:

        # 112233 meets these criteria because the digits never decrease and all repeated
        # digits are exactly two digits long.
        # 123444 no longer meets the criteria (the repeated 44 is part of a larger group
        # of 444).
        # 111122 meets the criteria (even though 1 is repeated more than twice, it still
        # contains a double 22).
        # How many different passwords within the range given in your puzzle input meet all of the criteria?
        sPass = str(iPass)

        if len(sPass) != 6: return False

        lDupeList = []
        for dupe in self.sDupes:
            #print sPass, dupe
            if dupe in sPass:
                #print "Got a Dupe", dupe
                lDupeList.append(dupe)
        #print lDupeList

        if lDupeList == []:
            return False

        lDupeCnt = []
        for sDupe in lDupeList:
            cDupe = sDupe[0]
            #print cDupe

            bGotStart = False
            iConCnt = 0

            for tChr in sPass:
                if bGotStart and tChr == cDupe:
                    #print "Got Start", tChr
                    iConCnt += 1               
                elif tChr == cDupe:
                    #print "Got Start", tChr
                    iConCnt = 1
                    bGotStart = True
            lDupeCnt.append(iConCnt)       
            #print "sDupe:", tChr, cDupe, iConCnt

        if min(lDupeCnt) != 2:
            return False

        return int(sPass[0]) <= int(sPass[1]) <= int(sPass[2]) <= int(sPass[3]) <= int(sPass[4]) <= int(sPass[5])

    def CheckRangeA(self, iStart, iEnd):
        tCnt = 0
        for tPass in range(iStart, iEnd):
            #if (tCnt % 100) == 0: print '.',
            if self.CheckValidPassA(tPass): tCnt += 1
        return tCnt

    def CheckRangeB(self, iStart, iEnd):
        tCnt = 0
        for tPass in range(iStart, iEnd):
            #if (tCnt % 100) == 0: print '.',
            bValid = self.CheckValidPassB(tPass)
            if bValid:
                #print tPass
                tCnt += 1
        return tCnt

    #==============================================================================================
    # DECEMBER05
    #==============================================================================================

    def DEC05(self, IntCode = [], lArgs = [], iVerbosity = 0):
        if self.Verbosity == 201905: print( "\nDEC05A Running Intcode")
        ICComp = ADV19_IntcodeComputer(IntCode, lArgs=lArgs, iVerbosity=iVerbosity)
        ICComp.RestartProgram()
        if iVerbosity >= 5: ICComp.PrintIncodeMEM()
        return ICComp.StdOut


    #==============================================================================================
    # DECEMBER06
    #==============================================================================================

    OrbObjects = {}

    def LoadObjects(self, sInData = ''):
        self.OrbObjects = {}
        for tPair in sInData.strip().split('\n'):
            sBase, sOrbiter = tPair.split(')')
            #print '[DATA] %s is orbiting %s' % (sOrbiter, sBase)

            if sBase in self.OrbObjects:
                #print "Have Base %s in list @ " % sBase, self.OrbObjects[sBase]
                pass
            else:
                self.OrbObjects[sBase] = OrbitalObject(sBase)

            if sOrbiter in self.OrbObjects:
                #print "Have Sattelite %s in list @" % sOrbiter, self.OrbObjects[sOrbiter]
                pass
            else:
                self.OrbObjects[sOrbiter] = OrbitalObject(sOrbiter, self.OrbObjects[sBase])

            self.OrbObjects[sOrbiter].Parent = self.OrbObjects[sBase]

    def DEC06A(self, sInData = ''):
        self.LoadObjects(sInData)
        sum = 0
        for tSat in self.OrbObjects:
            #print tSat, "has %d orbits" % self.OrbObjects[tSat].CountOrbits()
            sum += self.OrbObjects[tSat].CountOrbits()
        return sum

    def DEC06B(self, sInData = ''):
        self.LoadObjects(sInData)
        lYOU = self.OrbObjects['YOU'].OrbitPath()
        lSAN = self.OrbObjects['SAN'].OrbitPath()
        
        common =  set(lYOU).intersection(lSAN)

        min = maxsize
        for tObj in common:
            dist = lYOU.index(tObj) + lSAN.index(tObj)
            if dist < min: min = dist

        return min
        


    #==============================================================================================
    # DECEMBER07
    #==============================================================================================

    Amplifiers = []

    def DEC07_CalcSingleAmplification(self, IntCode = [], lPhases = [], iVerbosity = 0):
        self.Amplifiers = []
        for _ in range(5):
            self.Amplifiers.append( ADV19_IntcodeComputer(IntCode, iVerbosity=iVerbosity) )
        #print(self.Amplifiers)

        iLastOut = 0
        for iAmp in range(5):
            self.Amplifiers[iAmp].LoadProgramToMemory( lArgs=[lPhases[iAmp], iLastOut] )
            self.Amplifiers[iAmp].RestartProgram()
            iLastOut = self.Amplifiers[iAmp].StdOut[0]
        
        return iLastOut

    def DEC07A(self, IntCode = [], iVerbosity = 0):
        # Get all permutations of [1, 2, 3] 
        perm = permutations([0, 1, 2, 3, 4]) 
          
        maxThrust = 0
        for i in list(perm): 
            ampOut = self.DEC07_CalcSingleAmplification(IntCode = IntCode, lPhases = i, iVerbosity = iVerbosity)
            if ampOut > maxThrust: maxThrust = ampOut
        
        return maxThrust

    def DEC07_CalcMultAmplification(self, IntCode = [], lPhases = [], iVerbosity = 0):
        self.Amplifiers = []
        for iAmp in range(5):
            self.Amplifiers.append( ADV19_IntcodeComputer(IntCode, iVerbosity=iVerbosity) )
            self.Amplifiers[iAmp].LoadProgramToMemory( lArgs=[lPhases[iAmp]] )
            self.Amplifiers[iAmp].RestartProgram()
            
        iLastOut = 0
        AmpsRunning = 5
        
        while AmpsRunning:
            AmpsRunning = 0
            for iAmp in range(5):
                self.Amplifiers[iAmp].AppendStdIn([iLastOut])
                self.Amplifiers[iAmp].Continue()
                iLastOut = self.Amplifiers[iAmp].StdOut[-1]
                #print( self.Amplifiers[iAmp].MachineState )
                if self.Amplifiers[iAmp].MachineState != 99: AmpsRunning += 1
            
        return iLastOut

    def DEC07B(self, IntCode = [], iVerbosity = 0):
        perm = permutations([5, 6, 7, 8, 9])   

        maxThrust = 0
        for i in list(perm): 
            ampOut = self.DEC07_CalcMultAmplification(IntCode = IntCode, lPhases = i, iVerbosity = iVerbosity)
            if ampOut > maxThrust: maxThrust = ampOut
        
        return maxThrust        
      
    #==============================================================================================
    # DECEMBER08
    #==============================================================================================

    def UnpackSIFStream(self, sSIF = '123456789012', iWidth = 3, iHeight = 2):
        
        lLayers = []
        lFrames = []
        
        iLayer = 0
        iFrameSize = iWidth * iHeight
        iIdx = 0

        while iIdx < len(sSIF):
            lFrame = [char for char in sSIF[iIdx:iIdx+iFrameSize]]

            #print("New Frame: ", lFrame)
            lFrames.append(lFrame)           
            
            tLayer = self.FrameToLayer(lFrame, iWidth = iWidth, iHeight = iHeight)
            #print("New Layer: ", tLayer)
            lLayers.append(tLayer)

            iIdx += iFrameSize
    
        return lLayers,  lFrames


    def FrameToLayer(self, sFrame = '123456', iWidth = 3, iHeight = 2):
        iFrameSize = iWidth * iHeight
        tLayer = []            
        for iRow in range(iHeight):
            iCdx = iRow * iWidth
            lRow = []
            for tPx in sFrame[iCdx:iCdx+iWidth]:
                lRow.append(tPx)
            tLayer.append(lRow) 
        return tLayer
   
        
    def DecodeSIFImage(self, sSIF ='', iWidth = 0, iHeight = 0):
        lDecoded = '2'*iWidth*iHeight
        #print("Blank Decoded Image:")
        #self.PrintImage(lDecoded, iWidth = iWidth, iHeight = iHeight)
        #print(sSIF, lDecoded)
        lLayers, lFrames = self.UnpackSIFStream(sSIF =sSIF, iWidth = iWidth, iHeight = iHeight)
        for lFrame in lFrames:
            #print("Next Layer: ", lFrame, lDecoded)
            tDecode = ''
            for iIdx in range(iWidth*iHeight):
                #print(lDecoded[iIdx], lFrame[iIdx])
                if lDecoded[iIdx] == '2':
                    tDecode += lFrame[iIdx]
                else:
                    tDecode += lDecoded[iIdx]
            lDecoded = tDecode
            #print(lDecoded)
                 
        #print("decoded", lDecoded)

        tFinalImage = self.FrameToLayer(sFrame =lDecoded, iWidth = iWidth, iHeight = iHeight)
        return tFinalImage


    def StringImage(self, lImage = [], iWidth = 0, iHeight = 0, iOffset=0):
        tStr = ' ' * iOffset
        tStr += '+' + '-' * iWidth + '+\n'

        for iRx in range(iHeight):
            tStr += ' ' * iOffset + '|'
            for iCx in range(iWidth):
                if lImage[iRx][iCx] == '0': 
                    tStr += ' '
                elif lImage[iRx][iCx] == '1': 
                    tStr += '#'
                else:
                    tStr += '.'
            tStr += '|\n'

        tStr += ' ' * iOffset + '+' + '-' * iWidth + '+'

        
        return tStr
    
    def PrintImage(self, lImage = [], iWidth = 0, iHeight = 0, iOffset=0):
        print( self.StringImage(lImage = lImage, iWidth = iWidth, iHeight = iHeight, iOffset=iOffset) )


    def DEC08A(self, sSIF = ''):
        lLayers, lFrames = self.UnpackSIFStream(sSIF = sSIF, iWidth =25, iHeight =6)
        
        iMin = maxsize
        iMinLayer = maxsize
        for iIdx in range(len(lFrames)):
            lFrame = lFrames[iIdx]
            iLayerZeros = lFrame.count('0')

            if iLayerZeros < iMin:
                iMin = iLayerZeros
                iMinLayer = iIdx
                
                
        #print( iMinLayer, iMin, lFrames[iMinLayer].count('1'), lFrames[iMinLayer].count('2'), lFrames[iMinLayer].count('1') * lFrames[iMinLayer].count('2'))
      
        return lFrames[iMinLayer].count('1') * lFrames[iMinLayer].count('2')


    def DEC08B(self, sSIF = '', iOffset = 0):        
        lImg = self.DecodeSIFImage(sSIF = sSIF, iWidth =25, iHeight =6)
        return self.StringImage(lImg, iWidth =25, iHeight =6, iOffset=iOffset)


    #==============================================================================================
    # DECEMBER09
    #==============================================================================================

    def DEC09A(self, IntCode = [], iVerbosity=0):
        if self.Verbosity == 201909: print( "\nDEC09A Running Intcode")
        ICComp = ADV19_IntcodeComputer(IntCode, lArgs=[1], iVerbosity=iVerbosity)
        ICComp.RestartProgram()
        if iVerbosity >= 5: ICComp.PrintIncodeMEM()
        return ICComp.StdOut[-1]       

    def DEC09B(self, IntCode = [], iVerbosity=0):
        if self.Verbosity == 201909: print( "\nDEC09B Running Intcode")
        ICComp = ADV19_IntcodeComputer(IntCode, lArgs=[2], iVerbosity=iVerbosity)
        ICComp.RestartProgram()
        if iVerbosity >= 5: ICComp.PrintIncodeMEM()
        return ICComp.StdOut[-1] 


    #==============================================================================================
    # DECEMBER10
    #==============================================================================================
 
    def ParseAsteroidMap(self, sMap = ''):
        lRows = sMap.strip().split('\n')
        #print(lRows, len(lRows))
        lMap = []
        dMap = {}
        iRIdx = 0
        for tR in lRows:
            tRow = tR.strip()
            #print(tRow, len(tRow) )
            iCIdx = 0
            for tCol in tRow:
                #print(tCol)
                if tCol == '#':
                    #print(iRIdx, iCIdx)
                    lMap.append( [iCIdx, iRIdx ] )
                    tKey = "%d,%d"% (iCIdx, iRIdx )
                    dMap[tKey] = [iCIdx, iRIdx ]
                iCIdx += 1
            iRIdx += 1
        
        #print( [iRIdx, iCIdx] )
        #print( lMap )
        return lMap, dMap, [iCIdx, iRIdx]


    def LinePoints(self, lPoint=[3,4], lDest=[1,0] ):
        #print( "Evaluating Line: ", lPoint, lDest )

        dLinePoints = {}

        if lPoint[0] == lDest[0]:
            #print("vert")
            iX = lPoint[0]
            tMin = min(lDest[1], lPoint[1])
            tMax = max(lDest[1], lPoint[1])
            for tY in range(tMin, tMax+1):
                if [iX, int(tY)] != lPoint:
                    #print( [iX, int(tY)])
                    tDist = abs(lPoint[0] - iX) + abs(lPoint[1] - int(tY)) 
                    dLinePoints[ "%d,%d"%(iX, int(tY)) ] = [iX, int(tY), tDist]    
            
        else:
            tM = (float(lDest[1]) - float(lPoint[1])) / (float(lDest[0]) - float(lPoint[0]))
            tB = float(lPoint[1]) - tM * float(lPoint[0])  
            #print( "Y = %0.2fx + %0.2f" % (tM, tB))

            tMin = min(lDest[0], lPoint[0])
            tMax = max(lDest[0], lPoint[0])
            for iX in range(tMin, tMax+1):
                tY = round(tM * iX + tB,8)
                if tY == int(tY):
                    if [iX, int(tY)] != lPoint:
                        #print( [iX, int(tY)])
                        tDist = abs(lPoint[0] - iX) + abs(lPoint[1] - int(tY)) 
                        dLinePoints[ "%d,%d"%(iX, int(tY)) ] = [iX, int(tY), tDist]

        return dLinePoints      

            
    def GenVisMap(self, lMap = [], dMap={}):                    
        dVisMap = {}
        iMaxVis = 0
        maxKey = ''
        for tBase in lMap:
            #print("Checking Asteroid", tBase)

            lVisibles = []

            for tDest in lMap:
                if tBase != tDest: 
                    #print( "Checking Between Points: ", tBase, tDest)
                    dLinePoints = self.LinePoints(tBase, tDest)
                    #print(dLinePoints)
                    setCross = set(dLinePoints.keys()).intersection(set(dMap.keys())) 
                    #print( setCross )
                    tMinDist = maxsize
                    tMinKey = ''
                    for key in setCross:
                        if dLinePoints[key][2] < tMinDist:
                            tMinKey = key
                            tMinDist = dLinePoints[key][2]
                    #print(  dLinePoints[tMinKey][0:2] )
                    if dLinePoints[tMinKey][0:2] not in lVisibles:
                        lVisibles.append(dLinePoints[tMinKey][0:2])
            
            tKey = "%d,%d"%(tBase[0], tBase[1])
            dVisMap[ tKey ] = len(lVisibles)
            if dVisMap[ tKey ] > iMaxVis:
                iMaxVis = dVisMap[ tKey ]
                maxKey = tKey
            
                    
            #print(lVisibles, len(lVisibles))
        #print(dVisMap, maxKey)    
        return dVisMap, maxKey


    def PrintVisMap(self, dVisMap = {}, iWidth = 5, iHeight = 5):
        spacing = len(str(dVisMap[max(dVisMap, key=dVisMap.get)]))
        for tY in range(iHeight):
            print()
            for tX in range(iWidth):
                tKey = "%d,%d"%(tX, tY)
                if tKey in dVisMap:
                    sVal = "%d" % dVisMap[tKey]
                    sVal = sVal + ' ' * (spacing - len(str(dVisMap[tKey])) + 1 )
                    print( sVal, end='')
                else:
                    sVal = '.' + ' ' * (spacing)
                    print(sVal, end='')
        print()        


    def ConvertToPolar(self, dMap = {}, lStation=[0,0]):

        lPolarMap = []
        for tAst in dMap:
            if dMap[tAst] != lStation:
                #print("\nConverting Point:    ", dMap[tAst])
                tZ = complex(dMap[tAst][0] - lStation[0], dMap[tAst][1] - lStation[1])
                tP = polar(tZ)
                #print("   Shifted, to Polar:", tP, math.degrees(tP[1]))
                tlP = [tP[0], tP[1] + (pi/2)]
                #print("   Rotated:          ", tlP, math.degrees(tlP[1]))
                if tlP[1] < 0: tlP[1] += 2*pi
                if tlP[1] > 2*pi: tlP[1] -= 2*pi
                #print("   Normalized:       ", tlP, math.degrees(tlP[1]))
                lPolarMap.append([tlP[1], tlP[0], dMap[tAst][0], dMap[tAst][1]] )

        return lPolarMap

    def GiantLAZR(self, dMap = {}, lStation=[0,0], iWidth = 5, iHeight = 5 ):
        #print(dMap)
        #print(lStation)

        lPolarMap = self.ConvertToPolar(dMap=dMap, lStation=lStation)
        
        dHits = {}
        
        #print("Firing My Lazers!!")
        lMissed = lPolarMap[:]
        iHit = 0
        while len(lMissed) > 0:
            lMissed.sort(key=lambda x:( x[0], x[1]))
            tCurAngle = maxsize
            tMissed = []
            for tAst in lMissed:

                if tCurAngle != tAst[0]:
                    #print("HIT!", tAst)
                    iHit += 1
                    dHits[ str(iHit)] = [tAst[2], tAst[3]]
                else:
                    #print("MISSED", tAst)
                    tMissed.append(tAst)
                
                tCurAngle = tAst[0]
            lMissed = tMissed[:]
            
            #print(lMissed)

        #print(dHits)
        return dHits
        

    def DEC10A(self, sMap = ''):
        lMap, dMap, [iWidth, iHeight] = self.ParseAsteroidMap(sMap)
        dVisMap, maxKey = self.GenVisMap(lMap, dMap)
        # self.PrintVisMap(dVisMap, iWidth = iWidth, iHeight = iHeight)
        tMax = maxKey.split(',')
        return (dVisMap[maxKey], [int(tMax[0]), int(tMax[1])])

    def DEC10B(self, sMap = '', lStation = [0,0]):
        lMap, dMap, [iWidth, iHeight] = self.ParseAsteroidMap(sMap)
        dHits = self.GiantLAZR( dMap = dMap, lStation=lStation, iWidth = iWidth, iHeight = iHeight)
        Hit200 = dHits[str(200)] 
        return 100 * Hit200[0] + Hit200[1]
 

    #==============================================================================================
    # DECEMBER11
    #==============================================================================================
    def DEC11A(self, lIntCode=[]):
        HullBot = ADV19_PuzzleRobot( lIntCode=lIntCode, lArgs=[], lInitPosition=[0, 0], iInitHeading=0, iVerbosity = 0, iICVerbosity = 0 )
        iPanelsPainted, strPanelArray = HullBot.RunPaintSequence()
        return iPanelsPainted
        
    def DEC11B(self, lIntCode=[]):
        HullBot = ADV19_PuzzleRobot( lIntCode=lIntCode, lArgs=[], lInitPosition=[0, 0], iInitHeading=0, iVerbosity = 0, iICVerbosity = 0 )
        iPanelsPainted, strPanelArray = HullBot.RunPaintSequence(iStartColor=1)
        return HullBot.strPanelArray(iOffset = 26)


    #==============================================================================================
    # DECEMBER12
    #==============================================================================================

    def PrintPlanets(self, dPlanets):
        print()
        print("Planet Dictionary @ ", hex(id(dPlanets)) )
        for kPlan in dPlanets:
            print( "pos=<x= %03d, y= %03d, z= %03d>, pos=<x= %03d, y= %03d, z= %03d> %s" % (\
                    dPlanets[kPlan][0][0], dPlanets[kPlan][0][1], dPlanets[kPlan][0][2], \
                    dPlanets[kPlan][1][0], dPlanets[kPlan][1][1], dPlanets[kPlan][1][2], kPlan ))

    def NBodyStep(self, dPlanets):
 
        for kPBase in dPlanets: 
            for kPCalc in dPlanets:
                if kPBase != kPCalc:
                    #print(kPBase, kPCalc)
                    for tP in range(len(dPlanets[kPBase][0])):
                        tDiff = dPlanets[kPBase][0][tP] - dPlanets[kPCalc][0][tP]
                        #print(dPlanets[kPBase][0][tP], dPlanets[kPCalc][0][tP], tDiff)
                        if tDiff > 0:
                                dPlanets[kPBase][1][tP] -= 1
                        if tDiff < 0:
                                dPlanets[kPBase][1][tP] += 1
             
        for kPBase in dPlanets:
            for tP in range(len(dPlanets[kPBase][0])):
                dPlanets[kPBase][0][tP] += dPlanets[kPBase][1][tP]


    def CalcEnergy(self, lPlanet = [[],[],1]):

        tPot = 0
        for tIdx in range(len(lPlanet[0])):
            tPot += abs(lPlanet[0][tIdx])
        tKin = 0
        for tIdx in range(len(lPlanet[0])):
            tKin += abs(lPlanet[1][tIdx])
        return tPot * tKin
            
        
    def DEC12A(self, dPlanets = {} , iSteps = 10):
        #self.PrintPlanets( dPlanets )
        for _ in range(iSteps):
            self.NBodyStep( dPlanets )
            #self.PrintPlanets( dPlanets )

        iTotalEnergy = 0
        for kPlan in dPlanets:
            iTotalEnergy += self.CalcEnergy( dPlanets[kPlan] )
            
        return iTotalEnergy


    def GetAxisState(self, dPlanets ={}, iAxis=0 ):
        
        tPos = []
        tVel = []
        for kPlan in dPlanets:
            tPos.append( dPlanets[kPlan][0][iAxis] )
            tVel.append( dPlanets[kPlan][1][iAxis] )
        return [tPos, tVel]

    def DEC12B(self, dPlanets = {}):

        lFactors = []
        for tIdx in range(len(dPlanets['Io'][0])):
            tDPlanets = deepcopy(dPlanets)
            #self.PrintPlanets( dPlanets )
            #self.PrintPlanets( tDPlanets )
            #print( self.GetAxisState( dPlanets, tIdx ) )
            #print("Evaluating Axis ", tIdx)
            
            tLoopCnt = 0

            initAxisState = self.GetAxisState( tDPlanets, tIdx )
            curAxisState = []
            while curAxisState != initAxisState:
                #self.PrintPlanets( tDPlanets )
                #print(initAxisState, curAxisState)
                self.NBodyStep( tDPlanets )
                tLoopCnt += 1
                curAxisState = self.GetAxisState( tDPlanets, tIdx )
            #print(initAxisState, curAxisState)
                
            lFactors.append(tLoopCnt)
            
        #print(lFactors)

        lcm = lFactors[0]
        for i in lFactors[1:]:
            #print( lcm, i, lcm * i, gcd(lcm, i), int(lcm*i/gcd(lcm, i)) )
            lcm = int(lcm*i/gcd(lcm, i))
        return lcm
                
                
    #==============================================================================================
    # DECEMBER13
    #==============================================================================================

    def DEC13A(self, lIntCode = [], lArgs=[], iVerbosity = 0, iICVerbosity = 0 ):
        ArcadeCabinet = ADV19_ArcadeCabinet(  lIntCode = lIntCode, lArgs=[], iVerbosity = iVerbosity, iICVerbosity = iICVerbosity )
        iBlocksRemain = ArcadeCabinet.RestartGame()
        #ArcadeCabinet.DrawScreen()
        return iBlocksRemain
        
    def DEC13B(self, lIntCode = [], lArgs=[], iVerbosity = 0, iICVerbosity = 0 ):
        ArcadeCabinet = ADV19_ArcadeCabinet(  lIntCode = lIntCode, lArgs=[], iVerbosity = iVerbosity, iICVerbosity = iICVerbosity )
        ArcadeCabinet.AddCredits()
        ArcadeCabinet.RestartGame()
        return ArcadeCabinet.Score


    #==============================================================================================
    # DECEMBER14
    #==========+===================================================================================

    def ParseReactionList(self, sReactions = ''):
        lReactions = sReactions.strip().split('\n')

        dReactions = {}
        for tReac in lReactions:
            if tReac != '':
                tlReac = tReac.strip().split('=')
                tIns = tlReac[0].strip().split(',')
                tOut = tlReac[1][1:].strip()
                
                tdIns = {}
                for tIn in tIns:
                    tlIns = tIn.strip().split(' ')
                    kIn = tlIns[1]
                    tiIn = int(tlIns[0])
                    tdIns[kIn] = tiIn
                
                sOuts = tOut.strip().split(' ')
                dReactions[sOuts[1]] = [ int(sOuts[0]), tdIns ]
        return dReactions

    
    

    def GetReagents( self, dReactions = {}, kOut = '', dReagents = {}):
        if self.Verbosity >= 5: print( "[DEC14] Reagents Before Reaction: ", dReagents)    

        iNeedToMake = dReagents[kOut][0]
        dReactionInputs = dReactions[kOut][1]

        iReacCount = max(1, floor(iNeedToMake / dReactions[kOut][0] ))
        
        # Fail if we have a surplus of what we are making, that doesnt make sense.
        if dReagents[kOut][1] > iNeedToMake:
            print("PROBLEM WITH SURPLUSES!")
            exit()
        if self.Verbosity >= 5: print( "[DEC14] We need to make %d %s from " % (iNeedToMake, kOut), dReactions[kOut], "in %d reactions" % iReacCount ) 
        
        if self.Verbosity >= 5: print("[DEC14] Current Reaction Inputs: ", dReactionInputs)
        for keyInput in dReactionInputs:
            if self.Verbosity >= 5: print("[DEC14] Working with % s Reaction in" % keyInput, dReactionInputs )
            if keyInput in dReagents:
                if self.Verbosity >= 5: print("[DEC14] Currently Available Reagents: ", dReagents)
                
                tNeed = dReactionInputs[keyInput] * iReacCount 
                tSurplus = dReagents[keyInput][1]
                
                if self.Verbosity >= 5: print("[DEC14] We have a surplus of %d %s, we need %d"  \
                        % ( tSurplus,  keyInput , tNeed ) )
                        
                
                if tNeed > tSurplus:
                    #Used all Surplus
                    tAddBase = tNeed - tSurplus
                    tNewSurplus = 0
                elif tNeed < tSurplus:
                    #Leftover Surplus
                    tAddBase = 0
                    tNewSurplus = tSurplus - tNeed
                elif tNeed == tSurplus:
                    tAddBase = 0
                    tNewSurplus = 0
                    
                dReagents[keyInput][0] += tAddBase
                dReagents[keyInput][1] = tNewSurplus
                
            else:
                dReagents[keyInput] = [iReacCount * dReactionInputs[keyInput], 0]
                if self.Verbosity >= 5: print("[DEC14] We new need %d of new reagent %s " % (dReagents[keyInput][0], keyInput) )
 
            #input()


        iReactionMakes = dReactions[kOut][0]  * iReacCount

        if self.Verbosity >= 5: print(" This Reaction makes %d units of %s.  " % (iReactionMakes, kOut), end='' )
        if self.Verbosity >= 5: print(" We needed to make %d units." % iNeedToMake)
        
        dReagents[kOut][0] -= iReactionMakes
        
        if dReagents[kOut][0] < 0:
            dReagents[kOut][1] += -dReagents[kOut][0]
            dReagents[kOut][0] = 0
            

        if dReagents[kOut][0] == 0 and dReagents[kOut][1] == 0: dReagents.pop(kOut)

        if self.Verbosity >= 5: print( " Reagents After Reaction: ", dReagents)
        if self.Verbosity >= 5: print()
        #input()


    def CompleteReaction(self, dReactions = {}, dReagents = {} ):
        bReactionsRemain = True
        while bReactionsRemain:

            tKeys = list(dReagents.keys())

            bReactionsRemain = False
            for kReag in tKeys:
                if kReag != 'ORE' and dReagents[kReag][0] > 0:
                    self.GetReagents(dReactions, kReag, dReagents)
                    bReactionsRemain = True  
                    

    def DEC14A(self, sReactions = ''):
        dReactions = self.ParseReactionList( sReactions )
        
        dReagents = {}
        dReagents['FUEL'] = [1, 0]
        dReagents['ORE'] = [0, 0]
 
        self.CompleteReaction( dReactions, dReagents )
        
        return dReagents['ORE'][0]
        

    def DEC14B(self, sReactions = '', iAvailOre = 1000000000000 ):
        dReactions = self.ParseReactionList( sReactions )
        
        iNextFuel = 1
        expFactor = 9
        while True:
            dReagents = {}
            dReagents['FUEL'] = [iNextFuel, 0]
            dReagents['ORE'] = [0, 0]
     
            self.CompleteReaction( dReactions, dReagents )
            iOreUsed = dReagents['ORE'][0]

            if self.Verbosity >= 3: print("Used %d ORE to make %d FUEL [%d]" % (iOreUsed, iNextFuel, expFactor ) )

            if iOreUsed < iAvailOre:            
                iNextFuel += 10**expFactor
            else: 
                iNextFuel -= 10**expFactor
                expFactor -= 1
                
                if expFactor < 0:
                    break
                
                iNextFuel += 10**expFactor
                

        return iNextFuel


    #==============================================================================================
    # DECEMBER15
    #==========+===================================================================================

    def DEC15A(self, lIntCode = []):
    
        RepairDroid = ADV19_RepairDroid( lIntCode=lIntCode, lArgs=[], lInitPosition=[0, 0], iVerbosity = 5, iICVerbosity = 0 )
        RepairDroid.Cheated()

        return 'UNSOLVED'

    def DEC15B(self):
        return 'UNSOLVED'


    #==============================================================================================
    # DECEMBER16
    #==========+===================================================================================

    def DEC16A(self):
        return 'UNSOLVED'

    def DEC16B(self):
        return 'UNSOLVED'


    #==============================================================================================
    # DECEMBER17
    #==========+===================================================================================

    def DEC17A(self):
        return 'UNSOLVED'

    def DEC17B(self):
        return 'UNSOLVED'


    #==============================================================================================
    # DECEMBER18
    #==========+===================================================================================

    def DEC18A(self):
        return 'UNSOLVED'

    def DEC18B(self):
        return 'UNSOLVED'


    #==============================================================================================
    # DECEMBER19
    #==========+===================================================================================

    def DEC19A(self):
        return 'UNSOLVED'

    def DEC19B(self):
        return 'UNSOLVED'


    #==============================================================================================
    # DECEMBER20
    #==========+===================================================================================

    def DEC20A(self):
        return 'UNSOLVED'

    def DEC20B(self):
        return 'UNSOLVED'


    #==============================================================================================
    # DECEMBER21
    #==========+===================================================================================

    def DEC21A(self):
        return 'UNSOLVED'

    def DEC21B(self):
        return 'UNSOLVED'


    #==============================================================================================
    # DECEMBER22
    #==========+===================================================================================

    def DEC22A(self):
        return 'UNSOLVED'

    def DEC22B(self):
        return 'UNSOLVED'


    #==============================================================================================
    # DECEMBER23
    #==========+===================================================================================

    def DEC23A(self):
        return 'UNSOLVED'

    def DEC23B(self):
        return 'UNSOLVED'


    #==============================================================================================
    # DECEMBER24
    #==========+===================================================================================

    def DEC24A(self):
        return 'UNSOLVED'

    def DEC24B(self):
        return 'UNSOLVED'


    #==============================================================================================
    # DECEMBER2
    #==========+===================================================================================

    def DEC25A(self):
        return 'UNSOLVED'

    def DEC25B(self):
        return 'UNSOLVED'





       
if __name__ == '__main__':
    
    from Advent2019_DATA_AJR import *
    ADV = ADVENT2019(iVerbosity = 1)
    curYear = 2019


    

    #==============================================================================================
    # DECEMBER25
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 25 ):

        print(" ** DEC25A PUZZLE ANSWER: %s [???] **" % ADV.DEC25A( ) )
        print(" ** DEC25B PUZZLE ANSWER: %s [???] **" % ADV.DEC25B( ) )

    #exit()

    #==============================================================================================
    # DECEMBER24
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 24 ):

        print(" ** DEC24A PUZZLE ANSWER: %s [???] **" % ADV.DEC24A( ) )
        print(" ** DEC24B PUZZLE ANSWER: %s [???] **" % ADV.DEC24B( ) )

    #exit()

    #==============================================================================================
    # DECEMBER23
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 23 ):

        print(" ** DEC23A PUZZLE ANSWER: %s [???] **" % ADV.DEC23A( ) )
        print(" ** DEC23B PUZZLE ANSWER: %s [???] **" % ADV.DEC23B( ) )

    #exit()

    #==============================================================================================
    # DECEMBER22
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 22 ):

        print(" ** DEC22A PUZZLE ANSWER: %s [???] **" % ADV.DEC22A( ) )
        print(" ** DEC22B PUZZLE ANSWER: %s [???] **" % ADV.DEC22B( ) )

    #exit()

    #==============================================================================================
    # DECEMBER21
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 21 ):

        print(" ** DEC21A PUZZLE ANSWER: %s [???] **" % ADV.DEC21A( ) )
        print(" ** DEC21B PUZZLE ANSWER: %s [???] **" % ADV.DEC21B( ) )

    #exit()

    #==============================================================================================
    # DECEMBER20
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 20 ):

        print(" ** DEC20A PUZZLE ANSWER: %s [???] **" % ADV.DEC20A( ) )
        print(" ** DEC20B PUZZLE ANSWER: %s [???] **" % ADV.DEC20B( ) )

    #exit()

    #==============================================================================================
    # DECEMBER19
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 19 ):

        print(" ** DEC19A PUZZLE ANSWER: %s [???] **" % ADV.DEC19A( ) )
        print(" ** DEC19B PUZZLE ANSWER: %s [???] **" % ADV.DEC19B( ) )

    #exit()
    
    #==============================================================================================
    # DECEMBER18
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 18 ):

        print(" ** DEC18A PUZZLE ANSWER: %s [???] **" % ADV.DEC18A( ) )
        print(" ** DEC18B PUZZLE ANSWER: %s [???] **" % ADV.DEC18B( ) )

    #exit()
    
    #==============================================================================================
    # DECEMBER17
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 17 ):

        print(" ** DEC17A PUZZLE ANSWER: %s [???] **" % ADV.DEC17A( ) )
        print(" ** DEC17B PUZZLE ANSWER: %s [???] **" % ADV.DEC17B( ) )

    #exit()
    
    #==============================================================================================
    # DECEMBER16
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 16 ):

        print(" ** DEC16A PUZZLE ANSWER: %s [???] **" % ADV.DEC16A( ) )
        print(" ** DEC16B PUZZLE ANSWER: %s [???] **" % ADV.DEC16B( ) )

    #exit()
    
    #==============================================================================================
    # DECEMBER15
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 15 ):

        print(" ** DEC15A PUZZLE ANSWER: %s [???] **" % ADV.DEC15A( lIntCode = DEC15 ) )
        #print(" ** DEC15B PUZZLE ANSWER: %s [???] **" % ADV.DEC15B( ) )

    exit()
    
    #==============================================================================================
    # DECEMBER14
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 14 ):

        #print( ADV.DEC14A( DEC14A_TV01 ) )
        #print( ADV.DEC14A( DEC14A_TV02 ) )
        #print( ADV.DEC14A( DEC14A_TV03 ) )
        #print( ADV.DEC14A( DEC14A_TV04 ) )
        #print( ADV.DEC14A( DEC14A_TV05 ) )
        print(" ** DEC14A PUZZLE ANSWER: %d [1065255] **" % ADV.DEC14A(DEC14) )
        
        #print( ADV.DEC14B( DEC14A_TV03 ) )
        #print( ADV.DEC14B( DEC14A_TV04 ) )
        #print( ADV.DEC14B( DEC14A_TV05 ) )
        print(" ** DEC14B PUZZLE ANSWER: %s [1766154] **" % ADV.DEC14B(DEC14 ) )

    #exit()

    #==============================================================================================
    # DECEMBER13
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 13 ):

        print(" ** DEC13A PUZZLE ANSWER: %d [315] **" % ADV.DEC13A( lIntCode=DEC13, lArgs=[], iVerbosity = 0, iICVerbosity = 0 ) )
        print(" ** DEC13B PUZZLE ANSWER: %d [16171] **" % ADV.DEC13B( lIntCode=DEC13, lArgs=[], iVerbosity = 0, iICVerbosity = 0 ))

    #exit()

    #==============================================================================================
    # DECEMBER12
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 12 ):

        # print( ADV.DEC12A( dPlanets = DEC12_TV01, iSteps = 10) )
        # print( ADV.DEC12A( dPlanets = DEC12_TV02, iSteps = 100) )    
        print(" ** DEC12A PUZZLE ANSWER: %d [6220] **" % ADV.DEC12A( dPlanets = DEC12A, iSteps = 1000) )

        # print( ADV.DEC12B( dPlanets = DEC12_TV01) )
        # print( ADV.DEC12B( dPlanets = DEC12_TV02) )
        print(" ** DEC12B PUZZLE ANSWER: %d [548525804273976] **" % ADV.DEC12B( DEC12A ) )

    #exit()

    #==============================================================================================
    # DECEMBER11
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 11 ):

        print(" ** DEC11A PUZZLE ANSWER: %d [1863] **" % ADV.DEC11A(lIntCode=DEC11A) )
        print(" ** DEC11B PUZZLE ANSWER: \n%s [BLULZJLZ] **" % ADV.DEC11B(lIntCode=DEC11A) )

    #exit()

    #==============================================================================================
    # DECEMBER10
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 10 ):

        # print(" ** DEC10A_TV01 ANSWER: %d [8]  @ %s **" % ADV.DEC10A(DEC10A_TV01) )
        # print(" ** DEC10A_TV02 ANSWER: %d [33]  @ %s **" %  ADV.DEC10A(DEC10A_TV02) )
        # print(" ** DEC10A_TV03 ANSWER: %d [35]  @ %s **" %  ADV.DEC10A(DEC10A_TV03) )
        # print(" ** DEC10A_TV04 ANSWER: %d [41]  @ %s **" %  ADV.DEC10A(DEC10A_TV04) )
        # print(" ** DEC10A_TV05 ANSWER: %d [210]  @ %s **" %  ADV.DEC10A(DEC10A_TV05) )
        print(" ** DEC10A PUZZLE ANSWER: %d [344]  @ %s **" % ADV.DEC10A(DEC10A) ) 
        print(" ** DEC10B PUZZLE ANSWER: %d [2732] **" % ADV.DEC10B(DEC10B, ADV.DEC10A(DEC10A)[1]) )

    #exit()

    #==============================================================================================
    # DECEMBER09
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 9 ):

        #ADV.RunIntcode(DEC09A_TV01, 1)
        #ADV.RunIntcode(DEC09A_TV02, 1)
        #ADV.RunIntcode(DEC09A_TV03, 1)

        print(" ** DEC09A PUZZLE ANSWER: %d [2406950601] ** " % ADV.DEC09A(IntCode=DEC09A,  iVerbosity=0))     # 2406950601
        print(" ** DEC09B PUZZLE ANSWER: %d [83239] ** " % ADV.DEC09B(IntCode=DEC09B,  iVerbosity=0))

    #exit()

    #==============================================================================================
    # DECEMBER08
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 8 ):

        # print(ADV.UnpackSIFStream()[1])
        print(" ** DEC08A PUZZLE ANSWER: %d [1360] ** " %ADV.DEC08A(DEC08A) )

        #ADV.PrintImage(ADV.DecodeSIFImage(DEC08B_TV01, 2, 2), 2, 2)
        print(" ** DEC08B PUZZLE ANSWER:\n%s [FPUAR] **" % ( ADV.DEC08B(DEC08B, 26) ) )

    #exit()
 
    #==============================================================================================
    # DECEMBER07
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 7 ):

        # print( ADV.DEC07_CalcAmplification(IntCode=DEC07A_TV01_code, lPhases=DEC07A_TV01_Phases, iVerbosity = 0) )
        # print( ADV.DEC07_CalcAmplification(IntCode=DEC07A_TV02_code, lPhases=DEC07A_TV02_Phases, iVerbosity = 0) )
        # print( ADV.DEC07_CalcAmplification(IntCode=DEC07A_TV03_code, lPhases=DEC07A_TV03_Phases, iVerbosity = 0) )
        print(" ** DEC07A PUZZLE ANSWER: %d [17440] ** " % ADV.DEC07A(IntCode=DEC07A_Code, iVerbosity = 0) ) # 17440
        
    #    print( ADV.DEC07_CalcMultAmplification(IntCode=DEC07B_TV01_code, lPhases=DEC07B_TV01_Phases, iVerbosity = 1) ) # 139629729
    #    print( ADV.DEC07_CalcMultAmplification(IntCode=DEC07B_TV02_code, lPhases=DEC07B_TV02_Phases, iVerbosity = 1) ) # 18216
        print(" ** DEC07B PUZZLE ANSWER: %d [27561242] ** " % ADV.DEC07B(IntCode=DEC07B_Code, iVerbosity = 0) ) # 27561242

    #exit()

    #==============================================================================================
    # DECEMBER06
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 6 ):

        # print( ADV.DEC06A(DEC06A_TV01) ) # OUT: 42
        print(" ** DEC06A PUZZLE ANSWER: %d [247089] ** " % ADV.DEC06A(DEC06A) )

        # print( ADV.DEC06B(DEC06B_TV01) ) # 4
        print(" ** DEC06B PUZZLE ANSWER: %d [442] ** " % ADV.DEC06B(DEC06B))

    #exit()

    #==============================================================================================
    # DECEMBER05
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 5 ):

        # ADV.DEC05(DEC05A_TV01, iVerbosity=1)
        # ADV.DEC05(DEC05A_TV02, iVerbosity=1)
        # ADV.DEC05(DEC05A_TV03, iVerbosity=1)
        # ADV.DEC05(DEC05A_TV04, iVerbosity=1)
        # ADV.DEC05(DEC05A_TV05, iVerbosity=1)
        # ADV.DEC05(DEC05A_TV06, iVerbosity=1)
        # ADV.DEC05(DEC05A_TV07, iVerbosity=1)
        #ADV.DEC05(DEC05A_TV08, lArgs=[-5], iVerbosity=1)
        print(" ** DEC05A PUZZLE ANSWER: %d [13978427]" %  ADV.DEC05(DEC05A, lArgs=[1])[-1] )
        
        # ADV.DEC05(DEC05B_TV01, lArgs=[5], iVerbosity=1) # Not Equal to 8
        # ADV.DEC05(DEC05B_TV01, lArgs=[8], iVerbosity=1) # Equal to 8
        # ADV.DEC05(DEC05B_TV02, lArgs=[5], iVerbosity=1) # Less than 8
        # ADV.DEC05(DEC05B_TV02, lArgs=[8], iVerbosity=1) # Not Less Than 8
        # ADV.DEC05(DEC05B_TV03, lArgs=[5], iVerbosity=1) # Not Equal to 8
        # ADV.DEC05(DEC05B_TV03, lArgs=[8], iVerbosity=1) # Equal to 8
        # ADV.DEC05(DEC05B_TV04, lArgs=[5], iVerbosity=1) # Less than 8
        # ADV.DEC05(DEC05B_TV04, lArgs=[8], iVerbosity=1) # Not Less Than 8
        # ADV.DEC05(DEC05B_TV05, lArgs=[0], iVerbosity=1) # Equal to 0
        # ADV.DEC05(DEC05B_TV05, lArgs=[8], iVerbosity=1) # Not Equal to 0
        # ADV.DEC05(DEC05B_TV06, lArgs=[0], iVerbosity=1) # Equal to 0
        # ADV.DEC05(DEC05B_TV06, lArgs=[8], iVerbosity=1) # Not Equal to 0
        # ADV.DEC05(DEC05B_TV07, lArgs=[7], iVerbosity=1)
        # ADV.DEC05(DEC05B_TV07, lArgs=[8], iVerbosity=1)
        # ADV.DEC05(DEC05B_TV07, lArgs=[9], iVerbosity=1)
        print(" ** DEC05B PUZZLE ANSWER: %d [11189491]" %  ADV.DEC05(DEC05B, lArgs=[5])[-1] )

    #exit()

    #==============================================================================================
    # DECEMBER04
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 4 ):
 
        # print(111111, ADV.CheckValidPassA(112345))
        # print(223450, ADV.CheckValidPassA(223450))
        # print(123789, ADV.CheckValidPassA(123789))
        print(" ** DEC04A PUZZLE ANSWER: %d [1694] ** " % ADV.CheckRangeA(156218, 652527))  #1694

        # print(112233, ADV.CheckValidPassB(112233))
        # print(123444, ADV.CheckValidPassB(123444))
        # print(111122, ADV.CheckValidPassB(111122))
        print(" ** DEC04B PUZZLE ANSWER: %d [1148] ** " %  ADV.CheckRangeB(156218, 652527))  #1148

    #exit()
 
    #==============================================================================================
    # DECEMBER03
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 3 ):

        # ADV.DEC03( DEC03_TV1As, DEC03_TV1Bs )
        # ADV.DEC03( DEC03_TV2As, DEC03_TV2Bs )
        # ADV.DEC03( DEC03_TV3As, DEC03_TV3Bs )
        print(" ** DEC03A PUZZLE ANSWER: %d [1983] **\n ** DEC03B PUZZLE ANSWER: %d [107754] ** (This took %dms)" % ADV.DEC03( DEC03_As, DEC03_Bs ) ) 

    #exit()

    #==============================================================================================
    # DECEMBER02
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 2 ):

        # ADV.DEC02A_TV(DEC02A_TV01, iVerbosity=3)
        # ADV.DEC02A_TV(DEC02A_TV02, iVerbosity=5)
        # ADV.DEC02A_TV(DEC02A_TV03, iVerbosity=5)
        # ADV.DEC02A_TV(DEC02A_TV04, iVerbosity=5)
        # ADV.DEC02A_TV(DEC02A_TV05, iVerbosity=5)
        print(" ** DEC02A PUZZLE ANSWER: %d [4138658] **" % ADV.DEC02A(DEC02A) )
        print(" ** DEC02B PUZZLE ANSWER: %d [7264] **"% ADV.DEC02B(DEC02A) )

    #exit()
    
    #==============================================================================================
    # DECEMBER01
    #==============================================================================================
    if datetime.now() >= datetime(curYear, 12, 1 ):

        # ADV.DEC01A_TV(DEC01A_TV01)
        # ADV.DEC01A_TV(DEC01A_TV02)
        # ADV.DEC01A_TV(DEC01A_TV03)
        # ADV.DEC01A_TV(DEC01A_TV04)
        print(" ** DEC01A PUZZLE ANSWER: %d [3279287] **" % ADV.DEC01A(DEC01A) )
        
        # ADV.DEC01B_TV(DEC01B_TV01)
        # ADV.DEC01B_TV(DEC01B_TV02)
        # ADV.DEC01B_TV(DEC01B_TV03)
        print(" ** DEC01B PUZZLE ANSWER: %d [4916076] **" % ADV.DEC01B(DEC01B) )