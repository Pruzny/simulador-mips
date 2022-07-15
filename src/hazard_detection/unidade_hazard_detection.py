from src.Instruction import Instruction
from src.pipeline_execution import RegisterPipeline

BOLHA_INSTRUCTION_LIST = ['sll', '$zero', '$zero', '0']
LIST_INSTRUCTION_DESVIO = ["beq", "bne", ]
FORWARDING_TYPES_RS = ['ForwardA', 'ForwardC']  # A B REG 2 C D 3
FORWARDING_TYPES_RT = ['ForwardB', 'ForwardD']


# regs_pipeline[2].instruction.result #regs_pipeline[3].instruction.result


# nomes_registradores_pipeline = ["IF_ID", "ID_EX", "EX_MEM", "MEM_WB"] = REG[0] = IF_ID | REG[1] = ID_EX | REG[2] = EX_MEM | REG[3] = MEM_WB

def create_bolha():
    bolha = Instruction(BOLHA_INSTRUCTION_LIST[0], 0, False, BOLHA_INSTRUCTION_LIST, 0, "NOP")
    return bolha


def check_instruction_hazard_dados_forwarding(instructions: list[Instruction], regs_pipeline: list[RegisterPipeline]):
    if regs_pipeline[3].instruction and regs_pipeline[1].instruction:
        try:
            index = instructions.index(regs_pipeline[1].instruction)
            if regs_pipeline[3].instruction.type == "r" or regs_pipeline[3].instruction.type == "i" and regs_pipeline[3].instruction.result != "":
                if regs_pipeline[3].instruction.rd == regs_pipeline[1].instruction.rs:
                    instructions[index].hazard_rs = FORWARDING_TYPES_RS[1]
                if regs_pipeline[3].instruction.rd == regs_pipeline[1].instruction.rt:
                    instructions[index].hazard_rt = FORWARDING_TYPES_RT[1]
        except:
            pass

    if regs_pipeline[2].instruction and regs_pipeline[1].instruction:
        try:
            index = instructions.index(regs_pipeline[1].instruction)
            if regs_pipeline[2].instruction.type == "r" or regs_pipeline[2].instruction.type == "i":
                if regs_pipeline[2].instruction.rd == regs_pipeline[1].instruction.rs:
                    instructions[index].hazard_rs = FORWARDING_TYPES_RS[0]
                if regs_pipeline[2].instruction.rd == regs_pipeline[1].instruction.rt:
                    instructions[index].hazard_rt = FORWARDING_TYPES_RT[0]
        except:
            pass


def check_hazards_dados_load(regs_pipeline: list[RegisterPipeline], instructions: list[Instruction]):
    if regs_pipeline[0].IF_ID and regs_pipeline[1].ID_EX:
        if regs_pipeline[1].instruction.name == "lw":
            if regs_pipeline[1].instruction.rt == regs_pipeline[0].instruction.rs or regs_pipeline[0].instruction.rt == regs_pipeline[1].instruction.rt:
                bolha = create_bolha()
                index = instructions.index(regs_pipeline[0].instruction)
                instructions.insert(index, bolha)


def check_hazard_controle_desvio(instructions: list[Instruction], regs_pipeline: list[RegisterPipeline]):
    CAMINHO_TOMADO = False
    if regs_pipeline[0].IF_ID:
        if regs_pipeline[0].instruction.name in LIST_INSTRUCTION_DESVIO:
            if CAMINHO_TOMADO:
                bolha = create_bolha()
                index = instructions.index(regs_pipeline[0].instruction)
                instructions.insert(index, bolha)


def check_instruction_hazard(instructions: list[Instruction], regs_pipeline: list[RegisterPipeline]):
    """Recebe a lista de instrução que está sendo executada no pipeline"""
    check_hazards_dados_load(regs_pipeline, instructions)
