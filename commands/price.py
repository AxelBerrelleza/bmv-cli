from typing import List

import typer
from rich.console import Console
from rich.table import Table

from api.client import request_prices

app = typer.Typer()


@app.command()
def price(symbols: List[str]):
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
        if data["bmv"]["f"] > data["biva"]["f"]:
            row = data["bmv"]
        else:
            row = data["biva"]
        table.add_row(symbol, *[str(value) for value in row.values()])

    console = Console()
    console.print(table)
