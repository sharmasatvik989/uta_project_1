
from random import randint
import  sys, string, time
wordsize = 31                                        # everything is a word
numregbits = 3                                       # actually +1, msb is indirect bit
opcodesize = 7
addrsize = wordsize - (opcodesize+numregbits+1+1)      # num bits in address
memloadsize = 1024                                   # change this for larger programs
numregs = 2**numregbits
regmask = (numregs*2)-1                              # including indirect bit
addmask = (2**(addrsize)) -1
nummask = (2**(wordsize))-1
opcposition = wordsize - (opcodesize + 1)            # shift value to position opcode
reg1position = opcposition - (numregbits +1)            # first register position
reg2position = reg1position - (numregbits +1)
memaddrimmedposition = reg2position                  # mem address or immediate same place as reg2
realmemsize = memloadsize * 1                        # this is memory size, should be (much) bigger than a program
codeseg = numregs - 1                                # last reg is a code segment pointer
dataseg = numregs - 2                                # next to last reg is a data segment pointer
trapreglink = numregs - 3                            # store return value here
trapval     = numregs - 4                            # pass which trap/int
mem = [0] * realmemsize                              # this is memory, init to 0 
reg = [0] * numregs                                  # registers
clock = 0                                            # clock starts ticking
ic = 0                                               # instruction count
numcoderefs = 0                                      # number of times instructions read
numdatarefs = 0                                      # number of times data read
starttime = time.time()
curtime = starttime






def startexechere ( p ):
    reg[ codeseg ] = p    
def loadmem():                                       # get binary load image
    curaddr = 0
    for line in open("a.out", 'r').readlines():
        token = line.split()      # first token on each line is mem word, ignore rest
        if ( token[ 0 ] == 'go' ):
            startexechere(  int( token[ 1 ] ) )
        else:    
            mem[ curaddr ] = int( token[ 0 ], 0 )                
            curaddr = curaddr = curaddr + 1
def getcodemem ( a ):
    memval = mem[ a + reg[ codeseg ] ]
    return ( memval )
def getdatamem ( a ):
    memval = mem[ a + reg[ dataseg ] ]
    return ( memval )

def getregval ( r ):
    if ( (r & (1<<numregbits)) == 0 ):               # not indirect
        rval = reg[ r ] 
    else:
        rval = getdatamem( reg[ r - numregs ] )       # indirect data with mem address
    return ( rval )
def checkres( v1, v2, res):
    v1sign = ( v1 >> (wordsize - 1) ) & 1
    v2sign = ( v2 >> (wordsize - 1) ) & 1
    ressign = ( res >> (wordsize - 1) ) & 1
    if ( ( v1sign ) & ( v2sign ) & ( not ressign ) ):
        return ( 1 )
    elif ( ( not v1sign ) & ( not v2sign ) & ( ressign ) ):
        return ( 1 )
    else:
        return( 0 )
def dumpstate ( d ):
    if ( d == 1 ):
        print (reg)
    elif ( d == 2 ):
        print (mem)
    elif ( d == 3 ):
        print ('clock=', clock, 'IC=', ic, 'Coderefs=', numcoderefs,'Datarefs=', numdatarefs, 'Start Time=', starttime, 'Currently=', time.time()) 
def trap ( t ):
    rl = trapreglink                            # store return value here
    rv = trapval
    if ( ( t == 0 ) | ( t == 1 ) ):
        dumpstate( 1 )
        dumpstate( 2 )
        dumpstate( 3 )
    elif ( t == 2 ):                          # sys call, reg trapval has a parameter
        what = reg[ trapval ] 
        if ( what == 1 ):
            print('whatever')
    return ( -1, -1 )
    return ( rv, rl )


store = 6 #store code
load = 6
opcodes = { 1: (2, 'add'),
            2: ( 2, 'sub'), 
            3: (1, 'dec'),
            4: ( 1, 'inc' ),
            7: (load, 'ld'),
            8: (store, 'st'),
            9: (3, 'ldi'),
            12: (3, 'bnz'),
            13: (3, 'brl'),
            14: (1, 'ret'),
            16: (3, 'int')}
startexechere( 0 )                                  # start execution here if no "go"
loadmem()                                           # load binary executable
ip = 0                                              # start execution at codeseg location 0
# while instruction is not halt

instructions = []
branchGuess = []
branchPrediction = []

