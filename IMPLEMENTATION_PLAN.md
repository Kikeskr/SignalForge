# SignalForge implementation plan

**Planning date:** 2026-10-11 (Europe/London, BST)
**Repository:** `SignalForge` (`feat/initial-setup`)
**Plan status:** Active build; M1–M6 and M9 verification are complete. M7/M8/M10 remain blocked.

## Verified constraints and assumptions

- **Verified:** The official neatHack page permits planning in advance, but requires all code to be written from the hackathon start on October 10 through the deadline on October 12. The published start is 12:30 PM IST = **7:00 AM BST on October 10**. The published submission window is October 12, 7:00–11:55 PM IST = **2:30–7:25 PM BST**. The page says the final cutoff will be announced on Discord, so 7:25 PM BST is the planned close, not a confirmed final cutoff. Check Discord before submission.
- **Verified:** At this planning pass, it is October 11 in BST. There is about 28 hours from 3:08 PM BST October 11 to the published planned close. This is wall-clock time; the plan budgets about 12 hours of focused work plus 1.5 hours of contingency and assumes the solo builder can supply the remaining time.
- **Verified:** The current repository has a single README-only commit (`8e1ac8d`, 2026-10-10 10:10 BST), no application package, no test suite, and an untracked `signalforge_antigravity_pack/` directory. Preserve that directory; it is not part of this plan's implementation scope.
- **Verified:** `py -3.12 --version` returns Python 3.12.10, and `uv --version` returns 0.12.5. Python 3.12 is within the current neatlogs SDK's documented range (>=3.10 and <3.14); default `python` 3.14.7 is outside it. Use Python 3.12 explicitly.
- **Verified:** The official hackathon page requires actual use of neatlogs, Entire, and cfo.ai, with checkable evidence. Documentation review or local substitutes are not integration evidence.
- **Assumption:** Use the existing simple Python CLI scope in `signalforge_antigravity_pack/PROJECT_BRIEF.md`; avoid a UI and multi-agent complexity.
- **M0 result:** BLOCKED. The event LiteLLM key is advertised for eligible checked-in teams, but `LITELLM_API_KEY` is absent. A Google Gemini free tier exists but requires a user-created key and its free-tier data-use terms have not been accepted. No model/search combination is currently available and verified. `ddgs` is documented as third-party educational-purpose metasearch and is not selected as the dependable MVP provider without a network/reliability/terms check.
- **Assumption:** The listed 12-hour milestone budget is an aggressive solo-builder estimate. If onboarding or integrations take longer, execute the fallback scope below and reserve the last hour for a real demo and submission.

## Deadline and working budget

| Item | Local time (BST) | Status |
|---|---:|---|
| Coding window opened | Oct 10, 2026, 7:00 AM | Officially published; already passed |
| Submission window opens | Oct 12, 2026, 2:30 PM | Officially published |
| Planned submission close | Oct 12, 2026, 7:25 PM | Officially published as planned; final Discord cutoff still needs confirmation |
| Focused build budget | 12 hours | Estimate, not a guarantee |
| Contingency | 1.5 hours | Estimate; protect for integration and demo issues |

Time conversion uses IST = UTC+05:30 and BST = UTC+01:00 on these dates (IST is 4 hours 30 minutes ahead of BST).

## Milestones

### Actual build results (updated 2026-10-11)

- **M1 PASS:** Python 3.12 project, CLI/config, `.env.example`, ignore rules, README and initial tests. `uv sync --python 3.12`; CLI help; pytest 4 passed; Ruff and mypy clean.
- **M2 PASS:** DDGS live search, bounded fetch/HTML extraction, safe URL filtering, canonicalization/deduplication and recovery behavior implemented. See `IMPLEMENTATION_STATUS.md` for current full verification commands.
- **M3 PASS:** Evidence ledger with deterministic IDs and atomic JSON state round-trip/recovery tests.
- **M4 PASS:** Live successful report and JSON output in ignored `reports/demo/`; one Python.org source, one capture, zero failures, 4 seconds.
- **M5 PASS:** Support/contradiction labels and bounded source retry behavior tested. This is a heuristic; no semantic model checking is configured.
- **M6 PASS:** `neatlogs==1.4.26`, local Doctor and authenticated probe passed, SignalForge traces observed in dashboard. Sanitized IDs recorded in `evidence/neatlogs-trace-records.md`.
- **M7 BLOCKED:** Entire 0.11.4 enabled. User approved hooks and public checkpoint; seven hooks still require approval in Codex UI. Graph release download failed due remote connection reset. No checkpoint exists.
- **M8 BLOCKED:** Existing cfo.ai workspace was observed; no signup/payment action. Awaiting user confirmation for hypothetical model creation. No genuine model evidence yet.
- **M9 PASS:** 23 tests, Ruff and mypy passed; live successful report and failure-recovery run inspected.
- **M10 BLOCKED:** Three-minute demo script and checklist created; final Discord cutoff remains human-check; submission not made.

