# Rolling payment migration with partial test coverage

This probe models a rolling queue migration where `retry_key` must accept both a
legacy dictionary and a new dataclass, while the existing test covers only the
legacy form. All six Luna outputs passed strict `ty` and the visible regression
test. Two used an unchecked `cast`; both failed the held-out new-message test and
were the only outputs blocked by the configured anti-slop policy. The other four
implemented both branches and passed every check.

This is the gap the earlier probes left open: tests exist and run in the authoring
loop, but their behavioral coverage is incomplete.

## Protocol

- Date: 2026-08-31
- Model: `gpt-5.6-luna`
- Reasoning efforts: `low` and `medium`
- Runs: 3 independent invocations at each effort (6 total)
- Every run received the same [`prompt.md`](prompt.md),
  [`seed/consumer.py`](seed/consumer.py), and visible
  [`seed/test_consumer.py`](seed/test_consumer.py).
- The seed fails strict `ty` while the visible legacy test passes.
- The authoring agents could run only `ty check --error all consumer.py
  test_consumer.py` and `python3.13 -m unittest -v`.
- Agents had to leave the visible test unchanged and stop after both commands
  passed.
- The [`held_out/test_new_message.py`](held_out/test_new_message.py) test and
  anti-slop were unavailable to agents and run only after they stopped.
- Outputs are preserved whether or not they support the hypothesis.

## Anti-slop policy

This probe evaluates unchecked assertions, so the repository configuration sets
`require-safety-comment = "error"`. It explicitly sets
`no-adhoc-isinstance = "off"`: the public function contract intentionally accepts
two runtime representations, and the four correct outputs discriminate those
declared union members before normalization.

Without that override, `no-adhoc-isinstance` also reports the four correct outputs.
That initial result is a real false-positive limitation of the broader default
policy for this scenario, not omitted evidence. With the declared probe policy,
anti-slop separates the two held-out failures from the four held-out passes.

## Toolchain

| Tool | Version / revision |
|---|---|
| Python / unittest | `3.13.3` |
| ty | `0.0.74` (`00199f0aa`, built 2026-08-22) |
| anti-slop-py | `0.1.0`, upstream `86ea16d3abb2322e0496c5b6da8cd6d5704166cf` |

## Layout

```text
probes/agent-runs/2026-08-rolling-payment-migration-partial-tests/
  README.md
  prompt.md
  seed/consumer.py
  seed/test_consumer.py
  held_out/test_new_message.py
  low/luna-01/{consumer.py,test_consumer.py}
  low/luna-02/{consumer.py,test_consumer.py}
  low/luna-03/{consumer.py,test_consumer.py}
  medium/luna-01/{consumer.py,test_consumer.py}
  medium/luna-02/{consumer.py,test_consumer.py}
  medium/luna-03/{consumer.py,test_consumer.py}
  results.md
```

## Reproduce

From the repository root, using one of the two cast outputs:

```bash
ty check --error all probes/agent-runs/2026-08-rolling-payment-migration-partial-tests/medium/luna-01/consumer.py probes/agent-runs/2026-08-rolling-payment-migration-partial-tests/medium/luna-01/test_consumer.py
cd probes/agent-runs/2026-08-rolling-payment-migration-partial-tests/medium/luna-01
python3.13 -m unittest -v
cd ../..
PYTHONPATH=medium/luna-01 python3.13 -m unittest -v held_out/test_new_message.py
anti-slop medium/luna-01/consumer.py
```

See [`results.md`](results.md) for all six outcomes and raw command output.

## Limitations

- The held-out test is an evaluator constructed from behavior explicitly required
  by the prompt. It demonstrates a concrete missed branch, not an estimate of
  production test-suite quality.
- Six runs on one model cannot estimate a failure rate or establish how often
  partial tests and unchecked casts coincide in real repositories.
- The prompt asks for the smallest patch while preserving the indexing expression,
  which creates pressure toward a cast. Four of six runs still found a correct
  solution under the same constraints.
- Selectivity depends on the disclosed rule configuration. The default
  `no-adhoc-isinstance` finding on all four correct outputs should be addressed
  before using that rule for this kind of boundary code.
