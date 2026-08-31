"""Existing regression coverage for the legacy retry payload."""
import unittest
from consumer import RetryEnvelope, retry_key

class RetryKeyTests(unittest.TestCase):
    def test_legacy_envelope_remains_supported(self) -> None:
        message: RetryEnvelope = {"payment_id": "pay_123", "amount_cents": 2500}
        self.assertEqual(retry_key(message), "payment:pay_123:2500")

if __name__ == "__main__":
    unittest.main()
