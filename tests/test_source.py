import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from akc.main import app


class TestSource(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner(env={"NO_COLOR": "1"})

    @patch("akc.source.SourcesApi")
    @patch("akc.source.get_client")
    def test_list_sources(self, mock_get_client, mock_sources_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_source = MagicMock()
        mock_source.pk = "test-uuid"
        mock_source.name = "test-name"
        mock_source.slug = "test-slug"
        mock_source.enabled = True
        mock_api_instance.sources_all_list.return_value.results = [mock_source]
        mock_sources_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["source", "list"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("test-uuid", result.stdout)
        self.assertIn("test-name", result.stdout)
        self.assertIn("test-slug", result.stdout)
        self.assertIn("True", result.stdout)

    @patch("akc.source.SourcesApi")
    @patch("akc.source.get_client")
    def test_get_source(self, mock_get_client, mock_sources_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_source = MagicMock()
        mock_source.to_dict.return_value = {"pk": "test-uuid", "name": "test-name"}
        mock_api_instance.sources_all_retrieve.return_value = mock_source
        mock_sources_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["source", "get", "test-slug"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("'pk': 'test-uuid'", result.stdout)
        self.assertIn("'name': 'test-name'", result.stdout)

    @patch("akc.source.SourcesApi")
    @patch("akc.source.get_client")
    def test_delete_source(self, mock_get_client, mock_sources_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_api_instance.sources_all_destroy.return_value = None
        mock_sources_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["source", "delete", "test-slug"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("Source 'test-slug' deleted successfully.", result.stdout)
