from src.Instruction import *
from src.pipeline_execution.RegisterPipeline import RegisterPipeline
from src.utils import *

lista = read_asm()
labels = create_labels(lista)

QUANTIDADES_REGISTRADORES_PIPELINE = 4
nomes_registradores_pipeline = ["IF_ID", "ID_EX", "EX_MEM", "MEM_WB"]

instructions = transforming_instruction(lista, labels, True)
lista_registradores_pipeline = list()
[print(x.__str__(), end="\n\n") for x in instructions]

for i in range(QUANTIDADES_REGISTRADORES_PIPELINE):
    lista_registradores_pipeline.append(RegisterPipeline(nomes_registradores_pipeline[i]))


