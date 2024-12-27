from textual.app import App, ComposeResult
from textual.widget import Widget


class Cell(Widget):
    def __init__(self, row: int, col: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row = row
        self.col = col
        self.walls = [False, False, False, False]  # N, E, S, W

    def render(self) -> str:
        return "#"

    def toggle_wall(self, direction: int):
        self.walls[direction] = not self.walls[direction]
        self.styles.outline_top = ("outer", "white") if self.walls[0] else None
        self.styles.outline_right = ("outer", "white") if self.walls[1] else None
        self.styles.outline_bottom = ("outer", "white") if self.walls[2] else None
        self.styles.outline_left = ("outer", "white") if self.walls[3] else None
        print(self.walls)


class Maze(Widget):
    SIZE = 8

    def __init__(self):
        super().__init__()
        self.styles.layout = "grid"
        self.styles.grid_size_rows = self.SIZE
        self.styles.grid_size_columns = self.SIZE
        self.current_cell = (0, 0)
        self.grid = [
            [Cell(row, col) for col in range(self.SIZE)] for row in range(self.SIZE)
        ]

    def compose(self) -> ComposeResult:
        for row in self.grid:
            for cell in row:
                yield cell

    def navigate(self, row_offset: int, col_offset: int):
        current_row, current_col = self.current_cell
        new_row = (current_row + row_offset) % self.SIZE
        new_col = (current_col + col_offset) % self.SIZE
        self.current_cell = (new_row, new_col)
        self.update_cursor()

    def update_cursor(self):
        for row in self.grid:
            for cell in row:
                cell.remove_class("focused")
        current_row, current_col = self.current_cell
        self.grid[current_row][current_col].add_class("focused")

    def toggle_wall(self, direction: int):
        current_row, current_col = self.current_cell
        self.grid[current_row][current_col].toggle_wall(direction)
        if direction == 0:
            self.grid[current_row - 1][current_col].toggle_wall(2)
        if direction == 1:
            self.grid[current_row][current_col + 1].toggle_wall(3)
        if direction == 2:
            self.grid[current_row + 1][current_col].toggle_wall(0)
        if direction == 3:
            self.grid[current_row][current_col - 1].toggle_wall(1)


class MazeApp(App):
    CSS_PATH = "styles.css"

    def compose(self) -> ComposeResult:
        self.maze = Maze()
        yield self.maze

    def action_navigate(self, row_offset: int, col_offset: int):
        self.maze.navigate(row_offset, col_offset)

    def action_toggle_wall(self, direction: int):
        self.maze.toggle_wall(direction)

    def on_mount(self):
        self.action_navigate(0, 0)
        self.action_toggle_wall(0)

    def key_up(self):
        self.action_navigate(-1, 0)

    def key_down(self):
        self.action_navigate(1, 0)

    def key_left(self):
        self.action_navigate(0, -1)

    def key_right(self):
        self.action_navigate(0, 1)

    def key_w(self):
        self.action_toggle_wall(0)

    def key_d(self):
        self.action_toggle_wall(1)

    def key_s(self):
        self.action_toggle_wall(2)

    def key_a(self):
        self.action_toggle_wall(3)


if __name__ == "__main__":
    MazeApp().run()
