## 1. API Investigation

- [ ] 1.1 Review DataBursatil API documentation for current specification
- [ ] 1.2 Identify breaking changes (authentication, endpoints, parameters, response format)
- [ ] 1.3 Document findings in a research note or issue comment
- [ ] 1.4 Test current API endpoints manually to confirm failures

## 2. Authentication Update

- [ ] 2.1 Update authentication method in `api/client.py` (token → new auth mechanism)
- [ ] 2.2 Update `.env.sample` with new environment variable names if changed
- [ ] 2.3 Update `AGENTS.md` setup instructions

## 3. Endpoint & Request Updates

- [ ] 3.1 Update `get_base_url()` in `api/client.py` with current endpoint paths
- [ ] 3.2 Update `request_prices()` query parameters (`concepto`, `emisora_serie`, `bolsa`)
- [ ] 3.3 Update `request_currencies()` query parameters
- [ ] 3.4 Verify requests succeed with updated parameters

## 4. Response Parsing Updates

- [ ] 4.1 Update `commands/price.py` to handle new response structure
- [ ] 4.2 Update `commands/currencies.py` to handle new response structure
- [ ] 4.3 Adjust field name mappings and data extraction logic
- [ ] 4.4 Verify Rich table output displays correctly

## 5. Testing & Verification

- [ ] 5.1 Test price command with live API: `uv run python main.py price AAPL`
- [ ] 5.2 Test currencies command with live API: `uv run python main.py currencies`
- [ ] 5.3 Update test fixtures in `commands/tests/fixtures/APIResponses.py` (if tests exist)
- [ ] 5.4 Run all quality gates: `ruff format --check`, `ruff check`, `mypy`, `pytest`

## 6. Documentation

- [ ] 6.1 Update `AGENTS.md` with current API documentation links
- [ ] 6.2 Remove "BROKEN" status warning from `AGENTS.md`
- [ ] 6.3 Document any new setup requirements or configuration changes
