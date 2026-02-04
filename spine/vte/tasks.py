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
    Executes an APPROVED decision.
    Currently supports: 'write_note' action on AppFolio.
    """
    logger.info(f"Executing Decision {decision_id}")
    db = SessionLocal()
    try:
        decision = db.query(DecisionObject).filter(DecisionObject.decision_id == decision_id).first()
        if not decision:
            logger.error(f"Decision {decision_id} not found.")
            return {"status": "failed", "reason": "not_found"}
            
        if decision.outcome != OutcomeEnum.APPROVED:
            logger.warning(f"Decision {decision_id} is not APPROVED ({decision.outcome}). Skipped.")
            return {"status": "skipped", "reason": "not_approved"}

        action = decision.intent_action
        target = decision.intent_target
        params = decision.intent_params or {}

        if action == "write_note":
            logger.info("Action: Write Note")
            client = AppFolioClient() 
            try:
                # Initialize Client (Headless by default, uses env vars for cookie)
                client.start()
                
                # Navigate
                if not client.navigate_to_tenant(target):
                    return {"status": "failed", "reason": "navigation_failed"}
                
                # Write
                content = params.get("content", "")
                dry_run = params.get("dry_run", False)
                
                if not content:
                     return {"status": "failed", "reason": "content_empty"}
                     
                if client.write_note(content, dry_run=dry_run):
                    return {"status": "success", "action": "write_note"}
                else:
                    return {"status": "failed", "reason": "write_failed"}
            except Exception as e:
                logger.error(f"Action Execution Error: {e}")
                return {"status": "failed", "error": str(e)}
            finally:
                client.close()
                
        else:
            logger.warning(f"Unknown Action: {action}")
            return {"status": "failed", "reason": "unknown_action"}
            
    except Exception as e:
        logger.error(f"Execution Task Error: {e}")
        raise e
    finally:
        db.close()
