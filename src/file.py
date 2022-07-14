import re


def read_instructions() -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    """Generates dictionaries of types, opcodes and functions. Returns a tuple with each one mapping name to binary value."""
    types = dict()
    opcodes = dict()
    functions = dict()

    for line in open("base/instructions.txt", 'r').readlines():
        line = line[:-1].split(';')
        types[line[0]] = line[1]
        opcodes[line[0]] = line[2]
        if line[1] == 'r':
            functions[line[0]] = line[3]

    return types, opcodes, functions


def read_registers() -> dict[str, str]:
    """Generates a dictionary mapping register name to its binary value."""
    registers = dict()

    for line in open("base/registers.txt", 'r').readlines():
        line = line[:-1].split(';')
        registers[line[0]] = line[1]

    return registers


def verificarFuncao(line):
    if ":" in line[-1] and line[-1][-1] == ":":
        return False
    return True


def read_asm() -> tuple[list, list]:
    """Reads the input file and returns a list with each line as an element. If there is not an input file 'entrada.asm', it reads the default 'exemplo.asm' file."""
    pattern = r"[ ,]"
    instruction_list = list()
    data_list = list()
    continue_data = False

    try:
        file = open("base/exemplodata.asm", 'r')
    except FileNotFoundError:
        file = open("base/exemplo.asm", 'r')
    for line in file.readlines():
        if ".data" in line or continue_data:
            line = re.split(pattern, line.replace("\n", "").lower())
            for i in range(line.count("")):
                line.remove("")
            continue_data = True
            if ".text" in line:
                continue_data = False
            if len(line) > 0 and continue_data:
                data_list.append(line)
        else:
            line = re.split(pattern, line.replace("\n", "").lower())
            for i in range(line.count("")):
                line.remove("")
            if len(line) > 0 and "li" not in line and "syscall" not in line and verificarFuncao(line):
                instruction_list.append(line)
    data_list.pop(0)
    print(instruction_list)
    return instruction_list, data_list
