import sys
import os
import json
import io
import unittest
from datetime import datetime



# Add cwd to path for vte package resolution
sys.path.append(os.getcwd())
try:
    from vte.ops.logger import get_logger, JsonFormatter
    from vte.ops.timeline import TimelineExporter
except ImportError as e:
    print(f"FAIL: Could not import vte.ops: {e}")
    sys.exit(1)

class TestObservability(unittest.TestCase):
    
    def test_json_logger(self):
        # Capture stdout
        captured = io.StringIO()
        handler = logging.StreamHandler(captured)
        handler.setFormatter(JsonFormatter())
        
        logger = logging.getLogger("test_json")
        logger.handlers = [] # Clear existing
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
        # Log event with PII
        logger.info("User email is test@example.com")
        
        output = captured.getvalue()
        try:
            log_entry = json.loads(output)
        except json.JSONDecodeError:
            self.fail("Log output is not valid JSON")
            
        self.assertEqual(log_entry["level"], "INFO")
        self.assertIn("[REDACTED_PII_EMAIL]", log_entry["message"])
        self.assertEqual(log_entry["logger"], "test_json")
        self.assertTrue("timestamp" in log_entry)

    def test_timeline_export(self):
        exporter = TimelineExporter()
        
        events = [
            {
                "timestamp_utc": "2023-01-01T12:00:00Z",
                "event_type": "ALERT_FIRED",
                "actor": "system",
                "details": {"alert_id": "cpu_high"}
            },
            {
                "timestamp_utc": "2023-01-01T12:05:00Z",
                "event_type": "MITIGATION_ACTION",
                "actor": "oncall_engineer",
                "details": {"action": "scale_up"}
            }
        ]
        
        output = exporter.export_timeline("INC-123", events)
        
        # Check T-1300 Schema Compliance
        self.assertEqual(output["incident_id"], "INC-123")
        self.assertEqual(output["start_time_utc"], "2023-01-01T12:00:00Z")
        self.assertEqual(output["end_time_utc"], "2023-01-01T12:05:00Z")
        self.assertEqual(len(output["events"]), 2)
        
        # Verify event structure
        self.assertEqual(output["events"][0]["event_type"], "ALERT_FIRED")

if __name__ == "__main__":
    import logging
    unittest.main()
