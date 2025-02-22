from relative_world.world import RelativeWorld
from textual.app import App

from textworld.tui.screens.mainmenu import MainMenuScreen
from textworld.tui.screens.game import TheGameScreen

class TextWorldApp(App):
    TITLE = "TextWorld"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def __init__(self, world: RelativeWorld):
        super().__init__()
        self.world = world

    def on_ready(self) -> None:
        self.push_screen(MainMenuScreen())

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def start_new_game(self):
        self.push_screen(TheGameScreen())

if __name__ == "__main__":
    world = RelativeWorld()
    app = TextWorldApp(world)
    app.run()
