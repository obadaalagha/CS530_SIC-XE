class StorageObject:
    def __init__(self, trueValue, indexValue, size):
        self.trueValue = trueValue;
        self.indexValue = indexValue;
        self.size = size;


# Initialize registers
#registers = np.random.rand(9);
#registers = registers*(2**20);
#registers = registers.astype("int32");

# Initialize memory
#memory = np.random.rand(2**20);
#memory = memory*(2**20);
#memory = memory.astype("int32");
# A X L B S T F PC SW
#A, X, L, B, S, T = StorageObject(None, None, None), StorageObject(None, None, None), StorageObject(None, None, None), StorageObject(None, None, None), StorageObject(None, None, None), StorageObject(None, None, None);
#F = 0.;
#PC = -1;
#SW = None;
#registers = [A, X, L, B, S, T, float(F), int(PC), str(SW)];

registers = {
    'A': StorageObject(None, None, None),
    'X': StorageObject(None, None, None),
    'L': StorageObject(None, None, None),
    'B': StorageObject(None, None, None),
    'S': StorageObject(None, None, None),
    'T': StorageObject(None, None, None),
    'F': float(0.),
    'PC': -1,
    'SW': None
};

memory = [];
for i in range(0, 0x1000000):
    x = StorageObject(None, None, None);
    memory.append(x);

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
};

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
};

SYMTAB = {};
locRecord = [];

def first_pass(assembly_code):
    #line_count = 1;
    with open(assembly_code) as input:
        line_count = 0;
        # Reading the first line
        first_line = input.readline();
        first_line = first_line.strip();
        #line_count = 0;

        # Getting program starting address
        start = int(first_line[17:], 16);
        loc_counter = start;
        #line_count += 1;

        for line in input:
            # Getting label, mnemonic and arg from each line
            label = line[0:7].strip();
            mnemonic = line[9:15].strip();
            arg = line[17:].strip();

            line_count += 1;
            # If there is something in label, add it to the SYMTAB
            if(len(label) > 0):
                SYMTAB[label] = (loc_counter, line_count);

            #line_count = 0;

            plus = False;
            if(line[8] == "+"):
                plus = True;
            locRecord.append(loc_counter);
            if(mnemonic in OpTable):
                if(OpTable[mnemonic][1] > 2):
                    if(plus == True):
                        loc_counter += 4;
                    else:
                        loc_counter += 3;
                elif((OpTable[mnemonic][1] == 2) and (plus == False)):
                    loc_counter += 2;
                elif((OpTable[mnemonic][1] == 1) and (plus == False)):
                    loc_counter += 1;
            elif (mnemonic in directives):
                if(mnemonic == 'RESW'):
                    loc_counter += int(arg) * 3;
                elif(mnemonic == 'RESB'):
                    loc_counter += int(arg);
                elif(mnemonic == 'WORD'):
                    loc_counter += 3;
                elif(mnemonic == 'BYTE'):
                    loc_counter += 1;
                elif(mnemonic in directives):
                    continue;
                elif(directives[mnemonic] == 'END'):
                    break;
            else:
                print("Error");

    # TESTING PURPOSES
    print("SYMTAB");
    for key,value in SYMTAB.items():
        print("%-6s, 0x%X, %d" %(key, value[0], value[1]));

    return SYMTAB;

def changeMemory(toAdd, address):
    if type(toAdd) == str:
        memory[address].size = len(toAdd) - 1;
        memory[address].trueValue = toAdd;
        for i in range(0, len(toAdd)):
            memory[address+i].indexValue = ord(toAdd[i]);
    elif type(toAdd) == int:
        if(toAdd < 0x100):
            memory[address].size = 0;
            memory[address].trueValue = toAdd;
            memory[address].indexValue = (toAdd & 0x0000FF);
        elif(toAdd < 0x10000):
            memory[address].size = 1;
            memory[address].trueValue = toAdd;
            memory[address].indexValue = (toAdd & 0x00FF00);
            memory[address+1].indexValue = (toAdd & 0x0000FF);
        elif(toAdd < 0x1000000):
            memory[address].size = 2;
            memory[address].trueValue = toAdd;
            memory[address].indexValue = (toAdd & 0xFF0000);
            memory[address+1].indexValue = (toAdd & 0x00FF00);
            memory[address+2].indexValue = (toAdd & 0x0000FF);
        else:
            print("ERROR 1");
    else:
        print("ERROR 2");

