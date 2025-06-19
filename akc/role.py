import typer
from rich.console import Console
from rich.table import Table
import json
from authentik_client.models import Role
from .main import get_client, app

role_app = typer.Typer()
console = Console()

@role_app.command("create")
def create_role(name: str):
    """
    Create a new role.
    """
    client = get_client()
    role = Role(name=name)
    try:
        new_role = client.roles.create(role)
        console.print(f"[bold green]Role '{new_role.name}' created successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error creating role: {e}[/bold red]")

@role_app.command("list")
def list_roles(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all roles.
    """
    client = get_client()
    try:
        roles = client.roles.list()
        if output == "json":
            console.print(json.dumps([r.to_dict() for r in roles], indent=2))
        else:
            table = Table(title="Roles")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            for role in roles:
                table.add_row(str(role.id), role.name)
            console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error listing roles: {e}[/bold red]")

@role_app.command("update")
def update_role(
    role_id: int = typer.Argument(..., help="The ID of the role to update."),
    name: str = typer.Option(..., "--name", help="New name for the role."),
):
    """
    Update a role.
    """
    client = get_client()
    try:
        role = client.roles.retrieve(role_id)
        role.name = name
        updated_role = client.roles.update(role_id, role)
        console.print(f"[bold green]Role '{updated_role.name}' (ID: {updated_role.id}) updated successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error updating role: {e}[/bold red]")

@role_app.command("delete")
def delete_role(role_id: int = typer.Argument(..., help="The ID of the role to delete.")):
    """
    Delete a role.
    """
    client = get_client()
    try:
        client.roles.delete(role_id)
        console.print(f"[bold green]Role with ID {role_id} deleted successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error deleting role: {e}[/bold red]")

app.add_typer(role_app, name="role")

