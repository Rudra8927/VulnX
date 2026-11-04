# VulnX — Advanced Web Vulnerability Scanner

VulnX is a Python-based web security assessment tool designed for cybersecurity learners, ethical hackers, and security researchers. It helps identify potential website security weaknesses and common misconfigurations through automated checks, web reconnaissance, and a same-origin crawler.

## Features

- DNS and TLS information gathering
- HTTP security-header analysis
- Cookie security-attribute checks
- Bounded same-origin website crawling
- Checks for common exposed files and endpoints
- SQLite-based scan history
- JSON, CSV, and HTML report generation
- Command-line interface (CLI)
- FastAPI-powered web dashboard
- Designed for Linux and Windows

## Technology Stack

Python · FastAPI · HTTPX · SQLite · Uvicorn · dnspython

## Getting Started

Clone the repository:

```bash
git clone https://github.com/Rudra8927/VulnX.git
cd VulnX
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux / Kali Linux:

```bash
source .venv/bin/activate
```

Or on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the web dashboard from the project root:

```bash
uvicorn web.app:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 in your browser.

Refer to the CLI help and configuration files for the options supported by your installed version.

## Responsible Use

Only scan websites and systems that you own or have explicit permission to assess. Respect the agreed scope, applicable laws, and target service limits. VulnX is intended for educational and authorized security testing. Scan results are indicators for further validation, not proof that a system is secure or vulnerable.

## Disclaimer

This project is provided for educational and research purposes. The author is not responsible for misuse, unauthorized testing, service disruption, or damage arising from use of this tool.

## Author

**Rudra8927** · [GitHub Profile](https://github.com/Rudra8927)
