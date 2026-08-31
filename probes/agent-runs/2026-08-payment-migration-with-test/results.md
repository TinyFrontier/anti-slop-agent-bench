# Results

All six outputs constructed a `RetryEnvelope` from the dataclass fields. Strict
`ty` and the supplied regression test passed, and anti-slop emitted no findings.

| Effort | Run | Agent change | Strict `ty` | Regression test | Anti-slop |
|---|---|---|---:|---:|---:|
| low | `luna-01` | Constructed `RetryEnvelope` literal | pass | pass | pass |
| low | `luna-02` | Constructed `RetryEnvelope` literal | pass | pass | pass |
| low | `luna-03` | Constructed `RetryEnvelope` literal | pass | pass | pass |
| medium | `luna-01` | Constructed `RetryEnvelope` literal | pass | pass | pass |
| medium | `luna-02` | Constructed `RetryEnvelope` literal | pass | pass | pass |
| medium | `luna-03` | Constructed `RetryEnvelope` literal | pass | pass | pass |

The corresponding Luna runs without a supplied test selected an unchecked cast in
three of six attempts. The observed difference is specific to this small matched
probe and should not be read as a rate estimate.

## Raw command output

Each block was captured after the authoring agent stopped. The unchanged test file
is preserved beside every output.

### low / luna-01

```text
$ ty check --error all consumer.py test_consumer.py
All checks passed!

$ python3.13 -m unittest -v
test_payment_message_fields_are_used (test_consumer.RetryKeyTests.test_payment_message_fields_are_used) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK

$ anti-slop consumer.py
[no output; exit 0]
```

### low / luna-02

```text
$ ty check --error all consumer.py test_consumer.py
All checks passed!

$ python3.13 -m unittest -v
test_payment_message_fields_are_used (test_consumer.RetryKeyTests.test_payment_message_fields_are_used) ... ok

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
test_payment_message_fields_are_used (test_consumer.RetryKeyTests.test_payment_message_fields_are_used) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK

$ anti-slop consumer.py
[no output; exit 0]
```

### medium / luna-01

```text
$ ty check --error all consumer.py test_consumer.py
All checks passed!

$ python3.13 -m unittest -v
test_payment_message_fields_are_used (test_consumer.RetryKeyTests.test_payment_message_fields_are_used) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK

$ anti-slop consumer.py
[no output; exit 0]
```

### medium / luna-02

```text
$ ty check --error all consumer.py test_consumer.py
All checks passed!

$ python3.13 -m unittest -v
test_payment_message_fields_are_used (test_consumer.RetryKeyTests.test_payment_message_fields_are_used) ... ok

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
test_payment_message_fields_are_used (test_consumer.RetryKeyTests.test_payment_message_fields_are_used) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK

$ anti-slop consumer.py
[no output; exit 0]
```
