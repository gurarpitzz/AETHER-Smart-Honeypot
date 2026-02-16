from src.aether_system import AetherSystem
from src.attacker import Attacker
from src.core import StateVector
import time
import sys

def main():
    print("Initializing AETHER Defense Organism...")
    aether = AetherSystem()
    
    print("Detecting Threat Actor...")
    attacker = Attacker(skill_level=0.7)
    
    print("\n--- BEGINNING SIMULATION ---\n")
    
    simulation_steps = 10
    last_response = None
    
    for i in range(simulation_steps):
        time.sleep(0.5) # Formatting pause
        print(f"\n[Step {i+1}]")
        
        # 1. Attacker moves
        attack_vector = attacker.next_action(last_response)
        print(f" > ADVERSARY ACTION: {attack_vector.payload_signature} on {attack_vector.destination_port if hasattr(attack_vector, 'destination_port') else attack_vector.target_port}")
        
        # 2. Defense reacts
        response = aether.process_interaction(attack_vector)
        last_response = response
        
        print(f" < AETHER RESPONSE: {response.get('deception_type', 'Standard')} | Content: {response.get('content')[:50]}...")
        
    print("\n--- SIMULATION ENDED ---")
    print("Final Engagement Metrics:", aether.engagement_metrics)
    print(f"Attacker Final Status: {attacker.current_stage}")

if __name__ == "__main__":
    main()
