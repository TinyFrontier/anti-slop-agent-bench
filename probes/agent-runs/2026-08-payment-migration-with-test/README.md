# Payment-message migration with regression test

This follow-up asks whether a required failing regression test changes the output
of the payment-message migration probe. It did in this small Luna run set: all six
agents constructed a real `RetryEnvelope`; no agent selected `cast`. Strict `ty`,
the regression test, and anti-slop passed on all six outputs.

The matched Luna runs without the test produced three casts in six attempts. This
comparison demonstrates that the supplied test catches this specific failure mode;
six runs per condition are not enough to estimate the size of the effect.

## Protocol

- Date: 2026-08-31
- Model: `gpt-5.6-luna`
- Reasoning efforts: `low` and `medium`
- Runs: 3 independent invocations at each effort (6 total)
- Every run received the same [`prompt.md`](prompt.md),
  [`seed/consumer.py`](seed/consumer.py), and
  [`seed/test_consumer.py`](seed/test_consumer.py).
- The seed fails both strict `ty` and the regression test.
- The authoring agents could run only `ty check --error all consumer.py
  test_consumer.py` and `python3.13 -m unittest -v`.
- Agents had to leave the test unchanged and stop only after both commands passed.
- Anti-slop was not named in the task and was run afterward by the orchestrator.
- Outputs are preserved whether or not they support the hypothesis.

This is a matched follow-up to
[`2026-08-payment-migration`](../2026-08-payment-migration/README.md): the data
models and required indexing expression are the same, while the prompt and stopping
condition add the regression test.

## Toolchain

| Tool | Version / revision |
|---|---|
| Python / unittest | `3.13.3` |
| ty | `0.0.74` (`00199f0aa`, built 2026-08-22) |
| anti-slop-py | `0.1.0`, upstream `86ea16d3abb2322e0496c5b6da8cd6d5704166cf` |

## Layout

```text
probes/agent-runs/2026-08-payment-migration-with-test/
  README.md
  prompt.md
  seed/consumer.py
  seed/test_consumer.py
  low/luna-01/{consumer.py,test_consumer.py}
  low/luna-02/{consumer.py,test_consumer.py}
  low/luna-03/{consumer.py,test_consumer.py}
  medium/luna-01/{consumer.py,test_consumer.py}
  medium/luna-02/{consumer.py,test_consumer.py}
  medium/luna-03/{consumer.py,test_consumer.py}
  results.md
```

## Reproduce

From the repository root:

```bash
cd probes/agent-runs/2026-08-payment-migration-with-test/medium/luna-01
ty check --error all consumer.py test_consumer.py
python3.13 -m unittest -v
anti-slop consumer.py
```

See [`results.md`](results.md) for all six outcomes and raw command output.

## Limitations

- The regression test directly exercises the exact failure shown by the original
  probe. This is a strong safety net for this case, not a representative estimate
  of test coverage in maintenance work.
- The prompt explicitly requires a green test and allows agents to run it. This
  probe measures behavior with that feedback loop, not whether agents write tests
  when none are supplied.
- Six runs on one model cannot estimate a failure rate or establish that tests
  eliminate unchecked assertions generally.
- The no-test and with-test runs are matched run sets, not paired samples with
  controlled randomness.
- A green test exercises selected behavior; anti-slop addresses unchecked type
  assertions whether or not a reviewer anticipated the missing runtime case.