### Next action

Open Codex `/hooks`, approve seven Entire hooks (user approved), then run
`entire status`. After that, create a reviewed commit/checkpoint and verify its
ID and accessible link before recording a PASS. Do not claim Graph or cfo.ai
success without actual output.

---

Milestone checkboxes are controlled by verified results in `IMPLEMENTATION_STATUS.md`; the criteria below remain acceptance targets.

### M0 — Confirm rules, environment, accounts, and provider choices (0.5 h)

- **Depends on:** None.
- **Scope/files:** `ENVIRONMENT_CHECK.md`, `.env.example` (later), `README.md` (later).
- **Acceptance:** Confirm final Discord cutoff; decide the lowest-friction supported search/model APIs; confirm credentials and non-paid access; use Python 3.12; confirm partner onboarding constraints. No secret values enter Git.
- **Verification:** `py -3.12 --version`; `uv --version`; `git status --short --branch`; inspect official provider docs and account access. Record actual results.
- **Actual verification:** `py -3.12 --version` → `Python 3.12.10` (PASS); `uv --version` → `uv 0.12.5 (210d1f678 2026-08-14 x86_64-pc-windows-msvc)` (PASS); `git status --short --branch` before/after preserved all pre-existing untracked paths (PASS). Official schedule checked; planned close 7:25 PM BST Oct 12, final Discord cutoff not verified. No model/search credentials available. **M0 BLOCKED; checkbox remains unchecked.** See `ENVIRONMENT_CHECK.md` for evidence and human actions.

### M1 — Bootstrap the CLI and deterministic test harness (0.75 h)

- **Depends on:** M0.
- **Scope/files:** `pyproject.toml`, `.gitignore`, `.env.example`, `README.md`, `src/signalforge/__init__.py`, `src/signalforge/cli.py`, `src/signalforge/config.py`, focused CLI/config tests.
- **Acceptance:** Python 3.12 environment resolves; CLI `--help` works; missing credentials yield an actionable error; `.env` and private evidence are ignored; placeholder-only `.env.example`; test/lint/type commands are documented.
- **Verification:** `uv run --python 3.12 pytest -q tests/test_cli.py tests/test_config.py`; `uv run --python 3.12 ruff check .`; `uv run --python 3.12 mypy src`; `uv run --python 3.12 python -m signalforge.cli --help`; `git check-ignore .env`.
- **Fallback:** Minimal `argparse` CLI and standard-library config; omit optional frameworks.
- **Actual verification:** **PASS (2026-10-11).** `uv sync --python 3.12` completed; `uv run --python 3.12 python -m signalforge.cli --help` displayed usage; `uv run --python 3.12 pytest -q` → 4 passed; `uv run --python 3.12 ruff check .` → all checks passed; `uv run --python 3.12 mypy src` → success; `git check-ignore .env` → `.env`. First pytest attempt failed because argparse help raises `SystemExit(0)`; test fixed and rerun. No app credentials read or changed.

### M2 — Search, fetch, extract, normalize, and deduplicate sources (1.5 h)

- **Depends on:** M0, M1.
- **Scope/files:** `src/signalforge/search.py`, `fetch.py`, `evidence.py`; targeted tests.
- **Acceptance:** Use one documented search provider; enforce timeouts, response-size bounds, safe URL handling, bounded retries, canonical URLs, and duplicate removal; continue when one source fails; no source-page instructions are executed.
- **Verification:** `uv run --python 3.12 pytest -q tests/test_search.py tests/test_fetch.py tests/test_evidence.py`; mocked HTTP only.
- **Fallback:** Accept a small list of user-provided URLs and perform bounded fetch/extraction; keep search provider behind a replaceable interface.
- **Actual verification:** **PASS.** `ddgs==9.16.0` live search and bounded Python.org fetch succeeded; URL safety, normalization/deduplication and failure recovery covered by mocked tests. Search remains best-effort third-party metasearch.

### M3 — Typed evidence ledger and recoverable state (0.75 h)

- **Depends on:** M1, M2.
- **Scope/files:** `src/signalforge/schemas.py`, `state.py`, evidence tests.
- **Acceptance:** Stable evidence IDs resolve; JSON records title, URL, retrieval time, excerpt, and publication date when available; state round-trips safely; partial work survives a simulated interruption.
- **Verification:** `uv run --python 3.12 pytest -q tests/test_evidence.py tests/test_recovery.py`.
- **Fallback:** Atomic JSON files and a single run directory; omit `--resume` unless persistence tests pass.
- **Actual verification field:** Not run.

### M4 — One end-to-end research workflow and cited report (2 h)

