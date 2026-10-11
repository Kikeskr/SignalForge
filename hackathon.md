# SignalForge neatHack build log

**Timezone:** Europe/London (BST, UTC+01:00)
**Coding window:** October 10, 2026 7:00 AM BST through the confirmed submission cutoff.
**Published planned close:** October 12, 2026 7:25 PM BST; confirm the final cutoff on official Discord.
**Rule:** Entries below report observed work only. Do not backfill unverified progress or call a partner integration successful without actual evidence.

## Project

- **Problem:** Complex research answers need traceable sources, claim checking, contradiction handling, and recoverable execution.
- **Planned approach:** A bounded Python CLI that gathers evidence and emits a cited report, a JSON ledger, verification labels, and run metadata.
- **Architecture status:** Python CLI implementation and core live demo are recorded below.
- **Partner evidence status:** neatlogs traces verified; Entire checkpoint/Graph and cfo.ai model evidence remain incomplete.

## Build entries

### 2026-10-10 — Repository history observed

- **Observed fact:** Current Git history contains commit `8e1ac8d` (`docs: add project README`) at 10:10 AM BST. The committed tree contains only `README.md`.
- **Interpretation:** This entry records inspected repository history only. It does not claim this author performed that work or infer any unrecorded build activity.
- **Tests/failures/fixes:** No tests or implementation outcomes were present in the inspected repository.

### 2026-10-11 — Planning and readiness review

- Read the full `signalforge_antigravity_pack/AGENTS.md` and `PROJECT_BRIEF.md`.
- Verified the official neatHack coding start and published submission window. Local BST conversions and the unconfirmed Discord final cutoff are recorded in `IMPLEMENTATION_PLAN.md` and `ENVIRONMENT_CHECK.md`.
- Inspected the nested Git repository, current branch/status, committed files, Python/Node/Git/uv versions, available Python interpreters, and credential-name presence without printing secret values.
- Reviewed official neatlogs Python SDK, Entire CLI/Entire Graph, and cfo.ai references. The cfo.ai hackathon-specific page could not be independently fetched; signup/billing details were confirmed from the official neatHack page.
- **Implementation:** None. Planning artifacts only. No dependencies installed, no application run, and no paid action taken.
- **Tests:** None run; no test suite exists yet.
- **Failures/blockers:** Entire CLI is absent; model/search credentials are not present in inspected process/user scopes (except neatlogs key at user scope); cfo.ai workspace access is unverified; final Discord cutoff is not confirmed.
- **Evidence:** See `ENVIRONMENT_CHECK.md`; no partner integration evidence exists yet.
- **Next step:** M0 in `IMPLEMENTATION_PLAN.md` — confirm final cutoff and available no-cost credentials/access, then record actual verification before bootstrapping.

### 2026-10-11 — M0 recheck (BLOCKED)

- **Checks:** `git status --short --branch` before and after; `py -3.12 --version`; `uv --version`; credential-name presence by process/user scope without printing values; official neatHack, neatlogs, Entire, Gemini, Ollama, and DDGS documentation.
- **Results:** Branch remains `feat/initial-setup`; existing `signalforge_antigravity_pack/` and planning files remain untracked and untouched. Python 3.12.10 and uv 0.12.5 are available. `NEATLOGS_API_KEY` is present in Windows user scope but absent from this process; all inspected model/search credential names are absent in both scopes. No model/search access is verified.
- **Official options reviewed:** neatHack advertises a shared $20 LiteLLM key after team check-in verification. Gemini advertises a limited free tier requiring a user-managed key and subject to free-tier data-use terms. DDGS docs show metasearch without a credential argument but carry an educational-purpose disclaimer; no live search or terms/reliability check was performed, so it was not selected.
- **Schedule:** Published planned close remains October 12, 11:55 PM IST / 7:25 PM BST. The official page says the final cutoff will be posted on Discord; it was not verified.
- **Partner actions:** No SDK/tool installation, trace, Entire login/hook enablement, cfo.ai signup/billing, or partner integration was attempted. Human actions and privacy/billing notes are in `ENVIRONMENT_CHECK.md`.
- **Tests/failures:** No tests run; this was a read-only M0 check and the repository has no suite.
- **Next exact command after user claims/sets the model key:** `py -3.12 -c "import os; print('LITELLM_API_KEY present:', bool(os.getenv('LITELLM_API_KEY')))"` (presence check only; does not print or validate the secret).
- **Next milestone:** M0 remains blocked until human account actions and a usable search option are confirmed; keep all milestone checkboxes unchecked.

