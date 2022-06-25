from src.Instruction import Instruction, InstructionSteps, Steps
from src.pipeline_execution import RegisterPipeline

BOLHA_INSTRUCTION_LIST = ['sll', '$zero', '$zero', '0']
LIST_INSTRUCTION_DESVIO = ["beq", "j", "bne", "jr", "jal"]


def create_bolha(pos: int, label: dict) -> InstructionSteps:
    primitive_bolha = Instruction(BOLHA_INSTRUCTION_LIST[0], BOLHA_INSTRUCTION_LIST, has_label_start=False, has_label_final=False, pos=pos, labels=label)
    bolha = InstructionSteps(primitive_bolha)
    return bolha


def check_instruction_hazard_dados(list_instructions: list[InstructionSteps], labels: dict) -> list:
    """Recebe a lista de instrução que está sendo executada no pipeline"""
    listinhas = list()

    for i in range(1, len(list_instructions)):
        instruction1 = list_instructions[i]
        instruction2 = list_instructions[i - 1]
        if instruction1.instruction_base.name == "lw" and instruction1.instruction_base.rd == instruction2.instruction_base.rt or instruction1.instruction_base.rd == instruction2.instruction_base.rs:
            listinhas.append(instruction1)
            listinhas.append(create_bolha(i, labels))
            listinhas.append(instruction2)

    return listinhas


def check_instruction_hazard_desvio(StepPipe: Steps, pos: int, label):
    if StepPipe is None:
        return None
    if LIST_INSTRUCTION_DESVIO.count(StepPipe.IF.name) >= 1:
        return create_bolha(pos, label=label)
    return None


def check_registerPipeline_hazard_dados(lista_registradores_pipeline: list[RegisterPipeline], pos: int, label: dict):
    # nomes_registradores_pipeline = ["IF_ID", "ID_EX", "EX_MEM", "MEM_WB"]
    register_id_ex = lista_registradores_pipeline[1]
    register_if_id = lista_registradores_pipeline[0]

    if register_id_ex.instruction.name == "lw" and (register_id_ex.instruction.rd == register_if_id.instruction.rt or register_id_ex.instruction.rd == register_if_id.instruction.rs):
        return create_bolha(pos, label=label)
    return None
