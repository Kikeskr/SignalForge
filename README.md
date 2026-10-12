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

## cfo.ai workspace context

The optional `--cfoai-read` flag connects to the existing cfo.ai workspace
through its official remote MCP endpoint. The first run opens a browser OAuth
approval and listens for the localhost callback. OAuth tokens and dynamic
client registration are held in memory only; a fresh process requires a new
authorization. SignalForge calls read-only workspace tools, writes the returned
context to the run output directory, and adds page/scenario links to the report.
It does not edit the cfo.ai model or send research findings to cfo.ai. Set
`CFOAI_MCP_URL` only if using the official endpoint (default:
`https://api.cfo.ai/mcp`).

```powershell
uv run --python 3.12 signalforge run "Your research question" --url https://example.org/ --output reports/run --cfoai-read
```

The cfo.ai context may include private workspace model data. Keep run output
local and ignored; do not publish the full `cfoai-context.json`.

## Demo

```powershell
uv run --python 3.12 signalforge run "Python 3.12.10 release notes changes and date" --output reports/demo
```

## Structured Evidence Ledger & Verification

SignalForge extracts deterministic structured evidence fields for each claim:
- **`claim_text`**: The extracted finding clause or claim statement.
- **`source_type`**: Evaluated as `primary` (academic preprints, RFCs, official specifications/repositories) or `secondary` (news media, blogs, secondary summaries).
- **`methodology`**: Deterministically classified (e.g. `Empirical benchmark evaluation`, `Randomized controlled trial`, `Official specification`).
- **`sample_size`**: Quantified benchmark runs or participant sizes (e.g. `N=45`).
- **`measured_outcome`**: Quantitative metric shifts (`%` speedup/slowdown, multipliers, execution times).
- **`limitations`**: Caveats, validity constraints, and flags such as `Missing quantitative details or sample size`.
- **`evidence_strength`**: Rated `strong`, `moderate`, `weak`, or `unsupported`.

### Verification Boundaries & Limitations
- **Source Attribution vs. Independent Verification**: Claims repeated across secondary sources remain marked `partially_supported` and `is_attributed_only=True`. Only multiple independent primary sources with empirical measurements elevate a claim to `verified_independent`.
- **Uncertainty & Contradictions**: Explicit preliminary or inconclusive language is assigned `status="uncertain"`, and conflicting performance claims are flagged as `status="conflicted"`.
- Findings reproduce extracted excerpts and heuristics without language model hallucinations.


## Web UI & Server

Launch the lightweight judge-friendly web interface:

```powershell
uv run --python 3.12 signalforge serve --host 0.0.0.0 --port 8080
```

Access `http://localhost:8080/` in a browser to submit research questions, inspect real-time progress, view generated Markdown reports, and audit structured JSON evidence ledgers. Endpoints include:
- `GET /` — Single-page research interface with partner badges and trace links
- `GET /health` — JSON health and engine status check
- `POST /api/research` — Programmatic research execution API (`{"question": "..."}`)

## AWS Deployment

SignalForge includes an automated deployment script tailored for the neatHack AWS environment (region `us-east-1`, `Hackathon_VPC`, single t3.micro instance, 20GB gp3 EBS):

```powershell
uv run --python 3.12 python deploy/deploy_aws.py
```

To terminate the instance after evaluation:
```powershell
uv run --python 3.12 python deploy/deploy_aws.py --terminate
```

See `IMPLEMENTATION_STATUS.md` for verified progress, `hackathon.md` for the
dated build log, and `SUBMISSION_CHECKLIST.md` for remaining actions.

## Team

SignalForge
