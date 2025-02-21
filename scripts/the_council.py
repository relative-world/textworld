from random import random

from relative_world.world import RelativeWorld

from textworld.models.entity import RoleplayEntity
from textworld.logs import init_logging

members = [
  {
    "name": "Jacob Whitman",
    "role_description": "Jacob is a pragmatic problem solver who values efficiency and structure. He approaches issues by breaking them down into smaller, manageable parts and applying proven methods to resolve them. He prefers clear objectives and timelines, often guiding teams with a no-nonsense, results-driven approach. While he may seem rigid at times, his reliability makes him a cornerstone in any problem-solving scenario."
  },
  {
    "name": "Melissa Carter",
    "role_description": "Melissa is a collaborative problem solver who thrives on team input and discussion. She believes that the best solutions come from diverse perspectives, so she actively listens and synthesizes ideas before making decisions. She’s known for her ability to mediate conflicts and bring people together, ensuring that all voices are heard and valued in the process."
  },
  {
    "name": "Brian Holloway",
    "role_description": "Brian is an intuitive problem solver who follows his gut instincts. He relies on experience, pattern recognition, and creativity to navigate complex issues. He often challenges conventional wisdom and isn't afraid to take risks. While his approach can sometimes seem unstructured, he frequently arrives at innovative solutions that others may not have considered."
  },
  {
    "name": "Samantha Nguyen",
    "role_description": "Samantha is an analytical problem solver who meticulously researches and evaluates data before making decisions. She enjoys digging into the details, questioning assumptions, and testing hypotheses. She often prefers working independently to form a well-supported conclusion before presenting her findings, and while she may take longer to decide, her solutions are typically well-reasoned and evidence-based."
  },
  {
    "name": "Derek Foster",
    "role_description": "Derek is an adaptive problem solver who thrives in uncertainty and change. He is quick to pivot when faced with obstacles and enjoys thinking on his feet. His ability to remain calm under pressure makes him well-suited for crisis management. He embraces experimentation and iteration, learning from failures and adjusting course as needed to find the best outcome."
  }
]


def run_example_simulation(timesteps: int = 10):
    init_logging()

    actors = [
        RoleplayEntity(
            name=member["name"],
            role_description=member["role_description"]
        ) for member in members
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
