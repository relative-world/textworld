from asyncio import run as aiorun

import typer

from textworld.io import get_assets_path, load_model_from_asset
from textworld.logs import init_logging
from textworld.stories.generate import generate_outline, generate_scene, generate_novelization
from textworld.stories.models import StoryOutline

app = typer.Typer()

init_logging()


@app.command()
def list(glob: str = typer.Argument("*")):
    print(f"Listing Stories matching: {glob}")
    for entry in (get_assets_path() / "stories").glob(glob):
        print(entry.name)


async def _create_outline(prompt):
    outline = await generate_outline(prompt)
    return outline


async def _create_story(prompt):
    outline = await _create_outline(prompt)
    print(outline.model_dump_json(indent=2))

    await _create_scenes(outline)


async def _create_scenes(outline: StoryOutline):
    defined_scenes = []
    for act in outline.acts:
        print("Act:", act.title)
        for act_num, scene in enumerate(act.scenes, 1):
            scene_title = f"{act.title} - Scene {act_num}: {scene}"
            print(scene_title)
            scene = await generate_scene(outline, scene_title, defined_scenes)
            defined_scenes.append(scene)
            print(scene.model_dump_json(indent=2))


async def _create_novel(prompt=None, outline_filename=None):
    if outline_filename:
        outline = load_model_from_asset(outline_filename, StoryOutline)
    elif prompt:
        outline = await _create_outline(prompt)
    else:
        raise ValueError("Either prompt or outline-filename must be provided")

    defined_scenes = []
    exiting_chapters = []
    print(outline.model_dump_json(indent=2))

    for act in outline.acts:
        # print("Act:", act.title)
        for scene_num, scene in enumerate(act.scenes, 1):
            scene_title = f"{act.title} - Scene {scene_num}: {scene}"
            scene = await generate_scene(outline, scene_title, defined_scenes)
            defined_scenes.append(scene)
            # print(scene.model_dump_json(indent=2))

            chapter = await generate_novelization(scene, outline, exiting_chapters)
            exiting_chapters.append(chapter)
            print(f"Chapter {scene_num}: {chapter.title}")
            print(chapter.text)

@app.command()
def write(prompt=None, outline_filename=None):
    aiorun(_create_novel(prompt, outline_filename))


@app.command()
def create(prompt):
    aiorun(_create_story(prompt))


@app.command()
def create_outline(prompt):
    outline = aiorun(_create_outline(prompt))
    print(outline.model_dump_json(indent=2))


def cli():
    app()
