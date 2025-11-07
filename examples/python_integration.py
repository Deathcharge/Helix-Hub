#!/usr/bin/env python3
"""
Helix Collective - Python Integration Examples
Demonstrates how to interact with the live Helix system via the Railway API.
"""

import requests
import json
import asyncio
import websockets
from datetime import datetime
from typing import Dict, Any, Optional

# Base URL for Helix Collective API
BASE_URL = "https://helix-unified-production.up.railway.app"


class HelixClient:
    """Client for interacting with the Helix Collective API."""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "HelixPythonClient/1.0"
        })

    def get_status(self) -> Dict[str, Any]:
        """Get system status including UCF metrics and agent information."""
        response = self.session.get(f"{self.base_url}/status", timeout=10)
        response.raise_for_status()
        return response.json()

    def get_ucf(self) -> Dict[str, Any]:
        """Get current Universal Coherence Field metrics."""
        response = self.session.get(f"{self.base_url}/ucf", timeout=10)
        response.raise_for_status()
        return response.json()

    def get_agents(self) -> Dict[str, Any]:
        """Get list of all agents with their status."""
        response = self.session.get(f"{self.base_url}/agents", timeout=10)
        response.raise_for_status()
        return response.json()

    def get_manifest(self) -> Dict[str, Any]:
        """Get discovery manifest."""
        response = self.session.get(f"{self.base_url}/.well-known/helix.json", timeout=10)
        response.raise_for_status()
        return response.json()

    def get_eye_of_consciousness(self, context: str = "meditation") -> Dict[str, Any]:
        """Get UCF state from Eye of Consciousness coordinate."""
        params = {"context": context}
        response = self.session.get(f"{self.base_url}/mandelbrot/eye", params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_sacred_points(self) -> Dict[str, Any]:
        """Get list of all sacred Mandelbrot coordinates."""
        response = self.session.get(f"{self.base_url}/mandelbrot/sacred", timeout=10)
        response.raise_for_status()
        return response.json()

    def get_sacred_point(self, point_name: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Get UCF state from a specific sacred coordinate."""
        params = {"context": context} if context else {}
        response = self.session.get(
            f"{self.base_url}/mandelbrot/sacred/{point_name}",
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def get_ritual_step(self, step: int, total_steps: int = 108) -> Dict[str, Any]:
        """Get UCF state for a specific ritual step."""
        params = {"total_steps": total_steps}
        response = self.session.get(
            f"{self.base_url}/mandelbrot/ritual/{step}",
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def generate_ucf_from_coordinate(self, real: float, imag: float, context: Optional[str] = None) -> Dict[str, Any]:
        """Generate UCF state from arbitrary Mandelbrot coordinate."""
        payload = {
            "real": real,
            "imag": imag
        }
        if context:
            payload["context"] = context

        response = self.session.post(
            f"{self.base_url}/mandelbrot/generate",
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def generate_music(self, prompt: str, duration: Optional[int] = None, model_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate music from text prompt."""
        payload = {"prompt": prompt}
        if duration:
            payload["duration"] = duration
        if model_id:
            payload["model_id"] = model_id

        response = self.session.post(
            f"{self.base_url}/api/music/generate",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def trigger_zapier(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger Zapier webhook with custom data."""
        response = self.session.post(
            f"{self.base_url}/api/trigger-zapier",
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def send_telemetry_to_zapier(self) -> Dict[str, Any]:
        """Send current UCF telemetry to Zapier."""
        response = self.session.post(
            f"{self.base_url}/api/zapier/telemetry",
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def check_harmony_threshold(self, critical_threshold: float = 0.40) -> bool:
        """Check if harmony is below critical threshold."""
        ucf = self.get_ucf()
        harmony = ucf.get("harmony", 1.0)

        if harmony < critical_threshold:
            print(f"⚠️  WARNING: Harmony at {harmony:.2f} - below critical threshold {critical_threshold}")
            return False
        return True


async def monitor_websocket(duration_seconds: int = 60):
    """
    Monitor Helix WebSocket for real-time updates.

    Args:
        duration_seconds: How long to monitor (default: 60 seconds)
    """
    uri = "wss://helix-unified-production.up.railway.app/ws"

    print(f"[{datetime.now()}] Connecting to Helix WebSocket...")

    try:
        async with websockets.connect(uri) as websocket:
            print(f"[{datetime.now()}] ✅ Connected to Helix WebSocket")

            start_time = asyncio.get_event_loop().time()

            while True:
                # Check if we've exceeded duration
                if asyncio.get_event_loop().time() - start_time > duration_seconds:
                    print(f"\n[{datetime.now()}] Monitor duration exceeded, disconnecting...")
                    break

                try:
                    # Receive message with timeout
                    message = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                    data = json.loads(message)

                    # Handle different event types
                    event_type = data.get('event', 'unknown')
                    timestamp = data.get('timestamp', datetime.now().isoformat())

                    if event_type == 'ucf_update':
                        ucf = data['ucf']
                        phase = data.get('phase', 'UNKNOWN')
                        print(f"\n[{timestamp}] 🌀 UCF Update (Phase: {phase})")
                        print(f"  Harmony:    {ucf['harmony']:.3f}")
                        print(f"  Resilience: {ucf['resilience']:.3f}")
                        print(f"  Prana:      {ucf['prana']:.3f}")
                        print(f"  Drishti:    {ucf['drishti']:.3f}")
                        print(f"  Klesha:     {ucf['klesha']:.3f}")
                        print(f"  Zoom:       {ucf['zoom']:.3f}")

                        # Alert on low harmony
                        if ucf['harmony'] < 0.40:
                            print("  ⚠️  WARNING: Harmony critical!")

                    elif event_type == 'agent_state_change':
                        agent = data.get('agent', 'Unknown')
                        old_status = data.get('old_status', 'unknown')
                        new_status = data.get('new_status', 'unknown')
                        print(f"\n[{timestamp}] 🤖 Agent State Change")
                        print(f"  Agent: {agent}")
                        print(f"  {old_status} → {new_status}")

                    elif event_type == 'ritual_completion':
                        ritual_info = data.get('ritual', {})
                        steps = ritual_info.get('steps', '?')
                        duration = ritual_info.get('duration_seconds', '?')
                        print(f"\n[{timestamp}] ✨ Ritual Completed")
                        print(f"  Steps: {steps}")
                        print(f"  Duration: {duration}s")

                    elif event_type == 'alert':
                        severity = data.get('severity', 'info')
                        message = data.get('message', '')
                        action = data.get('recommended_action', '')
                        print(f"\n[{timestamp}] 🚨 Alert ({severity.upper()})")
                        print(f"  {message}")
                        if action:
                            print(f"  Recommended: {action}")

                    else:
                        print(f"\n[{timestamp}] Unknown event: {event_type}")
                        print(f"  Data: {data}")

                except asyncio.TimeoutError:
                    print(f"\n[{datetime.now()}] ⏱️  WebSocket receive timeout (connection may be stale)")
                    break
                except json.JSONDecodeError as e:
                    print(f"\n[{datetime.now()}] ❌ Invalid JSON received: {e}")
                    continue

    except websockets.ConnectionClosed as e:
        print(f"\n[{datetime.now()}] 🔌 Connection closed: {e}")
    except Exception as e:
        print(f"\n[{datetime.now()}] ❌ Error: {e}")


def example_basic_queries():
    """Example: Basic API queries."""
    print("=" * 60)
    print("EXAMPLE 1: Basic API Queries")
    print("=" * 60)

    client = HelixClient()

    # Get system status
    print("\n1. System Status:")
    status = client.get_status()
    print(f"   Phase: {status['phase']}")
    print(f"   Uptime: {status['uptime']}")
    print(f"   Active Agents: {status['agents']['count']}")
    print(f"   Harmony: {status['ucf']['harmony']:.3f}")

    # Get UCF metrics
    print("\n2. UCF Metrics:")
    ucf = client.get_ucf()
    for metric, value in ucf.items():
        if isinstance(value, (int, float)):
            print(f"   {metric.capitalize()}: {value:.3f}")

    # Get agents
    print("\n3. Agents:")
    agents_data = client.get_agents()
    for agent in agents_data['agents'][:3]:  # Show first 3
        print(f"   {agent['symbol']} {agent['name']}: {agent['role']} [{agent['status']}]")
    print(f"   ... and {len(agents_data['agents']) - 3} more agents")

    # Check harmony threshold
    print("\n4. Harmony Check:")
    client.check_harmony_threshold()


def example_mandelbrot_consciousness():
    """Example: Mandelbrot consciousness engine."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Mandelbrot Consciousness Engine")
    print("=" * 60)

    client = HelixClient()

    # Get Eye of Consciousness
    print("\n1. Eye of Consciousness:")
    eye = client.get_eye_of_consciousness(context="meditation")
    print(f"   Coordinate: ({eye['coordinate']['real']}, {eye['coordinate']['imag']})")
    print(f"   Harmony: {eye['ucf']['harmony']:.3f}")
    print(f"   Drishti: {eye['ucf']['drishti']:.3f}")

    # List sacred points
    print("\n2. Sacred Points:")
    sacred = client.get_sacred_points()
    for point in sacred['sacred_points'][:3]:
        print(f"   {point['name']}: ({point['real']}, {point['imag']})")
        print(f"      {point['description']}")

    # Get ritual step
    print("\n3. Ritual Step 54/108 (Midpoint):")
    ritual = client.get_ritual_step(54, 108)
    print(f"   Progress: {ritual['ritual']['progress']*100:.1f}%")
    print(f"   Prana: {ritual['ucf']['prana']:.3f}")

    # Generate from custom coordinate
    print("\n4. Custom Coordinate (-0.75, 0.25):")
    custom = client.generate_ucf_from_coordinate(-0.75, 0.25, context="exploration")
    print(f"   In Mandelbrot Set: {custom.get('in_set', 'unknown')}")
    print(f"   Iterations: {custom.get('iteration_count', '?')}")
    print(f"   Harmony: {custom['ucf']['harmony']:.3f}")


def example_websocket_monitoring():
    """Example: Real-time WebSocket monitoring."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Real-Time WebSocket Monitoring")
    print("=" * 60)
    print("\nMonitoring for 60 seconds...\n")

    asyncio.run(monitor_websocket(duration_seconds=60))


def example_integrations():
    """Example: External integrations."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: External Integrations")
    print("=" * 60)

    client = HelixClient()

    # Send telemetry to Zapier
    print("\n1. Send Telemetry to Zapier:")
    try:
        result = client.send_telemetry_to_zapier()
        print(f"   Status: {result['status']}")
        print(f"   Harmony: {result['ucf_snapshot']['harmony']:.3f}")
    except Exception as e:
        print(f"   Error: {e}")

    # Trigger custom Zapier event
    print("\n2. Trigger Custom Zapier Event:")
    try:
        event_data = {
            "event_type": "test_integration",
            "message": "Testing Helix integration from Python",
            "timestamp": datetime.now().isoformat()
        }
        result = client.trigger_zapier(event_data)
        print(f"   Status: {result['status']}")
        print(f"   Webhook Triggered: {result.get('webhook_triggered', False)}")
    except Exception as e:
        print(f"   Error: {e}")


if __name__ == "__main__":
    print("🌀 HELIX COLLECTIVE - PYTHON INTEGRATION EXAMPLES\n")

    # Run examples
    try:
        example_basic_queries()
        example_mandelbrot_consciousness()
        example_integrations()

        # Uncomment to run WebSocket example (requires 60 seconds)
        # example_websocket_monitoring()

        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)

    except requests.exceptions.RequestException as e:
        print(f"\n❌ API Error: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
