from pydantic import BaseModel

from textworld.models.entity import RoleplayEntity


class RoleplayScenario(BaseModel):
    setting: str
    characters: list[RoleplayEntity]
