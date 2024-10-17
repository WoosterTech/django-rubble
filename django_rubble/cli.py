import typer

from django_rubble.secrets import env

app = typer.Typer()
app.add_typer(env.app, name="env")

if __name__ == "__main__":
    app()
