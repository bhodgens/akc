import json

import typer
from rich.console import Console
from rich.table import Table

from authentik_client import api
from authentik_client.exceptions import ApiException

from .main import get_client, app

outpost_app = typer.Typer()
console = Console()

@outpost_app.command("list")
def list_outposts(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all outposts.
    """
    client = get_client()
    outposts_api = api.OutpostsApi(client)
    try:
        outposts = outposts_api.outposts_instances_list()
        if output == "json":
            console.print(json.dumps([o.to_dict() for o in outposts.results], indent=2))
        else:
            table = Table(title="Outposts")
            table.add_column("UUID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Type", style="green")
            table.add_column("Service Connection", style="yellow")
            for outpost in outposts.results:
                table.add_row(
                    outpost.pk,
                    outpost.name,
                    outpost.type,
                    outpost.service_connection_name,
                )
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing outposts: {e.body}[/bold red]")

@outpost_app.command("get")
def get_outpost(uuid: str = typer.Argument(..., help="The UUID of the outpost to get.")):
    """
    Get an outpost.
    """
    client = get_client()
    outposts_api = api.OutpostsApi(client)
    try:
        outpost = outposts_api.outposts_instances_retrieve(uuid=uuid)
        console.print(outpost.to_dict())
    except ApiException as e:
        console.print(f"[bold red]Error getting outpost: {e.body}[/bold red]")

@outpost_app.command("delete")
def delete_outpost(uuid: str = typer.Argument(..., help="The UUID of the outpost to delete.")):
    """
    Delete an outpost.
    """
    client = get_client()
    outposts_api = api.OutpostsApi(client)
    try:
        outposts_api.outposts_instances_destroy(uuid=uuid)
        console.print(f"[bold green]Outpost '{uuid}' deleted successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error deleting outpost: {e.body}[/bold red]")

@outpost_app.command("health")
def health_outpost(uuid: str = typer.Argument(..., help="The UUID of the outpost to check health.")):
    """
    Get outpost health.
    """
    client = get_client()
    outposts_api = api.OutpostsApi(client)
    try:
        health = outposts_api.outposts_instances_health_list(uuid=uuid)
        console.print(json.dumps([h.to_dict() for h in health], indent=2))
    except ApiException as e:
        console.print(f"[bold red]Error getting outpost health: {e.body}[/bold red]")

app.add_typer(outpost_app, name="outpost")
