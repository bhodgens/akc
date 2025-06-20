import json
import pathlib
import yaml
from rich.console import Console
from rich.table import Table
import typer

from authentik_client import api
from authentik_client.exceptions import ApiException
from authentik_client.models.flow_request import FlowRequest
from authentik_client.models.flow_set_request import FlowSetRequest
from authentik_client.models.patched_flow_request import PatchedFlowRequest

from .main import get_client, app

flow_app = typer.Typer()
console = Console()

@flow_app.command("list")
def list_flows(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all flows.
    """
    client = get_client()
    flows_api = api.FlowsApi(client)
    try:
        flows = flows_api.flows_instances_list()
        if output == "json":
            console.print(json.dumps([f.to_dict() for f in flows.results], indent=2))
        else:
            table = Table(title="Flows")
            table.add_column("PK", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Slug", style="green")
            table.add_column("Title", style="yellow")
            for flow in flows.results:
                table.add_row(
                    flow.pk,
                    flow.name,
                    flow.slug,
                    flow.title,
                )
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing flows: {e.body}[/bold red]")

@flow_app.command("get")
def get_flow(flow_uuid: str = typer.Argument(..., help="The UUID of the flow to get.")):
    """
    Get a flow.
    """
    client = get_client()
    flows_api = api.FlowsApi(client)
    try:
        flow = flows_api.flows_instances_retrieve(flow_uuid=flow_uuid)
        console.print(flow.to_dict())
    except ApiException as e:
        console.print(f"[bold red]Error getting flow: {e.body}[/bold red]")

@flow_app.command("delete")
def delete_flow(flow_uuid: str = typer.Argument(..., help="The UUID of the flow to delete.")):
    """
    Delete a flow.
    """
    client = get_client()
    flows_api = api.FlowsApi(client)
    try:
        flows_api.flows_instances_destroy(flow_uuid=flow_uuid)
        console.print(f"[bold green]Flow '{flow_uuid}' deleted successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error deleting flow: {e.body}[/bold red]")

@flow_app.command("export")
def export_flow(
    flow_slug: str = typer.Argument(..., help="The slug of the flow to export."),
    output_file: pathlib.Path = typer.Option(None, "--output-file", "-o", help="Path to save the exported flow."),
):
    """
    Export a flow.
    """
    client = get_client()
    flows_api = api.FlowsApi(client)
    try:
        # The export endpoint returns a yaml file as a string
        exported_flow = flows_api.flows_instances_export_retrieve(fs_slug=flow_slug)
        if output_file:
            with open(output_file, "w") as f:
                f.write(exported_flow)
            console.print(f"[bold green]Flow '{flow_slug}' exported to {output_file}.[/bold green]")
        else:
            console.print(exported_flow)
    except ApiException as e:
        console.print(f"[bold red]Error exporting flow: {e.body}[/bold red]")


@flow_app.command("import")
def import_flow(
    file: typer.FileText = typer.Argument(..., help="Path to the flow file to import."),
):
    """
    Import a flow.
    """
    client = get_client()
    flows_api = api.FlowsApi(client)
    try:
        flow_data = file.read()
        parsed_data = yaml.safe_load(flow_data)
        # The API expects a FlowSetRequest object. The yaml file is a dictionary that can be used to create it.
        flow_set_request = FlowSetRequest(**parsed_data)
        flows_api.flows_instances_import_create(flow_set_request=flow_set_request)
        console.print(f"[bold green]Flow from '{file.name}' imported successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error importing flow: {e.body}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")

@flow_app.command("create")
def create_flow(
    name: str = typer.Argument(...),
    slug: str = typer.Argument(...),
    title: str = typer.Argument(...),
):
    """
    Create a flow.
    """
    client = get_client()
    flows_api = api.FlowsApi(client)
    try:
        flow_request = FlowRequest(name=name, slug=slug, title=title)
        flow = flows_api.flows_instances_create(flow_request=flow_request)
        console.print(f"[bold green]Flow '{flow.name}' created successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error creating flow: {e.body}[/bold red]")

@flow_app.command("update")
def update_flow(
    flow_uuid: str = typer.Argument(..., help="The UUID of the flow to update."),
    name: str = typer.Option(None, "--name"),
    slug: str = typer.Option(None, "--slug"),
    title: str = typer.Option(None, "--title"),
):
    """
    Update a flow.
    """
    client = get_client()
    flows_api = api.FlowsApi(client)
    try:
        update_data = PatchedFlowRequest()
        if name:
            update_data.name = name
        if slug:
            update_data.slug = slug
        if title:
            update_data.title = title

        flow = flows_api.flows_instances_partial_update(
            flow_uuid=flow_uuid, patched_flow_request=update_data
        )
        console.print(f"[bold green]Flow '{flow.name}' updated successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error updating flow: {e.body}[/bold red]")

app.add_typer(flow_app, name="flow")
