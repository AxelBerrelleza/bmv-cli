# bmv-cli

A command-line interface for Mexican stock market (BMV/BIVA) data via the [DataBursatil](https://www.databursatil.com) API v2.

Get real-time quotes, currency rates, API credits, search for symbols, and dividend information — all from your terminal.

## Installation

### uv tool (recommended)
```bash
uv tool install bmv-cli
```

### pipx
```bash
pipx install bmv-cli
```

### pip
```bash
pip install bmv-cli
```

## Setup

You need a DataBursatil API token. Get one at <https://www.databursatil.com>.

Set the token as an environment variable:

```bash
export BMV_API_TOKEN="your-token-here"
```

For local development, you can also create a `.env` file in the project root:

```bash
cp .env.sample .env
# Edit .env and add your BMV_API_TOKEN
```

## Usage

All commands require the `BMV_API_TOKEN` environment variable.

### Get real-time prices
```bash
bmv price GFNORTEO WALMEX*
```

### Get currency exchange rates
```bash
bmv currencies
```

### Check remaining API credits
```bash
bmv credits
```

### Search for stock symbols
```bash
bmv search WALMEX
bmv search GFNORTE --market global
```

### Get dividend information
```bash
bmv dividend FMTY14
bmv dividend WALMEX*
```

## Development

```bash
# Clone and setup
git clone https://github.com/AxelBerrelleza/bmv-cli.git
cd bmv-cli
uv sync --extra dev

# Run quality gates
uv run ruff format --check .
uv run ruff check .
uv run mypy src/bmv_cli/api src/bmv_cli/commands
uv run pytest

# Run the CLI during development
uv run bmv --help
```

See [AGENTS.md](AGENTS.md) for detailed development instructions.