# Payment-message migration probe

This probe asks whether a coding agent, under minimal-diff pressure, will use an
unchecked `cast` to make a dataclass-to-`TypedDict` migration pass strict type
checking. All twelve changes passed strict `ty`; six selected an unchecked cast
that failed at runtime and was blocked by anti-slop. Reasoning effort did not have
a consistent effect: Luna moved from one cast at low to two at medium, while Terra
moved from two to one. This is a small run set, not a benchmark or an estimate of
failure frequency.

## Protocol

- Date: 2026-08-31
- Models: `gpt-5.6-luna` and `gpt-5.6-terra`
- Reasoning efforts: `low` and `medium`
- Runs: 3 independent invocations per model at each effort (12 total)
- Every run received the same [`prompt.md`](prompt.md) and
  [`seed/consumer.py`](seed/consumer.py).
- The authoring agents could run only `ty check --error all`.
- Anti-slop was not named in the task and was run afterward by the orchestrator.
- Outputs are preserved even when they do not support the hypothesis.

`terra-01` at medium effort hit a harness error before its first `ty` process
started because the run directory had not been created. The same invocation then
materialized the solution it had already selected and reran `ty`; it was not
resampled or asked to reconsider the change. That run produced a non-cast output;
it is the run behind Terra's medium count of one.

`low` models the reasoning budget commonly used for a small maintenance task.
`medium` is included as a sensitivity check rather than an assumption that more
reasoning must eliminate the failure mode. The direction differed by model: Luna
selected `cast` in one of three low-effort runs and two of three medium-effort
runs; Terra selected it in two of three low-effort runs and one of three
medium-effort runs. Pooled across models, both efforts produced three casts in six
runs.

Execution identities are preserved as `luna-01` through `luna-03` and `terra-01`
through `terra-03`; no run was renumbered to put an interesting result first.

## Toolchain

| Tool | Version / revision |
|---|---|
| Python | `3.13.3` |
| ty | `0.0.74` (`00199f0aa`, built 2026-08-22) |
| anti-slop-py | `0.1.0`, upstream `86ea16d3abb2322e0496c5b6da8cd6d5704166cf` |

Running upstream anti-slop-py at the revision above reproduced the recorded
findings.

## Layout

```text
probes/agent-runs/2026-08-payment-migration/
  README.md
  prompt.md
  seed/consumer.py
  low/luna-01/consumer.py
  low/luna-02/consumer.py
  low/luna-03/consumer.py
  low/terra-01/consumer.py
  low/terra-02/consumer.py
  low/terra-03/consumer.py
  medium/luna-01/consumer.py
  medium/luna-02/consumer.py
  medium/luna-03/consumer.py
  medium/terra-01/consumer.py
  medium/terra-02/consumer.py
  medium/terra-03/consumer.py
  results.md
```

## Reproduce

From the repository root:

```bash
python3.13 -m pip install "ty==0.0.74"
python3.13 -m pip install "anti-slop-py @ git+https://github.com/TinyFrontier/anti-slop-py.git@86ea16d3abb2322e0496c5b6da8cd6d5704166cf"
cd probes/agent-runs/2026-08-payment-migration/low/luna-03
ty check --error all consumer.py
python3.13 -c 'from consumer import PaymentMessage, retry_key; print(retry_key(PaymentMessage("pay_123", 2500)))'
anti-slop consumer.py
```

See [`results.md`](results.md) for all twelve outcomes and raw command output.

## Limitations

- No tests were supplied to the agents or included in their stopping condition. A
  unit test exercising `retry_key` would catch the `TypeError`. This still models a
  plausible maintenance gap: retry and failure-handling paths are often less covered,
  and the task explicitly stopped at a green type checker.
- The prompt fixes the downstream indexing logic and requests the smallest change.
  That creates pressure toward a cast and is part of the scenario, not a neutral
  sample of Python work. The pressure was not inescapable: six of the twelve agents
  satisfied every stated constraint by constructing a `RetryEnvelope` without a
  cast.
- Twelve runs of one prompt on two models cannot estimate a failure rate or support
  a general claim about coding agents.
- Runtime and anti-slop checks were performed after each authoring agent stopped;
  the agents themselves saw only `ty`.
