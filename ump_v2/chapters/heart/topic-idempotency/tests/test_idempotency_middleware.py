import sys
import unittest
import time
from datetime import timedelta
from pathlib import Path

current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from idempotency_middleware import IdempotencyMiddleware, DuplicateExecutionError

class TestIdempotencyMiddleware(unittest.TestCase):
    
    def setUp(self):
        # Set a short TTL for testing expiry
        self.middleware = IdempotencyMiddleware(default_ttl_seconds=1)

    def test_first_execution_succeeds(self):
        ws_id = "tenant_1"
        action = "SEND_EMAIL"
        payload = {"to": "user@example.com", "body": "test"}
        
        intent_hash = self.middleware.check_and_record(ws_id, action, payload)
        self.assertIsNotNone(intent_hash)

    def test_duplicate_execution_fails(self):
        ws_id = "tenant_1"
        action = "SEND_EMAIL"
        payload = {"to": "user@example.com", "body": "test"}
        
        # First execution
        self.middleware.check_and_record(ws_id, action, payload)
        
        # Second execution within TTL
        with self.assertRaises(DuplicateExecutionError) as context:
            self.middleware.check_and_record(ws_id, action, payload)
            
        self.assertIn("Idempotency Guard", str(context.exception))

    def test_different_payloads_succeed(self):
        ws_id = "tenant_1"
        action = "SEND_EMAIL"
        payload1 = {"to": "user@example.com", "body": "test1"}
        payload2 = {"to": "user@example.com", "body": "test2"}
        
        hash1 = self.middleware.check_and_record(ws_id, action, payload1)
        hash2 = self.middleware.check_and_record(ws_id, action, payload2)
        
        self.assertNotEqual(hash1, hash2)
        
    def test_expired_execution_succeeds(self):
        ws_id = "tenant_1"
        action = "SEND_EMAIL"
        payload = {"to": "user@example.com", "body": "test"}
        
        self.middleware.check_and_record(ws_id, action, payload)
        
        # Artificial timeout to bypass the fast unittests and trigger TTL expiry (requires slightly manipulating the store manually for speed without sleep)
        # We simulate the passing of time by subtracting the TTL
        intent_hash = self.middleware._generate_hash(ws_id, action, payload)
        self.middleware._store[intent_hash] -= timedelta(seconds=2)
        
        # Should now succeed again
        try:
             self.middleware.check_and_record(ws_id, action, payload)
        except DuplicateExecutionError:
             self.fail("check_and_record raised DuplicateExecutionError on expired execution")

if __name__ == '__main__':
    unittest.main()
