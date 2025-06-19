import typer
from rich.console import Console
from rich.table import Table
import json
from authentik_client.models import Provider, PatchedProxyProviderRequest, ProxyProviderRequest
from .main import get_client, app

provider_app = typer.Typer()
console = Console()

@provider_app.command("list")
def list_providers(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all providers.
    """
    client = get_client()
    try:
        providers = client.providers.list()
        if output == "json":
            console.print(json.dumps([p.to_dict() for p in providers], indent=2))
        else:
            table = Table(title="Providers")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Authorization Flow", style="green")
            for provider in providers:
                table.add_row(
                    str(provider.id),
                    provider.name,
                    provider.authorization_flow.name,
                )
            console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error listing providers: {e}[/bold red]")

@provider_app.command("delete")
def delete_provider(provider_id: int = typer.Argument(..., help="The ID of the provider to delete.")):
    """
    Delete a provider.
    """
    client = get_client()
    try:
        client.providers.delete(provider_id)
        console.print(f"[bold green]Provider with ID {provider_id} deleted successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error deleting provider: {e}[/bold red]")

@provider_app.command("update")
def update_provider(
    provider_id: int = typer.Argument(..., help="The ID of the provider to update."),
    name: str = typer.Option(..., "--name", help="New name for the provider."),
):
    """
    Update a provider's name.
    """
    client = get_client()
    try:
        update_data = PatchedProxyProviderRequest(name=name)
        updated_provider = client.providers.partial_update(provider_id, patched_proxy_provider_request=update_data)
        console.print(f"[bold green]Provider '{updated_provider.name}' (ID: {updated_provider.id}) updated successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error updating provider: {e}[/bold red]")

@provider_app.command("create-proxy")
def create_proxy_provider(
    name: str = typer.Argument(..., help="The name of the proxy provider."),
    authorization_flow: str = typer.Argument(..., help="The authorization flow to use."),
    external_host: str = typer.Argument(..., help="The external host of the proxy provider."),
):
    """
    Create a new proxy provider.
    """
    client = get_client()
    try:
        provider = ProxyProviderRequest(
            name=name,
            authorization_flow=authorization_flow,
            external_host=external_host,
        )
        new_provider = client.providers.proxy_create(proxy_provider_request=provider)
        console.print(f"[bold green]Proxy provider '{new_provider.name}' created successfully.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error creating proxy provider: {e}[/bold red]")

app.add_typer(provider_app, name="provider")
