# Environment and documentation check

**Checked:** 2026-10-11 (Europe/London, BST; M0 recheck)
**Scope:** Read-only inspection. No dependencies or tools installed, no paid service accessed, no secrets read or changed, and no application code run.

## Repository and test baseline

- Opened workspace root contains a nested Git repository at `SignalForge/`.
- Inner repository branch: `feat/initial-setup`; HEAD `8e1ac8d` (`docs: add project README`, 2026-10-10 10:10 BST); remote `origin` is `https://github.com/Kikeskr/SignalForge.git`.
- Inner repository status before creating these planning files: `?? signalforge_antigravity_pack/`. This untracked directory is preserved.
- Committed tree contains only `README.md`; no package source, `pyproject.toml`, test directory, or test files were found.
- No pre-existing `hackathon.md`, `IMPLEMENTATION_PLAN.md`, or `IMPLEMENTATION_STATUS.md` existed at the inner repository root.
- Tests run during this planning pass: none. The user requested planning only; there is no suite to run.

## Installed tools

| Tool | Observed version/state | Notes |
|---|---|---|
| Windows PowerShell | 7.6.5 | Current shell. |
| Python default `python` | 3.14.7 | `C:\Users\This Pc\AppData\Local\Python\pythoncore-3.14-64\python.exe`; outside current neatlogs SDK's documented Python range. |
| Python 3.12 | 3.12.10 (`py -3.12 --version`) | `py -0p` lists `C:\Users\This Pc\AppData\Local\Python\pythoncore-3.12-64\python.exe`; compatible with neatlogs' current documented range. |
| Python 3.11.16 | Installed under uv | Also within the SDK's documented range. |
| pip | 26.2.1 | Associated with default Python 3.14; don't accidentally use it for the project environment. |
| uv | 0.12.5 (`uv --version`) | Available for environment/package management after M0. |
| Node.js | v22.23.2 | Available; not the planned app runtime. |
| npm | 12.0.2 | Available; not the planned app runtime. |
| Git | 2.55.0.windows.5 | Available. |
| `pytest` | Not installed in inspected default Python | No test suite exists. |
| `neatlogs` | Not installed in inspected default Python | No SDK or integration is present. |
| `ruff` / `mypy` | Not installed in inspected default Python | Add as project dev tools later if compatible with Python 3.12. |
| Entire CLI / Entire Graph | `entire` command not found | No local checkpoint or Graph verification. |
| Docker / Go | Commands not found | Not currently required by planned Python CLI. |

## Credential and account availability

Presence only was checked; secret values were never read into output or written to files.

