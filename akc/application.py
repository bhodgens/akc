import typer
from rich.console import Console
from rich.table import Table
import json
from authentik_client.models import Application
from .main import get_client, app

app_app = typer.Typer()
console = Console()

@app_app.command("create")
def create_application(
    name: str,
    slug: str,
    type: str = typer.Option("native", help="The type of application to create."),
):
    """
    Create a new application.
    """
    client = get_client()
    application = Application(name=name, slug=slug, type=type)
    try:
        new_app = client.applications.create(application)
        console.print(f"[bold green]Application '{new_app.name}' created successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error creating application: {e}[/bold red]")

@app_app.command("list")
def list_applications(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all applications.
    """
    client = get_client()
    try:
        apps = client.applications.list()
        if output == "json":
            console.print(json.dumps([a.to_dict() for a in apps], indent=2))
        else:
            table = Table(title="Applications")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Slug", style="green")
            table.add_column("Type", style="yellow")
            for app in apps:
                table.add_row(str(app.id), app.name, app.slug, app.type)
            console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error listing applications: {e}[/bold red]")

@app_app.command("update")
def update_application(
    app_id: int = typer.Argument(..., help="The ID of the application to update."),
    name: str = typer.Option(None, "--name", help="New name for the application."),
    slug: str = typer.Option(None, "--slug", help="New slug for the application."),
    type: str = typer.Option(None, "--type", help="New type for the application."),
):
    """
    Update an application.
    """
    client = get_client()
    try:
        app = client.applications.retrieve(app_id)
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if slug is not None:
            update_data['slug'] = slug
        if type is not None:
            update_data['type'] = type

        if not update_data:
            console.print("[bold yellow]No fields to update.[/bold yellow]")
            return

        updated_app = client.applications.update(app_id, app.model_copy(update=update_data))
        console.print(f"[bold green]Application '{updated_app.name}' (ID: {updated_app.id}) updated successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error updating application: {e}[/bold red]")

@app_app.command("delete")
def delete_application(app_id: int = typer.Argument(..., help="The ID of the application to delete.")):
    """
    Delete an application.
    """
    client = get_client()
    try:
        client.applications.delete(app_id)
        console.print(f"[bold green]Application with ID {app_id} deleted successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error deleting application: {e}[/bold red]")

app.add_typer(app_app, name="application")

