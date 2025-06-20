import typer
from rich.console import Console
from rich.table import Table
import json
from authentik_client import api
from authentik_client.exceptions import ApiException
from authentik_client.models import Application, PatchedApplicationRequest
from .main import get_client, app

app_app = typer.Typer()
console = Console()

@app_app.command("create")
def create_application(
    name: str,
    slug: str,
):
    """
    Create a new application.
    """
    client = get_client()
    applications_api = api.ApplicationsApi(client)
    application = Application(name=name, slug=slug)
    try:
        new_app = applications_api.applications_create(application)
        console.print(f"[bold green]Application '{new_app.name}' created successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error creating application: {e}[/bold red]")

@app_app.command("list")
def list_applications(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all applications.
    """
    client = get_client()
    applications_api = api.ApplicationsApi(client)
    try:
        apps = applications_api.applications_list()
        if output == "json":
            console.print(json.dumps([a.to_dict() for a in apps.results], indent=2))
        else:
            table = Table(title="Applications")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Slug", style="green")
            for app in apps.results:
                table.add_row(app.pk, app.name, app.slug)
            console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error listing applications: {e}[/bold red]")

@app_app.command("get")
def get_application(app_id: str = typer.Argument(..., help="The UUID of the application.")):
    """Get an application by UUID."""
    client = get_client()
    applications_api = api.ApplicationsApi(client)
    console = Console()
    try:
        application = applications_api.applications_retrieve(application_uuid=app_id)
        console.print(application.to_dict())
    except ApiException as e:
        console.print(f"[bold red]Error: {e.body}[/bold red]")

@app_app.command("update")
def update_application(
    app_id: str = typer.Argument(..., help="The ID of the application to update."),
    name: str = typer.Option(None, "--name", help="New name for the application."),
    slug: str = typer.Option(None, "--slug", help="New slug for the application."),
):
    """
    Update an application.
    """
    client = get_client()
    applications_api = api.ApplicationsApi(client)
    try:
        update_data = PatchedApplicationRequest()
        if name is not None:
            update_data.name = name
        if slug is not None:
            update_data.slug = slug

        if not update_data.model_dump(exclude_unset=True):
            console.print("[bold yellow]No fields to update.[/bold yellow]")
            return

        updated_app = applications_api.applications_partial_update(application_uuid=app_id, patched_application_request=update_data)
        console.print(f"[bold green]Application '{updated_app.name}' (ID: {updated_app.pk}) updated successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error updating application: {e}[/bold red]")

@app_app.command("delete")
def delete_application(app_id: str = typer.Argument(..., help="The ID of the application to delete.")):
    """
    Delete an application.
    """
    client = get_client()
    applications_api = api.ApplicationsApi(client)
    try:
        applications_api.applications_destroy(application_uuid=app_id)
        console.print(f"[bold green]Application with ID {app_id} deleted successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error deleting application: {e}[/bold red]")

app.add_typer(app_app, name="application")
