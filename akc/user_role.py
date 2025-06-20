import typer
from rich.console import Console

from authentik_client import api
from authentik_client.exceptions import ApiException
from authentik_client.models import PatchedUserRequest

from .main import get_client, app

user_role_app = typer.Typer()
console = Console()


@user_role_app.command("add")
def add_user_to_role(
    user_id: str = typer.Argument(..., help="The ID or username of the user."),
    role_id: str = typer.Argument(..., help="The ID or name of the role."),
):
    """
    Add a role to a user.
    """
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        role = core_api.core_roles_retrieve(role_uuid=role_id)
        user = core_api.core_users_retrieve(user_pk=int(user_id))
        user_roles = user.roles or []

        if role.pk in user_roles:
            console.print(f"[bold yellow]User '{user.username}' already has role '{role.name}'.[/bold yellow]")
            return

        user_roles.append(role.pk)

        update_request = PatchedUserRequest(roles=user_roles)
        core_api.core_users_partial_update(user_pk=user.pk, patched_user_request=update_request)

        console.print(f"[bold green]Role '{role.name}' added to user '{user.username}' successfully.[/bold green]")

    except ApiException as e:
        console.print(f"[bold red]Error adding role to user: {e.body}[/bold red]")


@user_role_app.command("remove")
def remove_user_from_role(
    user_id: str = typer.Argument(..., help="The ID or username of the user."),
    role_id: str = typer.Argument(..., help="The ID or name of the role."),
):
    """
    Remove a role from a user.
    """
    client = get_client()
    core_api = api.CoreApi(client)
    try:
        role = core_api.core_roles_retrieve(role_uuid=role_id)
        user = core_api.core_users_retrieve(user_pk=int(user_id))
        user_roles = user.roles or []

        if role.pk not in user_roles:
            console.print(f"[bold yellow]User '{user.username}' does not have role '{role.name}'.[/bold yellow]")
            return

        user_roles.remove(role.pk)

        update_request = PatchedUserRequest(roles=user_roles)
        core_api.core_users_partial_update(user_pk=user.pk, patched_user_request=update_request)

        console.print(f"[bold green]Role '{role.name}' removed from user '{user.username}' successfully.[/bold green]")

    except ApiException as e:
        console.print(f"[bold red]Error removing role from user: {e.body}[/bold red]")


app.add_typer(user_role_app, name="user-role")
