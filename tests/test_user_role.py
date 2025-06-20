import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from akc.main import app
from rich.console import Console
from authentik_client.models.user import User
from authentik_client.models.role import Role
from authentik_client.models.patched_user_request import PatchedUserRequest

class TestUserRoleCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        app.console = Console(force_terminal=False)

    @patch("akc.user_role.get_client")
    def test_add_user_to_role(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_user = User(pk="user-pk", username="testuser", roles=[])
        mock_client.users.retrieve.return_value = mock_user

        mock_role = Role(pk="role-pk", name="testrole")
        mock_client.roles.retrieve.return_value = mock_role

        result = self.runner.invoke(app, ["user-role", "add", "user-pk", "role-pk"])

        self.assertEqual(result.exit_code, 0)
        mock_client.users.partial_update.assert_called_with(
            "user-pk",
            patched_user_request=PatchedUserRequest(roles=["role-pk"])
        )
        self.assertIn("Role 'testrole' added to user 'testuser' successfully.", result.stdout)

    @patch("akc.user_role.get_client")
    def test_remove_user_from_role(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_user = User(pk="user-pk", username="testuser", roles=["role-pk"])
        mock_client.users.retrieve.return_value = mock_user

        mock_role = Role(pk="role-pk", name="testrole")
        mock_client.roles.retrieve.return_value = mock_role

        result = self.runner.invoke(app, ["user-role", "remove", "user-pk", "role-pk"])

        self.assertEqual(result.exit_code, 0)
        mock_client.users.partial_update.assert_called_with(
            "user-pk",
            patched_user_request=PatchedUserRequest(roles=[])
        )
        self.assertIn("Role 'testrole' removed from user 'testuser' successfully.", result.stdout)

if __name__ == "__main__":
    unittest.main()
