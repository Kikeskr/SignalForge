# SignalForge neatHack build log

**Timezone:** Europe/London (BST, UTC+01:00)
**Coding window:** October 10, 2026 7:00 AM BST through the confirmed submission cutoff.
**Published planned close:** October 12, 2026 7:25 PM BST; confirm the final cutoff on official Discord.
**Rule:** Entries below report observed work only. Do not backfill unverified progress or call a partner integration successful without actual evidence.

## Project

- **Problem:** Complex research answers need traceable sources, claim checking, contradiction handling, and recoverable execution.
- **Planned approach:** A bounded Python CLI that gathers evidence and emits a cited report, a JSON ledger, verification labels, and run metadata.
- **Architecture status:** Python CLI implementation and core live demo are recorded below.
- **Partner evidence status:** neatlogs traces and read-only cfo.ai MCP/model access are verified; Entire permanent checkpoint/Graph remain incomplete. The cfo.ai spreadsheet export was started but no saved local workbook was found.

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
| Entire / Entire Graph | Real checkpoint and actual graph query/output | Hooks approved; Entire 0.11.4 enabled with sync target `origin`; no checkpoint verified; Graph evidence incomplete |
| cfo.ai | Real model, model access, and assumptions evidence | Hypothetical SignalForge model is live; read-only OAuth/MCP inspection verified; evidence summary and live page links in `evidence/cfo/mcp-read-integration.md`; local workbook export still outstanding |

### 2026-10-11 — Runnable vertical slice and neatlogs verification

- **Implemented:** Python 3.12 CLI; DDGS search; bounded and guarded source fetching; HTML extraction; URL normalization/deduplication; evidence ledger and atomic JSON state; heuristic claim/contradiction labels; Markdown report, JSON ledger and run metadata. `README.md`, `.env.example`, `.gitignore`, `DEMO_SCRIPT.md`, and `SUBMISSION_CHECKLIST.md` updated/created. Pre-existing `signalforge_antigravity_pack/` remains untouched and untracked.
- **Live demo:** `reports/demo/` records question “Python 3.12.10 release notes changes and date”; DDGS found one source, Python.org fetch succeeded, 0 failures, 4.0 seconds. The Markdown finding links to the source evidence ID and is labeled `partially_supported`; there is no configured model.
- **Recovery demo:** `reports/recovery-demo/` rejected `https://localhost/` and still captured Python.org. Run metadata recorded one source failure and one source captured.
- **Verification:** `uv run --python 3.12 pytest -q` -> 23 passed; `uv run --python 3.12 ruff check .` -> all checks passed; `uv run --python 3.12 mypy src` -> success across 11 source files. Live runs use actual DDGS and public Python.org, while automated tests mock external search/fetch.
- **neatlogs:** Installed 1.4.26; local Doctor and authenticated probe passed; three actual SignalForge traces were visible in dashboard. Trace IDs, notes, and one accessible trace URL are in `evidence/neatlogs-trace-records.md`. No key is stored. The setup screen previously displayed a raw key; don't show it in the demo.
- **Entire at this entry:** Installed and enabled Entire CLI 0.11.4 for Codex; configured checkpoint sync to public `origin`. At that time, status reported seven hooks requiring approval, checkpoint count was zero, and Graph v0.4.0 release asset download failed due connection reset; plugin was not installed.
- **cfo.ai:** Existing signed-in workspace seen. No signup or billing action. Waiting for user confirmation before creating a hypothetical model; no integration evidence.
- **Deadline:** Official schedule publishes Oct 12, 2:30–7:25 PM BST; final cutoff still requires Discord confirmation.
- **Next at this entry:** Approve the seven hooks using Codex `/hooks`, then verify status and checkpoint ID/link. Do not call Entire or Graph complete before then.

### 2026-10-11 — Entire checkpoint state recheck

- **Verified setup:** Entire hooks have approval records; `entire --version` reports 0.11.4; `entire status --json` reports enabled with checkpoint sync target `origin`. `entire doctor` reports no stuck sessions.
- **Git history:** Code commit `99ce0a49e34884ac73896fe1b8f21692bd407fca` is on `origin/feat/initial-setup`. Focused docs commit `81c300a60778c9862330f0dc4ee9ab1956431353` was created without an `Entire-Checkpoint` trailer.
- **Checkpoint result at recheck:** `entire checkpoint list --json` and `entire checkpoint list --pending --json` returned zero entries before the latest attempt. Candidate ID `01M4NR2ZCCXTV19JX9GVGNA4QA` remains unresolved and is not treated as a checkpoint.
- **Hook diagnosis:** A single normal commit from an idle Entire session remained in `prepare-commit-msg` for over two minutes, with no new trace/log entry and no TCP connection owned by the Entire hook. It was stopped; HEAD stayed at `81c300a` and only the two evidence files remained staged. `entire doctor trace --last 5` showed the earlier 70,978 ms hook. No safe documented repair was identified.
- **Temporary checkpoint:** `entire checkpoint list --json` now confirms temporary ID `6238fac0c73e5dfef73c5b18816d55f7ad8d7a88`; `entire checkpoint explain` confirms its temporary status and session `01a12b8e-29d7-78d0-9c46-d4e060c69201`. No permanent checkpoint or accessible link exists yet.
- **Network check:** The prior Entire log contains proxy `127.0.0.1:443` enumeration failures. Current GitHub `git ls-remote` works, and current process environment/Git settings have no proxy configured. The present hook wait has not been tied to network access.
- **Working tree:** Existing untracked `signalforge_antigravity_pack/` remains untouched.
- **Evidence:** `evidence/entire-checkpoint.md`. No secrets recorded.

