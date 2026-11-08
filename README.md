# VulnX

**Low-impact website security assessment toolkit**

VulnX is a cross-platform Python tool for developers and authorized security testers. It performs bounded, non-exploitative checks and provides a dark FastAPI dashboard, CLI, SQLite scan history, and exportable reports.

> **Authorization required:** assess only systems you own or have explicit written permission to test. Follow the agreed scope and applicable laws.

## Capabilities

- DNS A-record lookup and TLS certificate metadata
- HTTP security-header and cookie-attribute checks
- Bounded same-origin crawler using GET requests
- Indicators for a small set of commonly exposed resources
- Severity-ranked findings
- JSON, CSV, HTML, and optional PDF reports
- FastAPI dashboard and local SQLite history
- Linux, Kali Linux, and Windows support

VulnX does not attempt password guessing, authentication bypass, exploit payload injection, destructive testing, denial of service, or arbitrary port scanning.

## Project structure

~~~text
VulnX/
├── cli/                  # CLI implementation
├── config/               # Configuration notes
├── core/                 # Scanner, scope, crawler, persistence
├── docs/                 # Architecture and safe-use guide
├── modules/              # Individual assessment modules
├── reports/              # Report generation
├── storage/              # Local database (Git-ignored)
├── tests/                # Automated tests
├── web/
│   ├── static/           # Dashboard assets
│   ├── templates/        # Dashboard HTML
│   └── app.py            # FastAPI application
├── .github/workflows/    # CI
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── run.py
└── cli.py
~~~

## Requirements

- Python 3.10+
- Network access to resolve and reach an authorized public target

## Installation

### Linux / Kali Linux

~~~bash
git clone https://github.com/Rudra8927/VulnX.git
cd VulnX
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
~~~

### Windows PowerShell

~~~powershell
git clone https://github.com/Rudra8927/VulnX.git
Set-Location VulnX
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
~~~

## Start the dashboard

~~~bash
python run.py
~~~

Open http://127.0.0.1:8000. Keep the dashboard bound to localhost unless you have secured the deployment environment.

Alternative:

~~~bash
uvicorn web.app:app --host 127.0.0.1 --port 8000
~~~

## CLI usage

~~~bash
python cli.py https://your-authorized-domain.example --confirm-authorized
~~~

Add --out reports to choose a report directory.

## Configuration

Copy .env.example to .env and adjust conservative limits only when appropriate.

| Variable | Default | Purpose |
|---|---:|---|
| VULNX_HOST | 127.0.0.1 | Dashboard bind address |
| VULNX_PORT | 8000 | Dashboard port |
| VULNX_MAX_PAGES | 15 | Maximum pages crawled |
| VULNX_MAX_DEPTH | 2 | Crawl depth |
| VULNX_TIMEOUT | 8 | Network timeout in seconds |
| VULNX_CONCURRENCY | 2 | Concurrent request limit |

Reports are written to reports/ and SQLite history to storage/vulnx.db. Local secrets, databases, virtual environments, and generated reports are excluded from Git.

## Tests

~~~bash
python -m pip install pytest
python -m pytest -q
~~~

## Limitations

Findings are indicators, not proof of exploitability. Checks are unauthenticated and may miss routes or produce false positives. VulnX is not a replacement for professional penetration testing, source review, or manual validation.

Read docs/SAFE_USE.md and docs/ARCHITECTURE.md before use.

## License

MIT. See LICENSE.
