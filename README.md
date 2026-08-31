# anti-slop agent bench

Small, inspectable probes used to test where strict Python type checking ends and
an evidence policy adds a distinct signal.

In the current probe, all twelve agent changes passed strict `ty`; six selected an
unchecked `cast` that failed at runtime and was blocked by anti-slop. Reasoning
effort did not have a consistent effect: Luna moved from one cast at low to two at
medium, while Terra moved from two to one.

In a matched Luna follow-up where the failing runtime case was supplied as a
required regression test, all six agents constructed a real `RetryEnvelope`: both
`ty` and the test passed, and anti-slop was silent on all six outputs.

Each probe keeps the exact seed, task prompt, unedited agent outputs, and raw
results together. A run is retained whether it supports or contradicts the
hypothesis.

Current probes:

- [`2026-08-payment-migration`](probes/agent-runs/2026-08-payment-migration/README.md)
- [`2026-08-payment-migration-with-test`](probes/agent-runs/2026-08-payment-migration-with-test/README.md)
