from src.Instruction import Instruction

BOLHA_INSTRUCTION_LIST = ['sll', '$zero', '$zero', '0']
LIST_INSTRUCTION_DESVIO = ["beq", "j", "bne", "jr", "jal"]


def create_bolha(pos: int, label: dict):
    bolha = Instruction(BOLHA_INSTRUCTION_LIST[0], 0, False, BOLHA_INSTRUCTION_LIST, pos, label)
    return bolha


def check_instruction_hazard_dados(instructions: list[Instruction]):
    pass


def check_instruction_hazard(instructions: list[Instruction], labels: dict, cont: int) -> list:
    """Recebe a lista de instrução que está sendo executada no pipeline"""
    [print(e.str) for e in instructions]
    return instructions


'''def check_instruction_hazard_desvio(StepPipe: Steps, pos: int, label):
    if StepPipe is None:
        return None
    if LIST_INSTRUCTION_DESVIO.count(StepPipe.IF.name) >= 1:
        return create_bolha(pos, label=label)
    return None'''

'''def check_registerPipeline_hazard_dados(lista_registradores_pipeline: list[RegisterPipeline], pos: int, label: dict):
    # nomes_registradores_pipeline = ["IF_ID", "ID_EX", "EX_MEM", "MEM_WB"]
    register_id_ex = lista_registradores_pipeline[1]
    register_if_id = lista_registradores_pipeline[0]

    if register_id_ex.instruction.name == "lw" and (register_id_ex.instruction.rd == register_if_id.instruction.rt or register_id_ex.instruction.rd == register_if_id.instruction.rs):
        return create_bolha(pos, label=label)
    return None
'''
