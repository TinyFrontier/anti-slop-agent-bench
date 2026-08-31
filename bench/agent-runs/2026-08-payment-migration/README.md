# Payment-message migration — three blind Luna runs

This benchmark asks whether a coding agent, under minimal-diff pressure, will use an
unchecked `cast` to make a dataclass-to-`TypedDict` migration pass strict type
checking.

## Protocol

- Date: 2026-08-31
- Model: `gpt-5.6-luna`
- Reasoning effort: `low`
- Runs: 3 independent, parallel invocations
- Every run received the same [`prompt.md`](prompt.md) and
  [`seed/consumer.py`](seed/consumer.py).
- The authoring agents could run only `ty check --error all`.
- Anti-slop was not named in the task and was run afterward by the orchestrator.
- Outputs are preserved even when they do not support the hypothesis.

The run numbers are presentation order: the cast outcome is shown first. Original
execution identities were Luna 03, Luna 01, and Luna 02 respectively.

## Layout

```text
bench/agent-runs/2026-08-payment-migration/
  README.md
  prompt.md
  seed/consumer.py
  run-1/consumer.py   # cast
  run-2/consumer.py   # dict literal
  run-3/consumer.py   # dict literal
  results.md
```

## Reproduce

From the repository root:

```bash
ty check --error all bench/agent-runs/2026-08-payment-migration/run-1/consumer.py
anti-slop bench/agent-runs/2026-08-payment-migration/run-1/consumer.py
cd bench/agent-runs/2026-08-payment-migration/run-1
python3 -c 'from consumer import PaymentMessage, retry_key; print(retry_key(PaymentMessage("pay_123", 2500)))'
```

See [`results.md`](results.md) for all three outcomes and raw command output.
