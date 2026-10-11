# SignalForge

An evidence-first research CLI built by Team SignalForge for neatHack 2026.

## Setup

Requires Python 3.12 and `uv`.

```powershell
uv sync --python 3.12
uv run --python 3.12 signalforge --help
uv run --python 3.12 pytest
```

Copy `.env.example` to `.env` only if using an integration that needs a key.
The application reads `NEATLOGS_API_KEY` from the process environment for
optional tracing. Never commit credentials.

## Demo

```powershell
uv run --python 3.12 signalforge run "Python 3.12.10 release notes changes and date" --output reports/demo
```

SignalForge searches with DDGS, fetches a bounded set of pages, normalizes and
deduplicates evidence, and writes a cited Markdown report, JSON ledger, and run
metadata under `reports/`. Search is third-party best-effort metasearch.
Findings are source excerpts with heuristic support/contradiction labels, not
model synthesis or independent fact verification. Review sources before
relying on results.

See `IMPLEMENTATION_STATUS.md` for verified progress, `hackathon.md` for the
dated build log, and `SUBMISSION_CHECKLIST.md` for remaining actions.

## Team

SignalForge
