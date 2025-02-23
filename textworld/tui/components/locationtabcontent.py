from typing import Annotated, Any

from pydantic import PrivateAttr
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import RichLog, Label

from relative_world.actor import Actor
from relative_world.entity import Entity
from relative_world.event import Event
from textworld.models.events import SaidAloudEvent, PerformedActionEvent, ThoughtEvent


class LogActor(Actor):
    _logger: Annotated[Any, PrivateAttr()]

    def should_log_event(self, entity: Entity, event: Event) -> bool:
        return True

    def format_event(self, entity: Entity, event: Event) -> str:
        if isinstance(event, SaidAloudEvent):
            return f"[{entity.chat_color}]{entity.name} said {event.message}[/]"
        if isinstance(event, PerformedActionEvent):
            return f"[{entity.action_color}]{entity.name} - {event.action}[/]"
        if isinstance(event, ThoughtEvent):
            return f"[{entity.thought_color}]{entity.name} thought {event.thought}[/]"

    async def handle_event(self, entity: Entity, event: Event) -> None:
        if self.should_log_event(entity, event):
            self._logger.write_to_log(self.format_event(entity, event))



class LocationTabContent(Widget):
    """
    A container for the content of a tab.
    """

    location = reactive(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_actor = LogActor()
        self.log_actor._logger = self

    def on_mount(self) -> None:
        location = next(self.app.world.iter_locations())
        self.app.world.add_actor(self.log_actor, location)

    def write_to_log(self, message: str):
        self.query_one("#LocationLog", RichLog).write(message)

    def set_location(self, location):
        self.location = location
        location.add_actor(self.log_actor)

    def compose(self) -> ComposeResult:
        yield Vertical(
            RichLog(id="LocationLog", markup=True, wrap=True),
        )
