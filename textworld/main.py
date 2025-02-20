import logging.config
from typing import Annotated

from pydantic import BaseModel, Field

from relative_world.entity import Entity
from relative_world.event import Event, BoundEvent
from relative_world_ollama.entity import OllamaEntity
from textworld.events import PerformedActionEvent, SaidAloudEvent
from textworld.logs import init_logging
from textworld.templating import render_template

init_logging()

chat_logger = logging.getLogger("chat")
thought_logger = logging.getLogger("thoughts")
action_logger = logging.getLogger("actions")


class RoleplayResponse(BaseModel):
    response: Annotated[str, Field(description="Something you are saying aloud.")]
    private_thought: Annotated[
        str | None, Field(description="Your private thoughts in the moment.")
    ] = None
    action: Annotated[
        str | None, Field(description="A description of actions you are performing.")
    ] = None


class SummarizationResponse(BaseModel):
    summary: Annotated[str, Field(description="The summary of the conversation.")]
    tags: Annotated[list[str], Field(description="Tags for the conversation.")]
    participants: Annotated[list[str], Field(description="The participants in the conversation.")]


class RoleplayEntity(OllamaEntity):
    response_model = RoleplayResponse
    _event_log: list[BoundEvent] = []
    _input_queue: list[BoundEvent] = []

    def get_prompt(self):
        if self._input_queue:
            input_queue, self._input_queue = self._input_queue, []
            return "\n".join(
                f"{entity.name} :: {event}" for entity, event in input_queue
            )
        else:
            return "<no one has spoken yet>"

    def get_system_prompt(self):
        context = {"entity": self, "response_model": self.response_model}

        if self._event_log:
            template_name = "system_prompts/conversation.continue.j2"
            context["event_log"] = self.render_event_log()
        else:
            template_name = "system_prompts/conversation.starter.j2"

        return render_template(template_name, **context)

    def render_event_log(self):
        return "\n".join(
            f"{entity.name} :: {event}" for entity, event in self._event_log
        )

    def handle_event(self, entity: Entity, event: Event):
        self._input_queue.append((entity, event))

    def handle_response(self, response: RoleplayResponse):
        if response.response:
            self.emit_event(SaidAloudEvent(context={"message": response.response}))
            chat_logger.info("%s :: %s", self.name, response.response)

        if response.private_thought:
            thought_logger.info("%s :: %s", self.name, response.private_thought)

        if response.action:
            self.emit_event(PerformedActionEvent(context={"action": response.action}))
            action_logger.info("%s :: %s", self.name, response.action)

        return super().handle_response(response)

    def summarize_conversation(self) -> SummarizationResponse:
        system_prompt = render_template(
            "system_prompts/conversation.summary.j2",
            entity=self,
            response_model=SummarizationResponse,
            event_log=self.render_event_log(),

        )

        return self.ollama_client.generate(
            prompt=self.render_event_log(),
            system=system_prompt,
            response_model=SummarizationResponse
        )


if __name__ == "__main__":
    import random
    from relative_world.world import RelativeWorld

    # number of time steps to evaluate
    timesteps = 1

    actors = [
        RoleplayEntity(name="Alice"),
        RoleplayEntity(name="Bob"),
        RoleplayEntity(name="Charlie"),
    ]

    random.shuffle(actors)

    world = RelativeWorld(children=actors)

    for _ in range(timesteps):
        list(world.update())

    # print conversation summaries
    print()
    for actor in actors:
        print("Conversation summary for", actor.name)
        print(actor.summarize_conversation())
        print("=" * 40)
