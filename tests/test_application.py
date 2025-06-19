import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from akc.main import app

class TestApplicationCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("akc.application.Application")
    @patch("akc.application.console")
    @patch("akc.application.get_client")
    def test_create_application(self, mock_get_client, mock_console, mock_application_model):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_app = MagicMock()
        mock_app.name = "testapp"
        mock_client.applications.create.return_value = mock_app

        result = self.runner.invoke(
            app,
            ["application", "create", "testapp", "testapp"],
        )

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]Application 'testapp' created successfully.[/bold green]")

    @patch("akc.application.console")
    @patch("akc.application.get_client")
    def test_list_applications(self, mock_get_client, mock_console):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        app1 = MagicMock()
        app1.id = 1
        app1.name = "app1"
        app1.slug = "app1"
        app1.type = "native"

        app2 = MagicMock()
        app2.id = 2
        app2.name = "app2"
        app2.slug = "app2"
        app2.type = "saml"

        mock_client.applications.list.return_value = [app1, app2]

        result = self.runner.invoke(app, ["application", "list"])

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called()


    @patch("akc.application.console")
    @patch("akc.application.get_client")
    def test_update_application(self, mock_get_client, mock_console):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        retrieved_app = MagicMock()
        mock_client.applications.retrieve.return_value = retrieved_app

        updated_app = MagicMock()
        updated_app.name = "newappname"
        updated_app.id = 1
        mock_client.applications.update.return_value = updated_app

        result = self.runner.invoke(
            app, ["application", "update", "1", "--name", "newappname", "--slug", "newappslug"]
        )

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]Application 'newappname' (ID: 1) updated successfully.[/bold green]")

    @patch("akc.application.console")
    @patch("akc.application.get_client")
    def test_delete_application(self, mock_get_client, mock_console):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(app, ["application", "delete", "1"])

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]Application with ID 1 deleted successfully.[/bold green]")
