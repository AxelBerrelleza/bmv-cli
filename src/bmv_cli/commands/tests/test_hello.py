from typer.testing import CliRunner

from bmv_cli.commands.hello import app


def test_hello_command():
    """Test hello command output and exit code."""
    runner = CliRunner()
    result = runner.invoke(app, [])

    assert result.exit_code == 0
    assert "Hello world" in result.stdout
