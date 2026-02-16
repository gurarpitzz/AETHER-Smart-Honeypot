from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import time
import uuid

@dataclass
class StateVector:
    """
    Represents the Attacker Interaction State Vector s_t.
    """
    timestamp: float = field(default_factory=time.time)
    source_ip: str = "0.0.0.0"
    target_port: Optional[int] = None
    protocol: str = "TCP"
    payload_signature: str = ""
    behavioral_score: float = 0.0  # 0.0 (benign) to 1.0 (malicious)
    interaction_history: List[str] = field(default_factory=list)

@dataclass
class InteractionEvent:
    """
    Represents a specific event in the simulation.
    """
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    actor: str = "UNKNOWN" # "Attacker" or "Defense"
    action_type: str = "INFO"
    details: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self):
        return f"[{time.ctime(self.timestamp)}] [{self.actor}] {self.action_type}: {self.details}"
