---
title: DevOps AI Agent
emoji: ⚙️
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.32.0
app_file: app.py
pinned: true
license: mit
---

# ⚙️ DevOps AI Agent

> A Gemini-powered AI assistant for DevOps and SRE engineers — chat, explain commands, analyse logs, and generate runbooks.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Gemini](https://img.shields.io/badge/Gemini-1.5_Flash-orange?logo=google)
![GCP](https://img.shields.io/badge/Google_Cloud-ML_Engineer-blue?logo=googlecloud)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Tool | Description |
|---|---|
| 💬 **AI Chat** | Ask anything about Kubernetes, GCP, Terraform, CI/CD — answers grounded with Google Search |
| 🖥️ **Command Explainer** | Paste any kubectl / terraform / docker / gcloud command → get a full plain-English breakdown |
| 📋 **Log Analyser** | Paste raw logs → root cause, severity, and step-by-step fix |
| 📖 **Runbook Generator** | Describe an incident → production-ready runbook you can download as Markdown |

---

## 🏗️ Architecture

```
User Input
    │
    ├── Chat query
    │       └──▶ Gemini 1.5 Flash + Google Search grounding
    │                   └──▶ Streamed response
    │
    ├── DevOps command
    │       └──▶ Command Explainer prompt builder
    │                   └──▶ Gemini 1.5 Flash
    │                               └──▶ Flag-by-flag breakdown
    │
    ├── Raw logs
    │       └──▶ Log Analyser prompt builder
    │                   └──▶ Gemini 1.5 Flash
    │                               └──▶ Root cause + fix plan
    │
    └── Incident description
            └──▶ Runbook Generator prompt builder
                        └──▶ Gemini 1.5 Flash
                                    └──▶ Downloadable .md runbook
```

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/Reenu90/devops-ai-agent.git
cd devops-ai-agent
```

### 2. Set up virtual environment
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key
```bash
cp .env.example .env
# Edit .env and add your key from https://aistudio.google.com/app/apikey
```

### 5. Run the app
```bash
streamlit run app.py
```

---

## 🔑 Getting a Free Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API Key**
4. Copy it into your `.env` file

The free tier is generous — no credit card required.

---

## 🗂️ Project Structure

```
devops-ai-agent/
├── app.py                      # Streamlit UI
├── requirements.txt
├── .env.example
├── src/
│   ├── __init__.py
│   └── agent.py                # Gemini integration + Google Search grounding
└── tools/
    ├── __init__.py
    ├── command_explainer.py    # Prompt builder for command breakdowns
    ├── log_analyser.py         # Prompt builder for log diagnosis
    └── runbook_generator.py    # Prompt builder for runbook generation
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | [Google Gemini 1.5 Flash](https://deepmind.google/technologies/gemini/) |
| Search grounding | Google Search (via Gemini API) |
| UI | [Streamlit](https://streamlit.io/) |
| Auth | Google AI Studio API key |

---

## 🔮 Roadmap

- [ ] GCP Monitoring integration — pull real logs directly from Cloud Logging
- [ ] Terraform plan analyser — paste a `terraform plan` output → get risk assessment
- [ ] Multi-turn incident response mode
- [ ] Slack bot integration
- [ ] Export runbooks to Confluence

---

## 👩‍💻 Author

Built by **Reenu Jacob** — Google Cloud Professional ML Engineer  
[LinkedIn](https://linkedin.com/in/reenu) · [GitHub](https://github.com/Reenu90)

---

## 📄 License

MIT
