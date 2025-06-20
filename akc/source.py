import json

import typer
from rich.console import Console
from rich.table import Table

from authentik_client import api
from authentik_client.exceptions import ApiException

from .main import get_client, app

source_app = typer.Typer()
console = Console()

@source_app.command("list")
def list_sources(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all sources.
    """
    client = get_client()
    sources_api = api.SourcesApi(client)
    try:
        sources = sources_api.sources_all_list()
        if output == "json":
            console.print(json.dumps([s.to_dict() for s in sources.results], indent=2))
        else:
            table = Table(title="Sources")
            table.add_column("UUID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Slug", style="green")
            table.add_column("Enabled", style="yellow")
            for source in sources.results:
                table.add_row(
                    source.pk,
                    source.name,
                    source.slug,
                    str(source.enabled)
                )
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing sources: {e.body}[/bold red]")

@source_app.command("get")
def get_source(slug: str = typer.Argument(..., help="The slug of the source to get.")):
    """
    Get a source.
    """
    client = get_client()
    sources_api = api.SourcesApi(client)
    try:
        source = sources_api.sources_all_retrieve(slug=slug)
        console.print(source.to_dict())
    except ApiException as e:
        console.print(f"[bold red]Error getting source: {e.body}[/bold red]")

@source_app.command("delete")
def delete_source(slug: str = typer.Argument(..., help="The slug of the source to delete.")):
    """
    Delete a source.
    """
    client = get_client()
    sources_api = api.SourcesApi(client)
    try:
        sources_api.sources_all_destroy(slug=slug)
        console.print(f"[bold green]Source '{slug}' deleted successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error deleting source: {e.body}[/bold red]")

@source_app.command("list-types")
def list_source_types():
    """List all available source types."""
    client = get_client()
    sources_api = api.SourcesApi(client)
    try:
        types = sources_api.sources_all_types_list()
        console.print([t.to_dict() for t in types])
    except ApiException as e:
        console.print(f"[bold red]Error listing source types: {e.body}[/bold red]")

@source_app.command("use")
def get_source_use(slug: str = typer.Argument(..., help="The slug of the source to check.")):
    """Check which objects are using a source."""
    client = get_client()
    sources_api = api.SourcesApi(client)
    try:
        used_by = sources_api.sources_all_used_by_list(slug=slug)
        console.print([item.to_dict() for item in used_by])
    except ApiException as e:
        console.print(f"[bold red]Error getting source usage: {e.body}[/bold red]")

app.add_typer(source_app, name="source")
