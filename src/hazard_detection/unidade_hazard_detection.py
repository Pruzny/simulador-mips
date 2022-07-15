from src.Instruction import Instruction
from src.pipeline_execution import RegisterPipeline

BOLHA_INSTRUCTION_LIST = ['sll', '$zero', '$zero', '0']
LIST_INSTRUCTION_DESVIO = ["beq", "j", "bne", "jr", "jal"]
FORWARDING_TYPES = ['ForwardA', 'ForwardB', 'ForwardC', 'ForwardD']  # 10, 10, 01, 01


# nomes_registradores_pipeline = ["IF_ID", "ID_EX", "EX_MEM", "MEM_WB"] = REG[0] = IF_ID | REG[1] = ID_EX | REG[2] = EX_MEM | REG[3] = MEM_WB

def create_bolha():
    bolha = Instruction(BOLHA_INSTRUCTION_LIST[0], 0, False, BOLHA_INSTRUCTION_LIST, 0, "NOP")
    return bolha


def check_instruction_hazard_dados_forwarding(regs_pipeline: list[RegisterPipeline]):
    if regs_pipeline[2].EX_MEM and regs_pipeline[1].ID_EX and regs_pipeline[3].MEM_WB:
        if regs_pipeline[2].type == "r":
            if regs_pipeline[2].instruction.rd == regs_pipeline[1].instruction.rs:
                return FORWARDING_TYPES[0], regs_pipeline[2].instruction.result
            if regs_pipeline[2].instruction.rd == regs_pipeline[1].instruction.rt:
                return FORWARDING_TYPES[1], regs_pipeline[2].instruction.result
        if regs_pipeline[3].type == "r":
            if regs_pipeline[3].instruction.rd == regs_pipeline[1].instruction.rs:
                return FORWARDING_TYPES[2], regs_pipeline[3].instruction.result
            if regs_pipeline[3].instruction.rd == regs_pipeline[1].instruction.rt:
                return FORWARDING_TYPES[3], regs_pipeline[3].instruction.result


def check_hazards_dados_load(regs_pipeline: list[RegisterPipeline], instructions: list[Instruction]):
    print(regs_pipeline[0].instruction.str)
    print(regs_pipeline[1].instruction.str)

    if regs_pipeline[0].IF_ID and regs_pipeline[1].ID_EX:
        if regs_pipeline[0].instruction.name == "lw":
            if regs_pipeline[0].instruction.rt == regs_pipeline[1].instruction.rd or regs_pipeline[0].instruction.rs == \
                    regs_pipeline[1].instruction.rd:
                bolha = create_bolha()
                index = instructions.index(regs_pipeline[0].Instruction)
                instructions.insert(index, bolha)


def check_instruction_hazard(instructions: list[Instruction], regs_pipeline: list[RegisterPipeline]):
    """Recebe a lista de instrução que está sendo executada no pipeline"""
    check_hazards_dados_load(regs_pipeline, instructions)
