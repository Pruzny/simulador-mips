from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame as pg


class Info:
    DISPLAY: pg.Surface
    REGS = dict()
    DATA = dict()
    STAGES = dict()
    pipeline_stage = -1

    @staticmethod
    def set_values(display: pg.Surface):
        Info.DISPLAY = display
        for line in open("base/registers.txt", "r").readlines():
            Info.REGS[line[:-1]] = "00000000"
        for line in open("base/stages.txt", "r").readlines():
            Info.STAGES[line[:-1]] = ""

    @staticmethod
    def sum_stage():
        Info.pipeline_stage += 1


class Colors:
    WHITE = (255, 255, 255)
    GRAY = (100, 100, 100)
    SMOOTH_GRAY = (158, 158, 158)
    LIGHT_GRAY = (192, 192, 192)
    DARK_GRAY = (51, 51, 51)
    BLACK = (0, 0, 0)
