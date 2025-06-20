import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from akc.main import app


class TestPropertyMapping(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner(env={"NO_COLOR": "1"})

    @patch("akc.propertymapping.PropertymappingsApi")
    @patch("akc.propertymapping.get_client")
    def test_list_propertymappings(self, mock_get_client, mock_propertymappings_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_propertymapping = MagicMock()
        mock_propertymapping.pk = "test-uuid"
        mock_propertymapping.name = "test-name"
        mock_propertymapping.managed = "test-managed"
        mock_api_instance.propertymappings_all_list.return_value.results = [mock_propertymapping]
        mock_propertymappings_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["propertymapping", "list"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("test-uuid", result.stdout)
        self.assertIn("test-name", result.stdout)
        self.assertIn("test-managed", result.stdout)

    @patch("akc.propertymapping.PropertymappingsApi")
    @patch("akc.propertymapping.get_client")
    def test_get_propertymapping(self, mock_get_client, mock_propertymappings_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_propertymapping = MagicMock()
        mock_propertymapping.to_dict.return_value = {"pk": "test-uuid", "name": "test-name"}
        mock_api_instance.propertymappings_all_retrieve.return_value = mock_propertymapping
        mock_propertymappings_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["propertymapping", "get", "test-uuid"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("'pk': 'test-uuid'", result.stdout)
        self.assertIn("'name': 'test-name'", result.stdout)

    @patch("akc.propertymapping.PropertymappingsApi")
    @patch("akc.propertymapping.get_client")
    def test_delete_propertymapping(self, mock_get_client, mock_propertymappings_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_api_instance.propertymappings_all_destroy.return_value = None
        mock_propertymappings_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["propertymapping", "delete", "test-uuid"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("Property mapping 'test-uuid' deleted successfully.", result.stdout)
