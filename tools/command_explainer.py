"""
Command Explainer Tool
Breaks down shell, kubectl, terraform, docker commands into plain English.
"""

SUPPORTED_TOOLS = ["bash", "kubectl", "terraform", "docker", "git", "helm", "aws", "gcloud"]


def get_command_context(command: str) -> str:
    """Detect what kind of command this is to give Gemini better context."""
    cmd = command.strip().lower()
    for tool in SUPPORTED_TOOLS:
        if cmd.startswith(tool):
            return tool
    return "shell"


def build_explain_prompt(command: str) -> str:
    tool = get_command_context(command)
    return f"""You are a senior DevOps engineer explaining a {tool} command to a junior engineer.

Command to explain:
```
{command}
```

Provide:
1. **What it does** — plain English, one sentence
2. **Flag-by-flag breakdown** — explain each flag/argument
3. **When to use it** — real-world scenario
4. **Watch out for** — any risks or common mistakes
5. **Related commands** — 2-3 similar commands they should know

Be concise but thorough. Use markdown formatting."""
