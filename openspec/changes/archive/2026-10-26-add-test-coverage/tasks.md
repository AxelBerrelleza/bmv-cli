## 1. Test Fixtures

- [x] 1.1 Create `commands/tests/fixtures/` directory
- [x] 1.2 Create `commands/tests/fixtures/__init__.py`
- [x] 1.3 Create `commands/tests/fixtures/APIResponses.py` with mock responses for price and currencies endpoints

## 2. Hello Command Tests

- [x] 2.1 Create `commands/tests/test_hello.py`
- [x] 2.2 Test hello command output using `CliRunner`
- [x] 2.3 Verify exit code is 0

## 3. Price Command Tests

- [x] 3.1 Create `commands/tests/test_price.py`
- [x] 3.2 Test single symbol price lookup with mocked API
- [x] 3.3 Test multiple symbols price lookup
- [x] 3.4 Verify table output contains expected columns and data
- [x] 3.5 Test BMV vs BIVA selection logic (higher `f` value wins)

## 4. Currencies Command Tests

- [x] 4.1 Create `commands/tests/test_currencies.py`
- [x] 4.2 Test currencies command with mocked API
- [x] 4.3 Verify table output contains expected currency data
- [x] 4.4 Verify date display

## 5. Documentation

- [x] 5.1 Update `AGENTS.md` with test examples and fixture usage patterns
