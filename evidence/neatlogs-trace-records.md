# neatlogs evidence record

Captured 2026-10-11 from the authenticated neatlogs dashboard and SDK Doctor.
No API key is stored here.

## SDK verification

- Installed Python package: `neatlogs==1.4.26` (Python 3.12).
- `uv run --python 3.12 python -m neatlogs doctor --local --json`: passed; 4 spans, schema v2, no dropped spans.
- Authenticated Doctor probe: all checks passed, including trace visibility, finalization, hierarchy, attributes, input/output, and metadata/token fields. Probe trace ID: `f95af74c9290545d3070473924561c3e`.

## SignalForge traces observed in dashboard

- `f54a0d93154181436d9a4a22cea2fe2f` — early live run; search/fetch activity and failures, prior to gzip fix.
- `ba80ec1cb51385941833d1769ccf4356` — successful live demo run, 4.0 seconds, 1 source captured, 3 spans. Dashboard trace: https://app.neatlogs.com/traces/ba80ec1cb51385941833d1769ccf4356
- `89cf5e69549f558e0f8013934803bda4` — unsafe-source rejection plus valid-source recovery run, 873 ms, 3 spans. Run metadata records one failure and one captured source.

The integration emits a workflow trace and nested search/fetch tool spans and
flushes/shuts down the SDK. Trace visibility was verified in the dashboard.
This records actual observed traces; it does not claim that span status is
marked ERROR for an exception swallowed by per-source recovery.

## Final live demo run

- Run ID `7732cba0ff5147189b2af487db482b7c`, executed 2026-10-11 after the final
  code/documentation changes. One source found and captured, zero failures,
  5.151 seconds, DDGS provider, no model/cost. Output is in ignored
  `reports/demo/`.
