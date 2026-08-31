"""Regression tests for retry key construction."""
import unittest
from consumer import PaymentMessage, retry_key

class RetryKeyTests(unittest.TestCase):
    def test_payment_message_fields_are_used(self) -> None:
        message = PaymentMessage(payment_id="pay_123", amount_cents=2500)
        self.assertEqual(retry_key(message), "payment:pay_123:2500")

if __name__ == "__main__":
    unittest.main()
