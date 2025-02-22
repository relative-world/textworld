import logging

from relative_world.entity import Entity, BoundEvent
from relative_world.event import Event
from relative_world_ollama.entity import OllamaEntity
from textworld.models.events import SaidAloudEvent, PerformedActionEvent, ThoughtEvent
from textworld.models.responses import RoleplayResponse, SummarizationResponse
from textworld.templating import render_template

chat_logger = logging.getLogger("chat")
thought_logger = logging.getLogger("thoughts")
action_logger = logging.getLogger("actions")


class RoleplayEntity(OllamaEntity):
    """
    A roleplay entity capable of engaging in conversation and performing actions.

    Attributes:
        response_model: Model used for validating roleplay responses.
        role_description: Description defining the entity's role.
        chat_color: Color for chat logging.
        thought_color: Color for thought logging.
        action_color: Color for action logging.
        _event_log: List of bound events that have already been processed.
        _input_queue: Queue for incoming events pending processing.
    """
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
        """
        Generate a prompt based on the queued input events.

        Returns:
            str: A concatenated string of events from the input queue. If no events are queued,
                 returns a default prompt.
        """
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
        """
        Generate the system prompt using the current conversation context.

        Returns:
            str: The rendered system prompt template.
        """
        context = {"entity": self, "response_model": self.response_model}

        if self._event_log:
            template_name = "system_prompts/conversation.continue.j2"
            context["event_log"] = self.render_event_log()
        else:
            template_name = "system_prompts/conversation.starter.j2"

        return render_template(template_name, **context)

    def render_event_log(self, include_queued=False):
        """
        Render the event log into a human-readable string.

        Args:
            include_queued (bool): Whether to include queued events in the log rendering.

        Returns:
            str: The rendered event log.
        """
        event_log = self._event_log[::]
        if include_queued:
            event_log = event_log + self._input_queue

        output = []
        for entity, event in event_log:
            if entity is self:
                entity_name = "You"
            else:
                entity_name = entity.name

            if isinstance(event, SaidAloudEvent):
                str_event = f"{entity_name} said {event.message}"
            elif isinstance(event, ThoughtEvent):
                str_event = f"{entity_name} thought {event.thought}"
            elif isinstance(event, PerformedActionEvent):
                str_event = f"{entity_name} performed this action: {event.action}"
            else:
                continue

            output.append(str_event)

        return "\n".join(output)

    async def handle_event(self, entity: Entity, event: Event):
        """
        Process an incoming event from a given entity without mind reading.

        Args:
            entity (Entity): The entity generating the event.
            event (Event): The event to be processed.
        """
        # no mind reading (by default)
        if isinstance(event, ThoughtEvent):
            if entity is not self:
                return
        self._input_queue.append((entity, event))

    async def handle_response(self, response: RoleplayResponse):
        """
        Handle a roleplay response by emitting the corresponding events and logging them.

        Args:
            response (RoleplayResponse): The response object containing spoken words, thoughts,
                                           and/or actions.
        """
        log_msg_template = "[{}]{}[/]"
        if response.response:
            self.emit_event(SaidAloudEvent(message=response.response))
            msg = log_msg_template.format(self.chat_color, "%s :: %s")
            chat_logger.info(msg, self.name, response.response, extra={"markup": True})

        if response.private_thought:
            self.emit_event(ThoughtEvent(thought=response.private_thought))
            msg = log_msg_template.format(self.thought_color, "%s :: %s")
            thought_logger.info(
                msg, self.name, response.private_thought, extra={"markup": True}
            )

        if response.action:
            self.emit_event(PerformedActionEvent(action=response.action))
            msg = log_msg_template.format(self.action_color, "%s :: %s")
            action_logger.info(
                msg, self.name, response.action, extra={"markup": True}
            )

        return await super().handle_response(response)

    async def summarize_conversation(self) -> SummarizationResponse:
        """
        Generate a summarization of the conversation based on the event log.

        Returns:
            SummarizationResponse: An object containing the conversation summary, tags,
                                   participants, and location details.
        """
        system_prompt = render_template(
            "system_prompts/conversation.summary.j2",
            entity=self,
            response_model=SummarizationResponse,
        )

        return await self.ollama_client.generate(
            prompt=self.render_event_log(include_queued=True),
            system=system_prompt,
            response_model=SummarizationResponse,
        )
