#!/bin/bash
# ZENITH-KALI PROVISIONER v2.5 (2025)
# License: GNU GPL v3
set -euo pipefail

IMAGE="zenith-kali-node.ext4"
SIZE="8G"

echo "[*] Initializing ADRE Volume..."
fallocate -l $SIZE $IMAGE
mkfs.ext4 $IMAGE

# Mounting and Populating
MOUNT_DIR="/tmp/zenith-mnt"
mkdir -p $MOUNT_DIR
sudo mount $IMAGE $MOUNT_DIR

echo "[*] Injecting Kali-Headless Suite and Zenith Core..."
docker run --rm -v $MOUNT_DIR:/output kali-linux-headless:latest sh -c "
    apt-get update && apt-get install -y kali-linux-headless mcp-kali-server python3-pip nmap sqlmap gobuster nikto
    mkdir -p /output/opt/zenith
"

# Copy Zenith components and requirements
sudo cp zenith_core.py $MOUNT_DIR/opt/zenith/core.py
sudo cp persistence_pod.py $MOUNT_DIR/opt/zenith/persistence.py
sudo cp requirements.txt $MOUNT_DIR/opt/zenith/requirements.txt

echo "[*] Finalizing Immutable Layer..."
sudo umount $MOUNT_DIR
echo "[SUCCESS] Zenith-Kali node is ready for Ring-0 execution."