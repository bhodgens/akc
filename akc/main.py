#!/usr/bin/env python3
import json
import os
import sys
from authentik_client.api_client import ApiClient as Client
import typer
from rich.console import Console

app = typer.Typer()
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

from . import user, group, role, application, user_group, user_role, provider

if __name__ == "__main__":
    app()
