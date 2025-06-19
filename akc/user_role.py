import typer
from rich.console import Console
from authentik_client.models import PatchedUserRequest
from .main import get_client, app

user_role_app = typer.Typer()
console = Console()

@user_role_app.command("add")
def add_user_to_role(
    user_id: int = typer.Argument(..., help="The ID of the user."),
    role_id: int = typer.Argument(..., help="The ID of the role."),
):
    """
    Add a role to a user.
    """
    client = get_client()
    try:
        role = client.roles.retrieve(role_id)
        user = client.users.retrieve(user_id)
        user_roles = user.roles or []

        if role.pk in user_roles:
            console.print(f"[bold yellow]User '{user.username}' already has role '{role.name}'.[/bold yellow]")
            return

        user_roles.append(role.pk)

        update_request = PatchedUserRequest(roles=user_roles)
        client.users.partial_update(user_id, patched_user_request=update_request)

        console.print(f"[bold green]Role '{role.name}' added to user '{user.username}' successfully.[/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error adding role to user: {e}[/bold red]")


@user_role_app.command("remove")
def remove_user_from_role(
    user_id: int = typer.Argument(..., help="The ID of the user."),
    role_id: int = typer.Argument(..., help="The ID of the role."),
):
    """
    Remove a role from a user.
    """
    client = get_client()
    try:
        role = client.roles.retrieve(role_id)
        user = client.users.retrieve(user_id)
        user_roles = user.roles or []

        if role.pk not in user_roles:
            console.print(f"[bold yellow]User '{user.username}' does not have role '{role.name}'.[/bold yellow]")
            return

        user_roles.remove(role.pk)

        update_request = PatchedUserRequest(roles=user_roles)
        client.users.partial_update(user_id, patched_user_request=update_request)

        console.print(f"[bold green]Role '{role.name}' removed from user '{user.username}' successfully.[/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error removing role from user: {e}[/bold red]")


app.add_typer(user_role_app, name="user-role")

