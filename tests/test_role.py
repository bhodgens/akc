import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from akc.main import app

class TestRoleCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("akc.role.Role")
    @patch("akc.role.console")
    @patch("akc.role.get_client")
    def test_create_role(self, mock_get_client, mock_console, mock_role_model):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_role = MagicMock()
        mock_role.name = "testrole"
        mock_client.roles.create.return_value = mock_role

        result = self.runner.invoke(
            app,
            ["role", "create", "testrole"],
        )

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]Role 'testrole' created successfully.[/bold green]")

    @patch("akc.role.console")
    @patch("akc.role.get_client")
    def test_list_roles(self, mock_get_client, mock_console):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        role1 = MagicMock()
        role1.id = 1
        role1.name = "role1"

        role2 = MagicMock()
        role2.id = 2
        role2.name = "role2"

        mock_client.roles.list.return_value = [role1, role2]

        result = self.runner.invoke(app, ["role", "list"])

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called()

    @patch("akc.role.console")
    @patch("akc.role.get_client")
    def test_update_role(self, mock_get_client, mock_console):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        retrieved_role = MagicMock()
        mock_client.roles.retrieve.return_value = retrieved_role

        updated_role = MagicMock()
        updated_role.name = "newrolename"
        updated_role.id = 1
        mock_client.roles.update.return_value = updated_role

        result = self.runner.invoke(
            app, ["role", "update", "1", "--name", "newrolename"]
        )

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]Role 'newrolename' (ID: 1) updated successfully.[/bold green]")

    @patch("akc.role.console")
    @patch("akc.role.get_client")
    def test_delete_role(self, mock_get_client, mock_console):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(app, ["role", "delete", "1"])

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]Role with ID 1 deleted successfully.[/bold green]")

if __name__ == "__main__":
    unittest.main()
