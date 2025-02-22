from relative_world.location import Location
from textworld.models.actors import RoleplayActor


class DetailedLocation(Location):
    description: str

    @property
    def character_count(self):
        return sum(isinstance(child, RoleplayActor) for child in self.children)
