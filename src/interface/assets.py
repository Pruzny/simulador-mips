from src.interface import *
from src.pipeline_execution.PipelineExecution import execute


class Align:
    UPPER_LEFT = 0
    UPPER_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3
    CENTER = 4


class Text:
    font: pg.font.Font
    pos: tuple[int, int]
    color: tuple[int, int, int]
    size: int

    def __init__(self, font: str, size: int, pos: tuple[int, int], color: tuple[int, int, int],
                 bold: bool = False) -> None:
        self.font = pg.font.SysFont(font, size, bold=bold)
        self.pos = pos
        self.color = color
        self.size = size

    def render(self, msg) -> pg.Surface:
        return self.font.render(msg, True, self.color)


class Box:
    font: Text
    text: dict
    x: int
    y: int
    width: int
    height: int
    border: int
    border_color: tuple[int, int, int]
    border_radius: int
    unselected_color: tuple[int, int, int]
    selected_color: tuple[int, int, int]
    selected: bool
    image = pg.Surface

    def __init__(self,
                 font: Text,
                 text: dict,
                 pos: tuple[int, int],
                 dimensions: tuple[int, int],
                 unselected_color: tuple[int, int, int],
                 selected_color: tuple[int, int, int],
                 border: int = 0,
                 border_color: tuple[int, int, int] = Colors.GRAY,
                 border_radius: int = 20,
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
            self.x -= self.width // 2
            self.y -= self.height // 2

        self.border = border
        self.border_color = border_color
        self.border_radius = border_radius
        self.unselected_color = unselected_color
        self.selected_color = selected_color
        self.selected = False
        self.image = pg.Surface(dimensions)

    def check_click(self, key: int, pos: tuple[int, int]) -> None:
        if 1 <= key <= 3:
            x, y = pos
            if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
                self.selected = True
            else:
                self.selected = False

    def draw_box(self) -> None:
        if self.selected:
            color = self.selected_color
        else:
            color = self.unselected_color

        pg.draw.rect(self.image, self.border_color, (0, 0, self.width, self.height), border_radius=self.border_radius)
        pg.draw.rect(self.image, color,
                     (self.border, self.border, self.width - self.border * 2, self.height - self.border * 2),
                     border_radius=self.border_radius)

    def draw(self) -> None:
        self.draw_box()
        Info.DISPLAY.blit(self.image, (self.x, self.y))


class TextBox(Box):
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
                 border_radius: int = 20,
                 alignment: int = Align.UPPER_LEFT,
                 ) -> None:
        super().__init__(font, text, pos, dimensions, unselected_color, selected_color, border, border_color,
                         border_radius, alignment)
        self.first_line = 0

    def check_key(self, key: int):
        if self.selected:
            if (key == pg.K_DOWN or key == 5) and self.first_line < len(self.text) - 13 and len(self.text) > 13:
                self.first_line += 1
            elif (key == pg.K_UP or key == 4) and self.first_line > 0:
                self.first_line -= 1

    def draw(self) -> None:
        self.draw_box()

        y = self.border * 2
        lines = tuple(f"{reg}: {value}" for reg, value in self.text.items())
        for line in lines[self.first_line:self.first_line + 13]:
            text = self.font.render(line)
            self.image.blit(text, ((self.width - text.get_width()) // 2 + self.border, y))
            y += text.get_height() - 1

        Info.DISPLAY.blit(self.image, (self.x, self.y))


class InstructionBox(TextBox):
    title_font: Text
    line_color: tuple[int, int, int]

    def __init__(self,
                 font: Text,
                 title_font: Text,
                 text: dict,
                 pos: tuple[int, int],
                 dimensions: tuple[int, int],
                 unselected_color: tuple[int, int, int],
                 selected_color: tuple[int, int, int],
                 line_color: tuple[int, int, int],
                 border: int = 0,
                 border_color: tuple[int, int, int] = Colors.GRAY,
                 border_radius: int = 20,
                 alignment: int = Align.UPPER_LEFT,
                 ) -> None:
        super().__init__(font, text, pos, dimensions, unselected_color, selected_color, border, border_color,
                         border_radius, alignment)
        self.title_font = title_font
        self.line_color = line_color

    def check_key(self, key: int):
        if self.selected:
            if key == pg.K_SPACE:
                Info.sum_stage()
                execute()

    def draw(self) -> None:
        self.draw_box()

        header = tuple(key for key in self.text.keys())
        lines = tuple(line for line in self.text.values())
        base_distance = (self.image.get_height() - self.border * 2) // 10
        line_width = self.image.get_width() // (3 / 2)
        line_height = base_distance * 3 / 2
        line_x = self.image.get_width() - line_width - (self.border + base_distance // 4)
        line_y = self.border + base_distance // 4
        for stage, instruction in zip(header, lines):
            title = self.title_font.render(stage)
            title_x = self.image.get_width() - line_width - (
                    self.border + base_distance // 4) - title.get_width() - base_distance // 2
            title_y = line_y + (line_height - title.get_height()) // 2
            self.image.blit(title, (title_x, title_y))
            pg.draw.rect(self.image, self.border_color, (line_x, line_y, line_width, line_height),
                         border_radius=self.border_radius)
            pg.draw.rect(self.image, self.line_color, (
                line_x + self.border, line_y + self.border, line_width - self.border * 2,
                line_height - self.border * 2),
                         border_radius=self.border_radius)
            line = self.font.render(instruction)
            self.image.blit(line, (
                line_x + (line_width - line.get_width()) // 2, line_y + (line_height - line.get_height()) // 2))
            line_y += base_distance * 2

        Info.DISPLAY.blit(self.image, (self.x, self.y))
