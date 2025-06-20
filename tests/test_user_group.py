import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from akc.main import app
from rich.console import Console
from authentik_client.models.user import User
from authentik_client.models.group import Group
from authentik_client.models.patched_user_request import PatchedUserRequest

class TestUserGroupCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        app.console = Console(force_terminal=False)

    @patch("akc.user_group.get_client")
    def test_add_user_to_group(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_user = User(pk="user-pk", username="testuser", groups=[])
        mock_client.users.retrieve.return_value = mock_user

        mock_group = Group(pk="group-pk", name="testgroup")
        mock_client.groups.retrieve.return_value = mock_group

        result = self.runner.invoke(app, ["user-group", "add", "user-pk", "group-pk"])

        self.assertEqual(result.exit_code, 0)
        mock_client.users.partial_update.assert_called_with(
            "user-pk",
            patched_user_request=PatchedUserRequest(groups=["group-pk"])
        )
        self.assertIn("User 'testuser' added to group 'testgroup' successfully.", result.stdout)

    @patch("akc.user_group.get_client")
    def test_remove_user_from_group(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_user = User(pk="user-pk", username="testuser", groups=["group-pk"])
        mock_client.users.retrieve.return_value = mock_user

        mock_group = Group(pk="group-pk", name="testgroup")
        mock_client.groups.retrieve.return_value = mock_group

        result = self.runner.invoke(app, ["user-group", "remove", "user-pk", "group-pk"])

        self.assertEqual(result.exit_code, 0)
        mock_client.users.partial_update.assert_called_with(
            "user-pk",
            patched_user_request=PatchedUserRequest(groups=[])
        )
        self.assertIn("User 'testuser' removed from group 'testgroup' successfully.", result.stdout)

if __name__ == "__main__":
    unittest.main()
