"""Retry key construction during the payment queue rollout."""

from dataclasses import dataclass
from typing import TypedDict

@dataclass(frozen=True, slots=True)
class PaymentMessage:
    """New message shape emitted by migrated producers."""
    payment_id: str
    amount_cents: int

class RetryEnvelope(TypedDict):
    """Legacy wire shape still emitted during the rollout."""
    payment_id: str
    amount_cents: int

def retry_key(message: PaymentMessage | RetryEnvelope) -> str:
    """Build the idempotency key used by the retry queue."""
    envelope: RetryEnvelope = message
    return f"payment:{envelope['payment_id']}:{envelope['amount_cents']}"

__all__ = ["PaymentMessage", "RetryEnvelope", "retry_key"]
