from relative_world.event import Event

SAID_ALOUD_EVENT_TYPE = "SAID_ALOUD"
PERFORMED_ACTION_EVENT_TYPE = "PERFORMED_ACTION"


class SaidAloudEvent(Event):
    type: str = SAID_ALOUD_EVENT_TYPE


class PerformedActionEvent(Event):
    type: str = PERFORMED_ACTION_EVENT_TYPE
