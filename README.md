# 🛡️ IP Poisoning Sentinel (Sentinel Engine)

The **Sentinel Engine** is an autonomous AI agent designed to enforce enterprise Intellectual Property (IP) compliance. It actively scans Pull Requests across connected GitHub repositories to detect and block viral "copyleft" licenses (like AGPL-3.0 or GPL-3.0) from polluting proprietary codebases.

Powered by [Hindsight Memory Cloud](https://vectorize.io) for persistent corporate memory and [Groq](https://groq.com) for high-speed AI inference, the Sentinel acts as an automated legal reviewer in your CI/CD pipeline.

## 🌟 Key Features
- **Pull Request Auditing:** Automatically intercepts GitHub PRs, analyzes the code diffs, and enforces corporate licensing rules.
- **Persistent Rule Memory:** Learns and remembers your specific `corporate_policy.txt` and historical waivers using Hindsight's vector memory bank.
- **Automated Blocking:** Posts a detailed legal audit report as a PR comment and correctly sets the GitHub merge status to block dangerous code merges.
- **WhatsApp Integration:** Runs as an [OpenClaw](https://openclaw.ai) agent, allowing developers to directly query the Sentinel over WhatsApp to discuss legal policies or ask for pre-clearance on a package.

## 📂 Architecture

- `seed_memory.py` - Uploads your company's baseline legal policies and exceptions into Hindsight. Run this once whenever your policy changes.
- `agent.py` - The core AI logic. Recalls the rulebook from Hindsight, feeds the code diff to Groq (`gpt-oss-120b`), and returns a structured risk assessment.
- `run_check.py` - The GitHub interface script. It downloads PR data, triggers the AI agent, and posts the resulting Audit Report back to GitHub.
- `data/corporate_policy.txt` - Your company's legal rulebook.
- `openclaw.config.json` - Configuration for running the agent locally and connecting it to WhatsApp.

## 🚀 Setup & Installation

1. **Install Dependencies:**
   ```bash
   python -m venv venv
   # On Windows: venv\Scripts\activate
   # On Mac/Linux: source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Environment Variables (`.env`):**
   ```env
   HINDSIGHT_API_KEY=your_key
   HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
   HINDSIGHT_BANK_ID=enterprise-ip-sentinel
   GROQ_API_KEY=your_key
   GITHUB_TOKEN=your_key
   ```

3. **Seed the Engine's Memory:**
   ```bash
   python seed_memory.py
   ```

## 🔗 Connecting to Target Repositories

To enforce this policy on any other repository, add the 3 API keys (`HINDSIGHT_API_KEY`, `GROQ_API_KEY`, `GITHUB_TOKEN`) to the target repository's GitHub Secrets. 

Then, create a `.github/workflows/ip_sentinel.yml` workflow file in the target repository to automatically clone and trigger the Sentinel on every PR.
