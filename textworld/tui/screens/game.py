from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Header, TabbedContent, TabPane, Label, Digits
from time import monotonic

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
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("escape", "show_menu", "Pause"),
    ]

    start_time = reactive(monotonic)
    runtime = reactive(0.0)
    previous_runtime = 0
    paused = reactive(False)

    def on_mount(self) -> None:
        """Called when the game screen loads.  schedules screen updates for 12fps."""
        self.set_interval(1 / 12, self.update_runtime)

    async def update_runtime(self):
        if not self.paused:
            self.runtime = monotonic() - self.start_time
            await self.app.schedule_update()

    def on_screen_suspend(self) -> None:
        self.paused = True

    def on_screen_resume(self) -> None:
        self.paused = False
        self.start_time = monotonic()
        self.runtime = 0

    def compose(self) -> ComposeResult:
        yield Header(id="Header")
        with TabbedContent():
            for location in self.app.world.iter_locations():
                tab_id = slugify(f"{location.name}-{location.id}")

                with TabPane(f"{location.name} ({location.character_count})", id=tab_id):
                    yield Vertical(
                        Label(location.name),
                        Label(location.description),
                    )
                    with TabbedContent():
                            with TabPane("inner"):

                                yield Vertical(
                                    Label(location.name),
                                    Label(location.description),
                                )

    def action_show_menu(self):
        self.app.push_screen(GameMenuScreen())
