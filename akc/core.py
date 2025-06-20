import typer
from rich.console import Console
from rich.table import Table

from authentik_client import api
from authentik_client.exceptions import ApiException
from authentik_client.models.patched_tenant_request import PatchedTenantRequest
from authentik_client.models.tenant_request import TenantRequest

from .main import get_client

app = typer.Typer()


@app.command()
def get_version():
    """Get the version of the Authentik API."""
    client = get_client()
    core_api = api.CoreApi(client)
    console = Console()
    try:
        version = core_api.core_version_retrieve()
        console.print(version.to_dict())
    except ApiException as e:
        console.print(f"[bold red]Error: {e.body}[/bold red]")


@app.command()
def list_tenants(output: str = typer.Option("table", help="Output format (table or json)")):
    """List all tenants."""
    client = get_client()
    core_api = api.CoreApi(client)
    console = Console()
    try:
        tenants = core_api.core_tenants_list()
        if output == "json":
            console.print([t.to_dict() for t in tenants.results])
        else:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Tenant UUID")
            table.add_column("Schema Name")
            table.add_column("Name")
            table.add_column("Domain")
            for tenant in tenants.results:
                table.add_row(
                    tenant.tenant_uuid,
                    tenant.schema_name,
                    tenant.name,
                    tenant.domain if tenant.domain else ""
                )
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error: {e.body}[/bold red]")


@app.command()
def create_tenant(
    schema_name: str = typer.Argument(..., help="The schema name of the tenant."),
    name: str = typer.Option(None, help="The name of the tenant."),
    domain: str = typer.Option(None, help="The domain of the tenant."),
):
    """Create a new tenant."""
    client = get_client()
    core_api = api.CoreApi(client)
    console = Console()
    try:
        tenant_data = TenantRequest(schema_name=schema_name)
        if name:
            tenant_data.name = name
        if domain:
            tenant_data.domain = domain

        new_tenant = core_api.core_tenants_create(tenant_request=tenant_data)
        console.print(f"[bold green]Tenant '{new_tenant.name}' created successfully.[/bold green]")
        console.print(new_tenant.to_dict())
    except ApiException as e:
        console.print(f"[bold red]Error: {e.body}[/bold red]")


@app.command()
def update_tenant(
    tenant_uuid: str = typer.Argument(..., help="The UUID of the tenant."),
    schema_name: str = typer.Option(None, help="The schema name of the tenant."),
    name: str = typer.Option(None, help="The name of the tenant."),
    domain: str = typer.Option(None, help="The domain of the tenant."),
):
    """Update a tenant."""
    client = get_client()
    core_api = api.CoreApi(client)
    console = Console()
    try:
        update_data = PatchedTenantRequest()
        if schema_name:
            update_data.schema_name = schema_name
        if name:
            update_data.name = name
        if domain:
            update_data.domain = domain

        updated_tenant = core_api.core_tenants_partial_update(
            tenant_uuid=tenant_uuid, patched_tenant_request=update_data
        )
        console.print(f"[bold green]Tenant '{updated_tenant.name}' updated successfully.[/bold green]")
        console.print(updated_tenant.to_dict())
    except ApiException as e:
        console.print(f"[bold red]Error: {e.body}[/bold red]")


@app.command()
def get_tenant(tenant_uuid: str = typer.Argument(..., help="The UUID of the tenant.")):
    """Get a tenant by UUID."""
    client = get_client()
    core_api = api.CoreApi(client)
    console = Console()
    try:
        tenant = core_api.core_tenants_retrieve(tenant_uuid=tenant_uuid)
        console.print(tenant.to_dict())
    except ApiException as e:
        console.print(f"[bold red]Error: {e.body}[/bold red]")


@app.command()
def delete_tenant(tenant_uuid: str = typer.Argument(..., help="The UUID of the tenant.")):
    """Delete a tenant by UUID."""
    client = get_client()
    core_api = api.CoreApi(client)
    console = Console()
    try:
        core_api.core_tenants_destroy(tenant_uuid=tenant_uuid)
        console.print(f"[bold green]Tenant with UUID '{tenant_uuid}' deleted successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error: {e.body}[/bold red]")
