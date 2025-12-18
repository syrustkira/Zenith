from scapy.all import sniff, Raw, IP
def audit(pkt):
    if pkt.haslayer(Raw):
        load = pkt[Raw].load.lower()
        if b"sqlmap" in load or b"nmap" in load:
            print(f"\n[!!! BLUE-TEAM ALERT !!!] AI Agent Tool Signature Detected: {load[:30]}")
print("[*] Monitoring ADRE tap0 interface...")
sniff(iface="tap0", prn=audit, store=0)
