from src.file import read_asm
from src.interface.screen import main, start_values
from src.pipeline_execution.PipelineExecution import execute_pipeline
from src.pipeline_execution.RegisterPipeline import RegisterPipeline
from src.utils import create_labels, transforming_instruction

lista, data = read_asm()
labels = create_labels(lista)

print(data)
start_values()

QUANTIDADES_REGISTRADORES_PIPELINE = 4
nomes_registradores_pipeline = ["IF_ID", "ID_EX", "EX_MEM", "MEM_WB"]

instructions_objects = transforming_instruction(lista, labels)
lista_registradores_pipeline = list()

for i in range(QUANTIDADES_REGISTRADORES_PIPELINE):
    lista_registradores_pipeline.append(RegisterPipeline(nomes_registradores_pipeline[i]))

instructions_executadas = dict()
# execute_pipeline(cont: int, instructions: list[Instruction], instructions_str: list[str], instruction_executadas: dict, command: bool):
execute_pipeline(5, instructions_objects,
                 instructions_executadas, True, labels, lista_registradores_pipeline)
execute_pipeline(6, instructions_objects,
                 instructions_executadas, True, labels, lista_registradores_pipeline)
[print(x.__str__()) for x in lista_registradores_pipeline]
main()
