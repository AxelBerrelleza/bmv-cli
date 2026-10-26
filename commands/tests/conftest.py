import pytest


@pytest.fixture
def cli_runner():
    """Provide a Typer CliRunner for testing CLI commands."""
    from typer.testing import CliRunner

    return CliRunner()
