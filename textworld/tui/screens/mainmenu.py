from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Rule


class MainMenuScreen(Screen):
    CSS = """
        MainMenuScreen {
            align: center middle;
        }
        
        #MainMenuButtons {
            align: center middle;
            height: 5;
        }
        
        #MainMenuTitle {
            width: 50%;
            align: center middle;
        }
        
        #WelcomeLabel {
            text-align: center;
        }
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(id="Header")

        yield Vertical(
            Label("Welcome to TextWorld!", id="WelcomeLabel"),
            Rule(line_style="heavy", id="WelcomeLabelRule"),
            Horizontal(
                Button("Start", id="start"),
                Button("Quit", id="quit"),
                id="MainMenuButtons"
            ),
            id="MainMenuTitle"
        )
        yield Footer(id="Footer")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        match button_id:
            case "start":
                self.app.pop_screen()
                self.app.start_new_game()
            case "quit":
                self.app.exit(0)
