## 1. Test Fixtures

- [ ] 1.1 Create `commands/tests/fixtures/` directory
- [ ] 1.2 Create `commands/tests/fixtures/__init__.py`
- [ ] 1.3 Create `commands/tests/fixtures/APIResponses.py` with mock responses for price and currencies endpoints

## 2. Hello Command Tests

- [ ] 2.1 Create `commands/tests/test_hello.py`
- [ ] 2.2 Test hello command output using `CliRunner`
- [ ] 2.3 Verify exit code is 0

## 3. Price Command Tests

- [ ] 3.1 Create `commands/tests/test_price.py`
- [ ] 3.2 Test single symbol price lookup with mocked API
- [ ] 3.3 Test multiple symbols price lookup
- [ ] 3.4 Verify table output contains expected columns and data
- [ ] 3.5 Test BMV vs BIVA selection logic (higher `f` value wins)

## 4. Currencies Command Tests

- [ ] 4.1 Create `commands/tests/test_currencies.py`
- [ ] 4.2 Test currencies command with mocked API
- [ ] 4.3 Verify table output contains expected currency data
- [ ] 4.4 Verify date display

## 5. Documentation

- [ ] 5.1 Update `AGENTS.md` with test examples and fixture usage patterns