### 2026-10-11 — Entire hook diagnosis follow-up

- **Current checks:** No Git/Entire process was running. Direct invocation of
  the installed binary reports Entire CLI 0.11.4; the current PowerShell PATH
  does not resolve `entire` by name. `entire doctor` reports hooks and Codex
  approvals present, no stuck sessions, and status remains enabled with an idle
  session and sync target `origin`.
- **Trace:** `entire doctor trace --hook prepare-commit-msg --last 10 --json`
  returns a 70,978 ms trace whose named steps total 189 ms; it does not expose
  the remaining delay. Current `git ls-remote origin` succeeds and this shell
  has no configured proxy variable or Git proxy key.
- **Upstream/release check:** Official reports #2725 and #2726 remain open.
  The release page lists 0.11.4 as latest stable and 0.11.5 only as nightly
  prereleases; published nightly changes do not document a fix for this stall.
  No CLI update or other configuration change is justified by that evidence.
- **Checkpoint:** Only temporary checkpoint
  `6238fac0c73e5dfef73c5b18816d55f7ad8d7a88` is confirmed. No permanent ID or
  accessible link is recorded. No commit was retried.
- **Next:** Keep the current evidence changes staged and wait for a specific
  Entire maintainer fix/instruction for the Windows 0.11.4 `prepare-commit-msg`
  hang; then verify the fix before one normal hooked commit.

### 2026-10-11 — cfo.ai live MCP integration

- **Goal:** Connect the SignalForge CLI to the existing cfo.ai model without modifying model data or initiating signup/billing.
- **Implementation:** Added `src/signalforge/cfoai.py` with cfo.ai MCP OAuth using the official MCP Python SDK provider, a localhost callback, and in-memory-only token/client storage. Added `signalforge run ... --cfoai-read`; it inspects the workspace after research and saves full context only under ignored run output, appending a short workspace/page/scenario reference to the report and `run.json`.
- **Human action:** User approved the SignalForge OAuth consent. cfo.ai consent listed email, identity/profile, and ongoing account access. No password or token was requested or stored in project files.
- **Live verification:** `uv run --python 3.12 signalforge run "SignalForge cfo.ai integration verification" --url https://www.python.org/ --output reports/cfoai-live-verification --cfoai-read` → exit 0; one research source captured; cfo.ai returned Warm Panther org `103166` (slug `warm-panther-ff1ea2d0`), three pages/10 blocks, and Main Scenario, Growth, and Conservative. Read calls used `list_orgs`, `inspect_skills`, `inspect_pages`, and `inspect_scenarios`; no edit tool was called. Actual report and JSON are in ignored `reports/cfoai-live-verification/`.
- **Actual model:** The pre-existing hypothetical SignalForge forecast has Assumptions, Forecast, and Scenarios & Risks pages. All values are estimates, and no live financial inputs are connected. The report links to those live pages; see `evidence/cfo/mcp-read-integration.md`.
- **Export:** The native Forecast “Download spreadsheet” action returned “Spreadsheet download started — SignalForge — Forecast.xlsx.” No workbook was found in the user Downloads directory, so a saved export is not claimed.
- **Tests:** `uv run --python 3.12 pytest -q` → 29 passed; `uv run --python 3.12 ruff check .` → all checks passed; `uv run --python 3.12 mypy src` → no issues in 12 source files; `git diff --check` → clean, with line-ending advisories only.
- **Known limits:** cfo.ai is a live read-only workspace/model context integration, not an LLM provider and not a write-back integration. Each fresh CLI process needs its own browser OAuth; OAuth data is not persisted. M8 passes for real model access and integration; a saved workbook remains a submission evidence task.
- **Next:** Diagnose the known Entire hook stall; continue trying to save the native cfo.ai workbook if available.

### 2026-10-11 — Entire 0.11.5 nightly hook test

- **Binary:** Official Windows AMD64 nightly `0.11.5-nightly.202610100625.1f44a6f96` was downloaded to a separate temporary directory. Its archive SHA-256 matched official `checksums.txt`; stable 0.11.4 and permanent PATH were not changed.
- **Relevant change:** The nightly includes upstream commit `85fa052786ff11e83343009b346bd0618772cd43`, which bounds and caches Gitlink/ignored-path classification in hook processing.
- **Read-only compatibility:** Nightly doctor/status/session/trace commands completed; hooks and approvals are present, no stuck sessions were reported, and the existing temporary checkpoint/session state remained unchanged. A legacy shadow-branch cleanup prompt was declined.
- **Bounded hook test:** With a temporary PATH override, Git Bash resolved `entire` to the nightly. A single direct `prepare-commit-msg` run against a temp message file outside the repository, source `template`, exited 0 in 698 ms. It added a candidate trailer to that temp file only; HEAD, index, checkpoint list, and session list did not change. This candidate is not checkpoint evidence.
- **Next:** Stage and inspect only `evidence/entire-checkpoint.md` and `hackathon.md`, then make one ordinary Git commit with the nightly resolved by a process-only PATH override. Verify the actual checkpoint before recording an ID or link.
