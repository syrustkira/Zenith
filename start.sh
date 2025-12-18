# 1. Clean up stale sockets
rm -f /tmp/firecracker.socket

# 2. Launch Firecracker using the API socket and the config file
# This initiates the OODA loop by bringing the Kali node online
./firecracker --api-sock /tmp/firecracker.socket --config-file kali_config.json