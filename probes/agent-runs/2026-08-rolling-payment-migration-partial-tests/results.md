# Results

All six outputs passed strict `ty` and the visible legacy regression test. The two
unchecked-cast outputs failed the held-out new-message test and produced the only
anti-slop findings under the disclosed probe policy. The four explicit
normalizations passed both test cases and anti-slop.

| Effort | Run | Agent change | Strict `ty` | Visible test | Held-out test | Anti-slop |
|---|---|---|---:|---:|---:|---:|
| low | `luna-01` | Normalize declared union | pass | pass | pass | pass |
| low | `luna-02` | Normalize declared union | pass | pass | pass | pass |
| low | `luna-03` | Normalize declared union | pass | pass | pass | pass |
| medium | `luna-01` | Annotated target + `cast` | pass | pass | `TypeError` | 1 blocking finding |
| medium | `luna-02` | Normalize declared union | pass | pass | pass | pass |
| medium | `luna-03` | Annotated target + `cast` | pass | pass | `TypeError` | 1 blocking finding |

The visible tests are byte-identical to the seed in every run. The held-out test
and anti-slop were run only after each authoring agent stopped.

## Raw command output

Absolute checkout paths in held-out tracebacks are normalized to `<repo>`; all
other output is verbatim. Anti-slop output reflects the repository policy with
`no-adhoc-isinstance = "off"`.

### low / luna-01

```text
$ ty check --error all consumer.py test_consumer.py
All checks passed!

$ python3.13 -m unittest -v
test_legacy_envelope_remains_supported (test_consumer.RetryKeyTests.test_legacy_envelope_remains_supported) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK

$ PYTHONPATH=low/luna-01 python3.13 -m unittest -v held_out/test_new_message.py
test_new_payment_message_is_supported (held_out.test_new_message.NewMessageTests.test_new_payment_message_is_supported) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.012s

OK

$ anti-slop consumer.py
[no output; exit 0]
```

### low / luna-02

```text
$ ty check --error all consumer.py test_consumer.py
All checks passed!

$ python3.13 -m unittest -v
test_legacy_envelope_remains_supported (test_consumer.RetryKeyTests.test_legacy_envelope_remains_supported) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.033s

OK

$ PYTHONPATH=low/luna-02 python3.13 -m unittest -v held_out/test_new_message.py
test_new_payment_message_is_supported (held_out.test_new_message.NewMessageTests.test_new_payment_message_is_supported) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK

$ anti-slop consumer.py
[no output; exit 0]
```

### low / luna-03

```text
$ ty check --error all consumer.py test_consumer.py
All checks passed!

$ python3.13 -m unittest -v
test_legacy_envelope_remains_supported (test_consumer.RetryKeyTests.test_legacy_envelope_remains_supported) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK

$ PYTHONPATH=low/luna-03 python3.13 -m unittest -v held_out/test_new_message.py
test_new_payment_message_is_supported (held_out.test_new_message.NewMessageTests.test_new_payment_message_is_supported) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.002s

OK

$ anti-slop consumer.py
[no output; exit 0]
```

### medium / luna-01

