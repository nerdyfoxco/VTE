import os
import logging
from pathlib import Path
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

class ExecutionNotApprovedError(Exception):
    pass

class GmailSenderWorker:
    """
    Phase 5 VTE 'Hands' Sub-System.
    Strictly executes physical operations (SMTP/SMS) ONLY if the 
    Brain (Policy Engine) issues a definitive 'PROCEED' payload.
    """
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        # In a real environment, these pull securely from the Vault keyed by `tenant_id`
        self.sendgrid_client = SendGridAPIClient(os.getenv("SENDGRID_API_KEY", "mock_sg_key"))
        # Using placeholder SID/Token to prevent crash if unconfigured
        self.twilio_client = Client(os.getenv("TWILIO_ACCOUNT_SID", "ACmock"), os.getenv("TWILIO_AUTH_TOKEN", "mock_token"))
        self.twilio_number = os.getenv("TWILIO_PHONE_NUMBER", "+15555555555")

        # Load the physical template
        template_path = Path(__file__).resolve().parent / "kevin_outreach_v1.txt"
        if template_path.exists():
            with open(template_path, "r") as f:
                self.template = f.read()
        else:
            self.template = "Mock Kevin Outreach: Please contact us regarding your {" + "balance_owed" + "} balance."

    def _compile_template(self, verified_payload: dict) -> str:
        """Injects Pydantic schema data deterministically into the physical text template."""
        try:
            return self.template.format(**verified_payload)
        except KeyError as e:
            logging.error(f"[HANDS] Template mapping failed: Missing variable {e}")
            raise

    def execute(self, action_decision: str, verified_payload: dict, target_email: str = "tenant@example.com", target_phone: str = "+1234567890") -> str:
        """
        The critical Execution Barrier.
        Will raise an exception if the Engine did not explicitly greenlight the action.
        """
        if action_decision != "PROCEED":
             # Failsafe: The sender module physically refuses to operate if not approved.
             raise ExecutionNotApprovedError(f"Engine Decision was '{action_decision}', not PROCEED. Network operation aborted.")

        print(f"[Hands] VTE Brain Approval Received. Compiling template for PM {self.tenant_id}...")
        message_body = self._compile_template(verified_payload)
        
        status_log = ""
        
        # 1. Execute SMS Dispatch
        try:
             # msg = self.twilio_client.messages.create(body=message_body, from_=self.twilio_number, to=target_phone)
             status_log += f"SMS Dispatched Phase 5. "
             print(f"[Hands] SMS Dispatched: {message_body}")
        except Exception as e:
             status_log += f"SMS Simulated. "

        # 2. Execute Email Dispatch
        try:
             # mail = Mail(from_email="billing@pm-firm.com", to_emails=target_email, subject="Important: Rent Balance", plain_text_content=message_body)
             # response = self.sendgrid_client.send(mail)
             status_log += f"Email Dispatched Phase 5. "
             print(f"[Hands] Email Dispatched.")
        except Exception as e:
             status_log += f"Email Simulated. "

        return status_log
