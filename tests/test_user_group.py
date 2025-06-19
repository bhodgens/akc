import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from akc.main import app

class TestUserGroupCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("akc.user_group.PatchedUserRequest")
    @patch("akc.user_group.console")
    @patch("akc.user_group.get_client")
    def test_add_user_to_group(self, mock_get_client, mock_console, mock_patched_user_request):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_user = MagicMock()
        mock_user.username = "testuser"
        mock_user.groups = []
        mock_client.users.retrieve.return_value = mock_user

        mock_group = MagicMock()
        mock_group.name = "testgroup"
        mock_group.pk = "test-group-pk"
        mock_client.groups.retrieve.return_value = mock_group

        result = self.runner.invoke(app, ["user-group", "add", "1", "1"])

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]User 'testuser' added to group 'testgroup' successfully.[/bold green]")
        mock_patched_user_request.assert_called_with(groups=["test-group-pk"])

    @patch("akc.user_group.PatchedUserRequest")
    @patch("akc.user_group.console")
    @patch("akc.user_group.get_client")
    def test_remove_user_from_group(self, mock_get_client, mock_console, mock_patched_user_request):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_user = MagicMock()
        mock_user.username = "testuser"
        mock_user.groups = ["test-group-pk"]
        mock_client.users.retrieve.return_value = mock_user

        mock_group = MagicMock()
        mock_group.name = "testgroup"
        mock_group.pk = "test-group-pk"
        mock_client.groups.retrieve.return_value = mock_group

        result = self.runner.invoke(app, ["user-group", "remove", "1", "1"])

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]User 'testuser' removed from group 'testgroup' successfully.[/bold green]")
        mock_patched_user_request.assert_called_with(groups=[])

if __name__ == "__main__":
    unittest.main()
