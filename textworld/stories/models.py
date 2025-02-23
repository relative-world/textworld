from typing import List, Dict, Optional, Annotated

from pydantic import BaseModel, Field


class Subplot(BaseModel):
    title: str
    purpose: str
    keypoints: List[str] = Field(default_factory=list)
    involved_characters: List[str] = Field(default_factory=list)
    intersections_with_main: List[str] = Field(default_factory=list)


class Character(BaseModel):
    name: str
    physical_description: str
    demeanor: str
    motivations: List[str] = Field(default_factory=list)
    knowledge: List[str] = Field(default_factory=list)
    relationships: Dict[str, str] = Field(default_factory=dict)  # e.g., {"Alice": "enemy", "Bob": "mentor"}
    character_arc: Optional[str] = None


class StoryLocation(BaseModel):
    name: str
    description: str
    key_events: List[str] = Field(default_factory=list)
    notable_inhabitants: List[str] = Field(default_factory=list)
    location_conflicts: List[str] = Field(default_factory=list)


class SceneLocation(BaseModel):
    name: str
    description: str
    exits: Annotated[list[str], Field(description="The names of the locations that can be reached from this location.")]

class SceneLocationList(BaseModel):
    locations: list[SceneLocation]

class StoryActScene(BaseModel):
    title: str
    description: str
    characters: list[str] = []
    key_events: list[str] = []
    location: SceneLocation

class StoryChapter(BaseModel):
    title: str
    text: str

class StorySceneSequence(BaseModel):
    title: str
    scenes: list[StoryActScene]


class StoryAct(BaseModel):
    title: str
    description: str
    scenes: list[StoryActScene] = Field(default_factory=list)


class StoryActOutline(BaseModel):
    title: str
    description: str
    key_events: list[str] = Field(default_factory=list)
    scenes: Annotated[list[str], Field(description="A list of scene titles")]
    subplots: list[Subplot] = Field(default_factory=list)

class StoryOutline(BaseModel):
    title: str
    genre: str
    medium: str
    acts: list[StoryActOutline]
    themes: List[str] = []
    locations: List[StoryLocation] = []
    characters: List[Character] = []
    subplots: List[Subplot] = []

    key_story_events: Dict[str, str] = Field(default_factory=dict)  # {"Inciting Incident": "desc", "Climax": "desc"}
