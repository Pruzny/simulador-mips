from src.hazard_detection.unidade_hazard_detection import check_instruction_hazard, create_bolha
from src.interface import Info
from src.pipeline_execution import RegisterPipeline
from src.pipeline_execution.Simulador import Simulador

LIST_JUMP = ["j"]


def check_instruction_jump(instructions, regs_pipeline):
    edit_list = False
    if regs_pipeline[1].ID_EX:
        if regs_pipeline[1].instruction.name in LIST_JUMP:
            bolha = create_bolha()
            index = instructions.index(regs_pipeline[0].instruction)
            instructions.insert(index, bolha)
            instructions.insert(index+1, bolha)
            edit_list = True
    return edit_list


def set_instruction(stage: str, instruction: str):
    Info.STAGES[stage] = instruction


def set_instruction_exec_if(instruction, instruction_str: str, instruction_executadas: dict):
    set_instruction(stage="IF", instruction=instruction_str)
    instruction_executadas["IF"] = instruction
    instruction.stage = "IF"


def set_instruction_vazia(stage: str):
    set_instruction(stage, "")


def set_instruction_exec_id(instruction, instruction_str: str, instruction_executadas: dict):
    set_instruction(stage="ID", instruction=instruction_str)
    instruction_executadas["ID"] = instruction
    instruction.stage = "ID"


def set_instruction_exec_ex(instruction, instruction_str: str, instruction_executadas: dict):
    set_instruction(stage="EX", instruction=instruction_str)
    instruction_executadas["EX"] = instruction
    instruction.stage = "EX"


def set_instruction_exec_mem(instruction, instruction_str: str, instruction_executadas: dict):
    set_instruction(stage="MEM", instruction=instruction_str)
    instruction_executadas["MEM"] = instruction
    instruction.stage = "MEM"


def set_instruction_exec_wb(instruction, instruction_str: str, instruction_executadas: dict):
    set_instruction(stage="WB", instruction=instruction_str)
    instruction_executadas["WB"] = instruction
    instruction.stage = "WB"


def execute_pipeline(cont: int, instructions: list, instruction_executadas: dict,
                     command: bool, registradores_pipeline: list[RegisterPipeline]):
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

        #[print(x.str) for x in instructions_in_execution]
        if cont == 0:
            try:
                set_instruction_exec_if(instructions_in_execution[0], instructions_in_execution[0].str,
                                        instruction_executadas)
            except:
                set_instruction_vazia("IF")
        if cont == 1:
            try:
                registradores_pipeline[0].instruction = instructions_in_execution[0]
                set_instruction_exec_id(instructions_in_execution[0], instructions_in_execution[0].str,
                                        instruction_executadas)
            except:
                set_instruction_vazia("IF")
            try:
                set_instruction_exec_if(instructions_in_execution[1], instructions_in_execution[1].str,
                                        instruction_executadas)
            except:
                set_instruction_vazia("ID")

        if cont == 2:
            entry_in_exception = False
            try:
                registradores_pipeline[0].instruction = instructions_in_execution[1]
            except:
                set_instruction_vazia("ID")
                entry_in_exception = True
            try:
                registradores_pipeline[1].instruction = instructions_in_execution[0]
            except:
                set_instruction_vazia("EX")
                entry_in_exception = True
            try:
                set_instruction_exec_if(instructions_in_execution[2], instructions_in_execution[2].str,
                                        instruction_executadas)
            except:
                set_instruction_vazia("IF")
            if not entry_in_exception:
                check_instruction_jump(instructions, registradores_pipeline)
                check_instruction_hazard(instructions, registradores_pipeline)
                set_instruction_exec_id(instructions_in_execution[1], instructions_in_execution[1].str,
                                        instruction_executadas)
                set_instruction_exec_ex(instructions_in_execution[0], instructions_in_execution[0].str,
                                        instruction_executadas)

        if cont == 3:
            entry_in_exception = False
            try:
                registradores_pipeline[0].instruction = instructions_in_execution[2]
            except:
                set_instruction_vazia("ID")
                entry_in_exception = True
            try:
                registradores_pipeline[1].instruction = instructions_in_execution[1]
            except:
                set_instruction_vazia("EX")
                entry_in_exception = True
            try:
                registradores_pipeline[2].instruction = instructions_in_execution[0]
            except:
                set_instruction_vazia("MEM")
            try:
                set_instruction_exec_if(instructions_in_execution[3], instructions_in_execution[3].str,
                                        instruction_executadas)
            except:
                set_instruction_vazia("IF")
            if not entry_in_exception:
                check_instruction_jump(instructions, registradores_pipeline)
                check_instruction_hazard(instructions, registradores_pipeline)
                set_instruction_exec_id(instructions_in_execution[2], instructions_in_execution[2].str,
                                        instruction_executadas)
                set_instruction_exec_ex(instructions_in_execution[1], instructions_in_execution[1].str,
                                        instruction_executadas)
                set_instruction_exec_mem(instructions_in_execution[0], instructions_in_execution[0].str,
                                         instruction_executadas)
        if cont >= 4:
            # nomes_registradores_pipeline = ["IF_ID", "ID_EX", "EX_MEM", "MEM_WB"] = REG[0] = IF_ID | REG[1] = ID_EX | REG[2] = EX_MEM | REG[3] = MEM_WB
            entry_in_exception_check = False
            reg_IF_ID = True
            reg_ID_EX = True
            reg_EX_MEM = True
            reg_MEM_WB = True

            try:
                registradores_pipeline[0].instruction = instructions_in_execution[3]
            except:
                reg_IF_ID = False
            try:
                registradores_pipeline[1].instruction = instructions_in_execution[2]
            except:
                reg_ID_EX = False
            try:
                registradores_pipeline[2].instruction = instructions_in_execution[1]
            except:
                reg_EX_MEM = False
            try:
                registradores_pipeline[3].instruction = instructions_in_execution[0]
            except:
                reg_MEM_WB = False


            try:
                check_instruction_hazard(instructions, registradores_pipeline)
            except:
                entry_in_exception_check = True

            if not entry_in_exception_check:
                try:
                    set_instruction_exec_if(instructions_in_execution[4], instructions_in_execution[4].str,
                                            instruction_executadas)
                except:
                    set_instruction_vazia("IF")
                if reg_IF_ID:
                    set_instruction_exec_id(instructions_in_execution[3], instructions_in_execution[3].str,
                                            instruction_executadas)
                else:
                    set_instruction_vazia("ID")
                if reg_ID_EX:
                    check_instruction_jump(instructions, registradores_pipeline)
                    set_instruction_exec_ex(instructions_in_execution[2], instructions_in_execution[2].str,
                                            instruction_executadas)
                else:
                    set_instruction_vazia("EX")
                if reg_EX_MEM:
                    set_instruction_exec_mem(instructions_in_execution[1], instructions_in_execution[1].str,
                                             instruction_executadas)
                else:
                    set_instruction_vazia("MEM")
                if reg_MEM_WB:
                    set_instruction_exec_wb(instructions_in_execution[0], instructions_in_execution[0].str,
                                            instruction_executadas)
                else:
                    set_instruction_vazia("WB")

            if len(instructions) > 0:
                instructions.pop(0)


def execute():
    execute_pipeline(
        Info.pipeline_stage,
        Simulador.instructions_queue,
        Simulador.instructions_executadas,
        True,
        Simulador.list_registers_pipeline
    )
