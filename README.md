# anti-slop agent bench

Small, inspectable probes used to test where strict Python type checking ends and
an evidence policy adds a distinct signal.

In the current probe, all six agent changes passed strict `ty`; three selected an
unchecked `cast` that failed at runtime and was blocked by anti-slop. The cast rate
rose from one of three runs at low reasoning effort to two of three at medium.

Each probe keeps the exact seed, task prompt, unedited agent outputs, and raw
results together. A run is retained whether it supports or contradicts the
hypothesis.

Current probe:

- [`2026-08-payment-migration`](probes/agent-runs/2026-08-payment-migration/README.md)