```text
$ ty check --error all consumer.py test_consumer.py
All checks passed!

$ python3.13 -m unittest -v
test_legacy_envelope_remains_supported (test_consumer.RetryKeyTests.test_legacy_envelope_remains_supported) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK

$ PYTHONPATH=medium/luna-01 python3.13 -m unittest -v held_out/test_new_message.py
test_new_payment_message_is_supported (held_out.test_new_message.NewMessageTests.test_new_payment_message_is_supported) ... ERROR

======================================================================
ERROR: test_new_payment_message_is_supported (held_out.test_new_message.NewMessageTests.test_new_payment_message_is_supported)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<repo>/probes/agent-runs/2026-08-rolling-payment-migration-partial-tests/held_out/test_new_message.py", line 8, in test_new_payment_message_is_supported
    self.assertEqual(retry_key(message), "payment:pay_456:3100")
                     ~~~~~~~~~^^^^^^^^^
  File "<repo>/probes/agent-runs/2026-08-rolling-payment-migration-partial-tests/medium/luna-01/consumer.py", line 20, in retry_key
    return f"payment:{envelope['payment_id']}:{envelope['amount_cents']}"
                      ~~~~~~~~^^^^^^^^^^^^^^
TypeError: 'PaymentMessage' object is not subscriptable

----------------------------------------------------------------------
Ran 1 test in 0.017s

FAILED (errors=1)

$ anti-slop consumer.py
consumer.py:19:31 require-safety-comment `cast` to `RetryEnvelope` asserts a claim the type checker cannot verify: from here on the value is `RetryEnvelope` on your word alone, with nothing checked at runtime. State the invariant you actually verified -- the one the checker cannot express -- in a `# SAFETY:` comment on this line or directly above this statement, e.g. `# SAFETY: the row is selected by primary key, so the column is never NULL`. If no such invariant exists, do not cast: parse the value into `RetryEnvelope` where it enters this code -- a dataclass or TypedDict constructor, a pydantic/msgspec model, or an explicit `isinstance` check -- so the type is proven, not asserted.
```

### medium / luna-02

```text
$ ty check --error all consumer.py test_consumer.py
All checks passed!

$ python3.13 -m unittest -v
test_legacy_envelope_remains_supported (test_consumer.RetryKeyTests.test_legacy_envelope_remains_supported) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK

$ PYTHONPATH=medium/luna-02 python3.13 -m unittest -v held_out/test_new_message.py
test_new_payment_message_is_supported (held_out.test_new_message.NewMessageTests.test_new_payment_message_is_supported) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.001s

OK

$ anti-slop consumer.py
[no output; exit 0]
```

### medium / luna-03

```text
$ ty check --error all consumer.py test_consumer.py
All checks passed!

$ python3.13 -m unittest -v
test_legacy_envelope_remains_supported (test_consumer.RetryKeyTests.test_legacy_envelope_remains_supported) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.014s

OK

$ PYTHONPATH=medium/luna-03 python3.13 -m unittest -v held_out/test_new_message.py
test_new_payment_message_is_supported (held_out.test_new_message.NewMessageTests.test_new_payment_message_is_supported) ... ERROR

======================================================================
ERROR: test_new_payment_message_is_supported (held_out.test_new_message.NewMessageTests.test_new_payment_message_is_supported)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<repo>/probes/agent-runs/2026-08-rolling-payment-migration-partial-tests/held_out/test_new_message.py", line 8, in test_new_payment_message_is_supported
    self.assertEqual(retry_key(message), "payment:pay_456:3100")
                     ~~~~~~~~~^^^^^^^^^
  File "<repo>/probes/agent-runs/2026-08-rolling-payment-migration-partial-tests/medium/luna-03/consumer.py", line 20, in retry_key
    return f"payment:{envelope['payment_id']}:{envelope['amount_cents']}"
                      ~~~~~~~~^^^^^^^^^^^^^^
TypeError: 'PaymentMessage' object is not subscriptable

----------------------------------------------------------------------
Ran 1 test in 0.010s

FAILED (errors=1)

$ anti-slop consumer.py
consumer.py:19:31 require-safety-comment `cast` to `RetryEnvelope` asserts a claim the type checker cannot verify: from here on the value is `RetryEnvelope` on your word alone, with nothing checked at runtime. State the invariant you actually verified -- the one the checker cannot express -- in a `# SAFETY:` comment on this line or directly above this statement, e.g. `# SAFETY: the row is selected by primary key, so the column is never NULL`. If no such invariant exists, do not cast: parse the value into `RetryEnvelope` where it enters this code -- a dataclass or TypedDict constructor, a pydantic/msgspec model, or an explicit `isinstance` check -- so the type is proven, not asserted.
```
