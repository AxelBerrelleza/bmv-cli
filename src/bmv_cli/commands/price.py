import typer
from rich.console import Console
from rich.table import Table

from bmv_cli.api.client import request_prices

app = typer.Typer()


@app.command()
def price(symbols: list[str]):
    response = request_prices(symbols)
    table = Table(
        "simbolo",
        "ultimo",
        "ppp",
        "anterior",
        "maximo",
        "minimo",
        "cambioporciento",
        "cambiopesos",
        "volumenoperado",
        "operaciones",
        "importeacumulado",
        "fecha",
    )
    for symbol, data in response.items():
        row = data["bmv"] if data["bmv"]["f"] > data["biva"]["f"] else data["biva"]
        table.add_row(symbol, *[str(value) for value in row.values()])

    console = Console()
    console.print(table)
