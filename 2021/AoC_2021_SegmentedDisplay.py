
class SevenSeg():
    
    Verbosity = None
    
    SegKnown = None
    SegChar = None
    SegCode = None
    
    def __init__(self, Segments='', Verbosity=0):
        self.Verbosity = Verbosity
        self.SegKnown = False
        self.SegChar = 'X'
        self.SegCode = Segments

        if len(self.SegCode) > 0:
            self.ParseSegments(self.SegCode)
            
    def ParseSegments(self, Segments):

        lenSeg = len(Segments)
        
        if lenSeg == 2:
            self.SegChar = '1'
            self.SegKnown = True
        
        elif lenSeg == 3:
            self.SegChar = '7'
            self.SegKnown = True
        
        elif lenSeg == 4:
            self.SegChar = '4'
            self.SegKnown = True
            
        elif lenSeg == 7:
            self.SegChar = '8'
            self.SegKnown = True

        else:
            self.SegChar = 'X'
            self.SegKnown = False

        if(self.SegKnown and self.Verbosity > 0):
            print("Got a %s" % self.SegChar)
        elif(self.Verbosity > 0):
            print('Unknown as of yet!')


class DigitDisplay():

    Inputs = None
    Outputs = None
    
    CharCodes = []

    def __init__(self, StateData = None):
        self.Inputs = []
        self.Outputs = []
        self.CharCodes = [None] * 10
        
        if StateData != None:
            self.ParseStateData(StateData)
        
    def ParseStateData(self, StateData):
        
        #print(StateData[1])
        
        for tIn in StateData[0]:
            #print("Parsing Input Set: ", tIn)
            self.Inputs.append( SevenSeg(tIn) )
        
        
        for tOut in StateData[1]:
            #print("Parsing Output Set: ", tOut)
            self.Outputs.append( SevenSeg(tOut) )


    def PrintSimpleDisplay(self):

        tDisp = ''
        for tIn in self.Inputs:
            tDisp += tIn.SegChar
        
        tDisp += ' -> '
        
        for tOut in self.Outputs:
            tDisp += tOut.SegChar
            
        #print(tDisp)

    def DecodeDisplay(self):

        for tIn in self.Inputs:
            if tIn.SegChar == '1':
                self.CharCodes[1] = tIn.SegCode
            elif tIn.SegChar == '4':
                self.CharCodes[4] = tIn.SegCode
            elif tIn.SegChar == '7':
                self.CharCodes[7] = tIn.SegCode
            elif tIn.SegChar == '8':
                self.CharCodes[8] = tIn.SegCode

        # TOP Segment is the part of 7 that is not in 4
        for tChar in self.CharCodes[7]:
            if tChar not in self.CharCodes[1]:
                Seg_Top = tChar
                break
        #print("Segment TOP:", Seg_Top)

        # BOTTOM Segment is the part of 9 that is not in 7&4
        for tIn in self.Inputs:
            if len(tIn.SegCode) == 6:
                #print("Could be 6 or 9 or 0", tIn.SegCode)
                tCode = [*tIn.SegCode]
                for tExChar in self.CharCodes[7] + self.CharCodes[4]:
                    if tExChar in tCode:
                        tCode.remove(tExChar)
                #print("after Exclusion", tCode)
                if len(tCode) == 1:
                    Seg_Bottom = tCode[0]
                    self.CharCodes[9] = tIn.SegCode
                    tIn.SegChar = '9'
                    tIn.SegKnown = True
                    break
        #print("Segment BOTTOM:", Seg_Bottom)

        # LOWLEFT Segment is the part of 6&0 that is not in 7&4&Bottom
        for tIn in self.Inputs:
            if len(tIn.SegCode) == 6 and not tIn.SegKnown:
                #print("Could be 6 or 0", tIn.SegCode)

                tCode = [*tIn.SegCode]
                for tExChar in self.CharCodes[7] + self.CharCodes[4] + Seg_Bottom:
                    if tExChar in tCode:
                        tCode.remove(tExChar)
                #print("after Exclusion", tCode)
                if len(tCode) == 1:
                    Seg_LowLeft = tCode[0]
                    break
        #print("Segment LowLeft:", Seg_LowLeft)

        # UPLEFT Segment is the part of 6 or 0 that we don't know and is not in 1
        for tIn in self.Inputs:
            if len(tIn.SegCode) == 6 and not tIn.SegKnown:
                #print("Could be 6 or 0", tIn.SegCode)

                tCode = [*tIn.SegCode]
                for tExChar in Seg_Bottom + Seg_Top + Seg_LowLeft + self.CharCodes[1]:
                    if tExChar in tCode:
                        tCode.remove(tExChar)

                #print("after Exclusion", tCode)
                if len(tCode) == 1:
                    Seg_UpLeft = tCode[0]
                    self.CharCodes[0] = tIn.SegCode
                    tIn.SegChar = '0'
                    tIn.SegKnown = True
                    break
        #print("Segment UPLEFT:", Seg_UpLeft)

        # SIX is now known
        for tIn in self.Inputs:
            if len(tIn.SegCode) == 6 and not tIn.SegKnown:
                #print("Must be 6", tIn.SegCode)
                self.CharCodes[6] = tIn.SegCode
                tIn.SegChar = '6'
                tIn.SegKnown = True

        # MIDDLE is the part of 8 that is not in 0
        tCode = [*self.CharCodes[8]]
        for tExChar in self.CharCodes[0]:
            if tExChar in tCode:
                tCode.remove(tExChar)
        #print("after Exclusion", tCode)
        Seg_Middle = tCode[0]
        #print("Segment MIDDLE:", Seg_Middle)


        # UPRIGHT is the part of 0 that is not in 6
        tCode = [*self.CharCodes[0]]
        for tExChar in self.CharCodes[6]:
            if tExChar in tCode:
                tCode.remove(tExChar)
        #print("after Exclusion", tCode)
        Seg_UpRight = tCode[0]
        #print("Segment UPRIGHT:", Seg_UpRight)


        # LOWRIGHT is the part of 1 that is not Upright
        tCode = [*self.CharCodes[1]]
        for tExChar in Seg_UpRight:
            if tExChar in tCode:
                tCode.remove(tExChar)
        #print("after Exclusion", tCode)
        Seg_LowRight = tCode[0]
        #print("Segment LOWRIGHT:", Seg_LowRight)


        for tIn in self.Inputs:
            if not tIn.SegKnown:
                #print("Still need to ID: ", tIn.SegCode, sorted(tIn.SegCode))
                if sorted(tIn.SegCode) == sorted( [Seg_Top, Seg_UpRight, Seg_Middle, Seg_LowLeft, Seg_Bottom]):
                    #print("TWO!")
                    self.CharCodes[2] = tIn.SegCode
                    tIn.SegChar = '2'
                    tIn.SegKnown = True
                elif sorted(tIn.SegCode) == sorted( [Seg_Top, Seg_UpRight, Seg_Middle, Seg_LowRight, Seg_Bottom]):
                    #print("THREE!")
                    self.CharCodes[3] = tIn.SegCode
                    tIn.SegChar = '3'
                    tIn.SegKnown = True
                elif sorted(tIn.SegCode) == sorted( [Seg_Top, Seg_UpLeft, Seg_Middle, Seg_LowRight, Seg_Bottom]):
                    #print("FIVE!")
                    self.CharCodes[5] = tIn.SegCode
                    tIn.SegChar = '5'
                    tIn.SegKnown = True
            

        #print( self.CharCodes )
        self.PrintSimpleDisplay()

    def DecodeOutput(self):

        tSortedCodes = []
        for tCode in self.CharCodes:
            tSortedCodes.append( sorted(tCode) )
        
        #print(tSortedCodes)

        tOutputDisp = ''
        for tOut in self.Outputs:
            #print(sorted(tOut.SegCode), tSortedCodes.index(sorted(tOut.SegCode)) )
            tOutputDisp += str(tSortedCodes.index(sorted(tOut.SegCode)))

        return int(tOutputDisp)