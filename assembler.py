
from random import randint


wordsize = 31  # everything is a word
numregbits = 3  # actually +1, msb is indirect bit
opcodesize = 7         
memloadsize = 1024  # change this for larger programs
numregs = 2 ** numregbits
opcposition = wordsize - (opcodesize + 1)  # shift value to position opcode
reg1position = opcposition - (numregbits + 1)  # first register position
reg2position = reg1position - (numregbits + 1)
memaddrimmedposition = reg2position  # mem address or immediate same place as reg2
startexecptr = 0

compulsarymiss=0
capacitymiss=0
valid=[0]*5
block_size=2
number_of_rows=4
set_rows=2
arr = [[-1 for x in range(block_size)] for y in range(number_of_rows)]
arr1 = [[-1 for x in range(block_size)] for y in range(set_rows)]
arr2 = [[-1 for x in range(block_size)] for y in range(set_rows)]
miss_count=0
hit_count=0
capacitymiss=0
compulsarymiss=0
miss_count=0
hit_count=0
compulsarymiss=0
capacitymiss=0
count=0
the_choice=None



def simulateSetAssociativeMap(address,memval,address2,memval2):
    print ('Set')
    print ('address'),address,('memval1'),memval
    global count
    count+=1
    print (count)
    way=2
    global miss_count
    global arr1
    global arr2
    global arr
    global hit_count
    global compulsarymiss
    global capacitymiss
    for x in range(set_rows):
        for y in range(block_size):
            if arr1[x][y]==memval or arr2[x][y]==memval:
                hit_count+=1
                flag=True
                print ('HIT')
                print (flag)
                print ('array1'),arr1
                print ('array2'),arr2
                return
    offset = address % block_size
    which_set = address % way 
    row_in_set= address % set_rows
    print ('set'),which_set
    flag=False
    if not flag:
            print ('inside if')
            compulsarymiss+=1
            for x in range(set_rows):
                for y in range(block_size):
                    if which_set==0:
                        if arr1[x][y]==0 and y%2==0 and arr1[x][y+1]==0 :
                            arr1[x][y]=memval
                            arr1[x][y+1]=memval2
                            miss_count+=1
                            print ('MISS')
                            print ('array1'),arr1
                            print ('array2'),arr2
                            return
                    if which_set==1:
                        if arr2[x][y]==0 and y % 2==0 and arr2[x][y+1]==0:
                            arr2[x][y]=memval
                            arr2[x][y+1]=memval2
                            miss_count+=1
                            print ('MISS')
                            print ('array1'),arr1
                            print ('array2'),arr2
                            return
    notempty=True
    if notempty:
            print ('inside not empty')
            print ('replace the value in array')
            capacitymiss+=1
            miss_count+=1

            row=randint(0,1)
            print ('row chosen'),row
            if which_set==0:
                #if arr1[row][offset]
                    arr1[row][0]=memval
                    arr1[row][1]=memval2
                    print ('array1'),arr1
                    print ('array2'),arr2
                    return
            if which_set==1:
                #if arr2[x][y]==0 and arr2[x][y+1]==0:
                    arr2[row][0]=memval
                    arr2[row][1]=memval2
                    print ('array1'),arr1
                    print ('array2'),arr2
                    return
def simulateDirectMap(address,memval,address2,memval2):
    print ('Direct')
    print ('address'),address
    print ('memval1'),memval
    global miss_count
    global hit_count
    global compulsarymiss
    global capacitymiss
    for x in range(number_of_rows):
        for y in range(block_size):
            if arr[x][y]==memval:
                flag=True
                print ('HIT')
                hit_count+=1
                print (flag)
                return
    offset = address % block_size
    row=address%number_of_rows #which word it will go to
    print ('offset'),offset
    print ('row'),row
    print ('valid'),valid
    flag=False
    if valid[int(row)] == 0 and not flag:
        print ('inside if')
        valid[int(row)]=1
        print ('valid'),valid
        miss_count+=1
        print ('MISS')
        compulsarymiss+=1
        if offset == 0:
            arr[row][offset]=memval
            arr[row][offset+1]=memval2
    else:
        print ('inside else')
        print ('replace the value in array')
        capacitymiss+=1
        miss_count+=1
        valid[int(row)]=1
        arr[row][0]=memval
        arr[row][1]=memval2
    print (arr)


def regval (rstr):  
    if rstr.isdigit():
        return (int(rstr))
    elif rstr[0] == '*':
        return (int (rstr[1:]) + (1 << numregbits))
    else:
        return 0  # should not happen

mem = [0] * memloadsize  
store = (6, 8)
load = (6, 7)
opcodes = {'add': (2, 1), 'sub': (2, 2),  # ie, "add" is a type 2 instruction, opcode = 1
           'dec': (1, 3), 'inc': (1, 4),
           'ld': load, 'st': store,
           'ldi': (3, 9), 'bnz': (3, 12), 'brl': (3, 13),
           'ret': (1, 14),
           'int': (3, 16), 'sys': (3, 16), 'go':(3, 0),  # syscalls are same as interrupts
           'dw': (4, 0), 'end': (0, 0) }  # pseudo ops