def getMemValue(address):
    '''

    '''
    return memory[address].indexValue;


def getLabel(label, what):
    """
    ARGS:

    RETURN:
    """
    if what == 'Value':
        return memory[SYMTAB[label][0]].trueValue;
    elif what == 'Address':
        return SYMTAB[label][0];
    elif what == 'Line':
        return SYMTAB[label][1];
    else:
        print('ERROR 3 just for paul');

def modifyReg(regName, content):
    if regName in registers:
        registers[regName] = content;
    else:
        print('ERROR 4 just for paul v2');

def getReg(regName):
    if regName in registers:
        return registers[regName];
    else:
        print('ERROR 5 JUST FOR PAUL');

def second_pass(assembly_file):
    with open(assembly_file) as input:
        line_count = 0;
        # Reading the first line
        first_line = input.readline();
        first_line = first_line.strip();

        # Getting program starting address
        start = int(first_line[17:], 16);
        loc_counter = start;
        line_count += 1;

        for line in input:
            # Getting label, mnemonic and arg from each line
            label = line[0:7].strip();
            mnemonic = line[9:15].strip();
            arg = line[17:].strip();

            line_count += 1;

            if(arg[16] == " "):
                arg = getMemValue(getLabel(arg, 'Address'));
            elif(arg[16] == "#"):
                if(arg not in SYMTAB):
                    arg = int(arg);
                else:
                    arg = int(getLabel(arg, 'Address'));
            elif("," in arg):
                pos = arg.find(",");
                one = arg[0:pos];
                two = arg[pos+1:];
                arg = (one,two);
            elif("+" in arg):
                pos = arg.find('+');
                one = arg[0:pos];
                two = arg[pos+1:];
                arg = getLabel(one, 'Address') + getLabel(two, 'Address');
            elif("-" in arg):
                pos = arg.find('-');
                one = arg[0:pos];
                two = arg[pos+1:];
                arg = getLabel(one, 'Address') - getLabel(two, 'Address');
            elif(arg[16] == "@"):
                arg = getMemValue(getMemValue(int(arg)));
            else:
                print("NADA NOT CORRECT YOU'VE GOT AN ERROR");
            
            if(mnemonic == "AND"):
                registers['A'].trueValue = registers['A'].trueValue & arg;
            elif(mnemonic == "OR"):
                registers['A'].trueValue = registers['A'].trueValue | arg;
            elif(mnemonic == "SHIFTL"):
                #registers = [A, X, L, B, S, T, float(F), int(PC), str(SW)];
                if(type(arg[0]) == "StorageObject"):
                    registers[arg[0]].trueValue = registers[arg[0]].trueValue << arg[1];
                #elif()
            elif(mnemonic == "SHIFTR"):
                registers[arg[0]].trueValue = registers[arg[0]].trueValue >> arg[1];
            '''
            # If there is something in label, add it to the SYMTAB
            if(len(label) > 0):
                SYMTAB[label] = loc_counter;

            plus = False;
            if(line[8] == "+"):
                plus = True;
            if(mnemonic in OpTable):
                if(OpTable[mnemonic][1] > 2):
                    if(plus == True):
                        loc_counter += 4;
                    else:
                        loc_counter += 3;
                elif((OpTable[mnemonic][1] == 2) and (plus == False)):
                    loc_counter += 2;
                elif((OpTable[mnemonic][1] == 1) and (plus == False)):
                    loc_counter += 1;
            elif (mnemonic in directives):
                if(mnemonic == 'RESW'):
                    loc_counter += int(arg) * 3;
                elif(mnemonic == 'RESB'):
                    loc_counter += int(arg);
                elif(mnemonic == 'WORD'):
                    loc_counter += 3;
                elif(mnemonic == 'BYTE'):
                    loc_counter += 1;
                elif(mnemonic in directives):
                    continue;
                elif(directives[mnemonic] == 'END'):
                    break;
            else:
                print("Error");
    '''


changeMemory("Obada", 4000);
print(memory[4000].trueValue, memory[4000].indexValue, memory[4000].size);

#def addRegister():

first_pass('SampleCode.txt')

