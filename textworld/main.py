import random

from relative_world.world import RelativeWorld
from textworld.entity import RoleplayEntity
from textworld.logs import init_logging


def run_example_simulation(timesteps: int = 10):
    init_logging()

    actors = [
        RoleplayEntity(name="Alice"),
        RoleplayEntity(name="Bob"),
        RoleplayEntity(name="Charlie"),
    ]

    random.shuffle(actors)

    world = RelativeWorld(children=actors)

    for _ in range(timesteps):
        list(world.update())

    # print conversation summaries
    print()
    for actor in actors:
        print("Conversation summary for", actor.name)
        print(actor.summarize_conversation())
        print("=" * 40)


if __name__ == "__main__":
    timesteps = 1
    run_example_simulation(timesteps)
