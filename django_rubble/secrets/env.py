"""This is a cli tool."""

from pathlib import Path

import typer

from django_rubble.secrets.utilities import create_env_sample, find_secrets_in_settings

app = typer.Typer()


@app.command()
def create_sample(
    settings_file: Path,
    output_file: Path,
):
    """Create a sample .env file from a Django settings file."""

    secrets = find_secrets_in_settings(settings_file)
    create_env_sample(secrets, output_file)
    typer.echo(f"Sample .env file created at {output_file}")
