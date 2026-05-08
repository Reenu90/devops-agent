"""
DevOps AI Agent — powered by Google Gemini
Handles general chat + specialised DevOps tools.
"""

import os
from typing import Generator
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_MODEL = "gemini-2.5-flash-lite"

SYSTEM_INSTRUCTION = """You are an expert DevOps and Site Reliability Engineer (SRE) assistant powered by Google Gemini.

You help engineers with:
- Kubernetes, Docker, Terraform, Helm, and cloud infrastructure
- CI/CD pipelines (GitHub Actions, Cloud Build, Jenkins)
- Incident response and troubleshooting
- Google Cloud Platform (GCP) services and best practices
- Shell scripting and automation
- Monitoring, alerting, and observability

Your responses are:
- Precise and actionable — no fluff
- Rich with code examples where relevant
- Grounded in real-world DevOps practices
- Formatted clearly with markdown

Always think like a senior engineer who has been paged at 3am and needs to solve problems fast."""


class DevOpsAgent:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        genai.configure(api_key=api_key)

        self._model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=SYSTEM_INSTRUCTION,
        )

        self._chat = self._model.start_chat(history=[])

    # ------------------------------------------------------------------ #
    # General chat                                                         #
    # ------------------------------------------------------------------ #

    def chat(self, message: str) -> Generator[str, None, None]:
        """Stream a response to a general DevOps question."""
        response = self._model.generate_content(
            message,
            stream=True,
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text

    # ------------------------------------------------------------------ #
    # Specialised tool endpoints                                           #
    # ------------------------------------------------------------------ #

    def run_tool(self, prompt: str) -> Generator[str, None, None]:
        """Run a specialised tool prompt with streaming."""
        response = self._model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text

    def clear_history(self) -> None:
        self._chat = self._model.start_chat(history=[])
