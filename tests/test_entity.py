import unittest
from unittest.mock import patch

from textworld.models.entity import RoleplayEntity
from textworld.models.events import SaidAloudEvent, ThoughtEvent
from textworld.models.responses import SummarizationResponse


class DummyEntity:
    def __init__(self, name):
        self.name = name


class DummyOllamaClient:
    def generate(self, prompt, system, response_model):
        # return a dummy summarization response.
        return response_model(summary="Test summary", tags=["test"], participants=["Tester"], location="Test location")


class TestRoleplayEntity(unittest.TestCase):
    def setUp(self):
        self.entity = RoleplayEntity()
        # Set a simple name for testing string outputs.
        self.entity.name = "Tester"
        # Assign a dummy ollama_client needed for summarize_conversation.
        self.entity.ollama_client = DummyOllamaClient()

    def test_get_prompt_empty(self):
        # When the input queue is empty, get_prompt should return the default prompt.
        self.entity._input_queue = []
        prompt = self.entity.get_prompt()
        self.assertEqual(prompt, "<no one has spoken yet>")

    def test_get_prompt_with_events(self):
        # Add an event to _input_queue and verify that get_prompt processes it.
        event = SaidAloudEvent(message="Hello")
        # Using a dummy entity with a name that is not self.
        dummy = DummyEntity("Dummy")
        self.entity._input_queue = [(dummy, event)]
        prompt = self.entity.get_prompt()
        # Check that the prompt contains the dummy's name and event string.
        self.assertIn("Dummy ::", prompt)
        self.assertIn("Hello", prompt)
        # Verify _input_queue is now empty and the event is stored in _event_log.
        self.assertEqual(len(self.entity._input_queue), 0)
        self.assertGreater(len(self.entity._event_log), 0)

    @patch('textworld.models.entity.render_template')
    def test_get_system_prompt_starter(self, mock_render):
        # When there is no _event_log, the starter template should be used.
        self.entity._event_log = []
        mock_render.return_value = "starter prompt"
        system_prompt = self.entity.get_system_prompt()
        mock_render.assert_called_with("system_prompts/conversation.starter.j2", entity=self.entity,
                                       response_model=self.entity.response_model)
        self.assertEqual(system_prompt, "starter prompt")

    @patch('textworld.models.entity.render_template')
    def test_get_system_prompt_continue(self, mock_render):
        # When there are events in _event_log, the continue template should be used.
        event = SaidAloudEvent(message="Hi")
        self.entity._event_log = [(self.entity, event)]
        mock_render.return_value = "continue prompt"
        system_prompt = self.entity.get_system_prompt()
        mock_render.assert_called_with("system_prompts/conversation.continue.j2", entity=self.entity,
                                       response_model=self.entity.response_model,
                                       event_log=self.entity.render_event_log())
        self.assertEqual(system_prompt, "continue prompt")

    def test_render_event_log(self):
        # Test rendering the event log with a SaidAloudEvent.
        dummy = DummyEntity("Dummy")
        event = SaidAloudEvent(message="Test message")
        self.entity._event_log = [(dummy, event)]
        log_output = self.entity.render_event_log()
        # Check that the output contains dummy's name and the message.
        self.assertIn("Dummy said", log_output)
        self.assertIn("Test message", log_output)

    def test_handle_event(self):
        # Test that handle_event for ThoughtEvent from a non-self entity does not add the event.
        dummy = DummyEntity("Dummy")
        event = ThoughtEvent(thought="Secret")
        initial_queue_length = len(self.entity._input_queue)
        self.entity.handle_event(dummy, event)
        self.assertEqual(len(self.entity._input_queue), initial_queue_length)

        # Now test that events from self are added even if they are ThoughtEvent.
        self.entity.handle_event(self.entity, event)
        self.assertEqual(len(self.entity._input_queue), initial_queue_length + 1)

    @patch('textworld.models.entity.render_template')
    def test_summarize_conversation(self, mock_render):
        # Test that summarize_conversation returns a SummarizationResponse.
        # Prepare the event log.
        dummy = DummyEntity("Dummy")
        event = SaidAloudEvent(message="Hello")
        self.entity._event_log = [(dummy, event)]
        # Patch render_template to return a dummy system prompt.
        mock_render.return_value = "summary system prompt"
        # Call summarize_conversation.
        summary = self.entity.summarize_conversation()
        # Check that the returned object is a SummarizationResponse with expected attributes.
        self.assertIsInstance(summary, SummarizationResponse)
        self.assertEqual(summary.summary, "Test summary")
        self.assertEqual(summary.tags, ["test"])
        self.assertEqual(summary.participants, ["Tester"])
        self.assertEqual(summary.location, "Test location")


if __name__ == '__main__':
    unittest.main()
