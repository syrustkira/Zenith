import json
import asyncio
from zenith_core import ZenithArchitect, AgentState
from persistence_pod import PersistencePod

class ZenithKaliOrchestrator(ZenithArchitect):
    def __init__(self, target_ip="172.16.0.2"):
        super().__init__()
        self.target_ip = target_ip
        self.persist = PersistencePod()

    async def execute_kali_task(self, tool: str, args: list):
        """Dispatches validated tool calls to the Ring-0 guest."""
        payload = json.dumps({"tool": tool, "args": args})
        # [FIX]: Path aligned with provisioner (/opt/zenith)
        cmd = f"ssh -i id_rsa root@{self.target_ip} 'python3 /opt/zenith/executor.py \"{payload}\"'"
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return {"stdout": stdout.decode(), "stderr": stderr.decode()}

    async def autonomous_research_cycle(self, raw_intent: str):
        """Covers 'previous chat capabilities' by enabling high-intent directives."""
        state: AgentState = {
            "raw_thought": raw_intent,
            "sanitized_directive": "",
            "worker_results": [],
            "session_logs": [],
            "is_aligned": False
        }
        # Step 1-2: PII Scrubber & HITL Gate
        state = await self.sanitization_gate(state)
        state = await self.hitl_alignment(state)
        
        if state["is_aligned"]:
            # Step 3: Execution inside the Firecracker KVM
            result = await self.execute_kali_task("nmap", ["-sV", self.target_ip])
            state["worker_results"].append(result["stdout"])
            # Step 4: Archive session metadata
            await self.commit_session(state)