import asyncio

from relative_world_ollama.client import PydanticOllamaClient
from relative_world_ollama.settings import settings
from textworld.logs import init_logging
from textworld.models.stories import Story
from textworld.templating import render_template

init_logging()

async def main():
    prompt = "a time when things were okay"
    system = render_template("system_prompts/scenario.create.j2", response_model=Story)
    ollama_client = PydanticOllamaClient(settings.base_url, settings.default_model)
    response = await ollama_client.generate(prompt=prompt, system=system, response_model=Story)

    print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
