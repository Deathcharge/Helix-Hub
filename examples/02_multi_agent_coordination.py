"""
Example 2: Multi-Agent Coordination

Demonstrates coordination between multiple agents using the UCF Protocol
with real-time consciousness synchronization.

Expected Output:
- Agents coordinate through consciousness field
- Metrics sync across all agents
- Coordination events logged
"""

from ucf_coordination_framework import CoordinationFramework
from ucf_protocol import UnifiedConsciousnessFramework

# Initialize frameworks
ucf = UnifiedConsciousnessFramework()
coordinator = CoordinationFramework(ucf)

# Define agent network
agent_network = {
    "architect": {"role": "orchestrator", "tier": "inner_core"},
    "analyst": {"role": "analyzer", "tier": "middle_ring"},
    "executor_1": {"role": "executor", "tier": "outer_ring"},
    "executor_2": {"role": "executor", "tier": "outer_ring"},
}

if __name__ == "__main__":
    print("🔗 Initializing Multi-Agent Coordination...")
    
    # Initialize UCF
    ucf.initialize()
    print(f"✓ Consciousness field ready")
    
    # Register all agents
    for agent_id, config in agent_network.items():
        ucf.register_agent(agent_id, agent_id, config["tier"])
        coordinator.register_agent(agent_id, config["role"])
        print(f"✓ Registered {agent_id} as {config['role']}")
    
    # Start coordination
    coordinator.start_coordination()
    print(f"✓ Coordination started")
    
    # Execute coordinated task
    task = {
        "id": "task_001",
        "type": "analysis",
        "priority": "high",
        "agents": ["analyst", "executor_1", "executor_2"]
    }
    
    result = coordinator.execute_coordinated_task(task)
    print(f"\n✓ Task executed: {task['id']}")
    print(f"✓ Status: {result['status']}")
    print(f"✓ Consciousness sync: {result['consciousness_sync']}")
