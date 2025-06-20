import typer
from rich.console import Console
from rich.table import Table
import json
from authentik_client import api
from authentik_client.exceptions import ApiException
from authentik_client.models import PatchedRoleRequest, Role, Group, User
from .main import get_client, app

role_app = typer.Typer()
console = Console()

@role_app.command("create")
def create_role(name: str):
    """
    Create a new role.
    """
    client = get_client()
    core_api = api.CoreApi(client)
    role = Role(name=name)
    try:
        new_role = core_api.core_roles_create(role)
        console.print(f"[bold green]Role '{new_role.name}' created successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error creating role: {e.body}[/bold red]")

@role_app.command("list")
def list_roles(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all roles.
    """
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        roles = core_api.core_roles_list()
        if output == "json":
            console.print(json.dumps([r.to_dict() for r in roles.results], indent=2))
        else:
            table = Table(title="Roles")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            for role in roles.results:
                table.add_row(role.pk, role.name)
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing roles: {e.body}[/bold red]")

@role_app.command("get")
def get_role(role_id: str = typer.Argument(..., help="The ID or UUID of the role.")):
    """Get a single role."""
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        role = core_api.core_roles_retrieve(role_uuid=role_id)
        console.print(role.to_dict())
    except ApiException as e:
        console.print(f"[bold red]Error getting role: {e.body}[/bold red]")

@role_app.command("update")
def update_role(
    role_id: str = typer.Argument(..., help="The ID of the role to update."),
    name: str = typer.Option(None, "--name", help="New name for the role."),
):
    """
    Update a role.
    """
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        update_data = PatchedRoleRequest()
        if name is not None:
            update_data.name = name

        if not update_data.model_dump(exclude_unset=True):
            console.print("[bold yellow]No fields to update.[/bold yellow]")
            return

        updated_role = core_api.core_roles_partial_update(role_uuid=role_id, patched_role_request=update_data)
        console.print(f"[bold green]Role '{updated_role.name}' (ID: {updated_role.pk}) updated successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error updating role: {e.body}[/bold red]")

@role_app.command("delete")
def delete_role(role_id: str = typer.Argument(..., help="The ID of the role to delete.")):
    """
    Delete a role.
    """
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        core_api.core_roles_destroy(role_uuid=role_id)
        console.print(f"[bold green]Role with ID {role_id} deleted successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error deleting role: {e.body}[/bold red]")

@role_app.command("list-users")
def list_role_users(
    role_id: str = typer.Argument(..., help="The ID or UUID of the role."),
    output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")
):
    """List users with a role."""
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        users = core_api.core_roles_users_list(role_uuid=role_id)
        if output == "json":
            console.print(json.dumps([u.to_dict() for u in users.results], indent=2))
        else:
            table = Table(title=f"Users with role {role_id}")
            table.add_column("ID", style="cyan")
            table.add_column("Username", style="magenta")
            table.add_column("Email", style="green")
            for user in users.results:
                table.add_row(str(user.pk), user.username, user.email)
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing users with role: {e.body}[/bold red]")

@role_app.command("list-groups")
def list_role_groups(
    role_id: str = typer.Argument(..., help="The ID or UUID of the role."),
    output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")
):
    """List groups with a role."""
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        groups = core_api.core_roles_groups_list(role_uuid=role_id)
        if output == "json":
            console.print(json.dumps([g.to_dict() for g in groups.results], indent=2))
        else:
            table = Table(title=f"Groups with role {role_id}")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            for group in groups.results:
                table.add_row(group.pk, group.name)
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing groups with role: {e.body}[/bold red]")

app.add_typer(role_app, name="role")
