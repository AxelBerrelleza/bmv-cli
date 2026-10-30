## Why

The BMV CLI tool is currently non-functional because DataBursatil released breaking changes to their API. The tool cannot retrieve stock prices or currency data, rendering it useless for its intended purpose.

Investigating and updating the API integration to match DataBursatil's current API specification restores core functionality and allows users to retrieve Mexican stock market data as originally intended.

## What Changes

- **Investigate API changes**: Review DataBursatil API documentation to identify what changed (endpoints, authentication, request/response format, rate limits).
- **Update authentication**: Migrate from `token` query parameter to whatever authentication method DataBursatil now uses (API key header, OAuth, etc.).
- **Update endpoint paths**: Modify `api/client.py` to use current endpoint paths for `cotizaciones` (quotes) and `divisas` (currencies).
- **Update request parameters**: Adjust query parameters to match current API specification (e.g., `concepto`, `emisora_serie`, `bolsa`).
- **Update response parsing**: Modify `commands/price.py` and `commands/currencies.py` to handle current response structure (field names, nesting, data types).
- **Update environment variables**: Adjust `.env.sample` and `AGENTS.md` if environment variable names change.
- **Test with live API**: Verify updated integration works with real DataBursatil API responses.
- **Update tests**: Adjust test fixtures in `commands/tests/fixtures/APIResponses.py` to match new response format (once tests are written).

## Capabilities

### New Capabilities
(none — restores existing capability)

### Modified Capabilities
- `api-integration`: Updated DataBursatil API client to match current API specification.

## Impact

- **API client**: Significant changes to `api/client.py` — base URL, authentication, request parameters, response handling.
- **Commands**: Updates to `commands/price.py` and `commands/currencies.py` — response field mapping, data extraction logic.
- **Configuration**: Possible changes to `.env.sample`, `.env`, and environment variable names.
- **Documentation**: Update `AGENTS.md` with current API documentation links and setup instructions.
- **Tests**: Update mock fixtures to match new response format (coordinate with `add-test-coverage` change).
- **Dependencies**: May need to update `requests` or add new authentication libraries if API requires OAuth or similar.

## Risks & Unknowns

- **API documentation availability**: DataBursatil may not publish comprehensive API docs; may require reverse-engineering or contacting support.
- **Breaking changes scope**: Unknown whether changes are minor (endpoint paths) or major (authentication flow, response structure).
- **Rate limits**: New API may have different rate limits requiring request throttling.
- **Data format**: Response structure may be fundamentally different, requiring significant refactoring of command logic.

## Investigation Steps

1. Check if DataBursatil has published migration guides or changelogs
2. Review any error messages from current API calls to identify specific failures
3. Test API endpoints manually with curl/httpie to understand current behavior
4. Contact DataBursatil support if documentation is unclear or unavailable
5. Compare old vs new response structures to identify mapping changes
