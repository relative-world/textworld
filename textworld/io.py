from typing import Type

import orjson as json
from pathlib import Path

from pydantic import BaseModel

from textworld.models.scenario import RoleplayScenario
from textworld.stories.models import StoryOutline


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

def load_model_from_asset(filename: str, model_class: Type[BaseModel]) -> BaseModel:
    """
    Loads a model from a JSON asset file.

    Parameters
    ----------
    filename : str
        The name of the JSON file to load.
    model_class : type
        The model class to use for loading the data.

    Returns
    -------
    model_class
        The loaded model.
    """
    data = load_json_asset(filename)
    return model_class.model_validate(data)


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

def load_story_from_json(data: dict) -> StoryOutline:
    """
    Loads a story from a JSON dictionary.

    Parameters
    ----------
    data : dict
        The JSON data representing the story.

    Returns
    -------
    StoryOutline
        The loaded story.
    """
    return StoryOutline.model_validate(data)

def load_story_from_asset(filename: str) -> StoryOutline:
    """
    Loads a story from a JSON asset file.

    Parameters
    ----------
    filename : str
        The name of the JSON file to load.

    Returns
    -------
    StoryOutline
        The loaded story.
    """
    data = load_json_asset(filename)
    return load_story_from_json(data)

# def load_scenes_from_json(data: dict) -> list[SceneOutline]:
#     """
#     Loads a list of scenes from a JSON dictionary.
#
#     Parameters
#     ----------
#     data : dict
#         The JSON data representing the scenes.
#
#     Returns
#     -------
#     list of Scene
#         The loaded scenes.
#     """
#     return [Scene.model_validate(scene) for scene in data]
#
#
# def load_scenes_from_asset(filename: str) -> list[Scene]:
#     """
#     Loads a list of scenes from a JSON asset file.
#
#     Parameters
#     ----------
#     filename : str
#         The name of the JSON file to load.
#
#     Returns
#     -------
#     list of Scene
#         The loaded scenes.
#     """
#     data = load_json_asset(filename)
#     return load_scenes_from_json(data)
