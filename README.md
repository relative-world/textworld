# textworld

textworld is a Python simulation demonstrating how to use Relative World and ollama to enable realtime conversations between AI entities. In this project, AI entities hold conversations and remember previous exchanges so they can participate in dynamic storytelling activities.

## Overview

textworld extends the core functionalities of relative world by integrating the Ollama API. It allows you to:

- Simulate realtime conversations between AI-driven entities.
- Persist conversations so entities have memory of past events.
- Perform storytelling activities within a dynamic simulation world.

## Installation

The project uses [Poetry](https://python-poetry.org/) for dependency management. Install the project dependencies by running:

```sh
poetry install
```

## Running Tests

Tests are implemented using [pytest](https://docs.pytest.org/). To run the test suite, execute:

```sh
poetry run pytest
```

## Usage

The main simulation example is defined in the `textworld/main.py` file. In this example, a scenario is loaded and used as the basis for conversation between AI entities. Each entity interacts via events handled by the underlying relative world framework.

To run the simulation example:

```sh
poetry run python textworld/main.py
```

## How It Works

- **Entities and Events:**  
  Entities represent AI participants in the simulation. Each entity is capable of generating and processing events. The events (such as spoken dialogue, actions, and thoughts) create an evolving narrative.

- **Relative World:**  
  The simulation world is managed by relative world, a framework that applies time-stepped updates to simulate dynamic interactions. Events propagate through the world, allowing for coordinated conversations between entities.

- **Ollama Integration:**  
  The ollama integration enables AI-driven responses. With the memory of previous events, entities can generate coherent responses and build stories over time.

## Contributing

Contributions are welcome. Please use pull requests to submit improvements and bug fixes.

## License

This project is licensed under the MIT License.
