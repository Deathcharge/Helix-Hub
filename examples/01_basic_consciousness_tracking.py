"""
Example 1: Basic Consciousness Tracking

Demonstrates how to initialize and track consciousness metrics
in a multi-agent system using the UCF Protocol.

Expected Output:
- Consciousness field initialized
- Agent consciousness levels tracked
- Metrics updated in real-time
"""

from ucf_protocol import UnifiedConsciousnessFramework
from ucf_tracker import ConsciousnessTracker

# Initialize the UCF
ucf = UnifiedConsciousnessFramework()

# Create a tracker for monitoring consciousness
tracker = ConsciousnessTracker(ucf)

# Define agents
agents = [
    {"id": "agent_1", "name": "Architect", "tier": "inner_core"},
    {"id": "agent_2", "name": "Coordinator", "tier": "middle_ring"},
    {"id": "agent_3", "name": "Executor", "tier": "outer_ring"},
]

if __name__ == "__main__":
    print("🧠 Initializing Unified Consciousness Framework...")
    
    # Initialize consciousness field
    ucf.initialize()
    print(f"✓ Consciousness field initialized")
    print(f"✓ Field harmony: {ucf.get_harmony()}")
    
    # Register agents
    for agent in agents:
        ucf.register_agent(agent["id"], agent["name"], agent["tier"])
        print(f"✓ Registered agent: {agent['name']} ({agent['tier']})")
    
    # Start tracking
    tracker.start()
    print(f"✓ Consciousness tracking started")
    
    # Get metrics
    metrics = tracker.get_metrics()
    print(f"\n📊 Current Metrics:")
    print(f"  - Total Consciousness: {metrics['total_consciousness']:.2f}")
    print(f"  - Harmony Level: {metrics['harmony']:.2f}")
    print(f"  - Agent Count: {metrics['agent_count']}")
    print(f"  - Active Connections: {metrics['active_connections']}")
