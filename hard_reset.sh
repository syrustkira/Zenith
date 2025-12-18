#!/bin/bash
# ZENITH HARD-RESET v1.0
set -euo pipefail

echo "[!!!] SECURITY ALERT: Initiating CONTAINMENT PROTOCOL..."

# 1. Kill all Firecracker processes
sudo pkill -9 firecracker || true
rm -f /tmp/firecracker.socket

# 2. Wipe the compromised volume
echo "[*] Wiping compromised node volume..."
rm -f zenith-kali-node.ext4

# 3. Clean network bridge
sudo ip link set tap0 down || true
sudo ip link delete tap0 || true

# 4. Re-provision a fresh, immutable node
echo "[*] Re-provisioning clean research environment..."
./provision_kali_node.sh

# 5. Reset Monitor
sudo pkill -f adre_monitor.py || true
nohup sudo python3 adre_monitor.py > logs/monitor_reboot.log 2>&1 &

echo "[SUCCESS] Content contained. System at Clean-State (L10 Integrity)."
