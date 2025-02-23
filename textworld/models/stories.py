from pydantic import BaseModel, Field
from typing import List, Dict

from relative_world.location import Location
from textworld.models.actors import Character
from textworld.models.location import StoryLocation


class Subplot(BaseModel):
    title: str
    purpose: str
    keypoints: List[str] = Field(default_factory=list)
    involved_characters: List[str] = Field(default_factory=list)
    intersections_with_main: List[str] = Field(default_factory=list)


class Story(BaseModel):
    title: str
    genre: str
    medium: str
    themes: List[str] = Field(default_factory=list)

    locations: List[StoryLocation] = Field(default_factory=list)
    characters: List[Character] = Field(default_factory=list)
    main_plot: Dict[str, str] = Field(default_factory=dict)  # {"summary": "text", "keypoints": ["event1", "event2"]}
    subplots: List[Subplot] = Field(default_factory=list)

    key_story_events: Dict[str, str] = Field(default_factory=dict)  # {"Inciting Incident": "desc", "Climax": "desc"}

