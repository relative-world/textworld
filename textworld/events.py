from relative_world.event import Event

SAID_ALOUD_EVENT_TYPE = "SAID_ALOUD"
PERFORMED_ACTION_EVENT_TYPE = "PERFORMED_ACTION"
THOUGHT_EVENT_TYPE = "THOUGHT"

class SaidAloudEvent(Event):
    type: str = SAID_ALOUD_EVENT_TYPE
    message: str


class PerformedActionEvent(Event):
    type: str = PERFORMED_ACTION_EVENT_TYPE
    action: str


class ThoughtEvent(Event):
    type: str = THOUGHT_EVENT_TYPE
    thought: str
