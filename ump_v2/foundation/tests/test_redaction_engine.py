import sys
import unittest
from pathlib import Path

# Explicitly ensure ump_v2 is in PYTHONPATH for the test runner
current_dir = Path(__file__).resolve().parent
uml_v2_root = current_dir.parent.parent
sys.path.insert(0, str(uml_v2_root))

from foundation.src.security.redaction_engine import RedactionEngine

class TestRedactionEngine(unittest.TestCase):

    def setUp(self):
        self.engine = RedactionEngine()

    def test_exact_key_redaction(self):
        payload = {
            "user": "Alice",
            "ssn": "123-456-7890",
            "public_id": "888"
        }
        redacted = self.engine.redact(payload)
        self.assertEqual(redacted["user"], "Alice")
        self.assertEqual(redacted["public_id"], "888")
        self.assertEqual(redacted["ssn"], "[REDACTED]")

    def test_partial_key_redaction(self):
        payload = {
            "user_email_address": "alice@example.com",
            "home_phone_number": "555-0100"
        }
        redacted = self.engine.redact(payload)
        self.assertEqual(redacted["user_email_address"], "[REDACTED]")
        self.assertEqual(redacted["home_phone_number"], "[REDACTED]")

    def test_nested_dictionary_redaction(self):
        payload = {
            "metadata": {
                "source": "api",
                "customer": {
                    "name": "Bob",
                    "credit_card": "4111-1111-1111-1111"
                }
            }
        }
        redacted = self.engine.redact(payload)
        self.assertEqual(redacted["metadata"]["source"], "api")
        self.assertEqual(redacted["metadata"]["customer"]["credit_card"], "[REDACTED]")
        self.assertEqual(redacted["metadata"]["customer"]["name"], "[REDACTED]")

    def test_list_redaction(self):
        payload = [
            {"id": 1, "ssn": "000"},
            {"id": 2, "ssn": "111"}
        ]
        redacted = self.engine.redact(payload)
        self.assertEqual(redacted[0]["id"], 1)
        self.assertEqual(redacted[0]["ssn"], "[REDACTED]")
        self.assertEqual(redacted[1]["ssn"], "[REDACTED]")

if __name__ == '__main__':
    unittest.main()
