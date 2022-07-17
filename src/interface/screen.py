from src.file import read_asm
from src.interface.assets import *
from src.pipeline_execution.RegisterPipeline import RegisterPipeline
from src.pipeline_execution.Simulador import Simulador
from src.utils import create_labels, transforming_instruction

pg.font.init()

WIDTH = 1280
HEIGHT = 720
TITLE = "Simulador MIPS"
FPS = 60

DEFAULT_FONT = "Source Code Pro"

EVENTS = {
    "show": True,
}

FONTS = {
    "text": Text(DEFAULT_FONT, 19, (WIDTH, 0), Colors.BLACK),
    "title": Text(DEFAULT_FONT, 50, (WIDTH, 0), Colors.BLACK, bold=True),
    "instruction": Text(DEFAULT_FONT, 40, (WIDTH, 0), Colors.BLACK),
}

ASSETS = {
    "databox": TextBox(FONTS["text"], Info.DATA, (WIDTH - 20, 20), (200, 320), Colors.LIGHT_GRAY, Colors.WHITE,
                       border=5, alignment=Align.UPPER_RIGHT),
    "rbox": TextBox(FONTS["text"], Info.REGS, (WIDTH - 20, HEIGHT // 2 + 20), (200, 320), Colors.LIGHT_GRAY,
                    Colors.WHITE, border=5, alignment=Align.UPPER_RIGHT),
    "ibox": InstructionBox(FONTS["instruction"], FONTS["title"], Info.STAGES, (20, 20), (800, 680), Colors.LIGHT_GRAY,
                           Colors.WHITE, Colors.SMOOTH_GRAY, border=5),
}


def start_values() -> None:
    Info.set_values(start_display())
    Simulador.list_asm, Simulador.data = read_asm()
    Simulador.labels = create_labels(Simulador.list_asm)
    Simulador.instructions = transforming_instruction(Simulador.list_asm, Simulador.labels)
    Simulador.instructions_queue = Simulador.instructions[:]
    Simulador.list_registers_pipeline = list(
        RegisterPipeline(Simulador.nomes_registradores_pipeline[i]) for i in
        range(Simulador.QUANTIDADES_REGISTRADORES_PIPELINE))
    for i in range(250):
        Info.DATA[dec_to_hex(i)] = dec_to_hex(0, 8)
    for label, index in Simulador.labels.items():
        Simulador.blocks[label] = Simulador.instructions[index:]


def show_screen() -> None:
    clock = pg.time.Clock()
    pg.display.set_caption(TITLE)

    while EVENTS["show"]:
        clock.tick(FPS)
        check_event()
        draw()

        pg.display.update()


def start_display() -> pg.Surface:
    pg.init()
    display = pg.display.set_mode((WIDTH, HEIGHT))
    return display


def check_event() -> None:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            EVENTS["show"] = False
        if event.type == pg.MOUSEBUTTONDOWN:
            for asset in ASSETS.values():
                if isinstance(asset, Box):
                    asset.check_click(event.button, pg.mouse.get_pos())
                if isinstance(asset, TextBox):
                    asset.check_key(event.button)
        if event.type == pg.KEYDOWN:
            for asset in ASSETS.values():
                if type(asset) == TextBox or type(asset) == InstructionBox:
                    asset.check_key(event.key)


def draw() -> None:
    for asset in ASSETS.values():
        asset.draw()
