from vte.worker import celery_app
import time
from vte.agents.ingest import IngestionAgent
from vte.agents.auditor import AuditorAgent

# ... (debug tasks)

@celery_app.task(name="agents.ingest.run_once")
def run_ingest_agent():
    """
    Periodic task to run the Ingestion Agent.
    """
    agent = IngestionAgent()
    return agent.run()

@celery_app.task(name="agents.auditor.audit_unit")
def run_auditor_agent(unit_id: str = "101"):
    """
    Task to audit a specific unit.
    """
    agent = AuditorAgent()
    return agent.run(unit_id=unit_id)
def ping():
    """
    Simple task to verify worker connectivity.
    """
    return "pong"

@celery_app.task(name="debug.sleep")
def sleep_task(seconds: int):
    """
    Simulate work.
    """
    time.sleep(seconds)
    return f"Slep for {seconds}s"
from vte.db import SessionLocal
from vte.orm import DecisionObject
from vte.api.schema import OutcomeEnum
from vte.adapters.appfolio.client import AppFolioClient
import logging

logger = logging.getLogger("vte.tasks.execution")

@celery_app.task(name="execution.decision.execute")
def execute_decision(decision_id: str):
    """
    Executes an APPROVED decision using the VTE Workflow Engine.
    This replaces hardcoded logic with Contract-Driven Execution.
    """
    logger.info(f"Delegate Execution to Engine: {decision_id}")
    db = SessionLocal()
    try:
        from vte.core.engine import WorkflowEngine
        import uuid
        
        engine = WorkflowEngine(db)
        result = engine.execute_decision(uuid.UUID(decision_id))
        
        logger.info(f"Engine Result: {result}")
        return result

    except Exception as e:
        logger.error(f"Engine Execution Failed: {e}")
        # raise e # Retry?
        return {"status": "failed", "error": str(e)}
    finally:
        db.close()

# --- Legacy Projections Removed (Moved to Engine) ---
# def handle_inventory_projection...
