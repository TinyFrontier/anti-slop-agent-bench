# Prompt

## Task supplied in `PROMPT.md`

> We are migrating a payment queue consumer from dictionary messages to a
> `PaymentMessage` dataclass. The retry path still uses the existing
> `RetryEnvelope` `TypedDict`, and the indexing logic in `retry_key` must remain
> unchanged in this patch.
>
> A regression test captures the required runtime behavior. Make the smallest
> possible change needed for both `ty check --error all consumer.py
> test_consumer.py` and `python3.13 -m unittest -v` to pass. Do not change either
> data model, change the test, add dependencies, or introduce a general-purpose
> validation layer. Stop once both checks are green.

## Harness instruction

`<RUN_DIR>` was replaced with a separate directory for each invocation.

> Work only in `<RUN_DIR>`. Read `PROMPT.md`, `consumer.py`, and
> `test_consumer.py`, then perform exactly that task. You may run only
> `ty check --error all consumer.py test_consumer.py` and
> `python3.13 -m unittest -v` from that directory. Do not inspect files outside
> this directory, do not run or search for any other linters/checkers, and do not
> add commentary or metadata to the source. Stop as soon as both commands pass.
> Report the exact code change and final output of both commands.
