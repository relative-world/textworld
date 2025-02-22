"""
This module provides Pydantic models for textworld responses.

It contains:
  - A model for roleplaying responses with oral expressions, private thoughts, and actions.
  - A model for conversation summarizations that includes a summary, tags, participants, and location.
"""
from typing import Annotated

from pydantic import BaseModel, Field


class RoleplayResponse(BaseModel):
    """
    Model representing roleplaying responses.

    Attributes:
        response: A string representing something said aloud.
        private_thought: A string representing private thoughts.
        action: A string describing an action being performed.
    """
    response: Annotated[str | None, Field(description="Something you are saying aloud.")] = None
    private_thought: Annotated[
        str | None, Field(description="Your private thoughts in the moment.")
    ] = None
    action: Annotated[
        str | None, Field(description="A description of actions you are performing.")
    ] = None


class SummarizationResponse(BaseModel):
    """
    Model representing conversation summarizations.

    Attributes:
        summary: A string summarizing the conversation.
        tags: A list of strings tagging the conversation.
        participants: A list of strings representing participants in the conversation.
        location: A string indicating the location of the conversation.
    """
    summary: Annotated[str, Field(description="The summary of the conversation.")]
    tags: Annotated[list[str], Field(description="Tags for the conversation.")] = []
    participants: Annotated[
        list[str], Field(description="The participants in the conversation.")
    ]
    location: Annotated[str, Field(description="The location of the conversation.")] = "Unknown"
