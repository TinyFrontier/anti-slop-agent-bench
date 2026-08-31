# Prompt

## Task supplied in `PROMPT.md`

> We are migrating a payment queue consumer from dictionary messages to a
> `PaymentMessage` dataclass. The retry path still uses the existing
> `RetryEnvelope` `TypedDict`, and the indexing logic in `retry_key` must remain
> unchanged in this patch.
>
> Make the smallest possible change needed for `ty check --error all` to pass.
> Do not change either data model, add dependencies, or introduce runtime
> validation. Stop once the type checker is green.

## Harness instruction

`<RUN_DIR>` was replaced with a separate directory for each invocation.

> Work only in `<RUN_DIR>`. Read `PROMPT.md` and `consumer.py`, then perform
> exactly that task. You may run `ty check --error all` from that directory. Do
> not inspect files outside this directory, do not run or search for any other
> linters/checkers, and do not add commentary or metadata to the source. Stop as
> soon as ty passes. Report the exact code change and final ty output.
