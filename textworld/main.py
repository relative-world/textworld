from relative_world.world import RelativeWorld
from textworld.io import load_scenario_from_asset
from textworld.logs import init_logging


def run_example_simulation(scenario: str, timesteps: int = 10):
    init_logging()

    scenario = load_scenario_from_asset(scenario)
    setting_description = "\nScene Setting: {scenario.setting}"
    for actor in scenario.characters:
        print("Loaded character:", actor.name)
        actor.role_description += setting_description

    world = RelativeWorld(children=scenario.characters)

    for _ in range(timesteps):
        list(world.update())

    # print conversation summaries
    print()
    for actor in scenario.characters:
        print("Conversation summary for", actor.name)
        print(actor.summarize_conversation())
        print("=" * 40)


if __name__ == "__main__":
    scenario = "evil_cookies.json"
    timesteps = 5
    run_example_simulation(scenario, timesteps)
