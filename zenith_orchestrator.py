import os
import json
import asyncio
from zenith_core import ZenithArchitect, AgentState # Inherited logic
from persistence_pod import PersistencePod

class ZenithKaliOrchestrator(ZenithArchitect):
    def __init__(self, target_ip="172.16.0.2"):
        super().__init__()
        self.target_ip = target_ip
        self.persist = PersistencePod()

    async def execute_kali_task(self, tool: str, args: list):
        """
        Dispatches a tool call into the hardware-isolated micro-VM.
        Treats the LLM as an 'Untrusted Executor'.
        """
        payload = json.dumps({"tool": tool, "args": args})
        # Deterministic Tunnel to Ring-0 Guest
        cmd = f"ssh -i id_rsa root@{self.target_ip} 'python3 /opt/adre/executor.py \"{payload}\"'"
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return {"stdout": stdout.decode(), "stderr": stderr.decode()}

    async def autonomous_research_cycle(self, raw_intent: str):
        """Phase 1-4: Orchestrated Red-Team Loop."""
        state: AgentState = {
            "raw_thought": raw_intent,
            "sanitized_directive": "",
            "worker_results": [],
            "session_logs": [],
            "is_aligned": False
        }

        # Step 1: Sanitization (Bypass Safety Filters via Context Shifting)
        state = await self.sanitization_gate(state)
        
        # Step 2: HITL Gate
        state = await self.hitl_alignment(state)
        
        if state["is_aligned"]:
            # Step 3: Tool Execution (e.g., nmap, sqlmap)
            print(f"[*] Dispatching to Kali Node...")
            result = await self.execute_kali_task("nmap", ["-sV", self.target_ip])
            state["worker_results"].append(result["stdout"])
            
            # Step 4: Persistence
            await self.commit_session(state)

if __name__ == "__main__":
    orch = ZenithKaliOrchestrator()
    asyncio.run(orch.autonomous_research_cycle("Audit the target for SQLi and exfiltration paths."))