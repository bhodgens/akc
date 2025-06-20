import json

import typer
from rich.console import Console
from rich.table import Table

from authentik_client import api
from authentik_client.exceptions import ApiException
from authentik_client.models import OAuth2ProviderRequest

from .main import get_client, app

provider_app = typer.Typer()
console = Console()


@provider_app.command("create-oauth2")
def create_oauth2_provider(
    name: str = typer.Argument(..., help="The name of the provider."),
    authorization_flow_slug: str = typer.Argument(..., help="The slug of the authorization flow."),
    client_type: str = typer.Option("confidential", help="Client type ('confidential' or 'public')."),
    redirect_uris: str = typer.Option("", help="Redirect URIs (comma-separated)."),
):
    """Create a new OAuth2 provider."""
    client = get_client()
    providers_api = api.ProvidersApi(client)
    flows_api = api.FlowsApi(client)
    try:
        # Find the authorization flow by slug to get its UUID
        flows = flows_api.flows_instances_list(slug=authorization_flow_slug)
        if not flows.results:
            console.print(f"[bold red]Authorization flow with slug '{authorization_flow_slug}' not found.[/bold red]")
            raise typer.Exit(1)
        authorization_flow_uuid = flows.results[0].pk

        provider_request = OAuth2ProviderRequest(
            name=name,
            authorization_flow=authorization_flow_uuid,
            client_type=client_type,
            redirect_uris=redirect_uris,
        )
        new_provider = providers_api.providers_oauth2_create(oauth2_provider_request=provider_request)
        console.print(f"[bold green]OAuth2 provider '{new_provider.name}' created successfully with ID {new_provider.pk}.[/bold green]")
        console.print(f"Client ID: {new_provider.client_id}")
        if new_provider.client_secret:
             console.print(f"Client Secret: {new_provider.client_secret}")

    except ApiException as e:
        console.print(f"[bold red]Error creating OAuth2 provider: {e.body}[/bold red]")


@provider_app.command("list")
def list_providers(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all providers.
    """
    client = get_client()
    providers_api = api.ProvidersApi(client)
    try:
        providers = providers_api.providers_all_list()
        if output == "json":
            console.print(json.dumps([p.to_dict() for p in providers.results], indent=2))
        else:
            table = Table(title="Providers")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Component", style="green")
            for provider in providers.results:
                table.add_row(
                    str(provider.pk),
                    provider.name,
                    provider.component,
                )
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing providers: {e.body}[/bold red]")


@provider_app.command("get")
def get_provider(provider_id: int = typer.Argument(..., help="The ID of the provider to get.")):
    """Get a single provider."""
    client = get_client()
    providers_api = api.ProvidersApi(client)
    try:
        provider = providers_api.providers_all_retrieve(provider_id=provider_id)
        console.print(provider.to_dict())
    except ApiException as e:
        console.print(f"[bold red]Error getting provider: {e.body}[/bold red]")


@provider_app.command("delete")
def delete_provider(provider_id: int = typer.Argument(..., help="The ID of the provider to delete.")):
    """
    Delete a provider.
    """
    client = get_client()
    providers_api = api.ProvidersApi(client)
    try:
        providers_api.providers_all_destroy(provider_id=provider_id)
        console.print(f"[bold green]Provider with ID {provider_id} deleted successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error deleting provider: {e.body}[/bold red]")


@provider_app.command("list-types")
def list_provider_types():
    """List all available provider types."""
    client = get_client()
    providers_api = api.ProvidersApi(client)
    try:
        types = providers_api.providers_all_types_list()
        console.print([t.to_dict() for t in types])
    except ApiException as e:
        console.print(f"[bold red]Error listing provider types: {e.body}[/bold red]")


@provider_app.command("use")
def get_provider_use(provider_id: int = typer.Argument(..., help="The ID of the provider to check.")):
    """Check which objects are using a provider."""
    client = get_client()
    providers_api = api.ProvidersApi(client)
    try:
        used_by = providers_api.providers_all_used_by_list(provider_id=provider_id)
        console.print([item.to_dict() for item in used_by])
    except ApiException as e:
        console.print(f"[bold red]Error getting provider usage: {e.body}[/bold red]")


app.add_typer(provider_app, name="provider")
