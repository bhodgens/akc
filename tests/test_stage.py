import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from akc.main import app


class TestStage(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner(env={"NO_COLOR": "1"})

    @patch("akc.stage.StagesApi")
    @patch("akc.stage.get_client")
    def test_list_stages(self, mock_get_client, mock_stages_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_stage = MagicMock()
        mock_stage.pk = "test-uuid"
        mock_stage.name = "test-name"
        mock_stage.component = "test-component"
        mock_api_instance.stages_all_list.return_value.results = [mock_stage]
        mock_stages_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["stage", "list"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("test-uuid", result.stdout)
        self.assertIn("test-name", result.stdout)
        self.assertIn("test-component", result.stdout)

    @patch("akc.stage.StagesApi")
    @patch("akc.stage.get_client")
    def test_get_stage(self, mock_get_client, mock_stages_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_stage = MagicMock()
        mock_stage.to_dict.return_value = {"pk": "test-uuid", "name": "test-name"}
        mock_api_instance.stages_all_retrieve.return_value = mock_stage
        mock_stages_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["stage", "get", "test-uuid"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("'pk': 'test-uuid'", result.stdout)
        self.assertIn("'name': 'test-name'", result.stdout)

    @patch("akc.stage.StagesApi")
    @patch("akc.stage.get_client")
    def test_delete_stage(self, mock_get_client, mock_stages_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_api_instance.stages_all_destroy.return_value = None
        mock_stages_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["stage", "delete", "test-uuid"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("Stage 'test-uuid' deleted successfully.", result.stdout)
