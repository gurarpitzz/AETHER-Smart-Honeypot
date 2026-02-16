import random
from typing import List, Optional
from .core import StateVector

class Attacker:
    """
    Simulates an adversary with evolving tactics.
    """
    def __init__(self, skill_level: float = 0.5):
        self.skill_level = skill_level
        self.current_stage = "RECONNAISSANCE"
        self.known_assets = []
        self.frustration_level = 0.0
    
    def next_action(self, last_response: Optional[dict] = None) -> StateVector:
        """
        Decides the next move based on the last response from the target.
        """
        state = StateVector()
        
        # Behavior transition logic
        if last_response:
            if last_response.get("deception_type"):
                # Captivated by the decoy?
                if random.random() > self.skill_level:
                    self.current_stage = "EXPLOITATION" # Fell for it
                    state.interaction_history.append("Interacting with decoy")
                else:
                    self.current_stage = "LATERAL_MOVEMENT" # Suspicious
                    self.frustration_level += 0.1
        
        # Generate Action parameters based on stage
        if self.current_stage == "RECONNAISSANCE":
            state.source_ip = f"192.168.1.{random.randint(2, 254)}"
            state.target_port = random.choice([22, 80, 443, 8080, 3306])
            state.payload_signature = "NMAP_SCAN_AGGRESSIVE"
            state.behavioral_score = 0.3
            
        elif self.current_stage == "EXPLOITATION":
            state.source_ip = f"192.168.1.{random.randint(2, 254)}" # May cycle IP
            state.target_port = random.choice([22, 443])
            state.payload_signature = "CVE-2023-XXXX_EXPLOIT_ATTEMPT"
            state.behavioral_score = 0.8
            state.interaction_history.append("Attempting credential brute-force")

        elif self.current_stage == "LATERAL_MOVEMENT":
            state.source_ip = "10.0.0.5" # Internal IP spoofing
            state.target_port = 445
            state.payload_signature = "SMB_EXPLOIT_ETERNAL"
            state.behavioral_score = 0.9

        return state
