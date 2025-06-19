import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from akc.main import app

class TestUserCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("akc.user.User")
    @patch("akc.user.console")
    @patch("akc.user.get_client")
    def test_create_user(self, mock_get_client, mock_console, mock_user_model):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_user = MagicMock()
        mock_user.username = "testuser"
        mock_client.users.create.return_value = mock_user

        result = self.runner.invoke(
            app,
            ["user", "create", "testuser", "test@test.com"],
        )

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]User 'testuser' created successfully.[/bold green]")

    @patch("akc.user.console")
    @patch("akc.user.get_client")
    def test_list_users(self, mock_get_client, mock_console):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        user1 = MagicMock()
        user1.id = 1
        user1.username = "user1"
        user1.email = "user1@test.com"
        user1.is_active = True
        user1.is_superuser = False

        user2 = MagicMock()
        user2.id = 2
        user2.username = "user2"
        user2.email = "user2@test.com"
        user2.is_active = False
        user2.is_superuser = True

        mock_client.users.list.return_value = [user1, user2]

        result = self.runner.invoke(app, ["user", "list"])

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called()

    @patch("akc.user.console")
    @patch("akc.user.get_client")
    def test_update_user(self, mock_get_client, mock_console):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        retrieved_user = MagicMock()
        mock_client.users.retrieve.return_value = retrieved_user

        updated_user = MagicMock()
        updated_user.username = "newname"
        updated_user.id = 1
        mock_client.users.update.return_value = updated_user

        result = self.runner.invoke(
            app, ["user", "update", "1", "--username", "newname"]
        )

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]User 'newname' (ID: 1) updated successfully.[/bold green]")

    @patch("akc.user.console")
    @patch("akc.user.get_client")
    def test_delete_user(self, mock_get_client, mock_console):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(app, ["user", "delete", "1"])

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]User with ID 1 deleted successfully.[/bold green]")

if __name__ == "__main__":
    unittest.main()
