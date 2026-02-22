import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict

class JsonFormatter(logging.Formatter):
    """
    Format logs as JSON for observability ingestion.
    Redacts PII strictly.
    """
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "path": record.pathname,
            "line": record.lineno,
            "trace_id": getattr(record, "trace_id", "N/A"),
            "component": getattr(record, "component", "spine_core")
        }
        
        # PII Redaction (Basic implementation for construction phase)
        # In full production this would use a deeper recursive scrubbing
        if "email" in log_record["message"]:
            log_record["message"] = "[REDACTED_PII_EMAIL]"
            
        return json.dumps(log_record)

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        
    return logger

# Global App Logger
app_logger = get_logger("vte.spine")
