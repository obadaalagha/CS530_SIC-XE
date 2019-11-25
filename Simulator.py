import random

print("WELCOME TO THE SIC/XE SIMULATOR WRITTEN BY OBADA ALAGHA, IN SAN CHAK, AND PAUL MAURO.");

class StorageObject:
    def __init__(self, trueValue, indexValue):
        self.trueValue = trueValue;
        self.indexValue = indexValue;

registers = {
    'A': StorageObject(random.randint(0, 0x1000000), None),
    'X': StorageObject(random.randint(0, 0x1000000), None),
    'L': StorageObject(random.randint(0, 0x1000000), None),
    'B': StorageObject(random.randint(0, 0x1000000), None),
    'S': StorageObject(random.randint(0, 0x1000000), None),
    'T': StorageObject(random.randint(0, 0x1000000), None),
    'F': float(0.),
    'PC': -1,
    'SW': random.randint(0, 0x1000000)
};

print("Please wait while the system intializes...");
# Filling up memory
memory = [];
for i in range(0, 0x1000000):
    x = StorageObject(None, (random.randint(0, 0x1000000) & 0x0000FF));
    memory.append(x);
print("System initialization complete.\n");

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

# Assembler Directives
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

#first_pass(fileName);

def first_pass(assembly_code):
    with open(assembly_code) as input:
        line_count = 0;
        offset_count = 0;

        # Reading the first line
        first_line = input.readline();
        offset_count += len(first_line);
        first_line = first_line.strip();

        # Getting program starting address
        start = int(first_line[17:], 16);
        #print('Starting address in decimal: %d, in hex: %X' %(start, start))
        loc_counter = start;
        locRecord.append(loc_counter);

        for line in input:
            # Getting label, mnemonic and arg from each line
            label = line[0:7];
            mnemonic = line[9:15];
            arg = line[17:];
            label = label.rstrip();
            mnemonic = mnemonic.rstrip();
            arg = arg.rstrip();

            line_count += 1;

            # If there is something in label, add it to the SYMTAB
            if(len(label) > 0):
                SYMTAB[label] = (loc_counter, line_count, offset_count);

            # Increment offset counter, ready for next line
            offset_count += len(line);

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
                    for i in range(0, int(arg)*3, 3):
                        changeMemory(random.randint(0, 0x1000000), loc_counter + i);
                    loc_counter += int(arg) * 3;
                elif(mnemonic == 'RESB'):
                    for i in range(0, int(arg)):
                        changeMemory(random.randint(0, 0x100), loc_counter + i);
                    loc_counter += int(arg);
                elif(mnemonic == 'WORD'):
                    changeMemory(int(arg), loc_counter);
                    loc_counter += 3;
                elif(mnemonic == 'BYTE'):
                    changeMemory(int(arg), loc_counter);
                    loc_counter += 1;
                elif(mnemonic in directives):
                    continue;
                elif(directives[mnemonic] == 'END'):
                    break;
            else:
                print("Error");
    # END FIRST PASS

def changeMemory(toAdd, address):
    if type(toAdd) == str:
        memory[address].trueValue = toAdd;
        for i in range(0, len(toAdd)):
            memory[address+i].indexValue = ord(toAdd[i]);
    elif type(toAdd) == int:
        if(toAdd < 0x100):
            memory[address].trueValue = toAdd;
            memory[address].indexValue = (toAdd & 0x0000FF);
        elif(toAdd < 0x10000):
            memory[address].trueValue = toAdd;
            memory[address].indexValue = (toAdd & 0x00FF00) >> 16;
            memory[address+1].indexValue = (toAdd & 0x0000FF);
        elif(toAdd < 0x1000000):
            memory[address].trueValue = toAdd;
            memory[address].indexValue = (toAdd & 0xFF0000) >> 16;
            memory[address+1].indexValue = (toAdd & 0x00FF00) >> 8;
            memory[address+2].indexValue = (toAdd & 0x0000FF);
        else:
            print("ERROR CHANGING MEMORY: Integer value is too big. toAdd = 0x%X, 0d%d" %(toAdd, toAdd));
    else:
        print("ERROR CHANGING MEMORY: Invalid data-type to store in memory. Valid types: %s, %s." %(int, str));

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
    elif what == 'Offset':
        return SYMTAB[label][2];
    else:
        print('ERROR: Please input a valid input.');

