import re


def read_instructions() -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    """Generates dictionaries of types, opcodes and functions.
    Returns a tuple with each one mapping name to binary value."""
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


def read_asm() -> tuple[list, list]:
    """Reads the input file and returns a list with each line as an element.
    If there is not an input file 'entrada.asm', it reads the default 'exemplo.asm' file."""
    pattern = r"[ ,]"
    instruction_list = list()
    data_list = list()
    continue_data = False

    try:
        file = open("base/entrada.asm", 'r')
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
            if len(line) > 0 and "#" not in line and "syscall" not in line and "la" not in line and "li" not in line:
                instruction_list.append(line)
    if data_list.__len__() > 0:
        data_list.pop(0)
    return instruction_list, data_list
