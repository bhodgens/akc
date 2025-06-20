import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from akc.main import app


class TestPolicy(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner(env={"NO_COLOR": "1"})

    @patch("akc.policy.PoliciesApi")
    @patch("akc.policy.get_client")
    def test_list_policies(self, mock_get_client, mock_policies_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_policy = MagicMock()
        mock_policy.pk = "test-uuid"
        mock_policy.name = "test-name"
        mock_policy.component = "test-component"
        mock_policy.bound_to = "test-bound"
        mock_api_instance.policies_all_list.return_value.results = [mock_policy]
        mock_policies_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["policy", "list"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("test-uuid", result.stdout)
        self.assertIn("test-name", result.stdout)
        self.assertIn("test-component", result.stdout)
        self.assertIn("test-bound", result.stdout)

    @patch("akc.policy.PoliciesApi")
    @patch("akc.policy.get_client")
    def test_get_policy(self, mock_get_client, mock_policies_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_policy = MagicMock()
        mock_policy.to_dict.return_value = {"pk": "test-uuid", "name": "test-name"}
        mock_api_instance.policies_all_retrieve.return_value = mock_policy
        mock_policies_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["policy", "get", "test-uuid"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("'pk': 'test-uuid'", result.stdout)
        self.assertIn("'name': 'test-name'", result.stdout)

    @patch("akc.policy.PoliciesApi")
    @patch("akc.policy.get_client")
    def test_delete_policy(self, mock_get_client, mock_policies_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_api_instance.policies_all_destroy.return_value = None
        mock_policies_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["policy", "delete", "test-uuid"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("Policy 'test-uuid' deleted successfully.", result.stdout)
