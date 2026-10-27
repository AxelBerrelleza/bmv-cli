import typer
from rich.console import Console

from api.client import request_credits

app = typer.Typer()


@app.command()
def credits():
    """Check remaining API credits"""
    response = request_credits()
    console = Console()
    console.print(f"[bold green]Remaining credits:[/] {response['disponibles']}")
