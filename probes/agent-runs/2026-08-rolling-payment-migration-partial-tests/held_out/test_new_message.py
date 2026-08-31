"""Held-out coverage for the new producer payload."""
import unittest
from consumer import PaymentMessage, retry_key

class NewMessageTests(unittest.TestCase):
    def test_new_payment_message_is_supported(self) -> None:
        message = PaymentMessage(payment_id="pay_456", amount_cents=3100)
        self.assertEqual(retry_key(message), "payment:pay_456:3100")

if __name__ == "__main__":
    unittest.main()
