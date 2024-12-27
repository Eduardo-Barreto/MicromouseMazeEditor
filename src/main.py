from textual.app import App, ComposeResult

from Grid import Grid

class MazeApp(App):
    """Aplicativo para controlar a navegação e manipulação de paredes no labirinto."""

    CSS_PATH = "styles.css"

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        """Componha o labirinto para o aplicativo."""
        self.grid = Grid(16)
        yield self.grid

    def action_toggle_wall(self, direction: int) -> None:
        """Ação para alternar uma parede em uma direção específica."""
        self.grid.toggle_wall(direction)

    def on_mount(self) -> None:
        """Ação a ser realizada quando o aplicativo for montado (iniciar navegação)."""
        self.grid.update_cursor(0, 0)

    def key_up(self) -> None:
        """Movimento para cima."""
        self.grid.move_cursor(-1, 0)

    def key_down(self) -> None:
        """Movimento para baixo."""
        self.grid.move_cursor(1, 0)

    def key_left(self) -> None:
        """Movimento para a esquerda."""
        self.grid.move_cursor(0, -1)

    def key_right(self) -> None:
        """Movimento para a direita."""
        self.grid.move_cursor(0, 1)

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
