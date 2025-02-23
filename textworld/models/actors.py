from typing import List, Dict, Optional

from pydantic import Field, BaseModel

from relative_world.actor import Actor
from textworld.models.entity import RoleplayEntity


class RoleplayActor(RoleplayEntity, Actor):
    pass


class Character(BaseModel):
    name: str
    physical_description: str
    demeanor: str
    motivations: List[str] = Field(default_factory=list)
    knowledge: List[str] = Field(default_factory=list)
    relationships: Dict[str, str] = Field(default_factory=dict)  # e.g., {"Alice": "enemy", "Bob": "mentor"}
    character_arc: Optional[str] = None
