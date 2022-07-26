from src.Instruction import Instruction
from src.pipeline_execution import RegisterPipeline

BOLHA_INSTRUCTION_LIST = ['sll', '$zero', '$zero', '0']
LIST_INSTRUCTION_DESVIO = ["beq", "bne", ]
FORWARDING_TYPES_RS = ['ForwardA', 'ForwardC']  # A B REG 2 C D 3
FORWARDING_TYPES_RT = ['ForwardB', 'ForwardD']


def create_bolha():
    bolha = Instruction(BOLHA_INSTRUCTION_LIST[0], 0, False, BOLHA_INSTRUCTION_LIST, 0, "NOP")
    bolha.id()
    return bolha


def check_instruction_hazard_dados_forwarding(instructions: list[Instruction], regs_pipeline: list[RegisterPipeline]):
    offset = 1
    if regs_pipeline[0].IF_ID and regs_pipeline[0].instruction.name in LIST_INSTRUCTION_DESVIO:
        offset = 0

    if regs_pipeline[3].instruction and regs_pipeline[offset].instruction:
        try:
            index = instructions.index(regs_pipeline[offset].instruction)
            if regs_pipeline[3].instruction.type == "r" or \
                    regs_pipeline[3].instruction.type == "i" and regs_pipeline[3].instruction.result != "":
                if regs_pipeline[3].instruction.rd == regs_pipeline[offset].instruction.rs and regs_pipeline[3].instruction.rd != "$zero":
                    instructions[index].hazard_rs = FORWARDING_TYPES_RS[1]
                if regs_pipeline[3].instruction.rd == regs_pipeline[offset].instruction.rt and regs_pipeline[3].instruction.rd != "$zero":
                    instructions[index].hazard_rt = FORWARDING_TYPES_RT[1]
        except:
            pass

    if regs_pipeline[2].instruction and regs_pipeline[offset].instruction:
        try:
            index = instructions.index(regs_pipeline[offset].instruction)
            if regs_pipeline[2].instruction.type == "r" or \
                    regs_pipeline[2].instruction.type == "i" and regs_pipeline[2].instruction.result != "":
                if regs_pipeline[2].instruction.rd == regs_pipeline[offset].instruction.rs and regs_pipeline[2].instruction.rd != "$zero":
                    instructions[index].hazard_rs = FORWARDING_TYPES_RS[0]
                if regs_pipeline[2].instruction.rd == regs_pipeline[offset].instruction.rt and regs_pipeline[2].instruction.rd != "$zero":
                    instructions[index].hazard_rt = FORWARDING_TYPES_RT[0]
        except:
            pass


def check_hazards_dados_load(regs_pipeline: list[RegisterPipeline], instructions: list[Instruction]):
    if regs_pipeline[0].IF_ID and regs_pipeline[1].ID_EX:
        if regs_pipeline[1].instruction.name == "lw":
            if regs_pipeline[1].instruction.rt == regs_pipeline[0].instruction.rs or \
                    regs_pipeline[0].instruction.rt == regs_pipeline[1].instruction.rt:
                bolha = create_bolha()
                index = instructions.index(regs_pipeline[0].instruction)
                instructions.insert(index, bolha)


def check_hazard_controle_desvio(instructions: list[Instruction], regs_pipeline: list[RegisterPipeline]):
    CAMINHO_TOMADO = False
    if regs_pipeline[0].IF_ID and regs_pipeline[0].instruction is not None:
        if regs_pipeline[0].instruction.name in LIST_INSTRUCTION_DESVIO:
            CAMINHO_TOMADO = regs_pipeline[0].instruction.result
            if CAMINHO_TOMADO:
                bolha = create_bolha()
                index = instructions.index(regs_pipeline[0].instruction)
                instructions.insert(index + 1, bolha)
                return CAMINHO_TOMADO, index + 2, regs_pipeline[0].instruction.str
    return CAMINHO_TOMADO, 0, ""


def check_instruction_hazard(instructions: list[Instruction], regs_pipeline: list[RegisterPipeline]):
    """Recebe a lista de instrução que está sendo executada no pipeline"""
    check_hazards_dados_load(regs_pipeline, instructions)
