import orjson

from relative_world_ollama.client import PydanticOllamaClient
from relative_world_ollama.settings import settings
from textworld.stories.models import StoryOutline, StoryActScene, StorySceneSequence, StoryChapter
from textworld.templating import render_template


async def _generate(prompt: str, template_path: str, response_model, **template_context):
    system = render_template(template_path, **template_context)
    ollama_client = PydanticOllamaClient(settings.base_url, settings.default_model)
    return await ollama_client.generate(prompt=prompt, system=system, response_model=response_model)


async def generate_outline(prompt: str):
    return await _generate(prompt, "stories/outline.j2", StoryOutline)


async def generate_scene(story_outline: StoryOutline, scene_title: str, reference_scenes: list[StoryActScene]):
    return await _generate(
        scene_title,
        "stories/scenes.j2",
        StorySceneSequence,
        story_outline=story_outline.model_dump_json(),
        reference_scenes=orjson.dumps([scene.model_dump() for scene in reference_scenes]),
    )

async def generate_novelization(scene: StoryActScene, story_outline: StoryOutline, existing_chapters: list[StoryChapter]):
    return await _generate(
        scene.model_dump_json(),
        "stories/scene.novelization.j2",
        StoryChapter,
        story_outline=story_outline.model_dump_json(),
        existing_chapters=orjson.dumps([chapter.model_dump() for chapter in existing_chapters]),
    )
#
# async def generate_characters():
#     story = load_story_from_asset("stories/golden_days/outline.json")
#     scenes = load_
#     system = render_template("system_prompts/../textworld/templates/stories/characters.j2")
#     ollama_client = PydanticOllamaClient(settings.base_url, settings.default_model)
#     response = await ollama_client.generate(prompt=story.model_dump_json(), system=system, response_model=SceneList)
#
#     print(response.model_dump_json(indent=2))
#
#
# async def generate_locations():
#     story = load_story_from_asset("stories/outline.json")
#     system = render_template("system_prompts/../textworld/templates/stories/locations.j2",
#                              response_model=SceneLocationList)
#     ollama_client = PydanticOllamaClient(settings.base_url, settings.default_model)
#     response = await ollama_client.generate(prompt=story.model_dump_json(), system=system,
#                                             response_model=SceneLocationList)
#
#     print(response.model_dump_json(indent=2))
