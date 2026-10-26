import typer
from rich.console import Console
from rich.table import Table

from api.client import request_emisoras

app = typer.Typer()


@app.command()
def search(
    text: str = typer.Argument(..., help="Search text (letter or company name)"),
    market: str = typer.Option(
        "local",
        "--market",
        "-m",
        help="Market type: local or global",
        case_sensitive=False,
    ),
):
    """Search for stock symbols"""
    response = request_emisoras(text, market)
    table = Table(
        "Symbol",
        "Status",
        "Company Name",
        "Exchange",
        "Type",
        "Shares Outstanding",
        "ISIN",
    )

    console = Console()

    # Response structure: {SYMBOL: {SERIE: {data...}}}
    for symbol, series_data in response.items():
        for serie, data in series_data.items():
            if isinstance(data, dict):
                table.add_row(
                    f"{symbol}{serie}",
                    data.get("estatus", "N/A"),
                    data.get("razon_social", "N/A"),
                    data.get("bolsa", "N/A"),
                    data.get("tipo_valor_descripcion", "N/A"),
                    str(data.get("acciones_en_circulacion", "N/A")),
                    data.get("isin", "N/A"),
                )

    console.print(table)
