# QualGent Research Scientist Coding Challenge

## 👤 Author
**Geetheswar Reddy Bhumireddy**  
Arizona State University | Computer Science

---

## 🧠 Project Overview

This is a multi-agent LLM-powered Mobile QA system built on top of the Agent-S architecture and AndroidEnv.

It includes 4 agents that collaboratively perform UI testing on Android apps:

- **Planner Agent**: Converts high-level QA goals into app-specific subgoals
- **Executor Agent**: Executes grounded mobile UI actions using ADB
- **Verifier Agent**: Validates step success based on current UI state
- **Supervisor Agent**: Analyzes test episodes and proposes improvements

---

## 🚀 How to Run

```bash
# Run core Wi-Fi toggle tests
python3 run_test.py "Turn Wi-Fi off"
python3 run_test.py "Turn Wi-Fi on"
python3 run_test.py "Turn Wi-Fi off and on"

# Run bonus session evaluation using real-world session logs
python3 android_in_the_wild_integration.py bonus_logs
```

## 🔐 OpenAI API Key

For security reasons, the API key is **not included in this codebase**.

To run LLM-powered components (like Planner or Supervisor), set your own API key as an environment variable:

```bash
export OPENAI_API_KEY=sk-...
```
