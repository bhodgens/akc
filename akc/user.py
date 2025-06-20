import typer
from rich.console import Console
from rich.table import Table
import json
from authentik_client import api
from authentik_client.exceptions import ApiException
from authentik_client.models import User, PatchedUserRequest, UserRequest, Role, Group, PasswordRequest
from .main import get_client, app

user_app = typer.Typer()
console = Console()

@user_app.command("create")
def create_user(
    username: str,
    email: str,
    name: str = typer.Option(None),
    is_active: bool = typer.Option(True),
    is_superuser: bool = typer.Option(False),
):
    """
    Create a new user.
    """
    client = get_client()
    core_api = api.CoreApi(client)
    user_request = UserRequest(
        username=username,
        email=email,
        name=name,
        is_active=is_active,
        is_superuser=is_superuser,
    )
    try:
        new_user = core_api.core_users_create(user_request=user_request)
        console.print(f"[bold green]User '{new_user.username}' created successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error creating user: {e.body}[/bold red]")

@user_app.command("list")
def list_users(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all users.
    """
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        users = core_api.core_users_list()
        if output == "json":
            console.print(json.dumps([u.to_dict() for u in users.results], indent=2))
        else:
            table = Table(title="Users")
            table.add_column("ID", style="cyan")
            table.add_column("Username", style="magenta")
            table.add_column("Email", style="green")
            table.add_column("Active", style="yellow")
            table.add_column("Superuser", style="blue")
            for user in users.results:
                table.add_row(
                    str(user.pk),
                    user.username,
                    user.email,
                    str(user.is_active),
                    str(user.is_superuser),
                )
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing users: {e.body}[/bold red]")

@user_app.command("get")
def get_user(user_id: str = typer.Argument(..., help="The ID or username of the user.")):
    """Get a single user."""
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        try:
            user = core_api.core_users_retrieve(user_pk=int(user_id))
            console.print(user.to_dict())
        except ValueError:
            users = core_api.core_users_list(username=user_id)
            if users.results:
                console.print(users.results[0].to_dict())
            else:
                console.print(f"[bold red]User '{user_id}' not found.[/bold red]")
    except ApiException as e:
        console.print(f"[bold red]Error getting user: {e.body}[/bold red]")

@user_app.command("update")
def update_user(
    user_id: int = typer.Argument(..., help="The ID of the user to update."),
    username: str = typer.Option(None, "--username", help="New username."),
    email: str = typer.Option(None, "--email", help="New email."),
    name: str = typer.Option(None, "--name", help="New name."),
    is_active: bool = typer.Option(None, "--is-active/--not-active", help="Activate or deactivate the user."),
    is_superuser: bool = typer.Option(None, "--is-superuser/--not-superuser", help="Make the user a superuser or not."),
):
    """
    Update a user.
    """
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        update_data = PatchedUserRequest()
        if username is not None:
            update_data.username = username
        if email is not None:
            update_data.email = email
        if name is not None:
            update_data.name = name
        if is_active is not None:
            update_data.is_active = is_active
        if is_superuser is not None:
            update_data.is_superuser = is_superuser

        if not update_data.model_dump(exclude_unset=True):
            console.print("[bold yellow]No fields to update.[/bold yellow]")
            return

        updated_user = core_api.core_users_partial_update(user_pk=user_id, patched_user_request=update_data)
        console.print(f"[bold green]User '{updated_user.username}' (ID: {updated_user.pk}) updated successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error updating user: {e.body}[/bold red]")

@user_app.command("delete")
def delete_user(user_id: int = typer.Argument(..., help="The ID of the user to delete.")):
    """
    Delete a user.
    """
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        core_api.core_users_destroy(user_pk=user_id)
        console.print(f"[bold green]User with ID {user_id} deleted successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error deleting user: {e.body}[/bold red]")

@user_app.command("set-password")
def set_password(
    user_id: int = typer.Argument(..., help="The ID of the user."),
    password: str = typer.Argument(..., help="The new password."),
):
    """
    Set a user's password.
    """
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        password_request = PasswordRequest(password=password)
        core_api.core_users_set_password_create(user_pk=user_id, password_request=password_request)
        console.print(f"[bold green]Password for user with ID {user_id} set successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error setting password: {e.body}[/bold red]")

@user_app.command("list-roles")
def list_user_roles(
    user_id: int = typer.Argument(..., help="The ID of the user."),
    output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")
):
    """List roles for a user."""
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        roles = core_api.core_users_roles_list(user_pk=user_id)
        if output == "json":
            console.print(json.dumps([r.to_dict() for r in roles.results], indent=2))
        else:
            table = Table(title=f"Roles for user {user_id}")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            for role in roles.results:
                table.add_row(role.pk, role.name)
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing roles for user: {e.body}[/bold red]")

@user_app.command("list-groups")
def list_user_groups(
    user_id: int = typer.Argument(..., help="The ID of the user."),
    output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")
):
    """List groups for a user."""
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        groups = core_api.core_users_groups_list(user_pk=user_id)
        if output == "json":
            console.print(json.dumps([g.to_dict() for g in groups.results], indent=2))
        else:
            table = Table(title=f"Groups for user {user_id}")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            for group in groups.results:
                table.add_row(group.pk, group.name)
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing groups for user: {e.body}[/bold red]")

app.add_typer(user_app, name="user")
