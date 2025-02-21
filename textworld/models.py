from typing import Annotated

from pydantic import BaseModel, Field


class RoleplayResponse(BaseModel):
    response: Annotated[str | None, Field(description="Something you are saying aloud.")]
    private_thought: Annotated[
        str | None, Field(description="Your private thoughts in the moment.")
    ] = None
    action: Annotated[
        str | None, Field(description="A description of actions you are performing.")
    ] = None


class SummarizationResponse(BaseModel):
    summary: Annotated[str, Field(description="The summary of the conversation.")]
    tags: Annotated[list[str], Field(description="Tags for the conversation.")] = []
    participants: Annotated[
        list[str], Field(description="The participants in the conversation.")
    ]
    location: Annotated[str, Field(description="The location of the conversation.")]
