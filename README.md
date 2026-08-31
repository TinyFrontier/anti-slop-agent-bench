# anti-slop agent bench

Small, inspectable probes used to test where strict Python type checking ends and
an evidence policy adds a distinct signal.

Each probe keeps the exact seed, task prompt, unedited agent outputs, and raw
results together. A run is retained whether it supports or contradicts the
hypothesis.

Current probe:

- [`2026-08-payment-migration`](probes/agent-runs/2026-08-payment-migration/README.md)
