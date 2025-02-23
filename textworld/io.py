import orjson as json
from pathlib import Path

from textworld.models.scenario import RoleplayScenario


def get_assets_path() -> Path:
    """
    Gets the path to the assets directory.

    Returns
    -------
    Path
        The path to the assets directory.
    """
    return Path(__file__).parent / 'assets'


def load_json_asset(filename: str) -> dict:
    """
    Loads a JSON asset from the assets directory.

    Parameters
    ----------
    filename : str
        The name of the JSON file to load.

    Returns
    -------
    dict
        The loaded JSON data.
    """
    with open(get_assets_path() / filename) as f:
        return json.loads(f.read())


def load_scenario_from_json(data: dict) -> RoleplayScenario:
    """
    Loads a scenario from a JSON dictionary.

    Parameters
    ----------
    data : dict
        The JSON data representing the scenario.

    Returns
    -------
    RoleplayScenario
        The loaded scenario.
    """
    return RoleplayScenario.model_validate(data)


def load_scenario_from_asset(filename: str) -> RoleplayScenario:
    """
    Loads a scenario from a JSON asset file.

    Parameters
    ----------
    filename : str
        The name of the JSON file to load.

    Returns
    -------
    RoleplayScenario
        The loaded scenario.
    """
    data = load_json_asset(filename)
    return load_scenario_from_json(data)


def list_scenarios() -> list[str]:
    """
    Lists all scenario files in the assets directory.

    Returns
    -------
    list of str
        A list of scenario filenames.
    """
    return [f.name for f in get_assets_path().glob("*.json")]
