import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from akc.main import app


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner(env={"NO_COLOR": "1"})

    @patch("akc.event.EventsApi")
    @patch("akc.event.get_client")
    def test_list_events(self, mock_get_client, mock_events_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_event = MagicMock()
        mock_event.pk = "test-uuid"
        mock_event.user = {"username": "test-user"}
        mock_event.action = "login"
        mock_event.app = "test-app"
        mock_event.created = "2025-06-19T12:00:00Z"
        mock_api_instance.events_events_list.return_value.results = [mock_event]
        mock_events_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["event", "list"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("test-uuid", result.stdout)
        self.assertIn("test-user", result.stdout)
        self.assertIn("login", result.stdout)
        self.assertIn("test-app", result.stdout)

    @patch("akc.event.EventsApi")
    @patch("akc.event.get_client")
    def test_get_event(self, mock_get_client, mock_events_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_event = MagicMock()
        mock_event.to_dict.return_value = {"pk": "test-uuid", "action": "login"}
        mock_api_instance.events_events_retrieve.return_value = mock_event
        mock_events_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["event", "get", "test-uuid"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("'pk': 'test-uuid'", result.stdout)
        self.assertIn("'action': 'login'", result.stdout)
