from typing import Dict, Any, List, Optional
from vte.core.agent import Agent
from vte.adapters.google.client import GmailClient
from vte.adapters.appfolio.client import AppFolioClient
from vte.api.schema import DecisionDraft, Actor, RoleEnum, Intent, OutcomeEnum
import hashlib
import json
import os
import requests
from datetime import datetime

class AuditorAgent(Agent):
    """
    Analyzes discrepancies between Tenants and Ledgers.
    """
    def __init__(self, agent_id: str = "auditor-01"):
        super().__init__(agent_id)
        self.gmail = GmailClient()
        self.appfolio = AppFolioClient()
        self.api_url = os.getenv("API_URL", "http://spine-api:8000/api/v1")

    def run(self, unit_id: str = "101") -> Dict[str, Any]:
        self.logger.info(f"Starting Audit for Unit {unit_id}...")

        # 1. Check Ledger (Truth)
        ledger = self.appfolio.fetch_ledger(unit_id)
        # Mock Logic: If generic mock, let's pretend balance is 1000
        balance = ledger.get("balance", 1000.0) 
        
        if balance <= 0:
            self.logger.info(f"Unit {unit_id} is clean (Balance: {balance}). No action.")
            return {"status": "clean", "balance": balance}

        self.logger.info(f"Unit {unit_id} is DELINQUENT (Balance: {balance}). Checking Tenant claims...")

        # 2. Check Emails (Claims)
        # In real life, we'd search for the tenant's email associated with Unit 101.
        # Here we mock-search for "payment"
        claims = []
        try:
            emails = self.gmail.fetch_emails(query=f"subject:payment unit:{unit_id}", max_results=1)
            if emails:
                self.logger.info(f"Found {len(emails)} payment claims via email.")
                claims = emails
            else:
                 self.logger.info("No payment claims found in email.")
        except Exception as e:
            self.logger.warning(f"Email fetch failed: {e}")

        # 3. Formulate Decision
        
        outcome = OutcomeEnum.NEEDS_MORE_EVIDENCE
        
        if claims:
            # USE LLM HERE
            from vte.core.llm import LLMClient
            llm = LLMClient()
            
            ledger_str = f"Unit: {unit_id}, Balance: {balance}"
            email_str = f"Subject: {claims[0]['subject']}, Snippet: {claims[0].get('snippet', '')}"
            
            analysis = llm.analyze_discrepancy(ledger_str, email_str)
            
            explanation = f"LLM ANALYSIS: {analysis}"
        else:
            explanation = f"Delinquency detected (Balance: {balance}). No tenant contact found."

        # 4. Draft Decision for Human Review
        draft = DecisionDraft(
            actor=Actor(
                user_id=self.agent_id,
                role=RoleEnum.system_bot
            ),
            intent=Intent(
                action="audit_delinquency",
                target_resource=f"unit:{unit_id}",
                parameters={
                    "balance": balance,
                    "claims_count": len(claims),
                    "explanation": explanation
                }
            ),
            evidence_hash=None, 
            outcome=outcome,
            policy_version="v2.0-beta"
        )

        # 5. Submit Draft
        try:
           self.emit(draft)
           self.logger.info(f"Submitted Decision Draft: {draft.model_dump_json()}")
           return {"status": "discrepancy_found", "draft": draft.model_dump()}
           
        except Exception as e:
            self.logger.error(f"Error submitting decision draft: {e}")

        return {"status": "audit_complete"}
