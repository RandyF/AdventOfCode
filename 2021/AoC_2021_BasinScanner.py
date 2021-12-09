from AoC_Utils import *

class BasinScanner():

    Verbosity = None

    LowPoints = None
    Scan = None
    MapSize = None


    def __init__(self, Verbosity=0 ):
        self.Verbosity = Verbosity
        self.LowPoints = []

    def _GetCrossPoints(self, Point):

        lenY, lenX = self.MapSize[0], self.MapSize[1]
        tY, tX = Point[0], Point[1]

        tVal = self.Scan[tY][tX]
        
        if tY == 0:
            tUp = 9
            pUp = None
        else:
            tUp = self.Scan[tY - 1][tX]
            pUp = [tY - 1,tX]
        
        if tY == (lenY -1):
            tDn = 9
            pDn = None
        else:
            tDn = self.Scan[tY + 1][tX]
            pDn = [tY + 1,tX]
       
        if tX == 0:
            tLf = 9
            pLf = None
        else:
            tLf = self.Scan[tY][tX - 1]
            pLf = [tY,tX - 1]
        
        if tX == (lenX - 1):
            tRt = 9
            pRt = None
        else:
            tRt = self.Scan[tY][tX + 1]
            pRt = [tY,tX + 1]

        return [tVal, tUp, tDn, tLf, tRt], [Point, pUp, pDn, pLf, pRt]


    def _FindLowPoints(self):
        self.LowPoints = []
        
        lenY, lenX = self.MapSize[0], self.MapSize[1]
        
        for tY in range(lenY):
            for tX in range(lenX):

                tVals, tPts = self._GetCrossPoints( [tY, tX] )
                #print(tVals, tPts)

                if tVals[0] < tVals[1] and tVals[0] < tVals[2] and tVals[0] < tVals[3] and tVals[0] < tVals[4]: 
                    self.LowPoints.append( [tY, tX] )
                    #print("Low Spot: ", tY, tX, tVals[0])
                    
        return len(self.LowPoints)


    def CalcRiskLevel(self, ScanArray):
        self.Scan = ScanArray
        self.MapSize = len(self.Scan), len(self.Scan[0])
        self._FindLowPoints()
    
        tRisk = 0
    
        for tPt in self.LowPoints:
            #print( tPt, self.Scan[ tPt[0], tPt[1] ] )
            tRisk += self.Scan[ tPt[0]][tPt[1] ] + 1
            
        return tRisk


    def _ProjectBasin(self, Point):
        #print("Projecting: ", Point)
        tVals, tPts = self._GetCrossPoints(Point)

        tNextEdge = []

        tLow = tVals[0]
        cntNextEdge = 0
        for i in range(1, len(tVals)):
            if tVals[i] >= tLow and tVals[i] != 9:
                tNextEdge.append( tPts[i] )
                cntNextEdge += 1
        
        return tNextEdge, cntNextEdge


    def BasinString(self, Basin):
        
        yMin = 2**32
        yMax = -1
        xMin = 2**32
        xMax = -1
        
        for tPt in Basin:
            yMin = min( tPt[0], yMin)
            yMax = max( tPt[0], yMax)
            xMin = min( tPt[1], xMin)
            xMax = max( tPt[1], xMax)


        tMap = 'Y   X'
        for tX in range( max(xMin - 1, 0), min( xMax + 2, self.MapSize[1] )):
            tMap += '%03d  ' % tX
        tMap += '\n'

        for tY in range( max(yMin - 1, 0), min( yMax + 2, self.MapSize[0] )):
            tMap += '%03d  ' % tY
            for tX in range( max(xMin - 1, 0), min( xMax + 2, self.MapSize[1] )):
                if [tY, tX] in Basin:
                    tIn = '*'
                else:
                    tIn = ' '
                tMap += ' %d%s  ' % (self.Scan[ tY][tX], tIn)
            tMap += '\n'
        
        return tMap


    def _FindBasin(self, Point):

        tBasin = [Point]

        tEdge = [Point]
        while(len(tEdge) > 0):
            tNextEdge = []

            #print('\nStarting New Edge Check: ', tEdge)

            for tE in tEdge:
                if tE != None:
                    #print('\nChecking Edge Point:', tE)

                    tProj, cntNextEdge = self._ProjectBasin(tE)
                    #print('Proj to: {%s} %d' % (tProj, cntNextEdge) )

                    for tPr in tProj:
                        #print('Evaluating ', tPr, (tPr not in tNextEdge), (tPr != None))
                    
                        if (tPr not in tNextEdge) and (tPr != None) and (tPr not in tBasin):
                            #print('Adding %s to %s' % (tPr, tNextEdge ))
                            tNextEdge += [tPr]

                        if (tPr not in tBasin) and (tPr != None):
                            tBasin += [tPr]

                    #print('After Eval Edge', tNextEdge)

            tEdge = tNextEdge

            #print('Next tEdge: ', tEdge, len(tEdge))
            debug(self.BasinString(tBasin), DebugLevel=DBG_MINOR, Verbosity=self.Verbosity )


        return tBasin, len(tBasin)


    def CalcBasinScore(self, ScanArray):
        self.Scan = ScanArray
        self._FindLowPoints()


        debug("Finding %d Basins..." % len(self.LowPoints), DebugLevel=DBG_MINOR_START, Verbosity=self.Verbosity )

        tSizes = []
        tCtr = 0
        for tPt in self.LowPoints:
            tCtr += 1
            debug("[%03d] Evaluating Basin @ %s" % ( tCtr, tPt) , DebugLevel=DBG_MINOR, Verbosity=self.Verbosity )
            tBasin, tSize = self._FindBasin(tPt)
            tSizes.append(tSize)

            debug(self.BasinString(tBasin), DebugLevel=DBG_MINOR, Verbosity=self.Verbosity )


        debug("Sorting Results...", DebugLevel=DBG_MINOR, Verbosity=self.Verbosity )
        tSc = sorted(tSizes)[-3:]
        
        return tSc[0] * tSc[1] * tSc[2]