- **Depends on:** M0–M3.
- **Scope/files:** `src/signalforge/agent.py`, `report.py`, `cli.py`; workflow tests.
- **Acceptance:** One research question is split into a few subquestions; at most 8–12 usable sources and two rounds; produce Markdown report, JSON evidence ledger, and run metadata; each material claim references evidence IDs; estimates are labeled; run budgets and limits are explicit.
- **Verification:** `uv run --python 3.12 pytest -q tests/test_agent.py tests/test_report.py`; mocked model and search responses.
- **Fallback:** One research round, 5–8 sources, clear limitations, and no unsupported claims. Prefer a complete honest report over multi-round breadth.
- **Actual verification field:** Not run.

### M5 — Claim checks, contradiction labels, bounded retries, and failure tests (1.5 h)

- **Depends on:** M3, M4.
- **Scope/files:** `src/signalforge/verify.py`, `cost.py`, tests for verification/recovery.
- **Acceptance:** Distinguish `supported`, `partially_supported`, `conflicted`, and `unsupported`; reject unknown evidence IDs; a citation's presence alone does not imply support; retry limits hold; empty search, timeout, malformed output, and one-source failure produce honest safe outcomes.
- **Verification:** `uv run --python 3.12 pytest -q tests/test_verify.py tests/test_recovery.py tests/test_agent.py`.
- **Fallback:** Deterministic excerpt/ID validation with explicit “not automatically verified” labels; do not claim semantic verification without evidence.
- **Actual verification field:** Not run.

### M6 — neatlogs instrumentation and genuine traces (1.25 h)

- **Depends on:** M0, M1, M4; Python 3.12 and actual Neatlogs project access.
- **Scope/files:** `pyproject.toml`, CLI/workflow entry point, `evidence/neatlogs/`, README setup.
- **Acceptance:** Follow current official Python SDK guidance; initialize once; trace the research workflow, model/tool calls, retries, failures, and verification; do not capture secrets; flush/shut down correctly for CLI; retain genuine baseline, improved, and error/recovery trace evidence. Mark measured token/cost values separately from estimates.
- **Verification:** `uv run --python 3.12 python -m neatlogs doctor --local --json`; targeted tests; a deliberately small authorized live run; inspect actual trace links/screenshots and ensure no key leakage. Run the live probe only when credentials and budget are available.
- **Fallback:** Instrument the real workflow if SDK/runtime compatibility permits; otherwise record the integration as blocked and never fabricate trace evidence. Do not replace it with fake spans.
- **Actual verification field:** Not run; project key is available at Windows user scope, but no live trace has been verified.

### M7 — Entire checkpoints and actual Entire Graph output (0.75 h)

- **Depends on:** M0; existing Git repository and installed Entire CLI/Graph plugin.
- **Scope/files:** repository-level Entire settings/hooks if needed; `evidence/entire/`; relevant build-log entry.
- **Acceptance:** Use official install and CLI docs; inspect installed `entire --help`/version; capture a real checkpoint and successful graph query/output; describe one actual way repository context/checkpoint informed a change or recovery.
- **Verification:** Installed-version commands as documented by that version; save actual command output and metadata under `evidence/entire/`; inspect Git diff/status for generated files.
- **Fallback:** If installation or graph support fails, keep only factual local checkpoint evidence if available and mark Graph integration incomplete. A source-control log or hand-written graph is not proof of Entire Graph use.
- **Actual verification field:** Not run; Entire and Entire Graph CLIs are not installed.

### M8 — Real cfo.ai model and business assumptions (1.25 h)

- **Depends on:** M0 and available cfo.ai workspace/credits; M4–M6 estimates improve the model.
- **Scope/files:** `evidence/cfo/`, concise assumptions note, build log.
- **Acceptance:** Create and inspect an actual cfo.ai model with conservative/base/growth cases, plan pricing, customer/revenue assumptions, model/search/hosting costs, margin, burn, and runway where meaningful; distinguish measured data from assumptions; retain a real export/screenshot and access evidence.
- **Verification:** Inspect actual cfo.ai model values and export/screenshot; reconcile them to the written assumptions. Do not describe a local spreadsheet or Markdown alone as cfo.ai integration.
- **Fallback:** If signup/credit access cannot be completed without a payment action or human login, stop at the access blocker and mark the partner requirement incomplete; no substitute counts as success.
- **Actual verification field:** Not run; cfo.ai workspace access is unverified. Official hackathon instructions say signup requires a card and instruct immediate cancellation; no signup or billing action was taken.

### M9 — Full verification, safety, and artifact audit (1 h)

