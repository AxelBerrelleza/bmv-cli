## ADDED Requirements

### Requirement: MIT license declared with LICENSE file

The project SHALL include a `LICENSE` file (MIT) at the repository root and declare it in `pyproject.toml` using the PEP 639 SPDX expression `license = "MIT"` (replacing the legacy `license = { text = "MIT" }` table form), with the build requirement raised to `setuptools>=77`.

#### Scenario: License file and metadata agree

- **WHEN** `pyproject.toml` and the repository root are inspected
- **THEN** `license = "MIT"` is declared in `[project]` and a matching MIT `LICENSE` file exists

### Requirement: README serves as the package landing page

`README.md` SHALL document, in this order: what the CLI does; installation via `uv tool install bmv-cli` (and `pipx install bmv-cli` / `pip install bmv-cli`); obtaining and configuring the DataBursatil token (`BMV_API_TOKEN` env var, `.env` for local use); usage examples for every subcommand; and a short development section (uv sync, quality gates, link to AGENTS.md).

#### Scenario: A new user can install and run from the README alone

- **WHEN** a reader follows only the README's install and token steps, then runs the shown `bmv` example
- **THEN** they can execute `bmv price`, `bmv currencies`, `bmv credits`, `bmv search`, and `bmv dividend` successfully

#### Scenario: Usage examples cover all commands

- **WHEN** the README usage section is read
- **THEN** an example exists for each of: price, currencies, credits, search, dividend

### Requirement: Complete trove classifiers and project URLs

`pyproject.toml` SHALL declare classifiers appropriate to the project (environment, license, intended audience, Python versions 3.12–3.14, topic) and `[project.urls]` linking the GitHub repository (homepage, issues).

#### Scenario: Classifiers and URLs present in metadata

- **WHEN** `[project]` and `[project.urls]` in `pyproject.toml` are inspected
- **THEN** classifiers include `Environment :: Console`, `License :: OSI Approved :: MIT License` **or** the PEP 639 SPDX expression (expression present means the license classifier is omitted), `Programming Language :: Python :: 3.12`/`3.13`/`3.14`, and `[project.urls]` includes the GitHub repo and issues links
