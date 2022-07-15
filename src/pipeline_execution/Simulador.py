from src.file import read_asm
from src.interface import Info
from src.pipeline_execution.PipelineExecution import execute_pipeline
from src.pipeline_execution.RegisterPipeline import RegisterPipeline
from src.utils import create_labels, transforming_instruction

QUANTIDADES_REGISTRADORES_PIPELINE = 4
nomes_registradores_pipeline = ["IF_ID", "ID_EX", "EX_MEM", "MEM_WB"]


class Simulador:
    list_asm, data = read_asm()
    labels = create_labels(list_asm)
    instructions = transforming_instruction(list_asm, labels)
    list_registers_pipeline = list(
        RegisterPipeline(nomes_registradores_pipeline[i]) for i in range(QUANTIDADES_REGISTRADORES_PIPELINE))
    instructions_executadas = dict()

    @staticmethod
    def execute():
        execute_pipeline(
            Info.pipeline_stage,
            Simulador.instructions,
            Simulador.instructions_executadas,
            True,
            Simulador.labels,
            Simulador.list_registers_pipeline
        )
