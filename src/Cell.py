from textual.message import Message
from textual.widget import Widget

class Cell(Widget):
    """Representa uma célula no labirinto com paredes e capacidade de alternar o estado das paredes."""

    def __init__(self, row: int, col: int) -> None:
        super().__init__()
        self.row = row
        self.col = col
        self.walls = [False, False, False, False]  # N, E, S, W
        self.selected = False

    def render(self) -> str:
        """Renderiza o conteúdo da célula (representando a célula como uma parede)."""
        self.update_wall_styles()
        self.update_cursor()
        return "#"

    def toggle_wall(self, direction: int) -> None:
        """Alterna o estado da parede na direção indicada (0: N, 1: E, 2: S, 3: W)."""
        self.walls[direction] = not self.walls[direction]
        self.update_wall_styles()

    def update_wall_styles(self) -> None:
        """Atualiza o estilo das paredes com base no estado atual."""
        self.styles.outline_top = ("outer", "white") if self.walls[0] else None
        self.styles.outline_right = ("outer", "white") if self.walls[1] else None
        self.styles.outline_bottom = ("outer", "white") if self.walls[2] else None
        self.styles.outline_left = ("outer", "white") if self.walls[3] else None

    class Selected(Message):
        def __init__(self, cell):
            self.cell = cell
            super().__init__()

    class ToggleWall(Message):
        def __init__(self, row, col, direction):
            self.row = row
            self.col = col
            self.direction = direction
            super().__init__()

    def on_mouse_up(self, event) -> None:
        """Alterna o estado de seleção da célula quando clicada."""
        cell_center_x = self.size.width / 2
        cell_center_y = self.size.height / 2

        top = cell_center_y - event.y
        right = event.x - cell_center_x
        bottom = event.y - cell_center_y
        left = cell_center_x - event.x

        self.update_cursor()
        self.post_message(self.Selected(self))

        if not self.selected:
            return

        elif top > left and top > right and top > bottom:
            self.post_message(self.ToggleWall(self.row, self.col, 0))
        elif right > left and right > top and right > bottom:
            self.post_message(self.ToggleWall(self.row, self.col, 1))
        elif bottom > left and bottom > right and bottom > top:
            self.post_message(self.ToggleWall(self.row, self.col, 2))
        if left > right and left > top and left > bottom:
            self.post_message(self.ToggleWall(self.row, self.col, 3))

    def update_cursor(self) -> None:
        """Atualiza o estilo da célula, destacando-a quando selecionada."""
        if self.selected:
            self.add_class("focused")
        else:
            self.remove_class("focused")
