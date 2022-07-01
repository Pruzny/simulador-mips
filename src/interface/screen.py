from src.interface.utils import *

pg.font.init()

WIDTH = 1280
HEIGHT = 720
TITLE = "Simulador MIPS"
FPS = 60

EVENTS = {
    "show": True,
}

FONTS = {
    "text": Text("DejaVu Sans Mono, Noto Mono, Source Code Pro", 19, (WIDTH, 0), Colors.DARK_GRAY, alignment=Align.UPPER_RIGHT),
}

ASSETS = {
    "databox": TextBox(FONTS["text"], Info.DATA, (WIDTH - 20, 20), (200, 320), Colors.LIGHT_GRAY, Colors.WHITE, border=5, alignment=Align.UPPER_RIGHT),
    "rbox": TextBox(FONTS["text"], Info.REGS, (WIDTH - 20, HEIGHT//2 + 20), (200, 320), Colors.LIGHT_GRAY, Colors.WHITE, border=5, alignment=Align.UPPER_RIGHT),
}


def main() -> None:
    DISPLAY = start_display()
    Info.set_values(DISPLAY)

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
                if type(asset) == TextBox:
                    asset.check_click(event.button, pg.mouse.get_pos())
                    asset.check_line(event.button)
        if event.type == pg.KEYDOWN:
            for asset in ASSETS.values():
                if type(asset) == TextBox:
                    asset.check_line(event.key)


def draw() -> None:
    for asset in ASSETS.values():
        asset.draw()


