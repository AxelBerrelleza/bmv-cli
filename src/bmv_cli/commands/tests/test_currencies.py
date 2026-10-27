import pytest
from typer.testing import CliRunner

from bmv_cli.commands.currencies import app
from bmv_cli.commands.tests.fixtures import currencies_response

runner = CliRunner()


@pytest.fixture
def mock_currencies_api(requests_mock):
    """Mock the divisas API endpoint."""
    response = currencies_response()
    requests_mock.get(
        "https://api.databursatil.com/v2/divisas",
        json=response,
    )
    return response


def test_currencies_command(requests_mock, mock_currencies_api):
    """Test currencies command with mocked API."""
    result = runner.invoke(app, [], env={"COLUMNS": "200"})

    assert result.exit_code == 0
    # Check that some currencies appear in output
    assert "USDMXN" in result.stdout
    assert "EURUSD" in result.stdout


def test_currencies_table_data(requests_mock, mock_currencies_api):
    """Verify table output contains expected currency data."""
    result = runner.invoke(app, [], env={"COLUMNS": "200"})

    assert result.exit_code == 0
    # Check for table headers
    assert "Currency" in result.stdout
    assert "Last Value" in result.stdout
    # Check for specific currency values from the fixture
    assert "17.5147" in result.stdout  # USDMXN rate
    assert "1.1408" in result.stdout  # EURUSD rate


def test_currencies_date_display(requests_mock, mock_currencies_api):
    """Verify date display."""
    result = runner.invoke(app, [], env={"COLUMNS": "200"})

    assert result.exit_code == 0
    # Check that the datetime is displayed
    assert "Datetime:" in result.stdout
    assert "2026-06-26 04:01:00" in result.stdout