curaddr = 0  # start assembling to location 0

infile = open("in.asm", 'r')
# Build Symbol Table
symboltable = {}
for line in infile.readlines():  # read our asm code
    tokens = line.split()  # tokens on each line
    firsttoken = tokens[0]

    if firsttoken.isdigit():  # if line starts with an address
        curaddr = int(firsttoken)  # assemble to here
    if firsttoken[0] == ';':  # skip comments
        continue
    if firsttoken == 'go':  # start execution here 
        continue
    if firsttoken[0] == '.':
        symboltable[firsttoken] = curaddr
    curaddr = curaddr + 1
print("symbol table") 
print(symboltable)
print("end sym table")
infile.close()

instructions = []



infile = open("in.asm", 'r')
for line in infile.readlines():  # read our asm code
    tokens = line.split()  # tokens on each line
    firsttoken = tokens[0]
    if firsttoken.isdigit():  # if line starts with an address
        curaddr = int(firsttoken)  # assemble to here
        tokens = tokens[1:]
    if firsttoken[0] == ';':  # skip comments
        continue
    if firsttoken == 'go':  # start execution here
        startexecptr = (int(tokens[ 1 ]) & ((2 ** wordsize) - 1))  # data
        continue
    if firsttoken[0] == '.':
        symaddr = symboltable[firsttoken]
        tokens = tokens[1:]
    memdata = 0  # build instruction step by step
    print("tokens", tokens)  # DEBUG
    instructions.append(tokens)
    print("here:", opcodes[ tokens[0] ])  # DEBUG
    instype = opcodes[ tokens[0] ] [0]
    memdata = (opcodes[ tokens[0] ] [1]) << opcposition  # put in opcode
    if instype == 4:  # dw type
        memdata = (int(tokens[ 1 ]) & ((2 ** wordsize) - 1))  # data is wordsize long
    elif instype == 0:  # end type
        memdata = memdata 
    elif instype == 1:  # dec, inc type, one reg
        memdata = memdata + (regval(tokens[1]) << reg1position)
    elif instype == 2:  # add, sub type, two regs
        memdata = memdata + (regval(tokens[1]) << reg1position) + (regval(tokens[2]) << reg2position)
    elif instype == 3:  
        token2 = tokens[2]
        if token2.isdigit():
            memaddr = int(token2)
        else:
            memaddr = symboltable[ token2 ] 
        memdata = memdata + (regval(tokens[1]) << reg1position) + memaddr
    elif instype == store[0]:  # ld, st
        token2 = tokens[2]
        if token2[0] == '*':
            #taken from add
            memdata = memdata + (regval(tokens[1]) << reg1position) + (regval(tokens[2]) << reg2position)      
        elif token2.isdigit():
            # for ld
            memaddr = int(token2)
            memdata = memdata + (regval(tokens[1]) << reg1position) + memaddr
        else:
            memaddr = symboltable[ token2 ] 
            memdata = memdata + (regval(tokens[1]) << reg1position) + memaddr
    mem[ curaddr ] = memdata  # memory image at the current location
    curaddr = curaddr + 1
    #print(memdata)
infile.close()

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
    '''print Scoreboard and the data hazard count
        and also the control hazard'''

    controlHazardCount = 0
    controlHazard = []
    print('Scoreboard: ')
    #print(instructions)
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
    #print(arr)
    scoreBoard = []
    for line in range(0, len(newList)):
        firsttoken = newList[line][0]
        if firsttoken == 'ld' or firsttoken == 'ldi' or firsttoken == 'inc' or firsttoken == 'dec':
            nexttoken = int(newList[line][1])
            #print(nexttoken)
            arr[line+1][nexttoken] = 'W'
        elif firsttoken == 'add':
            nexttoken = int(newList[line][1])
            nexttoken2 = int(newList[line][2][1:])
            #print(nexttoken)
            arr[line+1][nexttoken] = 'R/W'
            arr[line+1][nexttoken2] = 'R'
        elif firsttoken == 'bnz':
            nexttoken = int(newList[line][1])
            arr[line+1][nexttoken] = 'R'
            controlHazardCount += 1
        scoreBoard.append([newList[line]] + arr[line]) 

    for i in scoreBoard:
        #print(i[0])
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
            

outfile = open("a.out", 'w')  # done, write it out
outfile.write('go ' + '%d' % startexecptr)  # start execution here
outfile.write("\n")
for i in range(memloadsize):  # write memory image   
    outfile.write(hex(mem[ i ]) + "    " + '%d' % i)
    outfile.write("\n")
outfile.close()




