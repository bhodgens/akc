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


@app_app.command("assign-provider")
def assign_provider(
    app_id: str = typer.Argument(..., help="The UUID of the application."),
    provider_id: int = typer.Argument(..., help="The ID of the provider to assign."),
):
    """Assign a provider to an application."""
    client = get_client()
    applications_api = api.ApplicationsApi(client)
    try:
        update_data = PatchedApplicationRequest(provider=provider_id)
        updated_app = applications_api.applications_partial_update(
            application_uuid=app_id, patched_application_request=update_data
        )
        console.print(
            f"[bold green]Provider with ID {provider_id} assigned to application '{updated_app.name}' successfully.[/bold green]"
        )
    except ApiException as e:
        console.print(f"[bold red]Error assigning provider: {e.body}[/bold red]")


@app_app.command("bind-flow")
def bind_flow(
    app_id: str = typer.Argument(..., help="The UUID of the application."),
    flow_slug: str = typer.Argument(..., help="The slug of the flow to bind."),
    flow_type: str = typer.Option(
        "authorization",
        "--flow-type",
        "-t",
        help="The type of flow to bind (e.g., authorization, authentication, invalidation).",
    ),
):
    """Bind a flow to an application."""
    client = get_client()
    applications_api = api.ApplicationsApi(client)
    flows_api = api.FlowsApi(client)

    try:
        # Find the flow by slug to get its UUID
        flows = flows_api.flows_instances_list(slug=flow_slug)
        if not flows.results:
            console.print(f"[bold red]Flow with slug '{flow_slug}' not found.[/bold red]")
            raise typer.Exit(1)
        flow_uuid = flows.results[0].pk

        update_data = PatchedApplicationRequest()
        if flow_type == "authorization":
            update_data.authorization_flow = flow_uuid
        elif flow_type == "authentication":
            update_data.authentication_flow = flow_uuid
        elif flow_type == "invalidation":
            update_data.invalidation_flow = flow_uuid
        else:
            console.print(f"[bold red]Invalid flow type '{flow_type}'.[/bold red]")
            raise typer.Exit(1)

        updated_app = applications_api.applications_partial_update(
            application_uuid=app_id, patched_application_request=update_data
        )
        console.print(
            f"[bold green]Flow '{flow_slug}' bound to application '{updated_app.name}' as {flow_type} flow.[/bold green]"
        )
    except ApiException as e:
        console.print(f"[bold red]Error binding flow: {e.body}[/bold red]")


app.add_typer(app_app, name="application")
