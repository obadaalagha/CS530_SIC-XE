import numpy as np

# Initialize registers
registers = np.random.rand(9)
registers = registers*(2**20)
registers = registers.astype("int32")

# Initialize memory
memory = np.random.rand(2**20)
memory = memory*(2**20)
memory = memory.astype("int32")

# Operation Code table
OpTable = {
    'ADD': (0x18, 3),
    'ADDF': (0x58, 3),
    'ADDR': (0x90, 2),
    'AND': (0x40, 3),
    'CLEAR': (0x04, 2),
    'COMP': (0x28, 3),
    'COMPF': (0x88, 3),
    'COMPR': (0xA0, 2),
    'DIV': (0x24, 3),
    'DIVF': (0x64, 3),
    'DIVR': (0x9C, 3),
    'FIX': (0xC4, 1),
    'FLOAT': (0xC0, 1),
    'HIO': (0xF4, 1),
    'J': (0x3C, 3),
    'JEQ': (0x30, 3),
    'JGT': (0x34, 3),
    'JLT': (0x38, 3),
    'JSUB': (0x48, 3),
    'LDA': (0x00, 3),
    'LDB': (0x68, 3),
    'LDCH': (0x50, 3),
    'LDF': (0x70, 3),
    'LDL': (0x08, 3),
    'LDS': (0x6C, 3),
    'LDT': (0x74, 3),
    'LDX': (0x04, 3),
    'LPS': (0xD0, 3),
    'MUL': (0x20, 3),
    'MULF': (0x60, 3),
    'MULR': (0x98, 2),
    'NORM': (0xC8, 1),
    'OR': (0x44, 3),
    'RD': (0xD8, 3),
    'RMO': (0xAC, 2),
    'RSUB': (0x4C, 3),
    'SHIFTL': (0xA4, 2),
    'SHIFTR': (0xA8, 2),
    'SIO': (0xF0, 1),
    'SSK': (0xEC, 3),
    'STA': (0x0C, 3),
    'STB': (0x78, 3),
    'STCH': (0x54, 3),
    'STF': (0x80, 3),
    'STI': (0xD4, 3),
    'STL': (0x14, 3),
    'STS': (0x7C, 3),
    'STSW': (0xE8, 3),
    'STT': (0x84, 3),
    'STX': (0x10, 3),
    'SUB': (0x1C, 3),
    'SUBF': (0x5C, 3),
    'SUBR': (0x94, 2),
    'SVC': (0xB0, 2),
    'TD': (0xE0, 3),
    'TIO': (0xF8, 1),
    'TIX': (0x2C, 3),
    'TIXR': (0xB8, 2),
    'WD': (0xDC, 3)
}

directives = {
    'START': 'START',
    'END': 'END',
    'EQU': 'APPEND',
    'ORG': 0,
    'BASE': 0,
    'LTORG': 0,
    'RESW': 'MULTIPLY',
    'RESB': 0,
    'BYTE': 0,
    'NOBASE': 0,
    'WORD': 0
}

def first_pass(assembly_code):
    with open(assembly_code) as input:

        # Reading the first line
        first_line = input.readline()
        first_line = first_line.strip()

        # Getting program starting address
        start = int(first_line[17:], 16)
        loc_counter = start
        labelDict = {}

        for line in input:
            # Getting label, mnemonic and arg from each line
            label = line[0:7].strip()
            mnemonic = line[9:15].strip()
            arg = line[17:].strip()

            # If there is something in label, add it to the labelDict
            if(len(label) > 0):
                labelDict[label] = loc_counter

            plus = False
            if(line[8] == "+"):
                plus = True
            if(mnemonic in OpTable):
                if(OpTable[mnemonic][1] > 2):
                    if(plus == True):
                        loc_counter += 4
                    else:
                        loc_counter += 3
                elif((OpTable[mnemonic][1] == 2) and (plus == False)):
                    loc_counter += 2
                elif((OpTable[mnemonic][1] == 1) and (plus == False)):
                    loc_counter += 1
            elif (mnemonic in directives):
                if(mnemonic == 'RESW'):
                    loc_counter += int(arg) * 3
                elif(mnemonic == 'RESB'):
                    loc_counter += int(arg)
                elif(mnemonic == 'WORD'):
                    loc_counter += 3
                elif(mnemonic == 'BYTE'):
                    loc_counter += 1
                elif(mnemonic in directives):
                    continue
                elif(directives[mnemonic] == 'END'):
                    break
            else:
                print("Error")


    print("SYMTAB")
    for key,value in labelDict.items():
        print("%-6s, 0x%X" %(key, value))

    return labelDict


first_pass('SampleCode.txt')

