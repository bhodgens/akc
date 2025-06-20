import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from akc.main import app


class TestCore(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner(env={"NO_COLOR": "1"})

    @patch("akc.core.CoreApi")
    @patch("akc.core.get_client")
    def test_get_version(self, mock_get_client, mock_core_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_api_instance.core_version_retrieve.return_value.to_dict.return_value = {
            "version": "test-version",
            "build_hash": "test-hash",
        }
        mock_core_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["core", "get-version"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("'version': 'test-version'", result.stdout)
        self.assertIn("'build_hash': 'test-hash'", result.stdout)

    @patch("akc.core.CoreApi")
    @patch("akc.core.get_client")
    def test_list_tenants(self, mock_get_client, mock_core_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_tenant = MagicMock()
        mock_tenant.tenant_uuid = "test-uuid"
        mock_tenant.schema_name = "test-schema"
        mock_tenant.name = "test-name"
        mock_tenant.domain = "test-domain"
        mock_api_instance.core_tenants_list.return_value.results = [mock_tenant]
        mock_core_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["core", "list-tenants"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("test-uuid", result.stdout)
        self.assertIn("test-schema", result.stdout)
        self.assertIn("test-name", result.stdout)
        self.assertIn("test-domain", result.stdout)

    @patch("akc.core.CoreApi")
    @patch("akc.core.get_client")
    def test_create_tenant(self, mock_get_client, mock_core_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_new_tenant = MagicMock()
        mock_new_tenant.name = "new-tenant"
        mock_new_tenant.to_dict.return_value = {"name": "new-tenant"}
        mock_api_instance.core_tenants_create.return_value = mock_new_tenant
        mock_core_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["core", "create-tenant", "new-schema", "--name", "new-tenant"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("Tenant 'new-tenant' created successfully.", result.stdout)

    @patch("akc.core.CoreApi")
    @patch("akc.core.get_client")
    def test_get_tenant(self, mock_get_client, mock_core_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_tenant = MagicMock()
        mock_tenant.to_dict.return_value = {"tenant_uuid": "test-uuid", "name": "test-name"}
        mock_api_instance.core_tenants_retrieve.return_value = mock_tenant
        mock_core_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["core", "get-tenant", "test-uuid"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("'tenant_uuid': 'test-uuid'", result.stdout)
        self.assertIn("'name': 'test-name'", result.stdout)

    @patch("akc.core.CoreApi")
    @patch("akc.core.get_client")
    def test_delete_tenant(self, mock_get_client, mock_core_api_class):
        mock_get_client.return_value = MagicMock()
        mock_api_instance = MagicMock()
        mock_api_instance.core_tenants_destroy.return_value = None
        mock_core_api_class.return_value = mock_api_instance

        result = self.runner.invoke(app, ["core", "delete-tenant", "test-uuid"])

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertIn("Tenant with UUID 'test-uuid' deleted successfully.", result.stdout)


if __name__ == "__main__":
    unittest.main()
