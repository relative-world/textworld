# Relative World Ollama

This project extends the `relative-world` project by providing an interface to the 
Ollama API, allowing LLMs to generate and handle events.

## Installation

To install the project dependencies, use [Poetry](https://python-poetry.org/):

```sh
poetry install
```

## Running Tests

To run the tests, use:

```sh
poetry run pytest
```

## Core Classes

### Entity

The `Entity` class represents a core component in the system. It is designed to interact with the Ollama API to generate responses based on prompts. The `Entity` class includes methods for generating prompts, handling responses, and updating the entity state.

### Event

The `Event` class represents events that can be processed by entities. Events are used to trigger actions and handle responses within the system.

## Examples


it's not a guarantee, but it comes in handy when you're using shitty models.  
This is applied automatically by the `PydanticOllamaClient` as necessary.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
