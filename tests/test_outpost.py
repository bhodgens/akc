import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from akc.main import app


class TestOutpost(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner(env={"NO_COLOR": "1"})

    @patch("akc.outpost.OutpostsApi")
    @patch("akc.outpost.get_client")
    def test_list_outposts(self, mock_get_client, mock_outposts_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_outpost = MagicMock()
        mock_outpost.pk = "test-uuid"
        mock_outpost.name = "test-name"
        mock_outpost.type = "proxy"
        mock_outpost.service_connection_name = "test-connection"
        mock_api_instance.outposts_instances_list.return_value.results = [mock_outpost]
        mock_outposts_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["outpost", "list"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("test-uuid", result.stdout)
        self.assertIn("test-name", result.stdout)
        self.assertIn("proxy", result.stdout)
        self.assertIn("test-connection", result.stdout)

    @patch("akc.outpost.OutpostsApi")
    @patch("akc.outpost.get_client")
    def test_get_outpost(self, mock_get_client, mock_outposts_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_outpost = MagicMock()
        mock_outpost.to_dict.return_value = {"pk": "test-uuid", "name": "test-name"}
        mock_api_instance.outposts_instances_retrieve.return_value = mock_outpost
        mock_outposts_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["outpost", "get", "test-uuid"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("'pk': 'test-uuid'", result.stdout)
        self.assertIn("'name': 'test-name'", result.stdout)

    @patch("akc.outpost.OutpostsApi")
    @patch("akc.outpost.get_client")
    def test_delete_outpost(self, mock_get_client, mock_outposts_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_api_instance.outposts_instances_destroy.return_value = None
        mock_outposts_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["outpost", "delete", "test-uuid"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("Outpost 'test-uuid' deleted successfully.", result.stdout)

    @patch("akc.outpost.OutpostsApi")
    @patch("akc.outpost.get_client")
    def test_health_outpost(self, mock_get_client, mock_outposts_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_health = MagicMock()
        mock_health.to_dict.return_value = {"version": "test-version"}
        mock_api_instance.outposts_instances_health_list.return_value = [mock_health]
        mock_outposts_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["outpost", "health", "test-uuid"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("'version': 'test-version'", result.stdout)
