import re

import typer
from rich.console import Console
from rich.table import Table

from api.client import request_emisoras

app = typer.Typer()


def extract_emitter_name(symbol: str) -> str:
    """Extract emitter name from symbol+series (e.g., FMTY14 -> FMTY, GFNORTEO -> GFNORTE, WALMEX* -> WALMEX)"""
    symbol = symbol.upper()

    # If ends with *, strip it
    if symbol.endswith("*"):
        return symbol[:-1]

    # If ends with digits, strip them
    match = re.match(r"^([A-Z]+)\d+$", symbol)
    if match:
        return match.group(1)

    # If ends with a single letter, try stripping it (risky but common pattern)
    # Only do this if the remaining part is at least 3 characters
    if len(symbol) > 3 and symbol[-1].isalpha():
        return symbol[:-1]

    return symbol


@app.command()
def dividend(
    symbol: str = typer.Argument(..., help="Stock symbol (e.g., FMTY, FMTY14, WALMEX*)"),
):
    """Get dividend information for a symbol"""
    console = Console()

    # Try the symbol as-is first
    response = request_emisoras(symbol)

    # If API returns an error, try extracting just the emitter name
    if "Error" in response:
        emitter_name = extract_emitter_name(symbol)
        if emitter_name != symbol:
            console.print(f"[yellow]Trying with emitter name: {emitter_name}[/yellow]")
            response = request_emisoras(emitter_name)

    # Still an error?
    if "Error" in response:
        console.print(f"[red]Error: {response['Error']}[/red]")
        raise typer.Exit(code=1)

    # Response structure: {SYMBOL: {SERIE: {data...}}}
    found = False
    for emitter_key, series_data in response.items():
        if not isinstance(series_data, dict):
            continue

        for serie, data in series_data.items():
            if not isinstance(data, dict):
                continue

            dividendos = data.get("dividendos", {})
            found = True

            if not dividendos:
                console.print(
                    f"[yellow]No dividend information available for {emitter_key}{serie}[/yellow]"
                )
                continue

            console.print(f"\n[bold]Dividend Info for {emitter_key}{serie}:[/]")

            # Recent dividend
            if "reciente" in dividendos:
                console.print("\n[bold green]Most Recent Dividend(s):[/]")
                for date, info in dividendos["reciente"].items():
                    console.print(f"  Date: {date}")
                    console.print(f"  Ex-coupon Date: {info.get('fechaexcupon', 'N/A')}")
                    console.print(f"  Amount: {info.get('pago', 'N/A')} {info.get('divisa', '')}")
                    console.print(f"  Type: {info.get('tipo', 'N/A')}")
                    console.print()

            # Historical dividends
            if "historico" in dividendos:
                console.print("\n[bold blue]Dividend History:[/]")
                table = Table("Date", "Amount", "Type")

                for date, info in dividendos["historico"].items():
                    table.add_row(
                        date,
                        str(info.get("pago", "N/A")),
                        info.get("tipo", "N/A"),
                    )

                console.print(table)

    if not found:
        console.print(f"[red]No data found for symbol: {symbol}[/red]")
        raise typer.Exit(code=1)
