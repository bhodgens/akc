import typer
from rich.console import Console
from rich.table import Table
import json
from authentik_client.models import Group, PatchedGroupRequest, User
from authentik_client import api
from authentik_client.exceptions import ApiException
from .main import get_client, app

group_app = typer.Typer()
console = Console()

@group_app.command("create")
def create_group(name: str):
    """
    Create a new group.
    """
    client = get_client()
    core_api = api.CoreApi(client)
    group = Group(name=name)
    try:
        new_group = core_api.core_groups_create(group)
        console.print(f"[bold green]Group '{new_group.name}' created successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error creating group: {e.body}[/bold red]")

@group_app.command("list")
def list_groups(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all groups.
    """
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        groups = core_api.core_groups_list()
        if output == "json":
            console.print(json.dumps([g.to_dict() for g in groups.results], indent=2))
        else:
            table = Table(title="Groups")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            for group in groups.results:
                table.add_row(group.pk, group.name)
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing groups: {e.body}[/bold red]")

@group_app.command("get")
def get_group(group_id: str = typer.Argument(..., help="The ID or UUID of the group.")):
    """Get a single group."""
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        group = core_api.core_groups_retrieve(group_pk=group_id)
        console.print(group.to_dict())
    except ApiException as e:
        console.print(f"[bold red]Error getting group: {e.body}[/bold red]")

@group_app.command("update")
def update_group(
    group_id: str = typer.Argument(..., help="The ID of the group to update."),
    name: str = typer.Option(None, "--name", help="New name for the group."),
    is_superuser: bool = typer.Option(None, "--is-superuser/--not-superuser"),
):
    """
    Update a group.
    """
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        update_data = PatchedGroupRequest()
        if name is not None:
            update_data.name = name
        if is_superuser is not None:
            update_data.is_superuser = is_superuser

        if not update_data.model_dump(exclude_unset=True):
            console.print("[bold yellow]No fields to update.[/bold yellow]")
            return

        updated_group = core_api.core_groups_partial_update(group_pk=group_id, patched_group_request=update_data)
        console.print(f"[bold green]Group '{updated_group.name}' (ID: {updated_group.pk}) updated successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error updating group: {e.body}[/bold red]")

@group_app.command("list-users")
def list_group_users(
    group_id: str = typer.Argument(..., help="The ID or UUID of the group."),
    output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")
):
    """List users in a group."""
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        users = core_api.core_groups_users_list(group_pk=group_id)
        if output == "json":
            console.print(json.dumps([u.to_dict() for u in users.results], indent=2))
        else:
            table = Table(title=f"Users in group {group_id}")
            table.add_column("ID", style="cyan")
            table.add_column("Username", style="magenta")
            table.add_column("Email", style="green")
            for user in users.results:
                table.add_row(str(user.pk), user.username, user.email)
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing users in group: {e.body}[/bold red]")

@group_app.command("delete")
def delete_group(group_id: str = typer.Argument(..., help="The ID of the group to delete.")):
    """
    Delete a group.
    """
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        core_api.core_groups_destroy(group_pk=group_id)
        console.print(f"[bold green]Group with ID {group_id} deleted successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error deleting group: {e.body}[/bold red]")

app.add_typer(group_app, name="group")
