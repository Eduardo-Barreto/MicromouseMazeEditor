from textual.app import App, ComposeResult
from textual.widget import Widget


class Cell(Widget):
    """Representa uma célula no labirinto com paredes e capacidade de alternar o estado das paredes."""

    def __init__(self, row: int, col: int) -> None:
        super().__init__()
        self.row = row
        self.col = col
        self.walls = [False, False, False, False]  # N, E, S, W

    def render(self) -> str:
        """Renderiza o conteúdo da célula (representando a célula como uma parede)."""
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


class Maze(Widget):
    """Representa o labirinto, contendo uma grade de células e controle de navegação e paredes."""

    SIZE = 8

    def __init__(self) -> None:
        super().__init__()
        self.styles.layout = "grid"
        self.styles.grid_size_rows = self.SIZE
        self.styles.grid_size_columns = self.SIZE
        self.current_cell = (0, 0)
        self.grid = [
            [Cell(row, col) for col in range(self.SIZE)] for row in range(self.SIZE)
        ]

    def compose(self) -> ComposeResult:
        """Componha a grid de células do labirinto."""
        for row in self.grid:
            for cell in row:
                yield cell

    def navigate(self, row_offset: int, col_offset: int) -> None:
        """Navega para uma nova célula com base no deslocamento especificado."""
        current_row, current_col = self.current_cell
        new_row = (current_row + row_offset) % self.SIZE
        new_col = (current_col + col_offset) % self.SIZE
        self.current_cell = (new_row, new_col)
        self.update_cursor()

    def update_cursor(self) -> None:
        """Atualiza a célula que está sendo focalizada (indicada com a classe 'focused')."""
        for row in self.grid:
            for cell in row:
                cell.remove_class("focused")
        current_row, current_col = self.current_cell
        self.grid[current_row][current_col].add_class("focused")

    def toggle_wall(self, direction: int) -> None:
        """Alterna a parede na célula atual e na célula vizinha na direção oposta."""
        current_row, current_col = self.current_cell
        self.grid[current_row][current_col].toggle_wall(direction)
        self.toggle_neighbor_wall(current_row, current_col, direction)

    def toggle_neighbor_wall(self, row: int, col: int, direction: int) -> None:
        """Alterna a parede da célula vizinha com base na direção especificada."""
        if direction == 0:  # Norte
            if row == 0:
                return
            self.grid[row - 1][col].toggle_wall(2)
        elif direction == 1:  # Leste
            if col == self.SIZE - 1:
                return
            self.grid[row][col + 1 % self.SIZE].toggle_wall(3)
        elif direction == 2:  # Sul
            if row == self.SIZE - 1:
                return
            self.grid[row + 1 % self.SIZE][col].toggle_wall(0)
        elif direction == 3:  # Oeste
            if col == 0:
                return
            self.grid[row][col - 1 % self.SIZE].toggle_wall(1)


class MazeApp(App):
    """Aplicativo para controlar a navegação e manipulação de paredes no labirinto."""

    CSS_PATH = "styles.css"

    def compose(self) -> ComposeResult:
        """Componha o labirinto para o aplicativo."""
        self.maze = Maze()
        yield self.maze

    def action_navigate(self, row_offset: int, col_offset: int) -> None:
        """Ação para navegar no labirinto."""
        self.maze.navigate(row_offset, col_offset)

    def action_toggle_wall(self, direction: int) -> None:
        """Ação para alternar uma parede em uma direção específica."""
        self.maze.toggle_wall(direction)

    def on_mount(self) -> None:
        """Ação a ser realizada quando o aplicativo for montado (iniciar navegação)."""
        self.action_navigate(0, 0)

    def key_up(self) -> None:
        """Movimento para cima."""
        self.action_navigate(-1, 0)

    def key_down(self) -> None:
        """Movimento para baixo."""
        self.action_navigate(1, 0)

    def key_left(self) -> None:
        """Movimento para a esquerda."""
        self.action_navigate(0, -1)

    def key_right(self) -> None:
        """Movimento para a direita."""
        self.action_navigate(0, 1)

    def key_w(self) -> None:
        """Alterna a parede superior da célula atual."""
        self.action_toggle_wall(0)

    def key_d(self) -> None:
        """Alterna a parede direita da célula atual."""
        self.action_toggle_wall(1)

    def key_s(self) -> None:
        """Alterna a parede inferior da célula atual."""
        self.action_toggle_wall(2)

    def key_a(self) -> None:
        """Alterna a parede esquerda da célula atual."""
        self.action_toggle_wall(3)


if __name__ == "__main__":
    MazeApp().run()
