import typer
from rich.console import Console
from rich.table import Table
import json
from authentik_client.models import User
from .main import get_client, app

user_app = typer.Typer()
console = Console()

@user_app.command("create")
def create_user(
    username: str,
    email: str,
    first_name: str = typer.Option(None),
    last_name: str = typer.Option(None),
    is_active: bool = typer.Option(True),
    is_superuser: bool = typer.Option(False),
):
    """
    Create a new user.
    """
    client = get_client()
    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        is_active=is_active,
        is_superuser=is_superuser,
    )
    try:
        new_user = client.users.create(user)
        console.print(f"[bold green]User '{new_user.username}' created successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error creating user: {e}[/bold red]")

@user_app.command("list")
def list_users(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all users.
    """
    client = get_client()
    try:
        users = client.users.list()
        if output == "json":
            console.print(json.dumps([u.to_dict() for u in users], indent=2))
        else:
            table = Table(title="Users")
            table.add_column("ID", style="cyan")
            table.add_column("Username", style="magenta")
            table.add_column("Email", style="green")
            table.add_column("Active", style="yellow")
            table.add_column("Superuser", style="blue")
            for user in users:
                table.add_row(
                    str(user.id),
                    user.username,
                    user.email,
                    str(user.is_active),
                    str(user.is_superuser),
                )
            console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error listing users: {e}[/bold red]")

@user_app.command("update")
def update_user(
    user_id: int = typer.Argument(..., help="The ID of the user to update."),
    username: str = typer.Option(None, "--username", help="New username."),
    email: str = typer.Option(None, "--email", help="New email."),
    first_name: str = typer.Option(None, "--first-name", help="New first name."),
    last_name: str = typer.Option(None, "--last-name", help="New last name."),
    is_active: bool = typer.Option(None, "--is-active/--not-active", help="Activate or deactivate the user."),
    is_superuser: bool = typer.Option(None, "--is-superuser/--not-superuser", help="Make the user a superuser or not."),
):
    """
    Update a user.
    """
    client = get_client()
    try:
        user = client.users.retrieve(user_id)
        update_data = {}
        if username is not None:
            update_data['username'] = username
        if email is not None:
            update_data['email'] = email
        if first_name is not None:
            update_data['first_name'] = first_name
        if last_name is not None:
            update_data['last_name'] = last_name
        if is_active is not None:
            update_data['is_active'] = is_active
        if is_superuser is not None:
            update_data['is_superuser'] = is_superuser

        if not update_data:
            console.print("[bold yellow]No fields to update.[/bold yellow]")
            return

        updated_user = client.users.update(user_id, user.model_copy(update=update_data))
        console.print(f"[bold green]User '{updated_user.username}' (ID: {updated_user.id}) updated successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error updating user: {e}[/bold red]")

@user_app.command("delete")
def delete_user(user_id: int = typer.Argument(..., help="The ID of the user to delete.")):
    """
    Delete a user.
    """
    client = get_client()
    try:
        client.users.delete(user_id)
        console.print(f"[bold green]User with ID {user_id} deleted successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error deleting user: {e}[/bold red]")

app.add_typer(user_app, name="user")
