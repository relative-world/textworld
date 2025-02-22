from relative_world.world import RelativeWorld
from textworld.models.actors import RoleplayActor
from textworld.models.location import DetailedLocation
from textworld.tui.app import TextWorldApp

if __name__ == "__main__":
    world = RelativeWorld()
    location_descriptions = [
        ("Drunkie's", "A dimly lit bar with a strong smell of alcohol."),
        ("The Bar", "A lively place with music and chatter."),
        ("The Alley", "A narrow, dark alley with trash bins."),
        ("The Street", "A busy street with cars and pedestrians."),
        ("The Park", "A peaceful park with green trees and benches.")
    ]
    for name, description in location_descriptions:
        location = DetailedLocation(name=name, description=description)
        world.add_location(location)

    players = [
        ("Doug", "A friendly drunk."),
        ("Nancy", "A frisky lush.")
    ]
    for name, description in players:
        roleplayer = RoleplayActor(name=name, role_description=description)
        world.add_actor(roleplayer, location=world.children[0])

    app = TextWorldApp(world)
    app.run()
