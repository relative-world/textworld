import orjson as json
from pathlib import Path

from textworld.models.scenario import RoleplayScenario


def get_assets_path():
    return Path(__file__).parent / 'assets'

def load_json_asset(filename):
    with open(get_assets_path() / filename) as f:
        return json.loads(f.read())


def load_scenario_from_asset(filename: str):
    data = load_json_asset(filename)
    return RoleplayScenario.model_validate(data)
