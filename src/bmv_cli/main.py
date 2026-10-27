import typer

from bmv_cli.commands.credits import app as credits
from bmv_cli.commands.currencies import app as currencies
from bmv_cli.commands.dividend import app as dividend
from bmv_cli.commands.hello import app as hello
from bmv_cli.commands.price import app as price
from bmv_cli.commands.search import app as search

app = typer.Typer()
app.add_typer(hello)
app.add_typer(price)
app.add_typer(currencies)
app.add_typer(credits)
app.add_typer(search)
app.add_typer(dividend)


if __name__ == "__main__":
    app()
