# textworld/models/events.py

from relative_world.event import Event

SAID_ALOUD_EVENT_TYPE = "SAID_ALOUD"
PERFORMED_ACTION_EVENT_TYPE = "PERFORMED_ACTION"
THOUGHT_EVENT_TYPE = "THOUGHT"

class SaidAloudEvent(Event):
    """
    An event representing an entity speaking aloud.

    Attributes:
        type (str): The type of the event, always set to SAID_ALOUD_EVENT_TYPE.
        message (str): The spoken message.
    """
    type: str = SAID_ALOUD_EVENT_TYPE
    message: str


class PerformedActionEvent(Event):
    """
    An event representing an entity performing an action.

    Attributes:
        type (str): The type of the event, always set to PERFORMED_ACTION_EVENT_TYPE.
        action (str): The action performed.
    """
    type: str = PERFORMED_ACTION_EVENT_TYPE
    action: str


class ThoughtEvent(Event):
    """
    An event representing an entity's thought.

    Attributes:
        type (str): The type of the event, always set to THOUGHT_EVENT_TYPE.
        thought (str): The thought content.
    """
    type: str = THOUGHT_EVENT_TYPE
    thought: str
