import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from akc.main import app
from rich.console import Console
from authentik_client.models.user import User
from authentik_client.models.paginated_user_list import PaginatedUserList
from authentik_client.models.patched_user_request import PatchedUserRequest

class TestUserCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        app.console = Console(force_terminal=False)

    @patch("akc.user.UsersApi")
    def test_create_user(self, MockUsersApi):
        mock_api = MockUsersApi.return_value
        mock_api.users_create.return_value = User(username="testuser")

        result = self.runner.invoke(
            app,
            ["user", "create", "testuser", "test@test.com"],
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("User 'testuser' created successfully.", result.stdout)

    @patch("akc.user.UsersApi")
    def test_list_users(self, MockUsersApi):
        mock_api = MockUsersApi.return_value
        user1 = User(pk="user1-pk", username="user1", email="user1@test.com", is_active=True, is_superuser=False)
        user2 = User(pk="user2-pk", username="user2", email="user2@test.com", is_active=False, is_superuser=True)
        mock_api.users_list.return_value = PaginatedUserList(results=[user1, user2])

        result = self.runner.invoke(app, ["user", "list"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("user1-pk", result.stdout)
        self.assertIn("user2-pk", result.stdout)

    @patch("akc.user.UsersApi")
    def test_update_user(self, MockUsersApi):
        mock_api = MockUsersApi.return_value
        updated_user = User(pk="user-pk", username="newname")
        mock_api.users_partial_update.return_value = updated_user

        result = self.runner.invoke(
            app, ["user", "update", "user-pk", "--username", "newname"]
        )

        self.assertEqual(result.exit_code, 0)
        mock_api.users_partial_update.assert_called_with(
            user_pk="user-pk",
            patched_user_request=PatchedUserRequest(username="newname")
        )
        self.assertIn("User 'newname' (ID: user-pk) updated successfully.", result.stdout)

    @patch("akc.user.UsersApi")
    def test_delete_user(self, MockUsersApi):
        mock_api = MockUsersApi.return_value

        result = self.runner.invoke(app, ["user", "delete", "user-pk"])

        self.assertEqual(result.exit_code, 0)
        mock_api.users_destroy.assert_called_with(user_pk="user-pk")
        self.assertIn("User with ID user-pk deleted successfully.", result.stdout)

if __name__ == "__main__":
    unittest.main()
