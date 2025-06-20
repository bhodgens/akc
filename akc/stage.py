import json

import typer
from rich.console import Console
from rich.table import Table

from authentik_client import api
from authentik_client.exceptions import ApiException

from .main import get_client, app

stage_app = typer.Typer()
console = Console()

@stage_app.command("list")
def list_stages(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all stages.
    """
    client = get_client()
    stages_api = api.StagesApi(client)
    try:
        stages = stages_api.stages_all_list()
        if output == "json":
            console.print(json.dumps([s.to_dict() for s in stages.results], indent=2))
        else:
            table = Table(title="Stages")
            table.add_column("UUID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Component", style="green")
            for stage in stages.results:
                table.add_row(
                    stage.pk,
                    stage.name,
                    stage.component
                )
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing stages: {e.body}[/bold red]")

@stage_app.command("get")
def get_stage(uuid: str = typer.Argument(..., help="The UUID of the stage to get.")):
    """
    Get a stage.
    """
    client = get_client()
    stages_api = api.StagesApi(client)
    try:
        stage = stages_api.stages_all_retrieve(stage_uuid=uuid)
        console.print(stage.to_dict())
    except ApiException as e:
        console.print(f"[bold red]Error getting stage: {e.body}[/bold red]")

@stage_app.command("delete")
def delete_stage(uuid: str = typer.Argument(..., help="The UUID of the stage to delete.")):
    """
    Delete a stage.
    """
    client = get_client()
    stages_api = api.StagesApi(client)
    try:
        stages_api.stages_all_destroy(stage_uuid=uuid)
        console.print(f"[bold green]Stage '{uuid}' deleted successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error deleting stage: {e.body}[/bold red]")

@stage_app.command("list-types")
def list_stage_types():
    """List all available stage types."""
    client = get_client()
    stages_api = api.StagesApi(client)
    try:
        types = stages_api.stages_all_types_list()
        console.print([t.to_dict() for t in types])
    except ApiException as e:
        console.print(f"[bold red]Error listing stage types: {e.body}[/bold red]")

@stage_app.command("use")
def get_stage_use(uuid: str = typer.Argument(..., help="The UUID of the stage to check.")):
    """Check which objects are using a stage."""
    client = get_client()
    stages_api = api.StagesApi(client)
    try:
        used_by = stages_api.stages_all_used_by_list(stage_uuid=uuid)
        console.print([item.to_dict() for item in used_by])
    except ApiException as e:
        console.print(f"[bold red]Error getting stage usage: {e.body}[/bold red]")

app.add_typer(stage_app, name="stage")
