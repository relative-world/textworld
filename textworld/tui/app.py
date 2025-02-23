import asyncio

from relative_world.world import RelativeWorld
from textual.app import App

from textworld.io import load_scenario_from_asset
from textworld.tui.screens.mainmenu import MainMenuScreen
from textworld.tui.screens.scenarioloader import ScenarioLoaderScreen


class TextWorldApp(App):
    TITLE = "TextWorld"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def __init__(self, world: RelativeWorld):
        super().__init__()
        self._world = world.model_copy()  # for restarts
        self.world = world
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
        self.world = RelativeWorld(children=self.scenario.characters)

    async def schedule_update(self):
        if not self._world_updating:
            self._world_updating = True
            await self._update_world()

    async def _update_world(self):
        try:
            await asyncio.to_thread(self.world.step)
        except StopAsyncIteration:
            pass
        self._world_updating = False