### 2026-10-12 — Build log template

- **Goal:** Record each actual milestone, command and result, evidence path, failure/root cause, fix, known limitations, and next exact action.
- **Entry:** To be completed with work actually performed on this date. No progress is asserted here.

### 2026-10-11 — M1 bootstrap and M2 provider probe

- **Goal:** Establish the minimal Python 3.12 CLI and test harness, then test whether keyless public search is available.
- **Changed:** Added `pyproject.toml`, uv lock, `.gitignore`, `.env.example`, `src/signalforge/{__init__,config,cli}.py`, initial CLI/config tests, and README setup. Preserved the pre-existing untracked `signalforge_antigravity_pack/` directory.
- **Checks:** `uv sync --python 3.12` completed. `uv run --python 3.12 python -m signalforge.cli --help` displayed usage. `uv run --python 3.12 pytest -q` → **4 passed**. `uv run --python 3.12 ruff check .` → all checks passed. `uv run --python 3.12 mypy src` → success. `git check-ignore .env` → `.env`.
- **Failure/fix:** Initial help test failed because argparse exits via `SystemExit(0)`; adjusted test to assert that standard CLI behavior and reran successfully. A keyless `ddgs==9.16.0` test query returned two Python.org results; this proves one query worked, not provider reliability or source freshness.
- **Known limitations:** No hosted model credential. Search choice is provisional; no page fetching, report, or real neatlogs/Entire/cfo.ai integration yet. Discord cutoff still needs human check.
- **Next:** Finish M2 safe fetching/extraction and source normalization/deduplication, with mocked tests.

## Evidence index

| Partner | Required genuine evidence | Current state |
|---|---|---|
| neatlogs | Baseline, improved, and error/recovery traces | Trace IDs and accessible dashboard link recorded in `evidence/neatlogs-trace-records.md` |
| Entire / Entire Graph | Real checkpoint and actual graph query/output | Blocked: seven hooks pending UI approval; Graph download reset; zero checkpoints |
| cfo.ai | Actual business model export/screenshot and assumptions summary | Pending explicit confirmation for hypothetical model creation |

### 2026-10-11 — Runnable vertical slice and neatlogs verification

- **Implemented:** Python 3.12 CLI; DDGS search; bounded and guarded source fetching; HTML extraction; URL normalization/deduplication; evidence ledger and atomic JSON state; heuristic claim/contradiction labels; Markdown report, JSON ledger and run metadata. `README.md`, `.env.example`, `.gitignore`, `DEMO_SCRIPT.md`, and `SUBMISSION_CHECKLIST.md` updated/created. Pre-existing `signalforge_antigravity_pack/` remains untouched and untracked.
- **Live demo:** `reports/demo/` records question “Python 3.12.10 release notes changes and date”; DDGS found one source, Python.org fetch succeeded, 0 failures, 4.0 seconds. The Markdown finding links to the source evidence ID and is labeled `partially_supported`; there is no configured model.
- **Recovery demo:** `reports/recovery-demo/` rejected `https://localhost/` and still captured Python.org. Run metadata recorded one source failure and one source captured.
- **Verification:** `uv run --python 3.12 pytest -q` -> 23 passed; `uv run --python 3.12 ruff check .` -> all checks passed; `uv run --python 3.12 mypy src` -> success across 11 source files. Live runs use actual DDGS and public Python.org, while automated tests mock external search/fetch.
- **neatlogs:** Installed 1.4.26; local Doctor and authenticated probe passed; three actual SignalForge traces were visible in dashboard. Trace IDs, notes, and one accessible trace URL are in `evidence/neatlogs-trace-records.md`. No key is stored. The setup screen previously displayed a raw key; don't show it in the demo.
- **Entire:** Installed and enabled Entire CLI 0.11.4 for Codex; configured checkpoint sync to public `origin`. `entire status` reports seven hooks require Codex `/hooks` approval. User explicitly approved hook approval and public checkpoint creation. The approval screen could not be opened from the available task terminal. Checkpoint count is zero. Graph v0.4.0 release asset download failed due connection reset; plugin not installed.
- **cfo.ai:** Existing signed-in workspace seen. No signup or billing action. Waiting for user confirmation before creating a hypothetical model; no integration evidence.
- **Deadline:** Official schedule publishes Oct 12, 2:30–7:25 PM BST; final cutoff still requires Discord confirmation.
- **Next:** Human approves the seven hooks using Codex `/hooks`; then verify `entire status`, create checkpoint, and record checkpoint ID/link. Do not call Entire or Graph complete before then.
