import uuid

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Header, Tabs, Tab, Placeholder, Input, Footer
from time import monotonic

from textworld.tui.components.locationtabcontent import LocationTabContent
from textworld.tui.screens.gamemenu import GameMenuScreen
from textworld.tui.utils import slugify


class TheGameScreen(Screen):
    """
    This is the game itself.

    handles time management and global world state.
    """

    CSS = """
    #TabContainer {
        dock: top;
    }
    
    #LayoutContainer {
        layout: grid;
        grid-size: 2;
        grid-columns: 4fr 1fr;
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

    start_time = reactive(monotonic)
    runtime = reactive(0.0)
    previous_runtime = 0
    paused = reactive(False)
    _world_updating = False

    def on_mount(self) -> None:
        """Called when the game screen loads.  schedules screen updates for 12fps."""
        self.set_interval(1, self.update_runtime)

    def update_runtime(self):
        if not self.paused:
            self.runtime = monotonic() - self.start_time
            self.run_worker(self.schedule_update(), exclusive=False)

    async def schedule_update(self):
        if not self._world_updating:
            self._world_updating = True
            async for event in self.app.world.update():
                pass
            self._world_updating = False

    def on_screen_suspend(self) -> None:
        self.paused = True

    def on_screen_resume(self) -> None:
        self.paused = False
        self.start_time = monotonic()
        self.runtime = 0

    def compose(self) -> ComposeResult:
        yield Header(id="Header")
        yield Vertical(
            Tabs(*[
                Tab(f"{location.name} ({location.character_count})", id=slugify(f"{location.name}_demarc_{location.id}"))
                for location in self.app.world.iter_locations()
            ]),
            Container(
                LocationTabContent(classes="box"),
                Placeholder(classes="box"),
                id="LayoutContainer",
            ),
            Input(placeholder="Inject Command")
        )
        yield Footer()

    def action_show_menu(self):
        self.app.push_screen(GameMenuScreen())

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        location = self.app.world.get_location_by_id(uuid.UUID(event.tab.id.split("_demarc_")[-1].replace('_', '-')))
        self.query_one(LocationTabContent).set_location(location)


