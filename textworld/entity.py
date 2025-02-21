import logging

import orjson as json

from relative_world.entity import Entity, BoundEvent
from relative_world.event import Event
from relative_world_ollama.entity import OllamaEntity
from textworld.events import SaidAloudEvent, PerformedActionEvent
from textworld.models import RoleplayResponse, SummarizationResponse
from textworld.templating import render_template

chat_logger = logging.getLogger("chat")
thought_logger = logging.getLogger("thoughts")
action_logger = logging.getLogger("actions")


class RoleplayEntity(OllamaEntity):
    response_model = RoleplayResponse
    role_description: str = (
        "A roleplay entity that can engage in conversation and actions."
    )

    chat_color: str = "blue"
    thought_color: str = "dark_green"
    action_color: str = "green"

    _event_log: list[BoundEvent] = []
    _input_queue: list[BoundEvent] = []

    def get_prompt(self):
        if self._input_queue:
            input_queue, self._input_queue = self._input_queue, []
            prompt = "\n".join(
                f"{entity.name} :: {event}" for entity, event in input_queue
            )
            self._event_log.extend(input_queue)
        else:
            prompt = "<no one has spoken yet>"
        return prompt

    def get_system_prompt(self):
        context = {"entity": self, "response_model": self.response_model}

        if self._event_log:
            template_name = "system_prompts/conversation.continue.j2"
            context["event_log"] = self.render_event_log()
        else:
            template_name = "system_prompts/conversation.starter.j2"

        return render_template(template_name, **context)

    def render_event_log(self, include_queued=False):
        event_log = self._event_log[::]
        if include_queued:
            event_log = event_log + self._input_queue
        return json.dumps(
            [
                {
                    "entity": entity.model_dump(include={"id", "name"}),
                    "event": event.model_dump_json(),
                }
                for entity, event in event_log
            ]
        )

    def handle_event(self, entity: Entity, event: Event):
        self._input_queue.append((entity, event))

    def handle_response(self, response: RoleplayResponse):
        log_msg_template = "[{}]{}[/]"
        if response.response:
            self.emit_event(SaidAloudEvent(context={"message": response.response}))
            msg = log_msg_template.format(self.chat_color, "%s :: %s")
            chat_logger.info(msg, self.name, response.response, extra={"markup": True})

        if response.private_thought:
            msg = log_msg_template.format(self.thought_color, "%s :: %s")
            thought_logger.info(
                msg, self.name, response.private_thought, extra={"markup": True}
            )

        if response.action:
            self.emit_event(PerformedActionEvent(context={"action": response.action}))
            msg = log_msg_template.format(self.action_color, "%s :: %s")
            action_logger.info(
                msg, self.name, response.action, extra={"markup": True}
            )

        return super().handle_response(response)

    def summarize_conversation(self) -> SummarizationResponse:
        system_prompt = render_template(
            "system_prompts/conversation.summary.j2",
            entity=self,
            response_model=SummarizationResponse,
        )

        return self.ollama_client.generate(
            prompt=self.render_event_log(include_queued=True),
            system=system_prompt,
            response_model=SummarizationResponse,
        )
