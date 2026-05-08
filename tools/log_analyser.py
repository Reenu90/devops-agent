"""
Log Analyser Tool
Paste raw logs → get root cause, severity, and fix recommendations.
"""


def build_log_prompt(logs: str) -> str:
    return f"""You are a senior Site Reliability Engineer (SRE) analysing logs.

Raw logs:
```
{logs}
```

Provide a structured incident analysis:

## 🔴 Severity
Rate as: Critical / High / Medium / Low — and explain why.

## 🔍 Root Cause
What is the most likely root cause? Be specific.

## 📍 Key Error Lines
Highlight the exact log lines that point to the problem.

## 🛠️ Immediate Fix
Step-by-step actions to resolve this right now.

## 🔮 Prevention
How to prevent this from happening again (monitoring, alerts, code changes).

## 🔗 Related Issues to Check
Other systems or services that might be affected.

Be direct and actionable. This is a live incident."""


def detect_log_type(logs: str) -> str:
    """Try to detect the log source for better context."""
    logs_lower = logs.lower()
    if "kubectl" in logs_lower or "kubernetes" in logs_lower or "pod" in logs_lower:
        return "Kubernetes"
    elif "terraform" in logs_lower:
        return "Terraform"
    elif "nginx" in logs_lower or "apache" in logs_lower:
        return "Web Server"
    elif "error" in logs_lower and "stack" in logs_lower:
        return "Application"
    elif "gcp" in logs_lower or "google" in logs_lower:
        return "GCP"
    return "System"
