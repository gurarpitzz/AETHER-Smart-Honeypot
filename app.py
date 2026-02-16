from flask import Flask, render_template, jsonify
from src.aether_system import AetherSystem
from src.attacker import Attacker
from src.core import StateVector
import random

app = Flask(__name__)

# Global Simulation State
aether = AetherSystem()
attacker = Attacker(skill_level=0.7)
simulation_step_count = 0

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/step')
def step():
    global simulation_step_count, last_response
    simulation_step_count += 1
    
    # Loose state persistence
    last_resp = getattr(app, 'last_response', None)
    
    attack_vector = attacker.next_action(last_resp)
    
    # Defense Reaction
    response = aether.process_interaction(attack_vector)
    app.last_response = response
    
    data = {
        "step": simulation_step_count,
        "attacker": {
            "stage": attacker.current_stage,
            "ip": attack_vector.source_ip,
            "payload": attack_vector.payload_signature,
            "target_port": attack_vector.target_port,
            "behavior_score": attack_vector.behavioral_score # Keep as float for chart
        },
        "defense": {
            "action": response.get("deception_type", "MONITOR"),
            "content": response.get("content", ""),
            "metrics": aether.engagement_metrics
        },
        "log_message": f"[{simulation_step_count}] {attack_vector.payload_signature} -> {response.get('deception_type', 'ALLOW')}"
    }
    return jsonify(data)

@app.route('/api/reset')
def reset():
    global aether, attacker, simulation_step_count
    aether = AetherSystem()
    attacker = Attacker(skill_level=0.7)
    simulation_step_count = 0
    app.last_response = None
    return jsonify({"status": "reset"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
