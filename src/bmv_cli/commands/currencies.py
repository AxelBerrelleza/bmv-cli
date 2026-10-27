import typer
from rich.console import Console
from rich.table import Table

from bmv_cli.api.client import request_currencies

app = typer.Typer()


@app.command()
def currencies():
    response = request_currencies()
    table = Table(
        "Currency",
        "Last Value",
        "Change %",
        "Change",
    )
    date = response.get("t")
    response.pop("t")
    for currency, data in response.items():
        # pp(data)
        table.add_row(currency, *[str(value) for value in data.values()])

    console = Console()
    console.print(table)
    console.print(f"Datetime: {date}")
