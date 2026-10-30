## 1. API Investigation

- [x] 1.1 Review DataBursatil API documentation for current specification
- [x] 1.2 Identify breaking changes (authentication, endpoints, parameters, response format)
- [x] 1.3 Document findings in a research note or issue comment
- [x] 1.4 Test current API endpoints manually to confirm failures

## 2. Authentication Update

- [x] 2.1 Update authentication method in `api/client.py` (token → new auth mechanism)
- [x] 2.2 Update `.env.sample` with new environment variable names if changed
- [x] 2.3 Update `AGENTS.md` setup instructions

## 3. Endpoint & Request Updates

- [x] 3.1 Update `get_base_url()` in `api/client.py` with current endpoint paths
- [x] 3.2 Update `request_prices()` query parameters (`concepto`, `emisora_serie`, `bolsa`)
- [x] 3.3 Update `request_currencies()` query parameters
- [x] 3.4 Verify requests succeed with updated parameters

## 4. Response Parsing Updates

- [x] 4.1 Update `commands/price.py` to handle new response structure
- [x] 4.2 Update `commands/currencies.py` to handle new response structure
- [x] 4.3 Adjust field name mappings and data extraction logic
- [x] 4.4 Verify Rich table output displays correctly

## 5. Testing & Verification

- [x] 5.1 Test price command with live API: `uv run python main.py price AAPL`
- [x] 5.2 Test currencies command with live API: `uv run python main.py currencies`
- [x] 5.3 Update test fixtures in `commands/tests/fixtures/APIResponses.py` (if tests exist)
- [x] 5.4 Run all quality gates: `ruff format --check`, `ruff check`, `mypy`, `pytest`

## 6. Documentation

- [x] 6.1 Update `AGENTS.md` with current API documentation links
- [x] 6.2 Remove "BROKEN" status warning from `AGENTS.md`
- [x] 6.3 Document any new setup requirements or configuration changes
