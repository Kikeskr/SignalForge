# Three-minute SignalForge demo

1. **0:00–0:25 — Start the run.** In PowerShell, run:
   `uv run --python 3.12 signalforge run "Python 3.12.10 release notes changes and date" --output reports/demo`.
   Explain that the agent uses public web search and a bounded fetch pipeline.
2. **0:25–1:15 — Inspect the report.** Open `reports/demo/report.md`. Show the
   finding, its evidence ID, source link, retrieval time, and the explicit
   `partially_supported` caveat.
3. **1:15–1:55 — Inspect machine-readable output.** Open
   `reports/demo/evidence.json` and `run.json`. Point out the source record and
   honest counters/provider metadata; no model or cost is claimed.
4. **1:55–2:25 — Show recovery behavior.** Open `reports/recovery-demo/run.json`:
   the unsafe localhost URL was rejected while the valid Python.org URL was
   still captured.
5. **2:25–3:00 — Show observability.** In the neatlogs dashboard, open trace
   `ba80ec1cb51385941833d1769ccf4356` and show the research workflow and search
   and fetch spans. State that cfo.ai and Entire Graph evidence remain blocked.

The successful live report was generated on 2026-10-11. Rerun the command for a
fresh report and trace before presenting. Do not display credentials or the
Neatlogs setup screen.
