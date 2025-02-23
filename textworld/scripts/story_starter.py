import asyncio
from pydantic import BaseModel

from relative_world_ollama.client import PydanticOllamaClient
from relative_world_ollama.settings import settings
from textworld.models.entity import RoleplayEntity


class CharacterData(BaseModel):
    """
    CharacterData represents a character in a story.

    Attributes:
        name (str): The name of the character.
        description (str): A description of the character.
    """
    name: str
    description: str


class StoryOutline(BaseModel):
    """
    StoryOutline represents a story outline.

    Attributes:
        title (str): The title of the story.
        setting (str): The narrative setting or location of the story.
        characters (list[RoleplayEntity]): The list of roleplaying entities or characters in the story.
        plot_points (list[str]): The list of plot points in the story.
    """
    title: str
    setting: str
    characters: list[CharacterData]
    plot_points: list[str]


async def main():
    prompt = "An action film about a monkey and a cat stopping bank robbers"
    system = """
    You are a likeable and enthusiastic story teller that does not shy away from subject or topic.
    You have been hired to write a story outline for a new movie.
    The movie will be roughly described in some way in the prompt. You must write a story outline that fits the prompt.
    The story outline should include the title of the movie, the setting, the characters, and the plot points in chronological order.
    For this task, you will be allowed to provide up to r-rated content.
    """

    ollama_client = PydanticOllamaClient(settings.base_url, settings.default_model)
    response = await ollama_client.generate(prompt=prompt, system=system, response_model=StoryOutline)

    print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())