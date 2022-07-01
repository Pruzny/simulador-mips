from src.interface import *


class Align:
    UPPER_LEFT = 0
    UPPER_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3
    CENTER = 4


class Rectangle(pg.Rect):
    color: tuple
    border_radius: int

    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int], border_radius: int = 0) -> None:
        super().__init__(x, y, width, height)
        self.color = color
        self.border_radius = border_radius

    def draw(self):
        pg.draw.rect(Info.DISPLAY, self.color, self, border_radius=self.border_radius)


class Text:
    font: pg.font.Font
    pos: tuple[int, int]
    color: tuple[int, int, int]
    size: int
    width_correction: bool
    height_correction: bool

    def __init__(self, font: str, size: int, pos: tuple[int, int], color: tuple[int, int, int], alignment: int = Align.UPPER_LEFT) -> None:
        self.font = pg.font.SysFont(font, size)
        self.pos = pos
        self.color = color
        self.size = size

        self.width_correction = True if (alignment == Align.UPPER_RIGHT or alignment == Align.BOTTOM_RIGHT) else False
        self.height_correction = True if (alignment == Align.BOTTOM_LEFT or alignment == Align.BOTTOM_RIGHT) else False

    def render(self, msg) -> pg.Surface:
        return self.font.render(msg, False, self.color)


class TextBox:
    font: Text
    text: dict
    x: int
    y: int
    width: int
    height: int
    border: int
    unselected_color: tuple[int, int, int]
    selected_color: tuple[int, int, int]
    selected: bool
    image = pg.Surface
    first_line: int

    def __init__(self,
                 font: Text,
                 text: dict,
                 pos: tuple[int, int],
                 dimensions: tuple[int, int],
                 unselected_color: tuple[int, int, int],
                 selected_color: tuple[int, int, int],
                 border: int = 0,
                 border_color: tuple[int, int, int] = Colors.GRAY,
                 alignment: int = Align.UPPER_LEFT,
                 ) -> None:
        self.font = font
        self.text = text
        self.x, self.y = pos
        self.width, self.height = dimensions

        if alignment == Align.UPPER_RIGHT or alignment == Align.BOTTOM_RIGHT:
            self.x -= self.width
        if alignment == Align.BOTTOM_LEFT or alignment == Align.BOTTOM_RIGHT:
            self.y -= self.height
        if alignment == Align.CENTER:
            self.x -= self.width//2
            self.y -= self.height//2

        self.border = border
        self.border_color = border_color
        self.unselected_color = unselected_color
        self.selected_color = selected_color
        self.selected = False
        self.image = pg.Surface(dimensions)
        self.first_line = 0

    def check_click(self, key: int, pos: tuple[int, int]) -> None:
        if 1 <= key <= 3:
            x, y = pos
            if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
                self.selected = True
            else:
                self.selected = False

    def check_line(self, key: int):
        if self.selected:
            if (key == pg.K_DOWN or key == 5) and self.first_line < len(self.text) - 13 and len(self.text) > 13:
                self.first_line += 1
            elif (key == pg.K_UP or key == 4) and self.first_line > 0:
                self.first_line -= 1

    def draw(self) -> None:
        if self.selected:
            color = self.selected_color
        else:
            color = self.unselected_color

        pg.draw.rect(self.image, self.border_color, (0, 0, self.width, self.height), border_radius=20)
        pg.draw.rect(self.image, color, (self.border, self.border, self.width-self.border*2, self.height-self.border*2), border_radius=20)
        y = self.border * 2
        lines = list(f"{reg}: {format(int(value), f'08x')}" for reg, value in self.text.items())
        for line in lines[self.first_line:self.first_line + 13]:
            text = self.font.render(line)
            self.image.blit(text, ((self.width - text.get_width())//2 + self.border, y))
            y += text.get_height()
        Info.DISPLAY.blit(self.image, (self.x, self.y))
