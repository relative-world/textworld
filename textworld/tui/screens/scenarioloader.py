from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, ListView, ListItem, Button

from textworld.io import list_scenarios, load_scenario_from_asset
from textworld.tui.screens.game import TheGameScreen
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
            width: 30%;
            align: center middle;
        }
        
        #ScenarioList {
            align: center middle;
        }
        
        .scenario-btn {
            width: 30%;
            align: center middle
        }
    """

    _scenarios_by_slug = {}

    def compose(self) -> ComposeResult:
        scenario_names = list_scenarios()
        self._scenarios_by_slug = {
            slugify(scenario): scenario for scenario in scenario_names
        }

        yield Header(id="Header")
        yield Vertical(
            ListView(
                *[ListItem(Button(scenario, id=slugify(scenario), classes="scenario-btn")) for scenario in scenario_names],
                id="ScenarioList"
            ),
            id="ScenarioListContainer"
        )
        yield Footer(id="Footer")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        scenario = self._scenarios_by_slug[event.button.id]
        self.app.load_scenario(scenario)
        self.app.pop_screen()  # remove yourself from the screen stack
        self.app.push_screen(TheGameScreen())
