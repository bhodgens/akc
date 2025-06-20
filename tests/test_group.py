import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from akc.main import app
from rich.console import Console
from authentik_client.models.group import Group
from authentik_client.models.paginated_group_list import PaginatedGroupList

class TestGroupCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        app.console = Console(force_terminal=False)

    @patch("akc.group.GroupsApi")
    def test_create_group(self, MockGroupsApi):
        mock_api = MockGroupsApi.return_value
        mock_api.groups_create.return_value = Group(name="testgroup")

        result = self.runner.invoke(
            app,
            ["group", "create", "testgroup"],
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Group 'testgroup' created successfully.", result.stdout)

    @patch("akc.group.GroupsApi")
    def test_list_groups(self, MockGroupsApi):
        mock_api = MockGroupsApi.return_value
        group1 = Group(pk="group1-pk", name="group1")
        group2 = Group(pk="group2-pk", name="group2")
        mock_api.groups_list.return_value = PaginatedGroupList(results=[group1, group2])

        result = self.runner.invoke(app, ["group", "list"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("group1-pk", result.stdout)
        self.assertIn("group2-pk", result.stdout)

    @patch("akc.group.GroupsApi")
    def test_update_group(self, MockGroupsApi):
        mock_api = MockGroupsApi.return_value
        retrieved_group = Group(pk="group-pk", name="oldgroupname")
        mock_api.groups_retrieve.return_value = retrieved_group

        updated_group = Group(pk="group-pk", name="newgroupname")
        mock_api.groups_update.return_value = updated_group

        result = self.runner.invoke(
            app, ["group", "update", "group-pk", "--name", "newgroupname"]
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Group 'newgroupname' (ID: group-pk) updated successfully.", result.stdout)

    @patch("akc.group.GroupsApi")
    def test_delete_group(self, MockGroupsApi):
        mock_api = MockGroupsApi.return_value

        result = self.runner.invoke(app, ["group", "delete", "group-pk"])

        self.assertEqual(result.exit_code, 0)
        mock_api.groups_destroy.assert_called_with(group_pk="group-pk")
        self.assertIn("Group with ID group-pk deleted successfully.", result.stdout)

if __name__ == "__main__":
    unittest.main()
