import json

import typer
from rich.console import Console
from rich.table import Table

from authentik_client import api
from authentik_client.exceptions import ApiException
from authentik_client.models import PolicyBindingRequest

from .main import get_client, app

policy_app = typer.Typer()
console = Console()

@policy_app.command("list")
def list_policies(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all policies.
    """
    client = get_client()
    policies_api = api.PoliciesApi(client)
    try:
        policies = policies_api.policies_all_list()
        if output == "json":
            console.print(json.dumps([p.to_dict() for p in policies.results], indent=2))
        else:
            table = Table(title="Policies")
            table.add_column("UUID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Component", style="green")
            table.add_column("Bound To", style="yellow")
            for policy in policies.results:
                table.add_row(
                    policy.pk,
                    policy.name,
                    policy.component,
                    str(policy.bound_to)
                )
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing policies: {e.body}[/bold red]")

@policy_app.command("get")
def get_policy(uuid: str = typer.Argument(..., help="The UUID of the policy to get.")):
    """
    Get a policy.
    """
    client = get_client()
    policies_api = api.PoliciesApi(client)
    try:
        policy = policies_api.policies_all_retrieve(policy_uuid=uuid)
        console.print(policy.to_dict())
    except ApiException as e:
        console.print(f"[bold red]Error getting policy: {e.body}[/bold red]")

@policy_app.command("delete")
def delete_policy(uuid: str = typer.Argument(..., help="The UUID of the policy to delete.")):
    """
    Delete a policy.
    """
    client = get_client()
    policies_api = api.PoliciesApi(client)
    try:
        policies_api.policies_all_destroy(policy_uuid=uuid)
        console.print(f"[bold green]Policy '{uuid}' deleted successfully.[/bold green]")
    except ApiException as e:
        console.print(f"[bold red]Error deleting policy: {e.body}[/bold red]")

@policy_app.command("use")
def get_policy_use(uuid: str = typer.Argument(..., help="The UUID of the policy to check.")):
    """Check which objects are using a policy."""
    client = get_client()
    policies_api = api.PoliciesApi(client)
    try:
        used_by = policies_api.policies_all_used_by_list(policy_uuid=uuid)
        console.print([item.to_dict() for item in used_by])
    except ApiException as e:
        console.print(f"[bold red]Error getting policy usage: {e.body}[/bold red]")


@policy_app.command("bind-to-app")
def bind_policy_to_app(
    policy_uuid: str = typer.Argument(..., help="The UUID of the policy to bind."),
    app_uuid: str = typer.Argument(..., help="The UUID of the application to bind to."),
    order: int = typer.Argument(..., help="The order of the policy binding."),
):
    """Bind a policy to an application."""
    client = get_client()
    policies_api = api.PoliciesApi(client)
    try:
        binding_request = PolicyBindingRequest(
            policy=policy_uuid,
            target=app_uuid,
            order=order,
        )
        policies_api.policies_bindings_create(policy_binding_request=binding_request)
        console.print(
            f"[bold green]Policy '{policy_uuid}' bound to application '{app_uuid}' successfully.[/bold green]"
        )
    except ApiException as e:
        console.print(f"[bold red]Error binding policy: {e.body}[/bold red]")


app.add_typer(policy_app, name="policy")
