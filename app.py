"""
DevOps AI Agent — Streamlit UI
Powered by Google Gemini
"""

import streamlit as st
import os
from dotenv import load_dotenv

from src import DevOpsAgent
from tools import (
    build_explain_prompt,
    build_log_prompt,
    detect_log_type,
    build_runbook_prompt,
    build_runbook_title,
)

load_dotenv()

# ------------------------------------------------------------------ #
# Page config                                                          #
# ------------------------------------------------------------------ #
st.set_page_config(
    page_title="DevOps AI Agent",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------ #
# API Key check                                                        #
# ------------------------------------------------------------------ #
if not os.environ.get("GEMINI_API_KEY"):
    st.error(
        "⚠️ GEMINI_API_KEY not found. "
        "Add it to your .env file. "
        "Get a free key at https://aistudio.google.com/app/apikey"
    )
    st.stop()

# ------------------------------------------------------------------ #
# Session state                                                        #
# ------------------------------------------------------------------ #
if "agent" not in st.session_state:
    try:
        st.session_state.agent = DevOpsAgent()
    except Exception as e:
        st.error(f"Failed to initialise agent: {e}")
        st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_tool" not in st.session_state:
    st.session_state.active_tool = "💬 Chat"

# ------------------------------------------------------------------ #
# Sidebar                                                              #
# ------------------------------------------------------------------ #
with st.sidebar:
    st.title("⚙️ DevOps AI Agent")
    st.caption("Powered by Google Gemini")
    st.markdown("---")

    st.markdown("### 🛠️ Tools")
    tool = st.radio(
        "Select a tool",
        ["💬 Chat", "🖥️ Command Explainer", "📋 Log Analyser", "📖 Runbook Generator"],
        index=0,
        label_visibility="collapsed",
    )
    st.session_state.active_tool = tool

    st.markdown("---")
    st.markdown("### 💡 Example prompts")

    if tool == "💬 Chat":
        st.caption("• How do I set up horizontal pod autoscaling in GKE?")
        st.caption("• What's the difference between Deployment and StatefulSet?")
        st.caption("• How do I debug a CrashLoopBackOff error?")
        st.caption("• Explain blue-green vs canary deployments")

    elif tool == "🖥️ Command Explainer":
        st.caption("• kubectl rollout restart deployment/my-app -n production")
        st.caption("• terraform plan -target=module.vpc -var-file=prod.tfvars")
        st.caption("• docker build --no-cache -t myapp:v2 --build-arg ENV=prod .")
        st.caption("• gcloud container clusters get-credentials my-cluster --zone us-central1-a")

    elif tool == "📋 Log Analyser":
        st.caption("Paste Kubernetes, GCP, application, or system logs")

    elif tool == "📖 Runbook Generator":
        st.caption("• Database connection pool exhausted in production")
        st.caption("• GKE node pool needs to be upgraded")
        st.caption("• SSL certificate expiring in 7 days")
        st.caption("• Terraform state file is locked")

    st.markdown("---")
    if st.button("🔄 Clear conversation", type="secondary"):
        st.session_state.messages = []
        st.session_state.agent.clear_history()
        st.rerun()

    st.markdown("---")
    st.caption("Built with Gemini 1.5 Flash · Google Search grounding · [GitHub](https://github.com/Reenu90/devops-ai-agent)")

# ------------------------------------------------------------------ #
# Main area                                                            #
# ------------------------------------------------------------------ #

# ── Chat mode ──────────────────────────────────────────────────────
if st.session_state.active_tool == "💬 Chat":
    st.title("💬 DevOps AI Chat")
    st.caption("Ask anything about Kubernetes, GCP, Terraform, CI/CD, incidents, and more — answers grounded with Google Search.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a DevOps question…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            container = st.empty()
            full_response = ""
            try:
                for chunk in st.session_state.agent.chat(prompt):
                    full_response += chunk
                    container.markdown(full_response + "▌")
                container.markdown(full_response)
            except Exception as e:
                full_response = f"❌ Error: {e}"
                container.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

# ── Command Explainer ──────────────────────────────────────────────
elif st.session_state.active_tool == "🖥️ Command Explainer":
    st.title("🖥️ Command Explainer")
    st.caption("Paste any shell, kubectl, terraform, docker, or gcloud command and get a full breakdown.")

    command = st.text_area(
        "Paste your command here",
        placeholder="kubectl rollout restart deployment/my-app -n production",
        height=100,
    )

    if st.button("Explain Command ⚡", type="primary", disabled=not command.strip()):
        prompt = build_explain_prompt(command)
        with st.chat_message("assistant"):
            container = st.empty()
            full_response = ""
            with st.spinner("Analysing command…"):
                try:
                    for chunk in st.session_state.agent.run_tool(prompt):
                        full_response += chunk
                        container.markdown(full_response + "▌")
                    container.markdown(full_response)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ── Log Analyser ───────────────────────────────────────────────────
elif st.session_state.active_tool == "📋 Log Analyser":
    st.title("📋 Log Analyser")
    st.caption("Paste raw logs — get root cause, severity assessment, and a fix plan.")

    logs = st.text_area(
        "Paste your logs here",
        placeholder="Paste Kubernetes events, GCP logs, application stack traces, or any system logs…",
        height=250,
    )

    if logs.strip():
        log_type = detect_log_type(logs)
        st.caption(f"🔍 Detected log type: **{log_type}**")

    if st.button("Analyse Logs 🔍", type="primary", disabled=not logs.strip()):
        prompt = build_log_prompt(logs)
        with st.chat_message("assistant"):
            container = st.empty()
            full_response = ""
            with st.spinner("Diagnosing issue…"):
                try:
                    for chunk in st.session_state.agent.run_tool(prompt):
                        full_response += chunk
                        container.markdown(full_response + "▌")
                    container.markdown(full_response)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ── Runbook Generator ──────────────────────────────────────────────
elif st.session_state.active_tool == "📖 Runbook Generator":
    st.title("📖 Runbook Generator")
    st.caption("Describe an incident or operational task — get a production-ready runbook.")

    incident = st.text_area(
        "Describe the incident or task",
        placeholder="e.g. The main PostgreSQL database in production is running out of disk space and needs emergency cleanup and resize…",
        height=150,
    )

    if st.button("Generate Runbook 📖", type="primary", disabled=not incident.strip()):
        prompt = build_runbook_prompt(incident)
        title = build_runbook_title(incident)

        with st.chat_message("assistant"):
            container = st.empty()
            full_response = ""
            with st.spinner("Generating runbook…"):
                try:
                    for chunk in st.session_state.agent.run_tool(prompt):
                        full_response += chunk
                        container.markdown(full_response + "▌")
                    container.markdown(full_response)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        if full_response and not full_response.startswith("❌"):
            st.download_button(
                label="⬇️ Download Runbook (.md)",
                data=full_response,
                file_name=f"runbook_{title[:30].replace(' ', '_')}.md",
                mime="text/markdown",
            )
