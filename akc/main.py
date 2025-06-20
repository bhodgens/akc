#!/usr/bin/env python3
import json
import os
import sys
from authentik_client.api_client import ApiClient as Client
import typer
from rich.console import Console

app = typer.Typer(add_completion=True)
console = Console()

CONFIG_PATH = os.path.expanduser("~/.akc_config.json")

def get_client():
    if not os.path.exists(CONFIG_PATH):
        console.print(f"[bold red]Config file not found at {CONFIG_PATH}. Please create it with your Authentik URL and API token by running `akc init`[/bold red]")
        raise typer.Exit(code=1)
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    return Client(base_url=config["base_url"], api_token=config["api_token"])

@app.command()
def init(
    url: str = typer.Option(..., prompt="Authentik URL"),
    token: str = typer.Option(..., prompt="API Token", hide_input=True),
):
    """
    Initialize the CLI with your Authentik URL and API token.
    """
    config = {
        "base_url": url,
        "api_token": token,
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    console.print(f"Config saved to {CONFIG_PATH}")

from . import user, group, role, application, user_group, user_role, provider, flow, core, outpost, event, propertymapping, policy, stage, source

if __name__ == "__main__":
    app.add_typer(core.app, name="core")
    app.add_typer(outpost.outpost_app, name="outpost")
    app.add_typer(event.event_app, name="event")
    app.add_typer(propertymapping.propertymapping_app, name="propertymapping")
    app.add_typer(policy.policy_app, name="policy")
    app.add_typer(stage.stage_app, name="stage")
    app.add_typer(source.source_app, name="source")
    app()
