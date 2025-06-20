import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from akc.main import app
from rich.console import Console
from authentik_client.models.flow import Flow
from authentik_client.models.paginated_flow_list import PaginatedFlowList
from authentik_client.models.flow_set_request import FlowSetRequest

class TestFlowCommands(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        app.console = Console(force_terminal=False)

    @patch("akc.flow.FlowsApi")
    def test_list_flows(self, MockFlowsApi):
        mock_api = MockFlowsApi.return_value

        flow1 = Flow(pk="flow1-pk", name="flow1", slug="flow1-slug", title="Flow 1")
        flow2 = Flow(pk="flow2-pk", name="flow2", slug="flow2-slug", title="Flow 2")

        mock_api.flows_instances_list.return_value = PaginatedFlowList(results=[flow1, flow2])

        result = self.runner.invoke(app, ["flow", "list"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("flow1-pk", result.stdout)
        self.assertIn("flow2-pk", result.stdout)

    @patch("akc.flow.FlowsApi")
    def test_export_flow_to_stdout(self, MockFlowsApi):
        mock_api = MockFlowsApi.return_value
        mock_api.flows_instances_export_retrieve.return_value = "exported flow data"

        result = self.runner.invoke(app, ["flow", "export", "flow-slug"])

        self.assertEqual(result.exit_code, 0)
        mock_api.flows_instances_export_retrieve.assert_called_with(fs_slug="flow-slug")
        self.assertIn("exported flow data", result.stdout)

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("akc.flow.FlowsApi")
    def test_export_flow_to_file(self, MockFlowsApi, mock_file):
        mock_api = MockFlowsApi.return_value
        mock_api.flows_instances_export_retrieve.return_value = "exported flow data"

        result = self.runner.invoke(app, ["flow", "export", "flow-slug", "-o", "flow.yaml"])

        self.assertEqual(result.exit_code, 0)
        mock_api.flows_instances_export_retrieve.assert_called_with(fs_slug="flow-slug")
        mock_file.assert_called_with("flow.yaml", "w")
        mock_file().write.assert_called_with("exported flow data")
        self.assertIn("Flow 'flow-slug' exported to flow.yaml.", result.stdout)

    @patch("akc.flow.yaml.safe_load")
    @patch("akc.flow.FlowsApi")
    def test_import_flow(self, MockFlowsApi, mock_safe_load):
        mock_api = MockFlowsApi.return_value
        mock_safe_load.return_value = {"key": "value"}

        with self.runner.isolated_filesystem():
            with open("flow.yaml", "w") as f:
                f.write("some yaml data")

            result = self.runner.invoke(app, ["flow", "import", "flow.yaml"])

            self.assertEqual(result.exit_code, 0)
            mock_safe_load.assert_called_with("some yaml data")
            mock_api.flows_instances_import_create.assert_called_with(flow_set_request=FlowSetRequest(key="value"))
            self.assertIn("Flow from 'flow.yaml' imported successfully.", result.stdout)

if __name__ == "__main__":
    unittest.main()
