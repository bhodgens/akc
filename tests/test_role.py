import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from akc.main import app
from rich.console import Console
from authentik_client.models.role import Role
from authentik_client.models.paginated_role_list import PaginatedRoleList

class TestRoleCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        app.console = Console(force_terminal=False)

    @patch("akc.role.RolesApi")
    def test_create_role(self, MockRolesApi):
        mock_api = MockRolesApi.return_value
        mock_api.roles_create.return_value = Role(name="testrole")

        result = self.runner.invoke(
            app,
            ["role", "create", "testrole"],
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Role 'testrole' created successfully.", result.stdout)

    @patch("akc.role.RolesApi")
    def test_list_roles(self, MockRolesApi):
        mock_api = MockRolesApi.return_value
        role1 = Role(pk="role1-pk", name="role1")
        role2 = Role(pk="role2-pk", name="role2")
        mock_api.roles_list.return_value = PaginatedRoleList(results=[role1, role2])

        result = self.runner.invoke(app, ["role", "list"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("role1-pk", result.stdout)
        self.assertIn("role2-pk", result.stdout)

    @patch("akc.role.RolesApi")
    def test_update_role(self, MockRolesApi):
        mock_api = MockRolesApi.return_value
        retrieved_role = Role(pk="role-pk", name="oldrolename")
        mock_api.roles_retrieve.return_value = retrieved_role

        updated_role = Role(pk="role-pk", name="newrolename")
        mock_api.roles_update.return_value = updated_role

        result = self.runner.invoke(
            app, ["role", "update", "role-pk", "--name", "newrolename"]
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Role 'newrolename' (ID: role-pk) updated successfully.", result.stdout)

    @patch("akc.role.RolesApi")
    def test_delete_role(self, MockRolesApi):
        mock_api = MockRolesApi.return_value

        result = self.runner.invoke(app, ["role", "delete", "role-pk"])

        self.assertEqual(result.exit_code, 0)
        mock_api.roles_destroy.assert_called_with(role_pk="role-pk")
        self.assertIn("Role with ID role-pk deleted successfully.", result.stdout)

if __name__ == "__main__":
    unittest.main()
