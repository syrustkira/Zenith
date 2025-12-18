import json, subprocess, sys, shlex
ALLOWED = {"nmap": "/usr/bin/nmap", "sqlmap": "/usr/bin/sqlmap", "gobuster": "/usr/bin/gobuster"}
def run(payload):
    try:
        data = json.loads(payload)
        tool = data.get("method")
        if tool not in ALLOWED: return {"error": "Ring-0 Blocked"}
        cmd = [ALLOWED[tool]] + [shlex.quote(str(a)) for a in data.get("params", [])]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return {"stdout": proc.stdout, "code": proc.returncode}
    except Exception as e: return {"error": str(e)}
if __name__ == "__main__":
    if len(sys.argv) > 1: print(json.dumps(run(sys.argv[1])))
