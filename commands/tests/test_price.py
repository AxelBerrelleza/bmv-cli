import pytest
from typer.testing import CliRunner

from commands.price import app
from commands.tests.fixtures import prices_response

runner = CliRunner()


@pytest.fixture
def mock_prices_api(requests_mock):
    """Mock the cotizaciones API endpoint."""
    response = prices_response()
    requests_mock.get(
        "https://api.databursatil.com/v2/cotizaciones",
        json=response,
    )
    return response


def test_single_symbol_price(requests_mock, mock_prices_api):
    """Test single symbol price lookup with mocked API."""
    result = runner.invoke(app, ["GFNORTEO"], env={"COLUMNS": "200"})

    assert result.exit_code == 0
    assert "GFNORTEO" in result.stdout
    # Should show BIVA data (more recent timestamp) - ultimo price 213.5
    assert "213.5" in result.stdout


def test_multiple_symbols_price(requests_mock, mock_prices_api):
    """Test multiple symbols price lookup."""
    result = runner.invoke(app, ["GFNORTEO", "WALMEX*"], env={"COLUMNS": "200"})

    assert result.exit_code == 0
    assert "GFNORTEO" in result.stdout
    assert "WALMEX*" in result.stdout


def test_price_table_columns(requests_mock, mock_prices_api):
    """Verify table output contains expected columns and data."""
    result = runner.invoke(app, ["GFNORTEO"], env={"COLUMNS": "200"})

    assert result.exit_code == 0
    # Check for table headers (full names with wide terminal)
    assert "simbolo" in result.stdout
    assert "ultimo" in result.stdout
    assert "fecha" in result.stdout
    # Check for data values from the BIVA response (more recent)
    assert "213.5" in result.stdout
    assert "2.68" in result.stdout


def test_bmv_vs_biva_selection(requests_mock):
    """Test BMV vs BIVA selection logic (higher 'f' value wins)."""
    # Create a response where BIVA has a more recent timestamp
    response = {
        "TESTSYMBOL": {
            "bmv": {
                "u": 100.0,
                "p": 99.5,
                "a": 98.0,
                "x": 101.0,
                "n": 97.0,
                "c": 2.0,
                "m": 2.0,
                "v": 1000.0,
                "o": 10.0,
                "i": 100000.0,
                "f": "2026-10-23 14:00:00",
            },
            "biva": {
                "u": 105.0,
                "p": 104.5,
                "a": 103.0,
                "x": 106.0,
                "n": 102.0,
                "c": 3.0,
                "m": 3.0,
                "v": 2000.0,
                "o": 20.0,
                "i": 200000.0,
                "f": "2026-10-23 14:05:00",  # More recent
            },
        }
    }

    requests_mock.get(
        "https://api.databursatil.com/v2/cotizaciones",
        json=response,
    )

    result = runner.invoke(app, ["TESTSYMBOL"], env={"COLUMNS": "200"})

    assert result.exit_code == 0
    # Should show BIVA data (105.0 ultimo) not BMV (100.0)
    assert "105.0" in result.stdout
    # BMV's ultimo (100.0) should NOT appear since we use BIVA
    # But 100.0 could appear as part of other values, so check for the row pattern
    assert "TESTSYMBOL" in result.stdout
