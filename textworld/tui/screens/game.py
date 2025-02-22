from relative_world.location import Location
from time import monotonic

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Header, Input

from textworld.tui.screens.gamemenu import GameMenuScreen


class TheGameScreen(Screen):
    """
    This is the game itself.

    handles time management and global world state.
    """

    DEFAULT_CSS = """
    .container {
        width: 100%;
        height: 100%;
        layout: grid;
        grid-size: 2 1;
        grid-columns: 2fr 1fr;
    }
    
    .column-left {
        layout: grid;
        grid-size: 1 2;
        grid-rows: 12fr 1fr;
    }

    .column-right {
        layout: grid;
        grid-size: 1 3;
        grid-rows: 8fr 8fr 1fr;
    }
    
    .box {
        height: 100%;
        border: solid green;
    }
    """
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("escape", "show_menu", "Pause"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(id="Header")
        yield Footer(id="Footer")

    def action_show_menu(self):
        self.app.push_screen(GameMenuScreen())
