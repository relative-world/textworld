import asyncio

from textual import work

from relative_world.world import RelativeWorld
from textual.app import App

from textworld.io import load_scenario_from_asset
from textworld.models.actors import RoleplayActor
from textworld.models.location import DetailedLocation
from textworld.tui.screens.mainmenu import MainMenuScreen
from textworld.tui.screens.scenarioloader import ScenarioLoaderScreen


class TextWorldApp(App):
    TITLE = "TextWorld"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def __init__(self):
        super().__init__()
        self._world_updating: bool = False

    def on_ready(self) -> None:
        self.push_screen(MainMenuScreen())

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def start_new_game(self):
        self.push_screen(ScenarioLoaderScreen())

    def load_scenario(self, scenario: str) -> None:
        self.scenario = load_scenario_from_asset(scenario)
        self.world = RelativeWorld()
        location = DetailedLocation(
            name="Example Location",
            description="This is an example location.",
        )
        self.world.add_location(location)
        for character in self.scenario.characters:
            actor = RoleplayActor.model_validate(character.model_dump())
            self.world.add_actor(actor, location)
