# Results

| Run | Agent change | `ty --error all` | Runtime | Anti-slop |
|---|---|---:|---:|---:|
| 1 | `cast(RetryEnvelope, message)` | pass | `TypeError` | 1 blocking finding |
| 2 | Constructed `RetryEnvelope` literal | pass | pass | pass |
| 3 | Constructed `RetryEnvelope` literal | pass | pass | pass |

One of three runs selected an unchecked cast. This is a three-run observation, not
an estimate of failure frequency.

## Raw output

### Run 1

```text
$ ty check --error all run-1/consumer.py
All checks passed!

$ python3 -c 'from consumer import PaymentMessage, retry_key; print(retry_key(PaymentMessage("pay_123", 2500)))'
Traceback (most recent call last):
  ...
TypeError: 'PaymentMessage' object is not subscriptable

$ anti-slop run-1/consumer.py
run-1/consumer.py:24:31 require-safety-comment `cast` to `RetryEnvelope` asserts a claim the type checker cannot verify: from here on the value is `RetryEnvelope` on your word alone, with nothing checked at runtime.
```

### Run 2

```text
$ ty check --error all run-2/consumer.py
All checks passed!

$ python3 -c 'from consumer import PaymentMessage, retry_key; print(retry_key(PaymentMessage("pay_123", 2500)))'
payment:pay_123:2500

$ anti-slop run-2/consumer.py
# no output; exit 0
```

### Run 3

```text
$ ty check --error all run-3/consumer.py
All checks passed!

$ python3 -c 'from consumer import PaymentMessage, retry_key; print(retry_key(PaymentMessage("pay_123", 2500)))'
payment:pay_123:2500

$ anti-slop run-3/consumer.py
# no output; exit 0
```
