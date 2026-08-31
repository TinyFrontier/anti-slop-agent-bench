# anti-slop agent bench

Small, inspectable agent runs used to test where strict Python type checking ends
and an evidence policy adds a distinct signal.

Each benchmark keeps the exact seed, task prompt, unedited agent outputs, and raw
results together. A run is retained whether it supports or contradicts the
hypothesis.

Current benchmark:

- [`2026-08-payment-migration`](bench/agent-runs/2026-08-payment-migration/README.md)
