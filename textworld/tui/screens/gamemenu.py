from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Footer, Header


class GameMenuScreen(Screen):
    CSS = """
        GameMenuScreen {
            align: center middle;
            background: rgba(0,0,0,0.5);
        }
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("escape", "dismiss_menu", "Continue"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(id="Header")
        yield Button("Continue", id="continue")
        yield Button("Restart", id="restart")
        yield Button("Quit", id="quit")
        yield Footer(id="Footer")

    def action_dismiss_menu(self):
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        match button_id:
            case "continue":
                self.action_dismiss_menu()
            case "restart":
                self.app.pop_screen()
                self.app.start_new_game()
            case "quit":
                self.app.exit(0)
