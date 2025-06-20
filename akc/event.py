import typer
from rich.console import Console
from rich.table import Table
import json

from authentik_client.api.events_api import EventsApi
from authentik_client.exceptions import ApiException

from .main import get_client, app

event_app = typer.Typer()
console = Console()

@event_app.command("list")
def list_events(output: str = typer.Option("table", "--output", "-o", help="Output format (table or json)")):
    """
    List all events.
    """
    client = get_client()
    events_api = EventsApi(client)
    try:
        events = events_api.events_events_list()
        if output == "json":
            console.print(json.dumps([e.to_dict() for e in events.results], indent=2))
        else:
            table = Table(title="Events")
            table.add_column("UUID", style="cyan")
            table.add_column("User", style="magenta")
            table.add_column("Action", style="green")
            table.add_column("App", style="yellow")
            table.add_column("Created", style="blue")
            for event in events.results:
                table.add_row(
                    event.pk,
                    event.user.get("username"),
                    event.action,
                    event.app,
                    str(event.created),
                )
            console.print(table)
    except ApiException as e:
        console.print(f"[bold red]Error listing events: {e.body}[/bold red]")

@event_app.command("get")
def get_event(uuid: str = typer.Argument(..., help="The UUID of the event to get.")):
    """
    Get an event.
    """
    client = get_client()
    events_api = EventsApi(client)
    try:
        event = events_api.events_events_retrieve(event_uuid=uuid)
        console.print(event.to_dict())
    except ApiException as e:
        console.print(f"[bold red]Error getting event: {e.body}[/bold red]")

app.add_typer(event_app, name="event")

