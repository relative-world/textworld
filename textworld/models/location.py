from typing import List

from pydantic import Field, BaseModel

from relative_world.location import Location
from textworld.models.actors import RoleplayActor


class DetailedLocation(Location):
    description: str

    @property
    def character_count(self):
        return sum(isinstance(child, RoleplayActor) for child in self.children)


class StoryLocation(BaseModel):
    name: str
    description: str
    key_events: List[str] = Field(default_factory=list)
    notable_inhabitants: List[str] = Field(default_factory=list)
    location_conflicts: List[str] = Field(default_factory=list)
