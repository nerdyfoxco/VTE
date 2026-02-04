import google.generativeai as genai
from openai import OpenAI
import os
import logging
from typing import Optional

class LLMClient:
    """
    Wrapper for Generative AI (Gemini or OpenAI).
    """
    def __init__(self, api_key: Optional[str] = None):
        self.logger = logging.getLogger("vte.core.llm")
        self.provider = "none"
        
        # 1. Try OpenAI (Found in .env)
        self.openai_key = os.getenv("OPENAI_API_KEY")
        if self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)
            self.provider = "openai"
            self.logger.info("LLM Provider: OpenAI (Active)")
            return

        # 2. Try Gemini
        self.google_key = api_key or os.getenv("GOOGLE_API_KEY")
        if self.google_key:
            genai.configure(api_key=self.google_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.provider = "gemini"
            self.logger.info("LLM Provider: Gemini (Active)")
            return
            
        self.logger.warning("No API Keys found (OpenAI/Google). LLM Disabled (Mock Mode).")

    def analyze_discrepancy(self, ledger_data: str, email_content: str) -> str:
        """
        Asks the LLM to analyze the conflict.
        """
        prompt = f"""
        You are a Delinquency Auditor. Analyze the following discrepancy.
        
        [LEDGER SYSTEM SAYS]
        {ledger_data}
        
        [TENANT EMAIL SAYS]
        {email_content}
        
        QUESTION: Does the tenant provide valid proof of payment or a credible reason for the discrepancy? 
        If yes, summarize the claim. If no, state that the delinquency stands.
        Keep it concise (2 sentences).
        """

        if self.provider == "openai":
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4", # or gpt-3.5-turbo
                    messages=[
                        {"role": "system", "content": "You are a helpful auditor agent."},
                        {"role": "user", "content": prompt}
                    ]
                )
                return f"[OpenAI] {response.choices[0].message.content}"
            except Exception as e:
                self.logger.error(f"OpenAI Failed: {e}")
                return f"ERROR: OpenAI Analysis failed ({e})"

        elif self.provider == "gemini":
            try:
                response = self.model.generate_content(prompt)
                return f"[Gemini] {response.text}"
            except Exception as e:
                self.logger.error(f"Gemini Failed: {e}")
                return f"ERROR: Gemini Analysis failed ({e})"
        
        return "MOCK ANALYSIS: LLM Disabled. Assuming Tenant is making a claim."

    def generate(self, prompt: str) -> str:
        """
        Generic Generation interface for Agents.
        """
        if self.provider == "openai":
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            except Exception as e:
                self.logger.error(f"OpenAI Generate Failed: {e}")
                return "{}" # Return empty JSON-like string on failure
        
        elif self.provider == "gemini":
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                 self.logger.error(f"Gemini Generate Failed: {e}")
                 return "{}"

        return '{"action": "ABORT", "reason": "MOCK MODE (No Brain)"}'
