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


def read_asm() -> list:
    """Reads the input file and returns a list with each line as an element. If there is not an input file 'entrada.asm', it reads the default 'exemplo.asm' file."""
    pattern = r"[ ,]"
    instruction_list = list()
    try:
        file = open("entrada.asm", 'r')
    except FileNotFoundError:
        file = open("base/exemplo.asm", 'r')
    for line in file.readlines():
        line = re.split(pattern, line.replace("\n", "").lower())
        for i in range(line.count("")):
            line.remove("")
        instruction_list.append(line)
    return instruction_list
