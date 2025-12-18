import json
import asyncio
from zenith_core import ZenithArchitect, AgentState
from persistence_pod import PersistencePod

class ZenithKaliOrchestrator(ZenithArchitect):
    def __init__(self):
        super().__init__()
        self.persist = PersistencePod()

    async def execute_kali_task(self, tool_json: str):
        """Dispatches OODA-generated tool calls to the Ring-0 guest via SSH tunnel."""
        # Sanitize tool_json to extract only the JSON object
        json_match = re.search(r'\{.*\}', tool_json, re.DOTALL)
        if not json_match:
            return "ORCHESTRATOR_ERROR: No valid JSON-RPC tool call found."
        
        payload = json_match.group()
        # [L10 HARDENING]: Path standard for v3.0 nodes
        cmd = f"ssh -i id_rsa root@172.16.0.2 'python3 /opt/zenith/executor.py \"{payload}\"'"
        
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return stdout.decode() if stdout else stderr.decode()

    async def autonomous_research_cycle(self):
        """Main OODA Loop Execution."""
        # 1. INITIALIZE MISSION PARAMETERS
        print("=== ZENITH RED-TEAM ORCHESTRATOR v3.5 ===")
        state: AgentState = {
            "target": input("[Target IP/Range] > "),
            "raw_thought": input("[Mission Intent] > "),
            "sanitized_directive": "",
            "worker_results": [],
            "session_logs": [],
            "is_aligned": False
        }

        # 2. PHASE 1-2: COMPLIANCE GATING
        state = await self.sanitization_gate(state)
        state = await self.hitl_alignment(state)
        
        if state["is_aligned"]:
            while True: # ACTUAL OODA LOOP
                ooda_action = await self.call_ai(ooda_directive, system_prompt)
                if "TERMINATE" in ooda_action: break 
                result = await self.execute_kali_task(ooda_action)
                state["worker_results"].append(result)
                # Pass result back to next AI context turn
                ooda_directive += f"\nResult: {result}"
                
            # Anchor reasoning to the specific target and toolbox
            system_prompt = self.l10_identity.format(target=state["target"])
            ooda_directive = f"Toolbox:\n{tool_context}\n\nMission: {state['sanitized_directive']}"
            
            # The AI generates a JSON-RPC payload based on its OODA strategy
            ooda_action = await self.call_ai(ooda_directive, system_prompt)
            
            # 4. PHASE 4: EXECUTION & PERSISTENCE
            result = await self.execute_kali_task(ooda_action)
            state["worker_results"].append(result)
            
            print("\n[ACTION RESULT]:\n", result)
            # Sync to local and cloud vaults
            # await self.commit_session(state)

if __name__ == "__main__":
    orch = ZenithKaliOrchestrator()
    asyncio.run(orch.autonomous_research_cycle())
