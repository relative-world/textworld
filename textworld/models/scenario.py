"""Module for defining roleplaying scenarios used in text-based worlds.

This module defines the RoleplayScenario class, which encapsulates the
setting and characters participating in a roleplaying scenario.
"""

from pydantic import BaseModel

from textworld.models.entity import RoleplayEntity


class RoleplayScenario(BaseModel):
    """RoleplayScenario represents a roleplaying scenario.

    Attributes:
        setting (str): The narrative setting or location of the scenario.
        characters (list[RoleplayEntity]): The list of roleplaying entities or characters participating in the scenario.
    """
    setting: str
    characters: list[RoleplayEntity]
