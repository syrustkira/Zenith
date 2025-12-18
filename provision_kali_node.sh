#!/bin/bash
IMAGE="zenith-kali-node.ext4"
MOUNT_DIR="/tmp/zenith-mnt"

# 1. Create and Format
fallocate -l 8G $IMAGE && mkfs.ext4 $IMAGE
mkdir -p $MOUNT_DIR && sudo mount $IMAGE $MOUNT_DIR

# 2. Inject Kali Tools & Zenith Executor
# We use a Docker volume to populate the raw disk
sudo docker run --rm -v $MOUNT_DIR:/output kali-linux-headless:latest sh -c "
    apt-get update && apt-get install -y kali-linux-headless mcp-kali-server nmap sqlmap gobuster metasploit-framework python3
    mkdir -p /output/opt/zenith /output/root/.ssh
"

# 3. Synchronize Paths & Inject SSH Keys
sudo cp mcp_executor.py $MOUNT_DIR/opt/zenith/executor.py
sudo cp id_rsa.pub $MOUNT_DIR/root/.ssh/authorized_keys
sudo chmod 600 $MOUNT_DIR/root/.ssh/authorized_keys

sudo umount $MOUNT_DIR