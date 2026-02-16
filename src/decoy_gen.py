import random
from typing import Dict, Any
from .core import StateVector

class GenerativeDecoyModule:
    """
    Simulates the Generative Model G_phi(s_t, z) that synthesizes digital illusions.
    """
    
    def __init__(self, complexity_level: float = 1.0):
        self.complexity_level = complexity_level
        self.decoy_templates = {
            "ssh_banner": [
                "SSH-2.0-OpenSSH_7.4p1 Debian-10+deb9u7",
                "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5",
                "SSH-2.0-Dropbear_2019.78",
                "SSH-1.99-Cisco-1.25"
            ],
            "http_response": [
                "HTTP/1.1 200 OK\nServer: Apache/2.4.41 (Ubuntu)\nContent-Type: text/html\n\n<html><body>Login Page</body></html>",
                "HTTP/1.1 403 Forbidden\nServer: nginx/1.18.0\n\nAccess Denied",
                "HTTP/1.1 500 Internal Server Error\nServer: Microsoft-IIS/10.0\n\nDebug Trace..."
            ],
            "db_error": [
                "ERROR 1045 (28000): Access denied for user 'root'@'localhost'",
                "ORA-12154: TNS:could not resolve the connect identifier specified",
                "FATAL:  password authentication failed for user \"postgres\""
            ]
        }

    def generate_decoy(self, state: StateVector) -> Dict[str, Any]:
        """
        Synthesizes a contextually rich digital illusion I_t based on the state vector.
        """
        # Latent noise vector z simulation (just random choice here)
        
        illusion = {
            "type": "decoy_response",
            "content": "",
            "deception_score": 0.0
        }

        if state.target_port == 22:
            illusion["content"] = random.choice(self.decoy_templates["ssh_banner"])
            illusion["deception_type"] = "service_emulation"
        elif state.target_port == 80 or state.target_port == 443:
            illusion["content"] = random.choice(self.decoy_templates["http_response"])
            illusion["deception_type"] = "web_trap"
        elif "sql" in state.payload_signature.lower():
            illusion["content"] = random.choice(self.decoy_templates["db_error"])
            illusion["deception_type"] = "database_honeytoken"
        else:
            illusion["content"] = " Connection timed out (Fake)"
            illusion["deception_type"] = "latency_injection"

        # Adaptive complexity
        if state.behavioral_score > 0.7:
            illusion["content"] += " [DEBUG INFO LEAK: 0xDEADBEEF]"
            illusion["high_interaction"] = True
        
        return illusion
