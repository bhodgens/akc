import json

import typer
from rich.console import Console
from rich.table import Table

from authentik_client import api
from authentik_client.exceptions import ApiException

from .main import get_client, app

propertymapping_app = typer.Typer()
console = Console()

@propertymapping_app.command("list")
def list_propertymappings(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all property mappings.
    """
    client = get_client()
    propertymappings_api = api.PropertymappingsApi(client)
    try:
        propertymappings = propertymappings_api.propertymappings_all_list()
        if output == "json":
            console.print(json.dumps([p.to_dict() for p in propertymappings.results], indent=2))
        else:
            table = Table(title="Property Mappings")
            table.add_column("UUID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Managed", style="green")
            for propertymapping in propertymappings.results:
                table.add_row(
                    propertymapping.pk,
                    propertymapping.name,
                    str(propertymapping.managed)
                )
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing property mappings: {e.body}[/bold red]")

@propertymapping_app.command("get")
def get_propertymapping(uuid: str = typer.Argument(..., help="The UUID of the property mapping to get.")):
    """
    Get a property mapping.
    """
    client = get_client()
    propertymappings_api = api.PropertymappingsApi(client)
    try:
        propertymapping = propertymappings_api.propertymappings_all_retrieve(pm_uuid=uuid)
        console.print(propertymapping.to_dict())
    except ApiException as e:
        console.print(f"[bold red]Error getting property mapping: {e.body}[/bold red]")

@propertymapping_app.command("delete")
def delete_propertymapping(uuid: str = typer.Argument(..., help="The UUID of the property mapping to delete.")):
    """
    Delete a property mapping.
    """
    client = get_client()
    propertymappings_api = api.PropertymappingsApi(client)
    try:
        propertymappings_api.propertymappings_all_destroy(pm_uuid=uuid)
        console.print(f"[bold green]Property mapping '{uuid}' deleted successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error deleting property mapping: {e.body}[/bold red]")

app.add_typer(propertymapping_app, name="propertymapping")
