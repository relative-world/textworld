from pydantic import BaseModel

from textworld.ai.ollama import OllamaClient, fix_json_response
from textworld.settings import settings

if __name__ == "__main__":

    class Foo(BaseModel):
        title: str
        description: str

    ollama_client = OllamaClient(
        base_url=settings.ollama_base_url, model=settings.ollama_model
    )
    bad_json = "{'title': 'hello there', 'desc': 'an example of a bad json object'}"
    output = fix_json_response(ollama_client, bad_json, response_model=Foo)
    print(output)
