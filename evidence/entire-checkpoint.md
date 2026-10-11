# Entire setup and checkpoint evidence

Captured 2026-10-11 from the local Entire CLI and Git repository state.

## Setup and push

- Entire hooks are approved; the Entire status JSON has no `missing_approvals`.
- `entire --version` reports Entire CLI 0.11.4.
- `entire status --json` reports `enabled: true` and checkpoint sync target
  `origin`.
- Commit `99ce0a49e34884ac73896fe1b8f21692bd407fca` is the current local
  `origin/feat/initial-setup` ref, and was pushed to `origin/feat/initial-setup`.
- The prior untracked `signalforge_antigravity_pack/` remains untouched and
  untracked.

## Checkpoint

- `entire checkpoint list --json` now returns a locally confirmed temporary
  checkpoint, `6238fac0c73e5dfef73c5b18816d55f7ad8d7a88`, for session
  `01a12b8e-29d7-78d0-9c46-d4e060c69201`. `entire checkpoint explain` confirms
  it is temporary. It is not a permanent, remotely accessible checkpoint.
- `entire checkpoint list --pending --json` includes that temporary checkpoint.
- Candidate ID `01M4NR2ZCCXTV19JXG9VGNA4QA` was unresolved; it is not represented
  as a checkpoint, and no checkpoint link is recorded.
- `entire doctor` reported no stuck sessions.
- Focused docs commit `81c300a60778c9862330f0dc4ee9ab1956431353` was created
  without an `Entire-Checkpoint` trailer.
- A later normal commit attempt from a fresh active Codex session remained in
  `prepare-commit-msg` for more than two minutes, even after
  `entire status --json` reported the session `idle`. `entire doctor trace
  --last 5` still showed only an older 70,978 ms hook; the current hook added
  no trace or log entry and owned no TCP connection. Its Git and Entire
  processes were stopped; no commit was created, and the staged diff remained
  limited to this note and `hackathon.md`.
- The earlier Entire log contains `git ls-remote` failures via proxy
  `127.0.0.1:443`. In the current PowerShell environment, GitHub
  `git ls-remote` succeeds and no proxy variable or Git proxy setting is
  configured. The current stall therefore was not shown to be an active
  GitHub connectivity wait; the precise internal wait remains undiagnosed.
- No permanent checkpoint trailer or accessible checkpoint link is verified.

## 2026-10-11 — Hook stall recheck

- Current branch is `feat/initial-setup`, at `81c300a` (`docs: record Entire
  setup evidence`). No Git or Entire process was running during this check.
- The staged diff remains limited to this note and `hackathon.md`; the
  pre-existing untracked `signalforge_antigravity_pack/` remains untouched.
- The current PowerShell process cannot resolve `entire` by command name, but
  `C:\Users\This Pc\.local\bin\entire.exe` runs and reports Entire CLI 0.11.4.
  `entire doctor` reports Git hooks OK, Codex hooks installed, approval records
  present, and no stuck sessions. Status reports enabled, idle session
  `01a12b8e-29d7-78d0-9c46-d4e060c69201`, and sync target `origin`.
- `entire checkpoint list` shows only temporary checkpoint
  `6238fac0c73e5dfef73c5b18816d55f7ad8d7a88`; `entire checkpoint explain`
  confirms it is temporary. No permanent checkpoint or accessible link is
  verified.
- `entire doctor trace --hook prepare-commit-msg --last 10 --json` returns one
  trace: 70,978 ms overall, with reported step durations totaling 189 ms.
  The trace does not identify the remaining delay. The log records trailer
  insertion for the prior hook, but that candidate ID is not a permanent
  checkpoint. No new commit was attempted.
- `git ls-remote origin HEAD refs/heads/feat/initial-setup` succeeded; no
  Git proxy config keys or proxy environment variables were set in this
  PowerShell process. The old proxy error in the Entire log is not evidence
  that the current hook stall is caused by GitHub connectivity.
- Official issue #2725 reports the same Windows 0.11.4 active-session hook
  hang; issue #2726 tracks the SignalForge reproduction. Both are open with no
  documented resolution observed. The official release page lists 0.11.4 as
  latest stable; 0.11.5 builds shown there are prereleases, and their published
  notes do not identify this stall as fixed.
- No safe documented repair is established. Do not retry a normal commit until
  Entire publishes or provides a specific fix for this Windows hook stall.

## 2026-10-11 follow-up

- Official Entire checkpoint scenario documentation describes a normal commit
  after a turn reaches idle: `prepare-commit-msg` adds an `Entire-Checkpoint`
  trailer and `post-commit` condenses the shadow checkpoint. The pending
  temporary checkpoint is expected to be finalized by that workflow.
- The current `prepare-commit-msg` attempt did not complete, despite the
  session being idle. No documented non-destructive recovery command was
  identified; do not repeat the commit until the hook's local wait is
  diagnosed.

## 2026-10-11 — Official 0.11.5 nightly bounded hook test

- Kept stable Entire CLI 0.11.4 installed. Downloaded the official
  `entire_windows_amd64.zip` for
  `v0.11.5-nightly.202610100625.1f44a6f96` into a separate `%TEMP%` directory;
  SHA-256 `b43bedd2dc8bbf76a38e5dcce601f57d21afd44ce216d5114c8abf1434ad2d93`
  matched the release's `checksums.txt`. The extracted binary reports exact
  version `0.11.5-nightly.202610100625.1f44a6f96` (`windows/amd64`). No
  permanent PATH or stable binary was changed.
- GitHub compare confirms official fix commit
  `85fa052786ff11e83343009b346bd0618772cd43` is the merge base of the nightly
  release commit `1f44a6f9620d48f8f72f50fb5535c5f34d755e20`; it is included.
  The fix bounds and caches touched-path Gitlink/ignore classification that
  runs in commit-hook paths.
- Nightly `doctor`, `status --json`, `sessions list --json`, and
  `doctor trace --last 5` completed. Doctor reported hooks and Codex approvals
  present and no stuck sessions; it offered cleanup for one legacy shadow
  branch, which was declined. Status and session data remained compatible with
  the existing repository. The temporary PATH override made Git Bash's
  `command -v entire` resolve to the nightly binary.
- Ran one direct nightly `hooks git prepare-commit-msg <temporary-message-file>
  template` diagnostic with a 20-second process timeout, using a message file
  under `%TEMP%`, outside the repository. It exited 0 in 698 ms and added the
  temporary message trailer `01M4NYDNYA54C1KWKNQ0FDQTXQ`. This is only a
  candidate written to the diagnostic message file, not a checkpoint. HEAD,
  `.git/index`, checkpoint list, and session list were byte-for-byte unchanged.
- No normal commit had yet been run at the time of this diagnostic entry. The
  nightly passed the bounded test; permanent checkpoint evidence still depends
  on the normal hooked commit and subsequent Entire verification.
