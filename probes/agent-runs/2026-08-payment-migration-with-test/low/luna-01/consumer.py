"""Retry key construction for the payment queue."""

from dataclasses import dataclass
from typing import TypedDict

@dataclass(frozen=True, slots=True)
class PaymentMessage:
    """A message already validated by the queue adapter."""
    payment_id: str
    amount_cents: int

class RetryEnvelope(TypedDict):
    """Legacy wire shape used by the retry publisher."""
    payment_id: str
    amount_cents: int

def retry_key(message: PaymentMessage) -> str:
    """Build the idempotency key used by the retry queue."""
    envelope: RetryEnvelope = {"payment_id": message.payment_id, "amount_cents": message.amount_cents}
    return f"payment:{envelope['payment_id']}:{envelope['amount_cents']}"

__all__ = ["PaymentMessage", "RetryEnvelope", "retry_key"]
