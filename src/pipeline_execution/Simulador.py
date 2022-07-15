class Simulador:
    QUANTIDADES_REGISTRADORES_PIPELINE = 4
    nomes_registradores_pipeline = ["IF_ID", "ID_EX", "EX_MEM", "MEM_WB"]
    list_asm = list()
    data = list()
    labels = dict()
    blocks = dict()
    instructions = list()
    instructions_queue = list()
    list_registers_pipeline = list()
    instructions_executadas = dict()
