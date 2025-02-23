from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, ListView, ListItem, Button, Label

from textworld.io import list_scenarios, load_scenario_from_asset
from textworld.tui.screens.game import TheGameScreen
from textworld.tui.screens.mainmenu import MainMenuScreen
from textworld.tui.utils import slugify


class ScenarioLoaderScreen(Screen):
    """
    Screen for loading scenarios.

    Allows the user to select a scenario to load.
    """

    CSS = """
        ScenarioLoaderScreen {
            align: center middle;
        }
        
        #ScenarioListContainer {
            width: 50%;
            height: 50%;
        }
        
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("escape", "back", "Back"),
    ]

    _scenarios_by_slug = {}

    def compose(self) -> ComposeResult:
        scenario_names = list_scenarios()
        self._scenarios_by_slug = {
            slugify(scenario): scenario for scenario in scenario_names
        }

        yield Header(id="Header")
        yield Vertical(
            Label("Select a scenario to load:", id="ScenarioLoaderLabel"),
            ListView(
                *[ListItem(Label(scenario), id=slugify(scenario), classes="scenario-list-item") for scenario in scenario_names],
                id="ScenarioList"
            ),
            id="ScenarioListContainer"
        )
        yield Footer(id="Footer")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        scenario = self._scenarios_by_slug[event.item.id]
        self.app.load_scenario(scenario)
        self.app.pop_screen()  # remove ourselves from the screen stack
        self.app.push_screen(TheGameScreen())

    def action_back(self) -> None:
        self.app.pop_screen()
        self.app.push_screen(MainMenuScreen())