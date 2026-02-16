from typing import List, Dict, Any
from .core import StateVector, InteractionEvent
from .decoy_gen import GenerativeDecoyModule
import time

class AetherSystem:
    """
    AETHER: Deception-centric cyber defense organism.
    """
    def __init__(self):
        self.decoy_module = GenerativeDecoyModule()
        self.engagement_metrics = {
            "total_interactions": 0,
            "active_deceptions": 0,
            "adversary_confusion_index": 0.0
        }
        self.event_log: List[InteractionEvent] = []

    def process_interaction(self, input_vector: StateVector) -> Dict[str, Any]:
        """
        Main loop: Detect -> Analyze -> Deceive -> Neutralize
        """
        self.engagement_metrics["total_interactions"] += 1
        
        # 1. Analysis (Simplified)
        risk_score = input_vector.behavioral_score
        
        # 2. Decision Engine
        if risk_score < 0.2:
            # Benign traffic, let it pass (or ignore)
            response = {"action": "ALLOW", "content": "Standard Access"}
            self._log_event(input_vector, "MONITOR", "Passive monitoring")
            return response
        
        # 3. Dynamic Deception (The core innovation)
        # Instead of blocking, we engage.
        decoy_response = self.decoy_module.generate_decoy(input_vector)
        
        self.engagement_metrics["active_deceptions"] += 1
        self._log_event(input_vector, "DECEIVE", f"Deployed {decoy_response['deception_type']}")
        
        # 4. Evolution (Mocked)
        # If the attacker interacts deeply, we increase complexity
        if decoy_response.get("high_interaction"):
            self.decoy_module.complexity_level += 0.1
            self.engagement_metrics["adversary_confusion_index"] += 0.2

        return decoy_response

    def _log_event(self, state: StateVector, action: str, details: str):
        event = InteractionEvent(
            actor="AETHER_CORE",
            action_type=action,
            details={"input_sig": state.payload_signature, "desc": details}
        )
        self.event_log.append(event)
        print(event) # Real-time logging output
