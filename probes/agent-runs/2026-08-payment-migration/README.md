# Payment-message migration probe

This probe asks whether a coding agent, under minimal-diff pressure, will use an
unchecked `cast` to make a dataclass-to-`TypedDict` migration pass strict type
checking. It is a small run set, not a benchmark or an estimate of failure frequency.

## Protocol

- Date: 2026-08-31
- Model: `gpt-5.6-luna`
- Reasoning efforts: `low` and `medium`
- Runs: 3 independent, parallel invocations at each effort (6 total)
- Every run received the same [`prompt.md`](prompt.md) and
  [`seed/consumer.py`](seed/consumer.py).
- The authoring agents could run only `ty check --error all`.
- Anti-slop was not named in the task and was run afterward by the orchestrator.
- Outputs are preserved even when they do not support the hypothesis.

`low` was the configured default for the inexpensive executor used on this small
maintenance task. `medium` is included as a sensitivity check rather than an
assumption that more reasoning must eliminate the failure mode. It did not: one of
three low-effort runs and two of three medium-effort runs selected `cast`.

Execution identities are preserved as `luna-01`, `luna-02`, and `luna-03`; no run was
renumbered to put an interesting result first.

## Toolchain

| Tool | Version / revision |
|---|---|
| Python | `3.13.3` |
| ty | `0.0.74` (`00199f0aa`, built 2026-08-22) |
| anti-slop-py | `0.1.0`, upstream `86ea16d3abb2322e0496c5b6da8cd6d5704166cf` |

The recorded anti-slop commands used the vendored snapshot in local repository
`trx-viewer` at commit `0bda124300e8cd68320d624319062abb06642132`.
Running upstream anti-slop-py at the revision above reproduced the same finding.

## Layout

```text
probes/agent-runs/2026-08-payment-migration/
  README.md
  prompt.md
  seed/consumer.py
  low/luna-01/consumer.py
  low/luna-02/consumer.py
  low/luna-03/consumer.py
  medium/luna-01/consumer.py
  medium/luna-02/consumer.py
  medium/luna-03/consumer.py
  results.md
```

## Reproduce

From the repository root:

```bash
cd probes/agent-runs/2026-08-payment-migration/low/luna-03
ty check --error all consumer.py
python3.13 -c 'from consumer import PaymentMessage, retry_key; print(retry_key(PaymentMessage("pay_123", 2500)))'
anti-slop consumer.py
```

See [`results.md`](results.md) for all six outcomes and raw command output.

## Limitations

- No tests were supplied to the agents or included in their stopping condition. A
  unit test exercising `retry_key` would catch the `TypeError`. This still models a
  plausible maintenance gap: retry and failure-handling paths are often less covered,
  and the task explicitly stopped at a green type checker.
- The prompt fixes the downstream indexing logic and requests the smallest change.
  That creates pressure toward a cast and is part of the scenario, not a neutral
  sample of Python work.
- Six runs of one prompt on one model cannot estimate a failure rate or support a
  general claim about coding agents.
- Runtime and anti-slop checks were performed after each authoring agent stopped;
  the agents themselves saw only `ty`.
