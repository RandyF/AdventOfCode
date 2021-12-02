class ADV19_IntcodeComputer(object):

    def __init__(self, sIntcodeProg = [], lArgs = [], iMemSpace = 1024, iVerbosity = 0 ):
    
        self.Verbosity = iVerbosity
        self.IntcodeMEM = []
        self.IntcodeProgram = []
        self.Arguments = []
        self.curArg = 0
        self.IP = 0
        self.MachineState = 0
        self.RelativeBase = 0
        self.MemorySize = 1024

        self.ResetStdOut()

        self.LoadProgram(sIntcodeProg)
        self.LoadProgramToMemory(lArgs)
        if self.Verbosity >= 2: print("Initialized DEC05 Intcode Computer")
        if self.Verbosity >= 10: self.PrintIncodeMEM()


    def LoadProgram(self, sIntcodeProg = []):
        self.IntcodeProgram = sIntcodeProg + [0]*(self.MemorySize-len(self.IntcodeProgram))
 
 
    def LoadProgramToMemory(self, lArgs = []):
        self.IntcodeMEM = self.IntcodeProgram[:]
        self.Arguments = lArgs[:]


    def RestartProgram(self):
        self.IP = 0
        self.curArg = 0
        self.MachineState = 1
        self.RunFree()
        
        
    def RunFree(self):
        while self.MachineState == 1:
            self.ProcessCurrentInstruction()
               
               
    def AppendStdIn(self, lArgs = []):
        for arg in lArgs:
            #print("got arg", arg)
            self.Arguments.append(arg)
            
    def ResetStdOut(self):
        if self.Verbosity >= 2: print("[INTCODE] ResetStdOut")
        self.StdOut = []        
  
  
    def Continue(self):
        #print( "Continuing" )
        self.MachineState = 1
        self.RunFree()  

        
    # def DisassembleIncodeMEM(self, printIntCode = [], iWidth = 20):
        # if printIntCode == []:
            # pIC = self.IntcodeMEM
        # else:
            # pIC = printIntCode
        # print( "\n")
        # print( '=' * (iWidth + 20))
        # print( "IP: %d" % self.IP)
        # print( "Intcode Memory:")
        # print( '=' * (iWidth + 20))
        # tCtr = 0
        
        # while tCtr < len(pIC):
            # if pIC[tCtr] == 99:
                # print( '99',  (iWidth-2) * ' ',"** HALT")
                # tCtr += 1
            # else:
                # tOpCode = pIC[tCtr] - (pIC[tCtr] / 100) * 100
                # if tOpCode == 1:
                    # print( pIC[tCtr:tCtr+4], (iWidth-len(str(pIC[tCtr:tCtr+4]))) * ' ', "** ADDER")
                    # tCtr += 4
                # elif tOpCode == 2:
                    # print( pIC[tCtr:tCtr+4], (iWidth-len(str(pIC[tCtr:tCtr+4]))) * ' ', "** MULTIPLIER")
                    # tCtr += 4
                # elif tOpCode == 3:
                    # print( pIC[tCtr:tCtr+2], (iWidth-len(str(pIC[tCtr:tCtr+2]))) * ' ', "** INPUT")
                    # tCtr += 2
                # elif tOpCode == 4:
                    # print( pIC[tCtr:tCtr+2], (iWidth-len(str(pIC[tCtr:tCtr+2]))) * ' ', "** OUTPUT")
                    # tCtr += 2
                # elif tOpCode == 8:
                    # print( pIC[tCtr:tCtr+4], (iWidth-len(str(pIC[tCtr:tCtr+4]))) * ' ', "** EQUALS")
                    # tCtr += 3
                # else:
                    # print( pIC[tCtr], (iWidth-len(str(pIC[tCtr]))) * ' ',"** DATA")
                    # tCtr += 1

        # print( '=' * (iWidth + 20))

        
    def PrintIncodeMEM(self, printIntCode = [], iWidth = 10, iChrW = 5):
        if printIntCode == []:
            pIC = self.IntcodeMEM
        else:
            pIC = printIntCode
        print( "\n")
        print( '=' * (iWidth + 20))
        print( "IP: %d" % self.IP)
        print( "Relative Base: %d" % self.RelativeBase)
        print( "Intcode Memory:")
        print( '=' * (iWidth + 20))
        
        sIntF = "%%0%dd " % iChrW
        
        tCtr = 0
        for tInt in pIC:
            if (tCtr % iWidth) == 0:
                print( "\n[%05d] " % tCtr, end='')
            print( sIntF % tInt, end='')
            tCtr += 1
        print('\n')
        print( '=' * (iWidth + 20)   )

        
    def GetIntParams(self, lCmd = [], nInParams = 0, nOutParams = 0 ):
        #Parameter modes are stored in the same value as the instruction's opcode. The
        #opcode is a two-digit number based only on the ones and tens digit of the value,
        #that is, the opcode is the rightmost two digits of the first value in an instruction.
        #Parameter modes are single digits, one per parameter, read right-to-left from the opcode:
        #the first parameter's mode is in the hundreds digit, the second parameter's mode is in the
        #thousands digit, the third parameter's mode is in the ten-thousands digit, and so on.
        #Any missing modes are 0.
        iOpLen = nInParams + nOutParams + 2
        sOpCode = (('0' * iOpLen) + str(lCmd[0]))[-iOpLen:]
        #print( "lCmd", lCmd )
        if self.Verbosity >= 5: print( "      Extended Opcode: ", sOpCode )
        
        sModes = sOpCode[:nInParams + nOutParams ]
        #print( "Modes: ", sModes )

        lParams = []
        tParam = 0

        for i in range(len(sModes)):
            iPos = len(sModes) - i - 1
            if self.Verbosity >= 10: print( "      Mode[%d/%d]: %s" % ( i, iPos, sModes[iPos] ) )
            if i > (nInParams - 1):
                if sModes[iPos] == '1':
                    print("** OUTPUT ADDRESSING ERROR **")
                    tParam = -1
                elif  sModes[iPos] == '0':
                    if self.Verbosity >= 5: print( "       [OUT POS MODE] %d = " % lCmd[i+1], end='')
                    tParam = lCmd[i+1]
                    if self.Verbosity >= 5: print( tParam )
                elif sModes[iPos] == '2':
                    if self.Verbosity >= 5: print( "       [OUT REL MODE] *%d + %d = *%d = " % (self.RelativeBase, lCmd[i+1], self.RelativeBase + lCmd[i+1]), end='')
                    tParam = self.RelativeBase + lCmd[i+1]
                    if self.Verbosity >= 5: print( tParam )
                else:
                    print("** OUTPUT ADDRESSING ERROR **")
                    tParam = -1
            else:        
                    
                if sModes[iPos] == '0':
                    if self.Verbosity >= 5: print( "       [POS MODE] *%d = " % lCmd[i+1], end='')
                    tParam = self.IntcodeMEM[ lCmd[i+1] ]
                    if self.Verbosity >= 5: print( tParam )
                elif sModes[iPos] == '1':
                    if self.Verbosity >= 5: print( "       [IMM MODE] %d = " % lCmd[i+1], end='')
                    tParam = lCmd[i+1]
                    if self.Verbosity >= 5: print( tParam )
                elif sModes[iPos] == '2':
                    if self.Verbosity >= 5: print( "       [REL MODE] *%d = " % (self.RelativeBase + lCmd[i+1]), end='')
                    tParam = self.IntcodeMEM[ self.RelativeBase + lCmd[i+1] ]
                    if self.Verbosity >= 5: print( tParam )
                else:
                    print("** OUTPUT ADDRESSING ERROR **")
                    tParam = -1
            lParams.append(tParam)
            
        return lParams + lCmd[1+nInParams + nOutParams:]
                

    def IntOp_99(self):
        #99 means that the program is finished and should immediately halt.
        if self.Verbosity >= 2: print( "   ** PROGRAM HALT **")
        self.IP += 1
        self.MachineState = 99
        #self.print(IncodeMEM()


    def IntOp_01(self, lCmd = [] ):
            if self.Verbosity >= 3: print( "[%d] ADDER" % self.IP, lCmd )
            #Opcode 1 adds together numbers read from two positions and stores the result
            #in a third position. The three integers immediately after the opcode tell you
            #these three positions - the first two indicate the positions from which you
            #should read the input values, and the third indicates the position at which
            #the output should be stored.
            tParams = self.GetIntParams( lCmd, 2, 1 )
            if self.Verbosity >= 3: print( "    Adding %d to %d and sending to *%d" % (tParams[0], tParams[1], tParams[2])) 
            
            iAdd = tParams[0] + tParams[1]
            self.IntcodeMEM[ tParams[2] ] = iAdd
            self.IP += len(lCmd)
            #self.print(IncodeMEM()   


    def IntOp_02(self, lCmd = [] ):
            if self.Verbosity >= 3: print( "[%d] MULTIPLIER" % self.IP, lCmd) 
            #Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead
            #of adding them. Again, the three integers after the opcode indicate where the
            #inputs and outputs are, not their values.
            tParams = self.GetIntParams( lCmd, 2, 1 )
            if self.Verbosity >= 3: print( "    Multiplying %d by %d and sending to *%d" % (tParams[0], tParams[1], tParams[2]) )
            
            iMult = tParams[0] * tParams[1]
            self.IntcodeMEM[ tParams[2] ] = iMult
            self.IP += len(lCmd)
            #self.print(IncodeMEM()   

 
    def IntOp_03(self, lCmd = [] ):
        # Opcode 3 takes a single integer as input and saves it to the position given by its
        # only parameter. For example, the instruction 3,50 would take an input value and store
        # it at address 50.
        if self.Verbosity >= 3: print( "[%d] INPUT" % self.IP, lCmd)
        
        self.Op03_hold = lCmd
        if self.curArg < len(self.Arguments):
            tDest = self.GetIntParams( lCmd, 0, 1 )[0]

            if self.Verbosity >= 3: print( "    Input Destination *%d" % tDest )
            
            tIn = self.Arguments[self.curArg]
            self.curArg += 1
            iIn = int(tIn)
            self.IntcodeMEM[ tDest ] = iIn
            self.IP += len(lCmd)
            
            if self.Verbosity >= 1: print( "[INTCODE] Input: [", self.IntcodeMEM[ tDest ] , "] to *%d" % tDest )            
            #self.print(IncodeMEM()        
        else:
            if self.Verbosity >= 1: print( "[INTCODE] PAUSED FOR INPUT")
            self.MachineState = 2


    def IntOp_04(self, lCmd = [] ):
        # Opcode 4 outputs the value of its only parameter. For example, the instruction 4,50
        # would output the value at address 50.
        if self.Verbosity >= 3: print( "[%d] OUTPUT" % self.IP)
        tParams = self.GetIntParams( lCmd, 1 )
        #print( tParams
        self.StdOut.append(tParams[0])
        if self.Verbosity >= 2: print( "[INTCODE] Output: [", tParams[0] , "]" )
        self.IP += len(lCmd)
        #self.print(IncodeMEM()


    def IntOp_05(self, lCmd = [] ):
        #Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction
        #pointer to the value from the second parameter. Otherwise, it does nothing.
        if self.Verbosity >= 3: print( "[%d] JUMP IF TRUE" % self.IP, lCmd)
        
        tParams = self.GetIntParams( lCmd, 2 )
        #print( "Params:", tParams
        if tParams[0] != 0:
            if self.Verbosity >= 3: print( "    Jumping to [%d]" % tParams[1] )
            self.IP = tParams[1]
        else:
            self.IP += len(lCmd)
            if self.Verbosity >= 3: print( "    Continuing to [%d]" % self.IP  )

        #print( "New IP: ", self.IP
        
        
    def IntOp_06(self, lCmd = [] ):
        # Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction
        # pointer to the value from the second parameter. Otherwise, it does nothing.
        if self.Verbosity >= 3: print( "[%d] JUMP IF FALSE" % self.IP, lCmd)
        
        tParams = self.GetIntParams( lCmd, 2 )
        #print( "Params:", tParams
        if tParams[0] == 0:
            if self.Verbosity >= 3: print( "    Jumping to [%d]" % tParams[1] )
            self.IP = tParams[1]
        else:
            self.IP += len(lCmd)
            if self.Verbosity >= 3: print( "    Continuing to [%d]" % self.IP  )
        #print( "New IP: ", self.IP
       

    def IntOp_07(self, lCmd = [] ):
        # Opcode 7 is less than: if the first parameter is less than the second parameter, it
        # stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        if self.Verbosity >= 3: print( "[%d] LESS THAN" % self.IP, lCmd)
        
        tParams = self.GetIntParams( lCmd, 2, 1 )
        #print( "Params:", tParams
        if tParams[0] < tParams[1]:
            self.IntcodeMEM[ tParams[2] ] = 1
        else:
            self.IntcodeMEM[ tParams[2] ] = 0
        
        self.IP += len(lCmd)


    def IntOp_08(self, lCmd = [] ):
        # Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores
        # 1 in the position given by the third parameter. Otherwise, it stores 0.
        if self.Verbosity >= 3: print( "[%d] EQUAL" % self.IP, lCmd)
        
        tParams = self.GetIntParams( lCmd, 2, 1 )
        #print( "Params:", tParams
        if tParams[0] == tParams[1]:
            self.IntcodeMEM[ tParams[2] ] = 1
        else:
            self.IntcodeMEM[ tParams[2] ] = 0
        
        self.IP += len(lCmd)   


    def IntOp_09(self, lCmd = [] ):
        # Opcode 9 adjusts the relative base by the value of its only parameter. The relative base
        # increases (or decreases, if the value is negative) by the value of the parameter.
        if self.Verbosity >= 3: print( "[%d] REL BASE" % self.IP, lCmd)
        tParams = self.GetIntParams( lCmd, 1 )
        
        self.RelativeBase += tParams[0]
        if self.Verbosity >= 3: print( "    New Relative Base is *%d" % self.RelativeBase )
        
        self.IP += len(lCmd)
        

    def ProcessCurrentInstruction(self):
        #An Intcode program is a list of integers separated by commas (like 1,0,0,3,99).
        #To run one, start by looking at the first integer (called position 0). Here, 
        #you will find an opcode - either 1, 2, or 99. The opcode indicates what to do;
        #for example, 99 means that the program is finished and should immediately halt.
        #Encountering an unknown opcode means something went wrong.
        tIP = self.IP
        #print("cur IP:", tIP)
        tOpCode = self.IntcodeMEM[self.IP] - (int(self.IntcodeMEM[self.IP] / 100)) * 100
        if self.Verbosity >= 10: print( "OpCode at positiom %d is %d" % ( tIP, tOpCode ))
    
        if tOpCode == 99:
            self.IntOp_99()
            return 0
            
        elif tOpCode == 1:
            self.IntOp_01( self.IntcodeMEM[tIP:tIP+4] )
            
        elif tOpCode == 2:
            self.IntOp_02( self.IntcodeMEM[tIP:tIP+4] )
            
        elif tOpCode == 3:
            self.IntOp_03( self.IntcodeMEM[tIP:tIP+2] )
            
        elif tOpCode == 4:
            self.IntOp_04( self.IntcodeMEM[tIP:tIP+2] )
            
        elif tOpCode == 5:
            self.IntOp_05( self.IntcodeMEM[tIP:tIP+3] )
            
        elif tOpCode == 6:
            self.IntOp_06( self.IntcodeMEM[tIP:tIP+3] )
        
        elif tOpCode == 7:
            self.IntOp_07( self.IntcodeMEM[tIP:tIP+4] )
        
        elif tOpCode == 8:
            self.IntOp_08( self.IntcodeMEM[tIP:tIP+4] )
            
        elif tOpCode == 9:
            self.IntOp_09( self.IntcodeMEM[tIP:tIP+2] )

            
        else:
            #Encountering an unknown opcode means something went wrong.
            print( "Something Went Wrong!" )
            if self.Verbosity >= 2: self.PrintIncodeMEM()
            return 1
            

    

        
        