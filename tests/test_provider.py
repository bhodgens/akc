import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from akc.main import app

class TestProviderCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("akc.provider.console")
    @patch("akc.provider.get_client")
    def test_list_providers(self, mock_get_client, mock_console):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        provider1 = MagicMock()
        provider1.id = 1
        provider1.name = "provider1"
        provider1.authorization_flow = MagicMock()
        provider1.authorization_flow.name = "flow1"

        provider2 = MagicMock()
        provider2.id = 2
        provider2.name = "provider2"
        provider2.authorization_flow = MagicMock()
        provider2.authorization_flow.name = "flow2"

        mock_client.providers.list.return_value = [provider1, provider2]

        result = self.runner.invoke(app, ["provider", "list"])

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called()

    @patch("akc.provider.console")
    @patch("akc.provider.get_client")
    def test_delete_provider(self, mock_get_client, mock_console):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(app, ["provider", "delete", "1"])

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]Provider with ID 1 deleted successfully.[/bold green]")

    @patch("akc.provider.PatchedProxyProviderRequest")
    @patch("akc.provider.console")
    @patch("akc.provider.get_client")
    def test_update_provider(self, mock_get_client, mock_console, mock_patched_provider_request):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        updated_provider = MagicMock()
        updated_provider.name = "new-provider-name"
        updated_provider.id = 1
        mock_client.providers.partial_update.return_value = updated_provider

        result = self.runner.invoke(
            app, ["provider", "update", "1", "--name", "new-provider-name"]
        )

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with(
            f"[bold green]Provider 'new-provider-name' (ID: 1) updated successfully.[/bold green]"
        )
        mock_patched_provider_request.assert_called_with(name="new-provider-name")

    @patch("akc.provider.ProxyProviderRequest")
    @patch("akc.provider.console")
    @patch("akc.provider.get_client")
    def test_create_proxy_provider(self, mock_get_client, mock_console, mock_proxy_provider_request):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        new_provider = MagicMock()
        new_provider.name = "new-proxy-provider"
        mock_client.providers.proxy_create.return_value = new_provider

        result = self.runner.invoke(
            app, ["provider", "create-proxy", "new-proxy-provider", "flow-uuid", "https://external.host"]
        )

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with(
            f"[bold green]Proxy provider 'new-proxy-provider' created successfully.[/bold green]"
        )
        mock_proxy_provider_request.assert_called_with(
            name="new-proxy-provider",
            authorization_flow="flow-uuid",
            external_host="https://external.host"
        )
