## Why

The test infrastructure is now in place (`commands/tests/` directory, `conftest.py` with fixtures, pytest configured), but the test suite contains zero actual tests. Without test coverage, we cannot verify that existing commands work correctly, catch regressions when modifying code, or safely refactor the codebase.

Writing tests for the existing commands (`price`, `currencies`, `hello`) using `requests-mock` to stub API calls and `typer.testing.CliRunner` to exercise the CLI provides confidence in current behavior and establishes patterns for future command development.

## What Changes

- **Add tests for `hello` command**: Verify the hello command outputs expected text using `CliRunner`.
- **Add tests for `price` command**: Mock DataBursatil API responses, verify table output includes expected symbols and data fields, test single and multiple symbol inputs.
- **Add tests for `currencies` command**: Mock DataBursatil API responses, verify currency table output, test date display.
- **Create API response fixtures**: Add `commands/tests/fixtures/` directory with realistic mock responses in `APIResponses.py` for reuse across tests.
- **Document test patterns**: Update `AGENTS.md` with test examples and fixture usage patterns.

## Capabilities

### New Capabilities
- `test-coverage`: Comprehensive test suite for existing CLI commands with mocked API responses.

### Modified Capabilities
(none — adds tests without modifying existing command behavior)

## Impact

- **Test files**: Add `commands/tests/test_hello.py`, `commands/tests/test_price.py`, `commands/tests/test_currencies.py`.
- **Test fixtures**: Add `commands/tests/fixtures/__init__.py` and `commands/tests/fixtures/APIResponses.py` with mock response data.
- **Documentation**: Update `AGENTS.md` testing conventions section with examples.
- **Quality gates**: `pytest` will now execute actual tests instead of reporting "no tests collected."
- **Non-Goals**:
  - *Test coverage measurement*: Setting minimum coverage thresholds (e.g., 80%) is out of scope.
  - *Integration tests*: Tests will mock all external API calls; no live API testing.
