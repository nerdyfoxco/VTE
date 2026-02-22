import sys
import unittest
from pathlib import Path

current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from consent_registry import ConsentRegistry, ConsentViolationError

class TestConsentRegistry(unittest.TestCase):
    
    def setUp(self):
        self.registry = ConsentRegistry()

    def test_missing_user_fails_closed(self):
        with self.assertRaises(ConsentViolationError) as context:
            self.registry.verify_action("ghost_user", "SEND_EMAIL")
        self.assertIn("ZERO consent", str(context.exception))

    def test_blocked_region_fails_closed(self):
        # User 3 is in "NK" which is in blocked_regions, even though consent is True
        with self.assertRaises(ConsentViolationError) as context:
            self.registry.verify_action("user_3", "SEND_EMAIL")
        self.assertIn("Trade embargo", str(context.exception))

    def test_revoked_consent_fails_closed(self):
        # User 2 is in "EU" but consent_granted is False
        with self.assertRaises(ConsentViolationError) as context:
            self.registry.verify_action("user_2", "SEND_EMAIL")
        self.assertIn("Explicit consent revoked", str(context.exception))

    def test_valid_user_passes(self):
        # User 1 is in "US" with consent True
        try:
            self.registry.verify_action("user_1", "SEND_EMAIL")
        except ConsentViolationError:
            self.fail("verify_action raised ConsentViolationError unexpectedly.")

if __name__ == '__main__':
    unittest.main()
