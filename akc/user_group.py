import typer
from rich.console import Console
from authentik_client.models import PatchedUserRequest
from .main import get_client, app

user_group_app = typer.Typer()
console = Console()

@user_group_app.command("add")
def add_user_to_group(
    user_id: int = typer.Argument(..., help="The ID of the user."),
    group_id: int = typer.Argument(..., help="The ID of the group."),
):
    """
    Add a user to a group.
    """
    client = get_client()
    try:
        group = client.groups.retrieve(group_id)
        user = client.users.retrieve(user_id)
        user_groups = user.groups or []

        if group.pk in user_groups:
            console.print(f"[bold yellow]User '{user.username}' is already in group '{group.name}'.[/bold yellow]")
            return

        user_groups.append(group.pk)

        update_request = PatchedUserRequest(groups=user_groups)
        client.users.partial_update(user_id, patched_user_request=update_request)

        console.print(f"[bold green]User '{user.username}' added to group '{group.name}' successfully.[/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error adding user to group: {e}[/bold red]")


@user_group_app.command("remove")
def remove_user_from_group(
    user_id: int = typer.Argument(..., help="The ID of the user."),
    group_id: int = typer.Argument(..., help="The ID of the group."),
):
    """
    Remove a user from a group.
    """
    client = get_client()
    try:
        group = client.groups.retrieve(group_id)
        user = client.users.retrieve(user_id)
        user_groups = user.groups or []

        if group.pk not in user_groups:
            console.print(f"[bold yellow]User '{user.username}' is not in group '{group.name}'.[/bold yellow]")
            return

        user_groups.remove(group.pk)

        update_request = PatchedUserRequest(groups=user_groups)
        client.users.partial_update(user_id, patched_user_request=update_request)

        console.print(f"[bold green]User '{user.username}' removed from group '{group.name}' successfully.[/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error removing user from group: {e}[/bold red]")


app.add_typer(user_group_app, name="user-group")

