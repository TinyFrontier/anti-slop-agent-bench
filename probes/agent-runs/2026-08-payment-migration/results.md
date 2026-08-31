# Results

| Effort | Run | Agent change | `ty --error all` | Runtime | Anti-slop |
|---|---|---|---:|---:|---:|
| low | `luna-01` | Constructed `RetryEnvelope` literal | pass | pass | pass |
| low | `luna-02` | Constructed `RetryEnvelope` literal | pass | pass | pass |
| low | `luna-03` | Annotated target + `cast` | pass | `TypeError` | 1 blocking finding |
| medium | `luna-01` | Inferred target + `cast` | pass | `TypeError` | 1 blocking finding |
| medium | `luna-02` | Constructed `RetryEnvelope` literal | pass | pass | pass |
| medium | `luna-03` | Annotated target + `cast` | pass | `TypeError` | 1 blocking finding |

One of three low-effort runs and two of three medium-effort runs selected an
unchecked cast. Two wrote `envelope: RetryEnvelope = cast(...)`, declaring the
target type both in the annotation and the unchecked assertion; one relied on the
type inferred from `envelope = cast(...)`. These six runs are a probe of one
failure mode, not an estimate of its frequency.

## Raw command output

Each block was captured after the authoring agent stopped. Absolute checkout paths
in tracebacks are normalized to `<repo>`; all other output is verbatim.

### low / luna-01

```text
$ ty check --error all consumer.py
All checks passed!

$ python3.13 -c 'from consumer import PaymentMessage, retry_key; print(retry_key(PaymentMessage("pay_123", 2500)))'
payment:pay_123:2500

$ anti-slop consumer.py
[no output; exit 0]
```

### low / luna-02

```text
$ ty check --error all consumer.py
All checks passed!

$ python3.13 -c 'from consumer import PaymentMessage, retry_key; print(retry_key(PaymentMessage("pay_123", 2500)))'
payment:pay_123:2500

$ anti-slop consumer.py
[no output; exit 0]
```

### low / luna-03

```text
$ ty check --error all consumer.py
All checks passed!

$ python3.13 -c 'from consumer import PaymentMessage, retry_key; print(retry_key(PaymentMessage("pay_123", 2500)))'
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from consumer import PaymentMessage, retry_key; print(retry_key(PaymentMessage("pay_123", 2500)))
                                                          ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<repo>/probes/agent-runs/2026-08-payment-migration/low/luna-03/consumer.py", line 25, in retry_key
    return f"payment:{envelope['payment_id']}:{envelope['amount_cents']}"
                      ~~~~~~~~^^^^^^^^^^^^^^
TypeError: 'PaymentMessage' object is not subscriptable

$ anti-slop consumer.py
consumer.py:24:31 require-safety-comment `cast` to `RetryEnvelope` asserts a claim the type checker cannot verify: from here on the value is `RetryEnvelope` on your word alone, with nothing checked at runtime. State the invariant you actually verified -- the one the checker cannot express -- in a `# SAFETY:` comment on this line or directly above this statement, e.g. `# SAFETY: the row is selected by primary key, so the column is never NULL`. If no such invariant exists, do not cast: parse the value into `RetryEnvelope` where it enters this code -- a dataclass or TypedDict constructor, a pydantic/msgspec model, or an explicit `isinstance` check -- so the type is proven, not asserted.
```

### medium / luna-01

```text
$ ty check --error all consumer.py
All checks passed!

$ python3.13 -c 'from consumer import PaymentMessage, retry_key; print(retry_key(PaymentMessage("pay_123", 2500)))'
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from consumer import PaymentMessage, retry_key; print(retry_key(PaymentMessage("pay_123", 2500)))
                                                          ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<repo>/probes/agent-runs/2026-08-payment-migration/medium/luna-01/consumer.py", line 25, in retry_key
    return f"payment:{envelope['payment_id']}:{envelope['amount_cents']}"
                      ~~~~~~~~^^^^^^^^^^^^^^
TypeError: 'PaymentMessage' object is not subscriptable

$ anti-slop consumer.py
consumer.py:24:16 require-safety-comment `cast` to `RetryEnvelope` asserts a claim the type checker cannot verify: from here on the value is `RetryEnvelope` on your word alone, with nothing checked at runtime. State the invariant you actually verified -- the one the checker cannot express -- in a `# SAFETY:` comment on this line or directly above this statement, e.g. `# SAFETY: the row is selected by primary key, so the column is never NULL`. If no such invariant exists, do not cast: parse the value into `RetryEnvelope` where it enters this code -- a dataclass or TypedDict constructor, a pydantic/msgspec model, or an explicit `isinstance` check -- so the type is proven, not asserted.
```

### medium / luna-02

```text
$ ty check --error all consumer.py
All checks passed!

$ python3.13 -c 'from consumer import PaymentMessage, retry_key; print(retry_key(PaymentMessage("pay_123", 2500)))'
payment:pay_123:2500

$ anti-slop consumer.py
[no output; exit 0]
```

### medium / luna-03

```text
$ ty check --error all consumer.py
All checks passed!

$ python3.13 -c 'from consumer import PaymentMessage, retry_key; print(retry_key(PaymentMessage("pay_123", 2500)))'
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from consumer import PaymentMessage, retry_key; print(retry_key(PaymentMessage("pay_123", 2500)))
                                                          ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<repo>/probes/agent-runs/2026-08-payment-migration/medium/luna-03/consumer.py", line 25, in retry_key
    return f"payment:{envelope['payment_id']}:{envelope['amount_cents']}"
                      ~~~~~~~~^^^^^^^^^^^^^^
TypeError: 'PaymentMessage' object is not subscriptable

$ anti-slop consumer.py
consumer.py:24:31 require-safety-comment `cast` to `RetryEnvelope` asserts a claim the type checker cannot verify: from here on the value is `RetryEnvelope` on your word alone, with nothing checked at runtime. State the invariant you actually verified -- the one the checker cannot express -- in a `# SAFETY:` comment on this line or directly above this statement, e.g. `# SAFETY: the row is selected by primary key, so the column is never NULL`. If no such invariant exists, do not cast: parse the value into `RetryEnvelope` where it enters this code -- a dataclass or TypedDict constructor, a pydantic/msgspec model, or an explicit `isinstance` check -- so the type is proven, not asserted.
```