while( 1 ):    
    ir = getcodemem(ip)  # - fetch    
    ip = ip + 1
    clock = clock + 4
    opcode = ir >> opcposition  # - decode
    reg1 = (ir >> reg1position) & regmask
    reg2 = (ir >> reg2position) & regmask
    addr = (ir) & addmask
    ic = ic + 1
    clock = clock + 1
    instruction = []
    print('opcode: '+ str(opcode))
    print('reg1: '+ str(reg1))
    print('reg2: '+str(reg2))


    instruction.append(opcodes[opcode][1])
    instruction.append(str(reg1))
    instructions.append(instruction)
                                                                # - operand fetch    
    if not (opcode in opcodes):
        tval, treg = trap(0) 
        if (tval == -1):  # illegal instruction
            break
    memdata = 0  #     contents of memory for loads
    if opcodes[ opcode ] [0] == 1:  #     dec, inc type, one reg
        operand1 = getregval(reg1)  #       fetch operands
    elif opcodes[ opcode ] [0] == 2:  #     add, sub type, two regs
        operand1 = getregval(reg1)  #       fetch operands
        operand2 = getregval(reg2)
    elif opcodes[ opcode ] [0] == 3:
        operand1 = getregval(reg1)  #       fetch operands
        operand2 = addr          
    elif opcodes[ opcode ] [0] == store:  #     ld,st
        operand1 = getregval(reg1)                              #       fetch operands
        opc = 1 << numregbits
        if ((reg2 & (opc)) == 0):
            operand2 = addr 
        else:
            operand2 = reg[ reg2 - numregs ]   
    elif opcodes[ opcode ] [0] == 0:
        break
    if (opcode == 7):  # get data memory for loads
        memdata = getdatamem(operand2)
                                                        # execute
    if opcode == 1:  # add
        print("opcode is add which is 1")
        result = (operand1 + operand2) & nummask
        print("result: " + str(result))
        print("reg2position: " + str(reg2position))
        register = 3
        if str(operand2) == str('11'):
            register = 3
        elif str(operand2) == str('12'):
            register = 4
        elif str(operand2) == str('13'):
            register = 5
        elif str(operand2) == str('14'):
            register = 6    
        instruction.append(str(register))
        if (checkres(operand1, operand2, result)):
            tval, treg = trap(1) 
            if (tval == -1):  # overflow
                break
    elif opcode == 2:  # sub
        instruction.append(str(reg2))
        result = (operand1 - operand2) & nummask
        if (checkres(operand1, operand2, result)):
            tval, treg = trap(1) 
            if (tval == -1):  # overflow
                break
    elif opcode == 3:  # dec
        instruction.append(str(reg2))
        result = operand1 - 1
    elif opcode == 4:  # inc
        instruction.append(str(reg2))
        result = operand1 + 1
    elif opcode == 7:  # load
        instruction.append(str(reg2))
        result = memdata
    elif opcode == 8:  # store
        instruction.append(str(reg2))
        adr = operand2 + reg[dataseg]
        mem[adr] = operand1
    elif opcode == 9:  # load immediate
        instruction.append(str(reg2))
        result = operand2
    elif opcode == 12:  # conditional branch
        branchGuess.append(True)
        instruction.append(str(reg2))
        result = operand1
        if result != 0:
            ip = operand2
        branchPrediction.append(result != 0)
    elif opcode == 13:  # branch and link
        instruction.append(str(reg2))
        result = ip
        ip = operand2
    elif opcode == 14:  # return
        instruction.append(str(reg2))
        ip = operand1
    elif opcode == 16:  # interrupt/sys call
        instruction.append(str(reg2))
        result = ip
        tval, treg = trap(reg1)
        if (tval == -1):
            break
        reg1 = treg
        ip = operand2
    # write back
    if ((opcode == 1) | (opcode == 2) | 
        (opcode == 3) | (opcode == 4)):  # arithmetic
        reg[ reg1 ] = result
    elif ((opcode == 7) | (opcode == 9)):  # loads
        reg[ reg1 ] = result
    elif (opcode == 13):  # store return address
        reg[ reg1 ] = result
    elif (opcode == 16):  # store return address
        reg[ reg1 ] = result

   ##Check Data Hazard

def checkDataHazard(l1, l2):
    for i in range(0, len(l2)):
        row1 = l1[i]
        row2 = l2[i]
        #print(row1)
        #print(row2)
        if row1 == 'W' and row2 == 'R/W':
            return True
        elif row1 == 'W' and row2 == 'R':
            return True
    return False


## Create scoreboard
def createScoreboard(instructions):

    controlHazardCount = 0
    controlHazard = []
    print('Scoreboard: ')
    newList = []
    for line in instructions:
        if len(line) > 3:
            s = ' '.join([str(item) for item in line])
            #print(s)
            for i in range(0, len(s)):
                if s[i] == ';':  
                    newList.append(s[0:i].split())
        else:
            newList.append(line)

    rows, cols = (len(newList), 8)
    arr = [['*' for i in range(cols)] for j in range(rows)]
    scoreBoard = []
    for line in range(0, len(newList)):
        firsttoken = newList[line][0]
        if firsttoken == 'ld' or firsttoken == 'ldi' or firsttoken == 'inc' or firsttoken == 'dec':
            nexttoken = int(newList[line][1])
            arr[line+1][nexttoken] = 'W'

            
        elif firsttoken == 'add':
            nexttoken = int(newList[line][1])
            nexttoken2 = int(newList[line][2])
            arr[line+1][nexttoken] = 'R/W'
            arr[line+1][nexttoken2] = 'R'
            
        elif firsttoken == 'bnz':
            nexttoken = int(newList[line][1])
            arr[line+1][nexttoken] = 'R'
            controlHazardCount += 1
            
        scoreBoard.append([newList[line]] + arr[line]) 

    for i in scoreBoard:
        print(i[1:])

    dataHazard = []
    dataHazardCount = 0
    for row1 in range(0, len(scoreBoard)-1):
        l1 = scoreBoard[row1][1:]
        l2 = scoreBoard[row1+1][1:]
        dataHazard.append(checkDataHazard(l1, l2))
        if checkDataHazard(l1, l2):
            dataHazardCount += 1

    print('data Hazard Count: '+' '+str(dataHazardCount))
    print('control Hazard Count: '+' '+str(controlHazardCount))
    print('branchGuess: ')
    print(branchGuess)
    print('branchPrediction: ')
    print(branchPrediction)

createScoreboard(instructions)


