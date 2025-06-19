import typer
from rich.console import Console
from rich.table import Table
import json
from authentik_client.models import Group
from .main import get_client, app

group_app = typer.Typer()
console = Console()

@group_app.command("create")
def create_group(name: str):
    """
    Create a new group.
    """
    client = get_client()
    group = Group(name=name)
    try:
        new_group = client.groups.create(group)
        console.print(f"[bold green]Group '{new_group.name}' created successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error creating group: {e}[/bold red]")

@group_app.command("list")
def list_groups(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all groups.
    """
    client = get_client()
    try:
        groups = client.groups.list()
        if output == "json":
            console.print(json.dumps([g.to_dict() for g in groups], indent=2))
        else:
            table = Table(title="Groups")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            for group in groups:
                table.add_row(str(group.id), group.name)
            console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error listing groups: {e}[/bold red]")

@group_app.command("update")
def update_group(
    group_id: int = typer.Argument(..., help="The ID of the group to update."),
    name: str = typer.Option(..., "--name", help="New name for the group."),
):
    """
    Update a group.
    """
    client = get_client()
    try:
        group = client.groups.retrieve(group_id)
        group.name = name
        updated_group = client.groups.update(group_id, group)
        console.print(f"[bold green]Group '{updated_group.name}' (ID: {updated_group.id}) updated successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error updating group: {e}[/bold red]")

@group_app.command("delete")
def delete_group(group_id: int = typer.Argument(..., help="The ID of the group to delete.")):
    """
    Delete a group.
    """
    client = get_client()
    try:
        client.groups.delete(group_id)
        console.print(f"[bold green]Group with ID {group_id} deleted successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error deleting group: {e}[/bold red]")

app.add_typer(group_app, name="group")