- **Depends on:** M1–M8 for complete-MVP claim; can run relevant subset if integrations are blocked.
- **Scope/files:** tests and docs only as needed to resolve findings; report/evidence audit.
- **Acceptance:** Full deterministic suite, configured lint/type checks, CLI smoke check, missing-credential behavior, secret scan, citations/evidence audit, and report/evidence/run metadata all match actual outputs. No partner claim lacks direct evidence.
- **Verification:** `uv run --python 3.12 pytest -q`; `uv run --python 3.12 ruff check .`; `uv run --python 3.12 mypy src`; `uv run --python 3.12 python -m signalforge.cli --help`; `git diff --check`; inspect `git status --short` and tracked/untracked evidence.
- **Fallback:** Run only applicable checks and explicitly list blocked checks; never mark the full MVP complete.
- **Actual verification field:** Not run.

### M10 — Demo, public repo, and submission package (0.75 h)

- **Depends on:** M9; verified partner artifacts; confirmed Discord cutoff.
- **Scope/files:** `README.md`, `hackathon.md`, evidence index, demo video, final submission checklist.
- **Acceptance:** Public repository is safe to publish; demo is <=3 minutes and honestly shows the product plus neatlogs, Entire, and cfo.ai; evidence links resolve; quote-post draft includes team/project/repo/demo; user explicitly approves publishing the X post. Submit before the confirmed Discord cutoff.
- **Verification:** Play the final video; inspect every link/artifact; run final `git status --short` and secret/evidence audit; verify submission post is actually published only after user approval.
- **Fallback:** If a required partner or demo cannot be verified by the cutoff, submit only if eligible and disclose the gap; do not imply completed integrations.
- **Actual verification field:** Not run.

## Dependency and blocker gates

| Gate | Current evidence | Next action |
|---|---|---|
| Python runtime | Python 3.12 installed; default is unsupported Python 3.14 for current neatlogs SDK docs | Pin/use Python 3.12 explicitly in project commands |
| neatlogs | `NEATLOGS_API_KEY` exists in Windows user scope; absent from this inspection process; SDK not installed | New shells can inherit user variable; later verify same-interpreter local Doctor and project access |
| Model/search APIs | `LITELLM_API_KEY`, Google/model keys, and common search API keys absent in process/user scopes; DDGS docs are not sufficient proof of reliable provider access | Human: check team-lead check-in email and claim event LiteLLM shared key; identify/approve a documented search service with actual available access |
| Entire | CLI/plugin not found; packaged Windows PowerShell installer is documented; Git is present | Human: review checkpoint privacy disclosure; install, sign in, and enable hooks only after authorization |
| cfo.ai | Workspace/login not verified; hackathon signup requires a card and advises immediate subscription cancellation | Human decides and completes onboarding/billing steps; no action in M0 |
| Submission cutoff | Official page publishes planned close 7:25 PM BST Oct 12; final cutoff is on Discord | Human: check official Discord before submission |

**Next exact safe check after the user claims the event key and places it in the run environment:** `py -3.12 -c "import os; print('LITELLM_API_KEY present:', bool(os.getenv('LITELLM_API_KEY')))"`. This checks presence only, not validity; it does not reveal the secret.

## Fallback scope

If partner onboarding, model/search access, or runtime issues consume the contingency, prioritize a working single-question CLI, bounded source collection, honest evidence ledger, cited report, deterministic tests, and a readable demo. Reduce to one research round and 5–8 sources. Keep neatlogs/Entire/cfo.ai evidence attempts factual; any unavailable mandatory partner makes the submission incomplete against the official requirement. Drop optional resume, optional Crustdata, multiple agents, UI, extensive scenario breadth, and unverified cost claims before reducing safety or evidence quality.

## Official references checked

- [neatHack rules and schedule](https://neatlogs.com/hackathon) — coding window, published submission window, partner requirements, evidence criteria, cfo.ai signup/card instructions.
- [neatlogs Python SDK](https://docs.neatlogs.com/sdk/python) and [Python auto-instrumentation support table](https://docs.neatlogs.com/sdk/supported-libraries) — SDK install, Python support range, init/wrap/decorator/flush, instrumentation options.
- [Entire CLI](https://github.com/entireio/cli) — current installation and CLI overview; installed `entire --help` remains authoritative for this machine.
- [Entire Graph repository](https://github.com/entireio/entire-graph) and [Graph commands reference](https://github.com/entireio/entire-graph/blob/main/docs/commands.md) — plugin capabilities, install/use concepts, graph CLI help.
- [cfo.ai neatHack onboarding](https://cfo.ai/neathacks) — linked by the official hackathon page; its page could not be independently fetched in this documentation check. The official hackathon page itself says signup requires a card and advises cancelling immediately after signup; credits are provided by the hackathon team.
- [cfo.ai official product site](https://cfo.ai/) and [pricing](https://cfo.ai/pricing) — current product and paid plan information; no paid plan selected.
