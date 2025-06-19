import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from akc.main import app

class TestGroupCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("akc.group.Group")
    @patch("akc.group.console")
    @patch("akc.group.get_client")
    def test_create_group(self, mock_get_client, mock_console, mock_group_model):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_group = MagicMock()
        mock_group.name = "testgroup"
        mock_client.groups.create.return_value = mock_group

        result = self.runner.invoke(
            app,
            ["group", "create", "testgroup"],
        )

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]Group 'testgroup' created successfully.[/bold green]")

    @patch("akc.group.console")
    @patch("akc.group.get_client")
    def test_list_groups(self, mock_get_client, mock_console):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        group1 = MagicMock()
        group1.id = 1
        group1.name = "group1"

        group2 = MagicMock()
        group2.id = 2
        group2.name = "group2"

        mock_client.groups.list.return_value = [group1, group2]

        result = self.runner.invoke(app, ["group", "list"])

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called()

    @patch("akc.group.console")
    @patch("akc.group.get_client")
    def test_update_group(self, mock_get_client, mock_console):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        retrieved_group = MagicMock()
        mock_client.groups.retrieve.return_value = retrieved_group

        updated_group = MagicMock()
        updated_group.name = "newgroupname"
        updated_group.id = 1
        mock_client.groups.update.return_value = updated_group

        result = self.runner.invoke(
            app, ["group", "update", "1", "--name", "newgroupname"]
        )

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]Group 'newgroupname' (ID: 1) updated successfully.[/bold green]")

    @patch("akc.group.console")
    @patch("akc.group.get_client")
    def test_delete_group(self, mock_get_client, mock_console):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(app, ["group", "delete", "1"])

        self.assertEqual(result.exit_code, 0)
        mock_console.print.assert_called_with("[bold green]Group with ID 1 deleted successfully.[/bold green]")

if __name__ == "__main__":
    unittest.main()
