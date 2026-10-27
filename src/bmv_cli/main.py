import typer

from commands.credits import app as credits
from commands.currencies import app as currencies
from commands.dividend import app as dividend
from commands.hello import app as hello
from commands.price import app as price
from commands.search import app as search

app = typer.Typer()
app.add_typer(hello)
app.add_typer(price)
app.add_typer(currencies)
app.add_typer(credits)
app.add_typer(search)
app.add_typer(dividend)


if __name__ == "__main__":
    app()
