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


def set_instruction_vazia(stage: str):
    set_instruction(stage, "")


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

        if cont >= 5:
            qtd_instruction = 5
        else:
            qtd_instruction = cont + 1

        i = 0
        while i < len(instructions) and i < qtd_instruction:
            instructions_in_execution.append(instructions[i])
            i += 1

        if len(instructions) > 4:
            if cont == 0:
                set_instruction_exec_if(instructions_in_execution[0], instructions_in_execution[0].str,
                                        instruction_executadas)
            if cont == 1:
                registradores_pipeline[0].instruction = instructions_in_execution[0]
                set_instruction_exec_if(instructions_in_execution[1], instructions_in_execution[1].str,
                                        instruction_executadas)
                set_instruction_exec_id(instructions_in_execution[0], instructions_in_execution[0].str,
                                        instruction_executadas)
            if cont == 2:
                registradores_pipeline[0].instruction = instructions_in_execution[1]
                registradores_pipeline[1].instruction = instructions_in_execution[0]

                check_instruction_hazard(instructions_in_execution, registradores_pipeline)

                set_instruction_exec_if(instructions_in_execution[2], instructions_in_execution[2].str,
                                        instruction_executadas)
                set_instruction_exec_id(instructions_in_execution[1], instructions_in_execution[1].str,
                                        instruction_executadas)
                set_instruction_exec_ex(instructions_in_execution[0], instructions_in_execution[0].str,
                                        instruction_executadas)
            if cont == 3:
                registradores_pipeline[0].instruction = instructions_in_execution[2]
                registradores_pipeline[1].instruction = instructions_in_execution[1]
                registradores_pipeline[2].instruction = instructions_in_execution[0]

                check_instruction_hazard(instructions_in_execution, registradores_pipeline)

                set_instruction_exec_if(instructions_in_execution[3], instructions_in_execution[3].str,
                                        instruction_executadas)
                set_instruction_exec_id(instructions_in_execution[2], instructions_in_execution[2].str,
                                        instruction_executadas)
                set_instruction_exec_ex(instructions_in_execution[1], instructions_in_execution[1].str,
                                        instruction_executadas)
                set_instruction_exec_mem(instructions_in_execution[0], instructions_in_execution[0].str,
                                         instruction_executadas)
            if cont >= 4:
                registradores_pipeline[0].instruction = instructions_in_execution[3]
                registradores_pipeline[1].instruction = instructions_in_execution[2]
                registradores_pipeline[2].instruction = instructions_in_execution[1]
                registradores_pipeline[3].instruction = instructions_in_execution[0]

                check_instruction_hazard(instructions_in_execution, registradores_pipeline)

                set_instruction_exec_if(instructions_in_execution[4], instructions_in_execution[4].str,
                                        instruction_executadas)
                set_instruction_exec_id(instructions_in_execution[3], instructions_in_execution[3].str,
                                        instruction_executadas)
                set_instruction_exec_ex(instructions_in_execution[2], instructions_in_execution[2].str,
                                        instruction_executadas)
                set_instruction_exec_mem(instructions_in_execution[1], instructions_in_execution[1].str,
                                         instruction_executadas)
                set_instruction_exec_wb(instructions_in_execution[0], instructions_in_execution[0].str,
                                        instruction_executadas)
                instructions.pop(0)
        else:
            match (len(instructions)):
                case 4:
                    set_instruction_vazia("IF")
                    instructions.pop(0)
                case 3:
                    set_instruction_vazia("ID")
                    instructions.pop(0)
                case 2:
                    set_instruction_vazia("EX")
                    instructions.pop(0)
                case 1:
                    set_instruction_vazia("MEM")
                    instructions.pop(0)
                case 0:
                    set_instruction_vazia("WB")
