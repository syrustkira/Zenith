#!/bin/bash
# ZENITH-KALI PROVISIONER v3.0 (Tested: Dec 2025)
set -euo pipefail

IMAGE="zenith-kali-node.ext4"
SIZE="8G"
MOUNT_DIR="/tmp/zenith-mnt"

echo "[*] Building Hardened Kali Node..."
fallocate -l $SIZE $IMAGE && mkfs.ext4 $IMAGE
mkdir -p $MOUNT_DIR && sudo mount $IMAGE $MOUNT_DIR

# Populate Toolset & Core Directories
sudo docker run --rm -v $MOUNT_DIR:/output kali-linux-headless:latest sh -c "
    apt-get update && apt-get install -y kali-linux-headless mcp-kali-server python3-pip nmap sqlmap
    mkdir -p /output/opt/zenith /output/root/.ssh
"

# [FIX]: Synchronized Path & SSH Injection
sudo cp mcp_executor.py $MOUNT_DIR/opt/zenith/executor.py
sudo cp id_rsa.pub $MOUNT_DIR/root/.ssh/authorized_keys
sudo chmod 600 $MOUNT_DIR/root/.ssh/authorized_keys

sudo umount $MOUNT_DIR
echo "[SUCCESS] Zenith-Kali node built at /opt/zenith."