| Name/access | Process scope | Windows user scope | Result |
|---|---|---|---|
| `NEATLOGS_API_KEY` | Absent | Present | Value was not read. A newly started process may inherit it; this process does not. Project ownership/key validity and ingest access are unverified. |
| `LITELLM_API_KEY` | Absent | Absent | No event model key in inspected scopes. Official neatHack instructions say an eligible team lead must verify the check-in email to claim a shared $20 key. |
| `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `GROQ_API_KEY`, `MISTRAL_API_KEY`, `COHERE_API_KEY` | Absent | Absent | No hosted model credential found under these names. |
| `CRUSTDATA_API_KEY` | Absent | Absent | Optional company/people-data credits are advertised; no key found, and this is not general web search. |
| `TAVILY_API_KEY`, `BRAVE_SEARCH_API_KEY`, `SERPAPI_API_KEY`, `BING_SEARCH_API_KEY`, `GOOGLE_CSE_ID` | Absent | Absent | No credential found for these candidate search services. No search provider selected. |
| `ENTIRE_TOKEN` | Absent | Absent | Not required for normal interactive local login; Entire documents browser login and OS credential storage. |
| cfo.ai workspace/login | Not verified | Not applicable | No cfo.ai API key variable was established by reviewed public docs. Official hackathon page says signup requires a card and advises immediate cancellation; no account/billing action was taken. |

Credential checks do not prove validity, permissions, remaining credits, or successful connection.

## Model and search options reviewed

| Option | Official/documented facts | Availability and decision |
|---|---|---|
| neatHack LiteLLM (Nova/Claude) | The current official event page advertises a shared **$20 model budget** for checked-in teams; the team lead verifies the check-in email to claim the key. AWS allowance does not cover Bedrock. | `LITELLM_API_KEY` absent. This is the preferred model candidate if the human confirms eligibility and claims it; it is a capped event credit, not a generally free API. Not usable yet. |
| [Gemini Developer API free tier](https://ai.google.dev/gemini-api/docs/pricing) | Google's pricing page documents a limited free tier for selected models; [API key docs](https://ai.google.dev/gemini-api/docs/api-key) require an AI Studio project/key. The free tier may use submitted content to improve Google products. | No Gemini/Google key present; account, model quota, data-use terms, and consent not verified. Not selected. |
| [Ollama local model](https://ollama.com/download/windows) | Official Windows docs provide a local server/API; it would avoid hosted inference charges after setup. | `ollama` command not found in PATH and no local model availability checked. Installing/downloading a runtime/model is outside M0. Not usable now. |
| [`ddgs` Python metasearch](https://github.com/deedy5/ddgs) | The project README documents `DDGS().text(query, max_results=...)` and backends; its repository labels the library educational-purpose use. This is a third-party metasearch client, not an official search-provider API. | Its example constructor has no credential argument, but docs do not prove live backend access or provider terms/reliability. No package is installed and no live query was performed. Does not satisfy the brief's “maintained, working provider” requirement on docs alone; not selected. |
| Crustdata | The official hackathon page advertises 5,000 credits for company/people data. | Key absent and scope is not broad web search. Do not select as the research search provider. |

**M0 provider outcome:** No model/search combination is currently available and verified in this environment. Preferred next candidate is the event LiteLLM key plus a separately verified search provider. Gemini free tier is a possible human-provisioned fallback only if the user accepts its account/data terms. No provider credentials are presumed valid.

## Official documentation reviewed

### neatHack rules

- [Official neatHack page](https://neatlogs.com/hackathon), rechecked 2026-10-11: schedule remains October 10–12; the submission window opens October 12, 7:00 PM IST = 2:30 PM BST and planned close is 11:55 PM IST = 7:25 PM BST. The page explicitly says final cutoff on Discord; no Discord access/announcement was verified, so do not treat the planned close as the confirmed cutoff.
- The same page requires neatlogs, Entire, and cfo.ai, a public repository, evidence, and a <=3-minute demo. It states cfo.ai signup requires a card, directs participants to cancel immediately after signup, and says hackathon credits are supplied directly.
- The current page says the hackathon LiteLLM model key is a shared $20 budget available after the team lead verifies the check-in email. It separately advertises 5,000 Crustdata credits for company/people data, not general web search.
- **Current time context:** October 11, 2026. The coding window is open; official rules allow planning in advance and require code to be authored within the stated window. No application code was authored during this pass.

### neatlogs

- [Official Python SDK reference](https://docs.neatlogs.com/sdk/python), rechecked 2026-10-11: package `neatlogs`; Python >=3.10 and <3.14; documents `init()`, `wrap()`, `@neatlogs.span`, CLI flush/shutdown, and `python -m neatlogs doctor --local --json` before instrumentation. Python 3.12.10 passes the documented version requirement.
- [Official Python supported libraries](https://docs.neatlogs.com/sdk/supported-libraries): provider/framework-specific instrumentation keys, extras, and compatibility guidance.
- [Google Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing), [API keys](https://ai.google.dev/gemini-api/docs/api-key), [Ollama Windows](https://ollama.com/download/windows), and [DDGS repository documentation](https://github.com/deedy5/ddgs) were reviewed as no-cost model/search candidates. Their limitations and access state are in the table above.
- **Environment implication:** Python 3.12/3.11 are available and in range; default Python 3.14 is outside the documented range.
- **Human action:** Start a fresh PowerShell process and run `if ([string]::IsNullOrWhiteSpace($env:NEATLOGS_API_KEY)) { 'NEATLOGS_API_KEY missing' } else { 'NEATLOGS_API_KEY present' }`. Later, after dependencies are authorized/installed, run the SDK Doctor with the project interpreter and confirm the key actually belongs to the intended project. Do not share the value in chat or logs.
- **Integration state:** Documentation reviewed only; SDK not installed; no SDK Doctor, authenticated probe, or live trace was run.

### Entire and Entire Graph

- [Official Entire CLI README](https://github.com/entireio/cli): Windows setup supports PowerShell 5.1+; `irm https://entire.io/install.ps1 | iex` installs the stable package (Scoop if present, otherwise checksum-verifies binaries into `%USERPROFILE%\.local\bin` and updates user `PATH`). Packaged install does not require Go; Git and a supported authenticated agent are required. No installer was run; `entire` is not installed.
- [Official Entire Graph repository](https://github.com/entireio/entire-graph) and [Graph command reference](https://github.com/entireio/entire-graph/blob/main/docs/commands.md): describes graph plugin/query commands and says `entire graph help` and subcommand help reflect installed behavior.
- [Official Entire CLI Windows support](https://github.com/entireio/cli/blob/main/WINDOWS.md): lists Windows/Git for Windows requirements and installation expectations.
- **Privacy consideration:** [Official Entire security and privacy docs](https://github.com/entireio/cli/blob/main/docs/security-and-privacy.md) explain that agent prompts, transcripts, tool interactions, and metadata may be committed into the repository's checkpoint storage; public repository checkpoints can be publicly visible. Review before enabling/creating checkpoints.
- **Human action:** Review the checkpoint/privacy disclosure; if accepted, run the documented installer `irm https://entire.io/install.ps1 | iex`, then `entire plugin install graph`, `entire login`, and enable Codex hooks with `entire enable --agent codex`. Verify with `entire version` and `entire graph help`. These commands were not run in M0: install modifies user PATH, plugin install adds a tool, login stores credentials, and enabling hooks writes repository configuration/captures session data.
- **Integration state:** Docs reviewed only; Entire CLI and Graph are not installed; no checkpoint/query evidence exists.

### cfo.ai

- [Official neatHack page](https://neatlogs.com/hackathon) links the [cfo.ai neatHack onboarding page](https://cfo.ai/neathacks) and publishes the card/cancellation/credits directions. The onboarding URL itself could not be independently read by the documentation fetcher during this check.
- The current official hackathon page reiterates that signup requires a card, says to cancel the subscription immediately in Settings → Billing, and says the neatHack team provides cfo.ai credits.
- [Official cfo.ai product site](https://cfo.ai/) and [pricing](https://cfo.ai/pricing) were reviewed to establish that cfo.ai is a hosted financial planning/modeling service and that paid plans exist. No plan was selected or purchased.
- **Human action:** Decide whether to complete cfo.ai neatHack onboarding. If proceeding, the account holder must personally enter any required payment method, follow the page's immediate-cancellation directions, and confirm credits/workspace access. No signup or billing operation was initiated.
- **Integration state:** No workspace/login/model/export was inspected. No cfo.ai integration is claimed.

### Current M0 result

- **BLOCKED.** `py -3.12 --version` returned `Python 3.12.10`; `uv --version` returned `uv 0.12.5 (210d1f678 2026-08-14 x86_64-pc-windows-msvc)`. Both checks pass.
- The pre/post `git status --short --branch` showed branch `feat/initial-setup` and preserved all existing untracked paths: `ENVIRONMENT_CHECK.md`, `IMPLEMENTATION_PLAN.md`, `IMPLEMENTATION_STATUS.md`, `hackathon.md`, and `signalforge_antigravity_pack/`.
- The schedule and cutoff language were checked against the official page. Human Discord confirmation is still needed for the final cutoff.
- Only `NEATLOGS_API_KEY` was present at Windows user scope; it was absent in this process. No credential value was read. Model and search keys listed above are absent from both inspected scopes.
- Provider docs/options were reviewed but no live credentials/access are available to select a working no-cost combination. Event LiteLLM requires check-in/claim; Gemini requires a newly provisioned key and user acceptance of free-tier data terms; DDGS is only an unverified third-party metasearch candidate.
- No SDK/tools/dependencies installed; no paid action, app run, or integration test performed.

## Verified schedule and remaining uncertainty

| Event | Official time | London local time | Verification |
|---|---|---|---|
| Coding start | Oct 10, 2026 12:30 PM IST | Oct 10, 2026 7:00 AM BST | Confirmed on official neatHack page. |
| Submission opens | Oct 12, 2026 7:00 PM IST | Oct 12, 2026 2:30 PM BST | Confirmed on official neatHack page. |
| Planned close | Oct 12, 2026 11:55 PM IST | Oct 12, 2026 7:25 PM BST | Published planned close only. |
| Final cutoff | Announced on Discord | Unknown | Human must inspect official Discord; no cutoff guessed. |

No credentials, credit balances, partner account permissions, SDK compatibility with a live app, Entire Graph output, cfo.ai model, or trace behavior have been validated by this documentation/environment pass.

## Build-time recheck and integrations (2026-10-11)

This section supersedes the earlier planning-only status above where they
conflict. Secrets were not printed or written to project files.

- **Environment:** Python 3.12.10 and uv 0.12.5. Application environment
  created with `uv sync --python 3.12`; search dependency `ddgs==9.16.0` and
  observability dependency `neatlogs==1.4.26` installed. Model credentials remain
  absent; no LLM synthesis is configured.
- **Search access:** DDGS performed an actual keyless search and the CLI fetched
  a Python.org source successfully. This verifies observed access only, not
  uptime, ranking, affiliation, or provider terms. Reports disclose this.
- **neatlogs:** User-scope key was available (value never persisted to files or
  logs). Local SDK Doctor and authenticated probe passed; real SignalForge
  traces were visible in the signed-in dashboard. IDs and run descriptions:
  `evidence/neatlogs-trace-records.md`. A key was visibly displayed on the
  provider setup screen during earlier inspection; do not include it in a
  public recording or repository. Consider rotating it before external sharing.
- **Entire:** Official Windows installation completed, checksum verified;
  `entire version` -> 0.11.4. `entire enable --agent codex` succeeded and
  configured checkpoint sync to `origin`. `entire status` reports seven Codex
  hooks need approval via `/hooks`. User approved hook approval and public
  checkpoint creation, but this task terminal could not launch the desktop
  `/hooks` screen (`codex /hooks` reports the packaged CLI is unavailable).
  No checkpoint exists yet. Because the origin is public, checkpoint transcripts
  and tool activity may become public; user explicitly approved this.
- **Entire Graph:** No plugin installed. Official v0.4.0 download attempt failed
  because the remote connection reset while downloading release files. `entire
  plugin list` reports no plugins. Retry once network access permits; do not
  claim graph evidence.
- **cfo.ai:** Existing signed-in workspace observed in browser. No signup or
  billing action performed. A user confirmation request is pending before
  creating a hypothetical model; no model/export evidence exists yet.
- **Hackathon deadline:** Official web schedule: Oct 12, 2026 7:00–11:55 PM IST
  (2:30–7:25 PM BST). Final cutoff is announced on Discord and remains a human
  verification item.
- **Tests:** `uv run --python 3.12 pytest -q` -> 23 passed; Ruff and mypy clean.
  See `IMPLEMENTATION_STATUS.md` and `hackathon.md` for commands and outputs.
