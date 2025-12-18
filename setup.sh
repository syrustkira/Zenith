#!/bin/bash

# ZENITH ARCHITECTURAL INITIALIZATION SCRIPT v2.2
echo "[*] Initializing Zenith Red-Team Framework..."

# 1. Create Hierarchical Structure
mkdir -p agents tools logs context docs
touch .env .gitignore requirements.txt README.md

# 2. Initialize Security Gate (Gitignore)
echo "[*] Configuring Security Gate (.gitignore)..."
cat <<EOF > .gitignore
# Secrets & Credentials
.env
credentials.json
*.pem
*.key

# Environments & Dependencies
venv/
__pycache__/
.pytest_cache/

# Local Logs & Sensitive Data
logs/
context/session_state.json
EOF

# 3. Populate Requirements
echo "[*] Mapping Dependencies..."
cat <<EOF > requirements.txt
openai
python-dotenv
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
langgraph
typing-extensions
click
typer
EOF

# 4. Create README Template
cat <<EOF > README.md
# Project Zenith
**Role:** AI-Augmented Adversarial Resilience Framework
**Architecture:** Hierarchical Hybrid (Coordinator-Worker)
**Security:** Local PII Scrubbing + HITL Alignment Gates

## Deployment
1. Add 'OPENROUTER_API_KEY' and 'DRIVE_FOLDER_ID' to .env
2. Place 'credentials.json' in root
3. Execute 'python zenith_core.py'
EOF

# 5. Environment Setup
echo "[*] Setting up Python Virtual Environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
sudo apt update && sudo apt install -y qemu-utils libguestfs-tools bridge-utils python3-pip
pip install scapy openai python-dotenv google-api-python-client firecracker-python -y

sudo ip tuntap add dev tap0 mode tap
sudo ip addr add 172.16.0.1/24 dev tap0
sudo ip link set tap0 up
# Enable NAT for external research if needed
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# 6. Git Initialization
echo "[*] Initializing Local Repository..."
git init
git add .
git commit -m "Initial System Architecture: Zenith v2.2 Core"

echo "------------------------------------------------"
echo "[SUCCESS] Zenith Framework is ready for deployment."
echo "[ACTION] 1. Place your credentials.json in this folder."
echo "[ACTION] 2. Type 'source venv/bin/activate' to start."
echo "------------------------------------------------"