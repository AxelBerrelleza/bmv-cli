import typer

from commands.currencies import app as currencies
from commands.hello import app as hello
from commands.price import app as price

app = typer.Typer()
app.add_typer(hello)
app.add_typer(price)
app.add_typer(currencies)


if __name__ == "__main__":
    app()
