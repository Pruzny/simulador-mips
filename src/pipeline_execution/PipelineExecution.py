from src.Instruction import Instruction
from src.hazard_detection.main import check_instruction_hazard
from src.interface import Info
from src.pipeline_execution import RegisterPipeline


def set_instruction(stage: str, instruction: str):
    Info.STAGES[stage] = instruction


def set_instruction_exec_if(instruction: Instruction, instruction_str: str, instruction_executadas: dict):
    set_instruction(stage="IF", instruction=instruction_str)
    instruction_executadas["IF"] = instruction
    instruction.stage = "IF"


def set_instruction_exec_id(instruction: Instruction, instruction_str: str, instruction_executadas: dict):
    set_instruction(stage="ID", instruction=instruction_str)
    instruction_executadas["ID"] = instruction
    instruction.stage = "ID"


def set_instruction_exec_ex(instruction: Instruction, instruction_str: str, instruction_executadas: dict):
    set_instruction(stage="EX", instruction=instruction_str)
    instruction_executadas["EX"] = instruction
    instruction.stage = "EX"


def set_instruction_exec_mem(instruction: Instruction, instruction_str: str, instruction_executadas: dict):
    set_instruction(stage="MEM", instruction=instruction_str)
    instruction_executadas["MEM"] = instruction
    instruction.stage = "MEM"


def set_instruction_exec_wb(instruction: Instruction, instruction_str: str, instruction_executadas: dict):
    set_instruction(stage="WB", instruction=instruction_str)
    instruction_executadas["WB"] = instruction
    instruction.stage = "WB"


def execute_pipeline(cont: int, instructions: list[Instruction], instruction_executadas: dict,
                     command: bool, labels: dict, registradores_pipeline: list[RegisterPipeline]):
    if command:
        instructions_in_execution = list()
        for i in range(cont):
            instructions_in_execution.append(instructions[i])

        check_instruction_hazard(instructions_in_execution, labels, cont)
        if cont == 0:
            set_instruction_exec_if(instructions_in_execution[0], instructions_in_execution[0].str,
                                    instruction_executadas)
        if cont == 1:
            set_instruction_exec_if(instructions_in_execution[1], instructions_in_execution[1].str,
                                    instruction_executadas)
            registradores_pipeline[0].instruction = instructions_in_execution[0]
            set_instruction_exec_id(instructions_in_execution[0], instructions_in_execution[0].str,
                                    instruction_executadas)
        if cont == 2:
            set_instruction_exec_if(instructions_in_execution[2], instructions_in_execution[2].str,
                                    instruction_executadas)
            registradores_pipeline[0].instruction = instructions_in_execution[1]
            set_instruction_exec_id(instructions_in_execution[1], instructions_in_execution[1].str,
                                    instruction_executadas)
            registradores_pipeline[1].instruction = instructions_in_execution[0]
            set_instruction_exec_ex(instructions_in_execution[0], instructions_in_execution[0].str,
                                    instruction_executadas)
        if cont == 3:
            set_instruction_exec_if(instructions_in_execution[3], instructions_in_execution[3].str,
                                    instruction_executadas)
            registradores_pipeline[0].instruction = instructions_in_execution[2]
            set_instruction_exec_id(instructions_in_execution[2], instructions_in_execution[2].str,
                                    instruction_executadas)
            registradores_pipeline[1].instruction = instructions_in_execution[1]
            set_instruction_exec_ex(instructions_in_execution[1], instructions_in_execution[1].str,
                                    instruction_executadas)
            registradores_pipeline[2].instruction = instructions_in_execution[0]
            set_instruction_exec_mem(instructions_in_execution[0], instructions_in_execution[0].str,
                                     instruction_executadas)
        if cont >= 4:
            set_instruction_exec_if(instructions_in_execution[4], instructions_in_execution[4].str,
                                    instruction_executadas)
            registradores_pipeline[0].instruction = instructions_in_execution[3]
            set_instruction_exec_id(instructions_in_execution[3], instructions_in_execution[3].str,
                                    instruction_executadas)
            registradores_pipeline[1].instruction = instructions_in_execution[2]
            set_instruction_exec_ex(instructions_in_execution[2], instructions_in_execution[2].str,
                                    instruction_executadas)
            registradores_pipeline[2].instruction = instructions_in_execution[1]
            set_instruction_exec_mem(instructions_in_execution[1], instructions_in_execution[1].str,
                                     instruction_executadas)
            registradores_pipeline[3].instruction = instructions_in_execution[0]
            set_instruction_exec_wb(instructions_in_execution[0], instructions_in_execution[0].str,
                                    instruction_executadas)
        instructions.pop(0)
        '''if cont == 0:
            set_instruction_exec_if(instructions[0], instructions[0].str, instruction_executadas)
        if cont == 1:
            set_instruction_exec_if(instructions[1], instructions[1].str, instruction_executadas)
            set_instruction_exec_id(instructions[0], instructions[0].str, instruction_executadas)
        if cont == 2:
            set_instruction_exec_if(instructions[2], instructions[2].str, instruction_executadas)
            set_instruction_exec_id(instructions[1], instructions[1].str, instruction_executadas)
            set_instruction_exec_ex(instructions[0], instructions[0].str, instruction_executadas)
        if cont == 3:
            set_instruction_exec_if(instructions[3], instructions[3].str, instruction_executadas)
            set_instruction_exec_id(instructions[2], instructions[2].str, instruction_executadas)
            set_instruction_exec_ex(instructions[1], instructions[1].str, instruction_executadas)
            set_instruction_exec_mem(instructions[0], instructions[0].str, instruction_executadas)
        if cont >= 4:
            set_instruction_exec_if(instructions[4], instructions[4].str, instruction_executadas)
            set_instruction_exec_id(instructions[3], instructions[3].str, instruction_executadas)
            set_instruction_exec_ex(instructions[2], instructions[2].str, instruction_executadas)
            set_instruction_exec_mem(instructions[1], instructions[1].str, instruction_executadas)
            set_instruction_exec_wb(instructions[0], instructions[0].str, instruction_executadas)
            instructions.pop(0)'''
