import random

from relative_world.world import RelativeWorld
from textworld.entity import RoleplayEntity
from textworld.logs import init_logging


def run_example_simulation(timesteps: int = 10):
    init_logging()

    actors = [
        RoleplayEntity(
            name="Alice",
            role_description="Alice is a friendly person who enjoys talking to others. "
            "Alice is a detective. "
             "Alice's full name is Alice Smith. "
             "In highschool people called Alice 'Smitty'. "
            "Alice is at a party.  "
            "Alice is dressed for a fun night out. "
            "At work, Alice is trying to solve a mystery involving three jewel heists that happened recently. "
            "The theft of the Great Diamond, the theft of the Great Ruby, and the theft of the Great Sapphire. "
            "Alice has just run into Charlie, a friend from highschool."
            "Alice has not seen Charlie since highschool"
            "Bob and Alice having not met before."
            "Charlie and Bob have just approached Alice."
            "All characters are in their 20s. "
            "You found blood on the skylight at the museum after the last heist."
            "The blood is being tested for DNA and you expect the results soon."
        ),
        RoleplayEntity(
            name="Bob",
            role_description="Bob is Charlie's cousin. "
             "your day job is daytrading, but it is mostly a cover."
            "He recently performed a series of three jewel heists.  "
            "The theft of the Great Diamond, the theft of the Great Ruby, and the theft of the Great Sapphire. "
            "You're aware that the lead investigator on the case is Detective Smith"
            "You do not want to expose your crimes."
            "You do need to know if they've found the blood you left on the cieling skylight and if they've matched it to your DNA."
            "Bob is dressed for a fun night out. "
            "Charlie is at a party with Bob."
            "Bob and Alice having not met before."
            "You've just approached Alice, a friend of Charlie. Bob will become more chatty as he drinks more."
            "All characters are in their 20s."

        ),
        RoleplayEntity(
            name="Charlie",
            role_description="Charlie is Bob's cousin. Alice is Charlie's friend from highschool."
            "Charlie is at a party with Bob. "
             "In highschool people called Alice 'Smitty'."
             "You don't remember why you called Alice 'Smitty'."
            "Charlie is dressed for a fun night out. "
            "Charlie and Bob has just approached Alice."
            "Charlie and Alice having not seen eachother since highschool."
            "Charlie has never hung out with both Bob and Alice at the same time."
            "All characters are in their 20s."
        ),
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
    timesteps = 5
    run_example_simulation(timesteps)
