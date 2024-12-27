from textual.widget import Widget
from textual.app import ComposeResult

from Cell import Cell


class Grid(Widget):
    """Representa o labirinto, contendo uma grade de células e controle de navegação e paredes."""

    SIZE = 8

    def __init__(self) -> None:
        super().__init__()
        self.styles.layout = "grid"

        self.styles.grid_size_rows = self.SIZE
        self.styles.grid_size_columns = self.SIZE

        self.cursor_row = 0
        self.cursor_col = 0
        self.grid = [
            [Cell(row, col) for col in range(self.SIZE)] for row in range(self.SIZE)
        ]

    def compose(self) -> ComposeResult:
        """Componha a grid de células do labirinto."""
        for row in self.grid:
            for cell in row:
                yield cell

    def get_cell(self, row, col) -> Cell:
        """Retorna a célula na posição (row, col)."""
        return self.grid[row][col]

    def on_cell_selected(self, message: Cell.Selected) -> None:
        """Ação a ser realizada quando uma célula é selecionada."""
        self.update_cursor(message.cell.row, message.cell.col)

    def on_cell_toggle_wall(self, message: Cell.ToggleWall) -> None:
        """Ação a ser realizada quando uma parede é alternada."""
        self.update_cursor(message.row, message.col)
        self.toggle_wall(message.direction)

    def move_cursor(self, row_offset: int, col_offset: int) -> None:
        """Move o cursor na direção especificada."""
        row = (self.cursor_row + row_offset) % self.SIZE
        col = (self.cursor_col + col_offset) % self.SIZE
        self.update_cursor(row, col)

    def set_cursor(self, row: int, col: int) -> None:
        """Define a posição do cursor no labirinto."""
        self.cursor_row = row
        self.cursor_col = col

    def update_cursor(self, row: int, col: int) -> None:
        """Atualiza o cursor, removendo a seleção das outras células e selecionando a célula correta."""
        current_cell = self.get_cell(self.cursor_row, self.cursor_col)
        current_cell.selected = False
        current_cell.update_cursor()

        self.set_cursor(row, col)

        current_cell = self.get_cell(self.cursor_row, self.cursor_col)
        current_cell.selected = True
        current_cell.update_cursor()

    def toggle_wall(self, direction: int) -> None:
        """Alterna a parede na célula atual e na célula vizinha na direção oposta."""
        self.grid[self.cursor_row][self.cursor_col].toggle_wall(direction)
        self.toggle_neighbor_wall(self.cursor_row, self.cursor_col, direction)

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
