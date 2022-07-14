from src.Instruction import Instruction
from src.interface import Info


def set_instruction(stage: str, instruction: str):
    Info.STAGES[stage] = instruction


def set_instruction_exec_if(instruction: Instruction, instruction_str: str, instruction_executadas:
dict):
    set_instruction(stage="IF", instruction=instruction_str)
    instruction_executadas["IF"] = instruction


def set_instruction_exec_id(instruction: Instruction, instruction_str: str, instruction_executadas:
dict):
    set_instruction(stage="ID", instruction=instruction_str)
    instruction_executadas["ID"] = instruction


def set_instruction_exec_ex(instruction: Instruction, instruction_str: str, instruction_executadas:
dict):
    set_instruction(stage="EX", instruction=instruction_str)
    instruction_executadas["EX"] = instruction


def set_instruction_exec_mem(instruction: Instruction, instruction_str: str, instruction_executadas:
dict):
    set_instruction(stage="MEM", instruction=instruction_str)
    instruction_executadas["MEM"] = instruction


def set_instruction_exec_wb(instruction: Instruction, instruction_str: str, instruction_executadas:
dict):
    set_instruction(stage="WB", instruction=instruction_str)
    instruction_executadas["WB"] = instruction


def execute_pipeline(cont: int, instructions: list[Instruction], instructions_str: list[str],
                     instruction_executadas: dict, command: bool):
    if command:
        if cont == 0:
            set_instruction_exec_if(instructions[0], instructions_str[0], instruction_executadas)
        if cont == 1:
            set_instruction_exec_if(instructions[1], instructions_str[1], instruction_executadas)
            set_instruction_exec_id(instructions[0], instructions_str[0], instruction_executadas)
        if cont == 2:
            set_instruction_exec_if(instructions[2], instructions_str[2], instruction_executadas)
            set_instruction_exec_id(instructions[1], instructions_str[1], instruction_executadas)
            set_instruction_exec_ex(instructions[0], instructions_str[0], instruction_executadas)
        if cont == 3:
            set_instruction_exec_if(instructions[3], instructions_str[3], instruction_executadas)
            set_instruction_exec_id(instructions[2], instructions_str[2], instruction_executadas)
            set_instruction_exec_ex(instructions[1], instructions_str[1], instruction_executadas)
            set_instruction_exec_mem(instructions[0], instructions_str[0], instruction_executadas)
        if cont >= 4:
            set_instruction_exec_if(instructions[4], instructions_str[4], instruction_executadas)
            set_instruction_exec_id(instructions[3], instructions_str[3], instruction_executadas)
            set_instruction_exec_ex(instructions[2], instructions_str[2], instruction_executadas)
            set_instruction_exec_mem(instructions[1], instructions_str[1], instruction_executadas)
            set_instruction_exec_wb(instructions[0], instructions_str[0], instruction_executadas)
            instructions.pop(0)
            instructions_str.pop(0)
