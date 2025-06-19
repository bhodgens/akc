import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from akc.main import app

class TestUserRoleCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("akc.user_role.PatchedUserRequest")
    @patch("akc.user_role.console")
    @patch("akc.user_role.get_client")
    def test_add_user_to_role(self, mock_get_client, mock_console, mock_patched_user_request):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_user = MagicMock()
        mock_user.username = "testuser"
        mock_user.roles = []
        mock_client.users.retrieve.return_value = mock_user

        mock_role = MagicMock()
        mock_role.name = "testrole"
        mock_role.pk = "test-role-pk"
        mock_client.roles.retrieve.return_value = mock_role

        result = self.runner.invoke(app, ["user-role", "add", "1", "1"])

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]Role 'testrole' added to user 'testuser' successfully.[/bold green]")
        mock_patched_user_request.assert_called_with(roles=["test-role-pk"])

    @patch("akc.user_role.PatchedUserRequest")
    @patch("akc.user_role.console")
    @patch("akc.user_role.get_client")
    def test_remove_user_from_role(self, mock_get_client, mock_console, mock_patched_user_request):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_user = MagicMock()
        mock_user.username = "testuser"
        mock_user.roles = ["test-role-pk"]
        mock_client.users.retrieve.return_value = mock_user

        mock_role = MagicMock()
        mock_role.name = "testrole"
        mock_role.pk = "test-role-pk"
        mock_client.roles.retrieve.return_value = mock_role

        result = self.runner.invoke(app, ["user-role", "remove", "1", "1"])

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]Role 'testrole' removed from user 'testuser' successfully.[/bold green]")
        mock_patched_user_request.assert_called_with(roles=[])

if __name__ == "__main__":
    unittest.main()