def modifyReg(regName, content):
    if regName in registers:
        if(regName in ['A', 'X', 'S', 'B', 'T', 'L']):
            if (type(content) == str):
                content = content[0:3];
                registers[regName].trueValue = content;
            elif (type(content) == int):
                content = (content & 0xFFFFFF)
                registers[regName].trueValue = content;
            else:
                print("ERROR: Incorrect data type. Plesae input an integer or string.");
        elif(regName == "PC"):
            registers[regName] = int(content);
        elif(regName == "F"):
            registers[regName] = float(content);
        else:
            registers[regName] = int(content);
        # FIXME
    else:
        print("ERROR: Not a valid register name.");

def getReg(regName):
    if regName in registers:
        if(regName in ['A', 'X', 'S', 'B', 'T', 'L']):
            return registers[regName].trueValue;
        else:
            return registers[regName]; 
    else:
        print("ERROR: Not a valid register name.");

def second_pass(assembly_file):
    with open(assembly_file) as asm:
        line_count = 0;
        modifyReg('PC', locRecord[line_count + 1])

        # Reading the first line
        first_line = asm.readline();
        first_line = first_line.strip();

        # Getting program starting address
        start = int(first_line[17:], 16);

        line_count += 1;
        modifyReg('PC', locRecord[line_count + 1])

        print(first_line);
        input("Press any key to continue to the next step...");

        for line in asm:
            print(line, end="");
            input("");
            # Getting label, mnemonic and arg from each line
            label = line[0:7];
            mnemonic = line[9:15];
            arg = line[17:];
            label = label.rstrip();
            mnemonic = mnemonic.rstrip();
            arg = arg.rstrip();

            # If there are no arguments, go to a different case
            if(len(line) < 17):
                mode = "NOARG";
            else:
                mode = line[16];
            
            # Once you hit an assembler directive, make sure the assembler doesn't break down
            if(mnemonic in directives):
                if(mnemonic in ['RESW', 'RESB', 'WORD', 'BYTE']):
                    break;
                else:
                    continue;
            
            if(mode == " "):
                if(',' not in arg and '+' not in arg and '-' not in arg):
                    labelName = arg; # For Jumps
                    arg = getMemValue(getLabel(arg, 'Address'));
                elif("," in arg):
                    pos = arg.find(",");
                    one = arg[0:pos];
                    two = arg[pos+1:];
                    if(two != 'X'):
                        arg = (one,two);
                    else:
                        if(type(one) == int):
                            arg = one;
                        else:
                            arg = getMemValue(getLabel(one, 'Address'));
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
                else:
                    print("ERROR: Invalid arguments in argument field.");
            elif(mode == "#"):
                if(arg not in SYMTAB):
                    arg = int(arg);
                elif(',' in arg):
                    pos = arg.find(",");
                    one = arg[0:pos];
                    two = arg[pos+1:];
                    arg = (getLabel(one, 'Address'), two);
                else:
                    arg = int(getLabel(arg, 'Address'));
            elif(mode == "NOARG"):
                if(mnemonic == "JSUB"):
                    # PC into L, arg into PC
                    modifyReg('L', getReg('PC'));
                    modifyReg('PC', getLabel(arg, 'Address'));
                elif(mnemonic == "RSUB"):
                    modifyReg('PC', getReg('L'));
            elif(mode == "@"):
                if(',' not in arg):
                    arg = getMemValue(getMemValue(int(arg)));
                else:
                    pos = arg.find(",");
                    one = arg[0:pos];
                    two = arg[pos+1:];
                    arg = (getMemValue(getMemValue(one)), two);
            else:
                print("ERROR: Incorrect symbol in addressing mode field.");
            
            if(mnemonic == "AND"):
                modifyReg('A', (getReg('A') & arg));
            elif(mnemonic == "OR"):
                modifyReg('A', (getReg('A') | arg));
            elif(mnemonic == "SHIFTL"):
                modifyReg(arg[0], (getReg(arg[0]) << arg[1]));
            elif(mnemonic == "SHIFTR"):
                modifyReg(arg[0], (getReg(arg[0]) >> arg[1]));
            elif(mnemonic == "ADDF"):
                modifyReg('F', (getReg('F') + float(arg)));
            elif(mnemonic == "SUBF"):
                modifyReg('F', (getReg('F') - float(arg)));
            elif(mnemonic == "MULF"):
                modifyReg('F', (getReg('F') * float(arg)));
            elif(mnemonic == "DIVF"):
                modifyReg('F', (getReg('F') / float(arg)));
            elif(mnemonic == "COMP"):
                compare = getReg('A') - arg;
                if(compare > 0):
                    modifyReg('SW', 2);
                elif(compare < 0):
                    modifyReg('SW', 1);
                else:
                    modifyReg('SW', 0);
            elif(mnemonic == "COMPF"):
                compare = getReg('F') - arg;
                if(compare > 0):
                    modifyReg('SW', 2);
                elif(compare < 0):
                    modifyReg('SW', 1);
                else:
                    modifyReg('SW', 0);
            elif(mnemonic == "COMPR"):
                if((type(arg[0]) == int) and (type(arg[1]) == int)):
                    arg[1] = getReg(arg[1]) - getReg(arg[0]);
                    if (arg[1] > 0):
                        modifyReg('SW', 2);
                    elif (arg[1] < 0):
                        modifyReg('SW', 1);
                    else:
                        modifyReg('SW', 0);
                elif((type(arg[0]) == str) and (type(arg[1]) == str)):
                    if (getLabel(arg[0], 'Value') < getLabel(arg[1], 'Value')):
                        modifyReg('SW', 2);
                    elif (getLabel(arg[0], 'Value') > getLabel(arg[1], 'Value')):
                        modifyReg('SW', 1);
                    else:
                        modifyReg('SW', 0);
                else:
                    print("ERROR: Invalid registers.")
            elif(mnemonic == "NORM"):
                # SKIP FOR NOW BRO PART 2
                print('temp');
            elif(mnemonic == "ADD"):
                modifyReg('A', (getReg('A') + int(arg)));
            elif(mnemonic == "SUB"):
                modifyReg('A', (getReg('A') - int(arg)));
            elif(mnemonic == "MUL"):
                modifyReg('A', (getReg('A') * int(arg)));
            elif(mnemonic == "DIV"):
                modifyReg('A', (getReg('A') // int(arg)));
            elif(mnemonic == "ADDR"):
                modifyReg(arg[1], (getReg(arg[0]) + getReg(arg[1])));
            elif(mnemonic == "CLEAR"):
                modifyReg(arg[0], 0);
            elif(mnemonic == "DIVR"):
                modifyReg(arg[1], (getReg(arg[1]) // getReg(arg[0])));
            elif(mnemonic == "SUBR"):
                modifyReg(arg[1], (getReg(arg[1]) - getReg(arg[0])));
            elif(mnemonic == "MULR"):
                modifyReg(arg[1], (getReg(arg[1]) * getReg(arg[0])));
            elif(mnemonic == "FIX"):
                modifyReg('A', int(getReg('F')));
            elif(mnemonic == "FLOAT"):
                modifyReg('F', float(getReg('A')));
            elif(mnemonic == "RMO"):
                modifyReg(arg[1], getReg(arg[0]));
            elif(mnemonic == "J"):
                line_to_jump = getLabel(labelName, 'Line');
                offset = getLabel(labelName, 'Offset');
                asm.seek(offset, 0);
                line_count = line_to_jump - 1;
            elif(mnemonic == "JEQ"):
                if(getReg('SW') == 0):
                    line_to_jump = getLabel(labelName, 'Line');
                    offset = getLabel(labelName, 'Offset');
                    asm.seek(offset, 0);
                    line_count = line_to_jump - 1;
                else:
                    continue;
            elif(mnemonic == "JLT"):
                if(getReg('SW') == 1):
                    line_to_jump = getLabel(labelName, 'Line');
                    offset = getLabel(labelName, 'Offset');
                    asm.seek(offset, 0);
                    line_count = line_to_jump - 1;
                else:
                    continue;
            elif(mnemonic == "JGT"):
                if(getReg('SW') == 2):
                    line_to_jump = getLabel(labelName, 'Line');
                    offset = getLabel(labelName, 'Offset');
                    asm.seek(offset, 0);
                    line_count = line_to_jump - 1;
                else:
                    continue;
            elif(mnemonic == "LDA"):
                modifyReg('A', arg);
            elif(mnemonic == "LDB"):
                modifyReg('B', arg);
            elif(mnemonic == "LDCH"):
                if(arg[:4] == "CHAR"):
                    modifyReg('A', arg[4]);
                elif(type(arg) == int):
                    modifyReg('A', (arg & 0xF));
                elif(type(arg) == str):
                    modifyReg('A', getLabel(arg, 'Address'));
                else:
                    print("ERROR: No single readable character to print");
                modifyReg('A', arg);
            elif(mnemonic == "LDF"):
                modifyReg('F', arg);
            elif(mnemonic == "LDL"):
                modifyReg('L', arg);
            elif(mnemonic == "LDS"):
                modifyReg('S', arg);
            elif(mnemonic == "LDT"):
                modifyReg('T', arg);
            elif(mnemonic == "LDX"):
                modifyReg('X', arg);
            elif(mnemonic == "STA"):
                changeMemory(getReg('A'), getLabel(labelName, 'Address'));
            elif(mnemonic == "STB"):
                changeMemory(getReg('B'), getLabel(labelName, 'Address'));
            elif(mnemonic == "STCH"):
                if(arg[:4] == "CHAR"):
                    changeMemory(getReg('A'), arg[4]);
                elif(type(arg) == int):
                    changeMemory(getReg('A'), (arg & 0xF));
                elif(type(arg) == str):
                    changeMemory(getReg('A'), getLabel(labelName, 'Address'));
                else:
                    print("ERROR: No single readable character");
            elif(mnemonic == "STF"):
                changeMemory(getReg('F'), getLabel(labelName, 'Address'));
            elif(mnemonic == "STL"):
                changeMemory(getReg('L'), getLabel(labelName, 'Address'));
            elif(mnemonic == "STS"):
                changeMemory(getReg('S'), getLabel(labelName, 'Address'));
            elif(mnemonic == "STSW"):
                changeMemory(getReg('SW'), getLabel(labelName, 'Address'));
            elif(mnemonic == "STT"):
                changeMemory(getReg('T'), getLabel(labelName, 'Address'));
            elif(mnemonic == "STX"):
                changeMemory(getReg('X'), getLabel(labelName, 'Address'));
            elif(mnemonic == "TIX"):
                #modifyReg('X', 0);
                modifyReg('X', getReg('X') + 1);
                code = getReg('X') - getLabel(labelName, 'Value');
                if(code == 0):
                    modifyReg('SW', 0);
                elif(code < 0):
                    modifyReg('SW', 1);
                elif(code > 0):
                    modifyReg('SW', 2);
            elif(mnemonic == "TIXR"):
                modifyReg('X', getReg('X') + 1);
                code = getReg('X') - getReg(labelName);
                if(code == 0):
                    modifyReg('SW', 0);
                elif(code < 0):
                    modifyReg('SW', 1);
                elif(code > 0):
                    modifyReg('SW', 2);
            elif(mnemonic == "JSUB"):
                continue;
            elif(mnemonic == "RSUB"):
                continue;
            else:
                print("ERROR: No mnemonic was found. Please input a valid command.");
                continue;
             
            line_count += 1;
            modifyReg('PC', locRecord[line_count + 1])
    # END SECOND PASS

while(True):
    fileName = input("Please type a file name (.txt or .sic) to assemble: ");
    fileName = fileName.strip();
    try:
        abc = open(fileName);
        abc.close();
        break;
    except:
        print("File does not exist. Please use a file that exists.\n");

ext = fileName.split(".");
if(ext[len(ext)-1] == "txt" or ext[len(ext)-1] == "sic"):
    print("USE INSTRUCTIONS:\n- Type \u001b[32m<1ST>\u001b[0m to run the assembler's first pass.\n- Type \u001b[32m<2ND>\u001b[0m to run the assembler's second pass.\n- Type \u001b[32m<REG>\u001b[0m to display the registers and their values.\n- Type \u001b[32m<SYM>\u001b[0m to display the Symbol Table. The Symbol Table will only be filled after the first pass.\n\n- Type \u001b[32m<MEM>\u001b[36m [START] [END] [BASE]\u001b[0m to display memory, where [START] indicates your starting address, [END] indicates your ending address, and [BASE] indicates base 10 or 16 numbering for addressing.\n\n- Type \u001b[32m<CHM>\u001b[36m [CONTENT] [ADDRESS] [DATA TYPE] [BASE]\u001b[0m to change a memory address, where [Content] is the content you want to change and [Address] is the beginning address to change your content. [DATA TYPE] indicates the data type to input, string or integer. [BASE] indicates base 10 or 16 numbering for content and addressing.\nNOTE: a string will overflow into the next address if it does not fit into the current one; integers will not overflow.\n\n- Type \u001b[32m<CHR>\u001b[36m [CONTENT] [REGISTER NAME] [DATA TYPE]\u001b[0m to change a register, where [CONTENT] is the content you want to change, [REGISTER NAME] is the register to change, and [DATA TYPE] is an integer or float.\nNOTE: Register F only takes in floating point values. All other registers take in 3 byte integers. This allows 16,777,200 integer values.\n\n- Type \u001b[32m<HELP>\u001b[0m for help.\n- Type \u001b[32m<EXIT>\u001b[0m to exit.\n\n");
    # FIXME MAYBE: THINK ABOUT INDIVIDUAL LINE INSTRUCTIONS?
else:
    print("ERROR: Invalid file.\n");


condition = True;
while(condition == True):
    cmd = input("user@SIC/XE: ");
    if(cmd[0:3].upper() == "1ST"):
        if((len(cmd) == 4) and (cmd[3] != " ")):
            print("\u001b[31mInvalid command. \u001b[32mType HELP for help.\u001b[0m\n");
        else:
            print("Starting first pass...", end="");
            first_pass(fileName);
            print("first pass completed.\n");
    elif(cmd[0:3].upper() == "2ND"):
        if(len(SYMTAB) == 0):
            print("Please run the first pass before running the second pass.");
        elif((len(cmd) == 4) and (cmd[3] != " ")):
            print("\u001b[31mInvalid command. \u001b[32mType HELP for help.\u001b[0m\n");
        else:
            print("Starting second pass...");
            second_pass(fileName);
            print("Second pass completed.\n");
    elif(cmd[0:3].upper() == "MEM"):
        cmd = cmd.split(' ');
        if(len(cmd) == 4):
            if(cmd[3].upper() == "10" or cmd[3].upper() == "DEC" or cmd[3].upper() == "DECIMAL"):
                start = int(cmd[1]);
                end = int(cmd[2]) + 1;
                index = start;
                print('[', end="")
                while (index < end):
                    print(" %2X " %(memory[index].indexValue), end="");
                    index += 1;
                    if(index % 30 == 0):
                        print(']')
                        print('[', end="")
                print(']')
            elif(cmd[3].upper() == "16" or cmd[3].upper() == "HEX" or cmd[3].upper() == "HEXADECIMAL"):
                start = int(cmd[1], 16);
                end = int(cmd[2], 16) + 1;
                index = start;
                print('[', end="")
                while (index < end):
                    print(" %2X " %(memory[index].indexValue), end="");
                    index += 1;
                    if(index % 30 == 0):
                        print(']')
                        print('[', end="")
                print(']')
            else:
                print("\u001b[31mImproper format.\u001b[0m Command usage: MEM [START] [END] [ADDRESS BASE]");
        else:
            print("\u001b[31mImproper format.\u001b[0m Command usage: MEM [START] [END] [ADDRESS BASE]");
    elif(cmd[0:3].upper() == "REG"):
        # DISPLAY REGISTERS
        regNames = ['A', 'X', 'L', 'B', 'S', 'T', 'F', 'PC', 'SW'];
        if((len(cmd) == 4) and (cmd[3] != " ")):
            print("\u001b[31mInvalid command. \u001b[32mType HELP for help.\u001b[0m\n");
        else:
            print(" REGISTER |  VALUE")
            for j in range(0, 9):
                if(regNames[j] != 'F' and regNames[j] != 'PC' and regNames[j] != 'SW'):
                    print("   (%s)    | 0x%X" %(regNames[j], getReg(regNames[j])));
                elif(regNames[j] == 'PC' or regNames[j] == "SW"):
                    print("   (%s)   | 0x%X" %(regNames[j], getReg(regNames[j])));
                else:
                    print("   (%s)    | %.4f" %(regNames[j], getReg(regNames[j])));
        print()
    elif(cmd[0:3].upper() == "SYM"):
        # DISPLAY SYMTAB
        if((len(cmd) == 4) and (cmd[3] != " ")):
            print("\u001b[31mInvalid command. \u001b[32mType HELP for help.\u001b[0m\n");
        else:
            print(" SYMBOL |  TABLE ");
            for key,value in SYMTAB.items():
                print(" %-6s | 0x%X" %(key, value[0]));
    elif(cmd[0:3].upper() == "CHM"):
        # CHANGE MEMORY
        #if((len(cmd) == 4) and (cmd[3] != " ")):
        #    print("Invalid command. Type HELP for help.\n");
        cmd = cmd.split(' ');
        if(len(cmd) == 5):
            if(cmd[4] == "10" or cmd[4].upper() == "DEC" or cmd[4].upper() == "DECIMAL"):
                if(cmd[3].upper() == "STR" or cmd[3].upper() == "STRING"):
                    changeMemory(str(cmd[1]), int(cmd[2]));
                elif(cmd[3].upper() == "INT" or cmd[3].upper() == "INTEGER"):
                    changeMemory(int(cmd[1]), int(cmd[2]));
                else:
                    print("\u001b[31mImproper format.\u001b[0m Command usage: CHM [CONTENT] [ADDRESS] [DATA TYPE] [BASE]\n");
            elif(cmd[4] == "16" or cmd[4].upper() == "HEX" or cmd[4].upper() == "HEXADECIMAL"):
                if(cmd[3].upper() == "STR" or cmd[3].upper() == "STRING"):
                    changeMemory(str(cmd[1]), int(cmd[2], 16));
                elif(cmd[3].upper() == "INT" or cmd[3].upper() == "INTEGER"):
                    changeMemory(int(cmd[1], 16), int(cmd[2], 16));
                else:
                    print("\u001b[31mImproper format.\u001b[0m Command usage: CHM [CONTENT] [ADDRESS] [DATA TYPE] [BASE]\n");
        else:
            print("\u001b[31mImproper format.\u001b[0m Command usage: CHM [CONTENT] [ADDRESS] [DATA TYPE] [BASE]\n");
    elif(cmd[0:3].upper() == "CHR"):
        # CHANGE REGISTERS
        cmd = cmd.split(' ');
        if(len(cmd) == 4):
            if(cmd[3].upper() == "INT" or cmd[3].upper == "INTEGER"):
                modifyReg(cmd[2], int(cmd[1]));
            elif(cmd[3].upper() == "FLOAT" or cmd[3].upper() == "F"):
                modifyReg('F', float(cmd[1]));
            else:
                print("\u001b[31mImproper format.\u001b[0m Command usage: CHR [CONTENT] [REGISTER NAME] [DATA TYPE]\n");
        else:
            print("\u001b[31mImproper format.\u001b[0m Command usage: CHR [CONTENT] [REGISTER NAME] [DATA TYPE]\n");
    elif(cmd.upper() == "HELP"):
        # USER HELP
        print("- Type \u001b[32m<1ST>\u001b[0m to run the assembler's first pass.\n- Type \u001b[32m<2ND>\u001b[0m to run the assembler's second pass.\n- Type \u001b[32m<REG>\u001b[0m to display the registers and their values.\n- Type \u001b[32m<SYM>\u001b[0m to display the Symbol Table. The Symbol Table will only be filled after the first pass.\n\n- Type \u001b[32m<MEM>\u001b[36m [START] [END] [BASE]\u001b[0m to display memory, where [START] indicates your starting address, [END] indicates your ending address, and [BASE] indicates base 10 or 16 numbering for addressing.\n\n- Type \u001b[32m<CHM>\u001b[36m [CONTENT] [ADDRESS] [DATA TYPE] [BASE]\u001b[0m to change a memory address, where [Content] is the content you want to change and [Address] is the beginning address to change your content. [DATA TYPE] indicates the data type to input, string or integer. [BASE] indicates base 10 or 16 numbering for content and addressing.\nNOTE: a string will overflow into the next address if it does not fit into the current one; integers will not overflow.\n\n- Type \u001b[32m<CHR>\u001b[36m [CONTENT] [REGISTER NAME] [DATA TYPE]\u001b[0m to change a register, where [CONTENT] is the content you want to change, [REGISTER NAME] is the register to change, and [DATA TYPE] is an integer or float.\nNOTE: Register F only takes in floating point values. All other registers take in 3 byte integers. This allows 16,777,200 integer values.\n\n- Type \u001b[32m<HELP>\u001b[0m for help.\n- Type \u001b[32m<EXIT>\u001b[0m to exit.\n\n");
    elif(cmd.upper() == "EXIT"):
        # EXIT
        sure = input("Are you sure? \u001b[33m[Y/N]\u001b[0m\n");
        if(sure.upper() == "Y" or sure.upper() == "YES"):
            condition = False;
        elif(sure.upper() == "N" or sure.upper() == "NO"):
            continue;
        else:
            print("\u001b[33mPlease specify YES or NO.\u001b[0m");
    else:
        print("\u001b[31mPlease input a valid command!\u001b[32m Type HELP for help.\u001b[0m\n");