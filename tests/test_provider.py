import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from akc.main import app
from rich.console import Console
from authentik_client.models.provider import Provider
from authentik_client.models.paginated_provider_list import PaginatedProviderList
from authentik_client.models.proxy_provider_request import ProxyProviderRequest
from authentik_client.models.patched_proxy_provider_request import PatchedProxyProviderRequest

class TestProviderCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        app.console = Console(force_terminal=False)

    @patch("akc.provider.ProvidersApi")
    def test_list_providers(self, MockProvidersApi):
        mock_api = MockProvidersApi.return_value
        provider1 = Provider(pk="provider1-pk", name="provider1", authorization_flow=MagicMock(name="flow1"))
        provider2 = Provider(pk="provider2-pk", name="provider2", authorization_flow=MagicMock(name="flow2"))
        mock_api.providers_list.return_value = PaginatedProviderList(results=[provider1, provider2])

        result = self.runner.invoke(app, ["provider", "list"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("provider1-pk", result.stdout)
        self.assertIn("provider2-pk", result.stdout)

    @patch("akc.provider.ProvidersApi")
    def test_delete_provider(self, MockProvidersApi):
        mock_api = MockProvidersApi.return_value

        result = self.runner.invoke(app, ["provider", "delete", "provider-pk"])

        self.assertEqual(result.exit_code, 0)
        mock_api.providers_destroy.assert_called_with(provider_pk="provider-pk")
        self.assertIn("Provider with ID provider-pk deleted successfully.", result.stdout)

    @patch("akc.provider.ProvidersApi")
    def test_update_provider(self, MockProvidersApi):
        mock_api = MockProvidersApi.return_value
        updated_provider = Provider(pk="provider-pk", name="new-provider-name")
        mock_api.providers_partial_update.return_value = updated_provider

        result = self.runner.invoke(
            app, ["provider", "update", "provider-pk", "--name", "new-provider-name"]
        )

        self.assertEqual(result.exit_code, 0)
        mock_api.providers_partial_update.assert_called_with(
            provider_pk="provider-pk",
            patched_proxy_provider_request=PatchedProxyProviderRequest(name="new-provider-name")
        )
        self.assertIn("Provider 'new-provider-name' (ID: provider-pk) updated successfully.", result.stdout)

    @patch("akc.provider.ProvidersApi")
    def test_create_proxy_provider(self, MockProvidersApi):
        mock_api = MockProvidersApi.return_value
        new_provider = Provider(name="new-proxy-provider")
        mock_api.providers_proxy_create.return_value = new_provider

        result = self.runner.invoke(
            app, ["provider", "create-proxy", "new-proxy-provider", "flow-uuid", "https://external.host"]
        )

        self.assertEqual(result.exit_code, 0)
        mock_api.providers_proxy_create.assert_called_with(
            proxy_provider_request=ProxyProviderRequest(
                name="new-proxy-provider",
                authorization_flow="flow-uuid",
                external_host="https://external.host"
            )
        )
        self.assertIn("Proxy provider 'new-proxy-provider' created successfully.", result.stdout)
