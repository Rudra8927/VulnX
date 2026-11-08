# Architecture

- web/: FastAPI dashboard, static assets, and HTML template.
- cli/: command-line interface; cli.py remains a compatibility launcher.
- core/: scan orchestration, target normalization, same-origin crawling, and SQLite persistence.
- modules/: focused security checks.
- reports/: JSON, CSV, HTML, and optional PDF report generation.
- tests/: unit tests for scope handling and assessment checks.

The scanner returns a normalized result containing a scan identifier, target, timestamp, metadata, crawled pages, and findings. Both the dashboard and CLI use this shared engine.
