from src.interface.assets import *


def draw_text(font: Text, msg: str):
    render = font.font.render(msg, True, font.color)
    x_dif = render.get_width() if font.width_correction else 0
    y_dif = render.get_height() if font.height_correction else 0
    x, y = (font.pos[0] - x_dif, font.pos[1] - y_dif)
    Info.DISPLAY.blit(render, (x, y))
