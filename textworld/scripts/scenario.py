import asyncio

import typer

from relative_world.world import RelativeWorld
from textworld.io import load_scenario_from_asset
from textworld.logs import init_logging


async def run_example_simulation(scenario: str, timesteps: int = 10):
    init_logging()

    scenario = load_scenario_from_asset(scenario)
    setting_description = f"\nScene Setting: {scenario.setting}"
    for actor in scenario.characters:
        print("Loaded character:", actor.name)
        actor.role_description += setting_description

    world = RelativeWorld(children=scenario.characters)

    for _ in range(timesteps):
        await world.step()

    # print conversation summaries
    print()
    for actor in scenario.characters:
        print("Conversation summary for", actor.name)
        print(actor.summarize_conversation())
        print("=" * 40)


def sync_run_example_simulation(scenario: str, timesteps: int = 10):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_example_simulation(scenario, timesteps))


def cli():
    typer.run(sync_run_example_simulation)
