class ADV19_IntcodeComputer(object):

    def __init__(self, sIntcodeProg = [], iVerbosity = 0 ): 
        self.Verbosity = iVerbosity
        self.IntcodeMEM = []
        self.IntcodeProgram = []
        self.IP = 0
        
        self.LoadProgram(sIntcodeProg)
        self.LoadProgramToMemory()
        if self.Verbosity >= 1: print("Initialized DEC02 Intcode Computer")


    def PrintIncodeMEM(self, printIntCode = []):
        if printIntCode == []:
            pIC = self.IntcodeMEM
        else:
            pIC = printIntCode
        print("\n============================")
        print("IP: %d" % self.IP)
        print("Intcode Memory:")
        print("============================")
        tCtr = 0
        for iC in self.IntcodeMEM:
            print("%d, " % iC, end='')
            tCtr += 1
            if tCtr % 4 == 0 or iC == 99:
                print()
        print("\n============================\n")
 
 
    def LoadProgram(self, sIntcodeProg = []):
        self.IntcodeProgram = sIntcodeProg
 
    def LoadProgramToMemory(self):
        self.IntcodeMEM = self.IntcodeProgram[:]
 
    def RestartProgram(self):
        self.IP = 0
        self.ProcessCurrentInstruction()
    
    def ProcessCurrentInstruction(self):
        #An Intcode program is a list of integers separated by commas (like 1,0,0,3,99).
        #To run one, start by looking at the first integer (called position 0). Here, 
        #you will find an opcode - either 1, 2, or 99. The opcode indicates what to do;
        #for example, 99 means that the program is finished and should immediately halt.
        #Encountering an unknown opcode means something went wrong.
        tIP = self.IP
        tOpCode = self.IntcodeMEM[self.IP]    
        if self.Verbosity >= 5: print("OpCode at positiom %d is %d" % ( tIP, tOpCode ))
    
        if tOpCode == 99:
            #99 means that the program is finished and should immediately halt.
            if self.Verbosity >= 2: print("   ** PROGRAM HALT **")
            self.IP += 1
            #self.PrintIncodeMEM()
            return 0
            
        elif tOpCode == 1:
            if self.Verbosity >= 2: print("   ADDER")
            #Opcode 1 adds together numbers read from two positions and stores the result
            #in a third position. The three integers immediately after the opcode tell you
            #these three positions - the first two indicate the positions from which you
            #should read the input values, and the third indicates the position at which
            #the output should be stored.
            pVar1 = self.IntcodeMEM[ tIP + 1 ]
            pVar2 = self.IntcodeMEM[ tIP + 2 ]
            pDest = self.IntcodeMEM[ tIP + 3 ]
            
            if self.Verbosity >= 5: print(" Adding *%d to *%d and sending to *%d" % (pVar1, pVar2, pDest) )
            
            iVar1 = self.IntcodeMEM[ pVar1 ]
            iVar2 = self.IntcodeMEM[ pVar2 ]
            iAdd = iVar1 + iVar2
            
            if self.Verbosity >= 5: print("  Got %d + %d = %d" % ( iVar1, iVar2, iAdd) )
            
            self.IntcodeMEM[ pDest ] = iAdd
            self.IP += 4
            #self.PrintIncodeMEM()
            
        elif tOpCode == 2:
            if self.Verbosity  >= 2: print("   MULTIPLIER")
            #Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead
            #of adding them. Again, the three integers after the opcode indicate where the
            #inputs and outputs are, not their values.
            pVar1 = self.IntcodeMEM[ tIP + 1 ]
            pVar2 = self.IntcodeMEM[ tIP + 2 ]
            pDest = self.IntcodeMEM[ tIP + 3 ]
            
            if self.Verbosity  >= 5: print(" Multiplying *%d to *%d and sending to *%d" % (pVar1, pVar2, pDest) )
            
            iVar1 = self.IntcodeMEM[ pVar1 ]
            iVar2 = self.IntcodeMEM[ pVar2 ]
            iMult = iVar1 * iVar2
            
            if self.Verbosity  >= 5: print("  Got %d * %d = %d" % ( iVar1, iVar2, iMult) )
            
            self.IntcodeMEM[ pDest ] = iMult
            self.IP += 4
            #self.PrintIncodeMEM()
            
        else:
            #Encountering an unknown opcode means something went wrong.
            print("Something Went Wrong!")
            if self.Verbosity  >= 2: self.PrintIncodeMEM()
            return 1
            

        self.ProcessCurrentInstruction()
    
    

