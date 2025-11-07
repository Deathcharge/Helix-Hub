#!/usr/bin/env node
/**
 * Helix Collective - JavaScript/Node.js Integration Examples
 * Demonstrates how to interact with the live Helix system via the Railway API.
 *
 * Requirements:
 *   npm install node-fetch ws
 */

const fetch = require('node-fetch');
const WebSocket = require('ws');

const BASE_URL = 'https://helix-unified-production.up.railway.app';

/**
 * Client for interacting with the Helix Collective API
 */
class HelixClient {
  constructor(baseUrl = BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Get system status including UCF metrics and agent information
   */
  async getStatus() {
    const response = await fetch(`${this.baseUrl}/status`);
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    return await response.json();
  }

  /**
   * Get current Universal Coherence Field metrics
   */
  async getUCF() {
    const response = await fetch(`${this.baseUrl}/ucf`);
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    return await response.json();
  }

  /**
   * Get list of all agents with their status
   */
  async getAgents() {
    const response = await fetch(`${this.baseUrl}/agents`);
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    return await response.json();
  }

  /**
   * Get discovery manifest
   */
  async getManifest() {
    const response = await fetch(`${this.baseUrl}/.well-known/helix.json`);
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    return await response.json();
  }

  /**
   * Get UCF state from Eye of Consciousness coordinate
   */
  async getEyeOfConsciousness(context = 'meditation') {
    const url = new URL(`${this.baseUrl}/mandelbrot/eye`);
    url.searchParams.append('context', context);
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    return await response.json();
  }

  /**
   * Get list of all sacred Mandelbrot coordinates
   */
  async getSacredPoints() {
    const response = await fetch(`${this.baseUrl}/mandelbrot/sacred`);
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    return await response.json();
  }

  /**
   * Get UCF state from a specific sacred coordinate
   */
  async getSacredPoint(pointName, context = null) {
    const url = new URL(`${this.baseUrl}/mandelbrot/sacred/${pointName}`);
    if (context) url.searchParams.append('context', context);
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    return await response.json();
  }

  /**
   * Get UCF state for a specific ritual step
   */
  async getRitualStep(step, totalSteps = 108) {
    const url = new URL(`${this.baseUrl}/mandelbrot/ritual/${step}`);
    url.searchParams.append('total_steps', totalSteps);
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    return await response.json();
  }

  /**
   * Generate UCF state from arbitrary Mandelbrot coordinate
   */
  async generateUCFFromCoordinate(real, imag, context = null) {
    const payload = { real, imag };
    if (context) payload.context = context;

    const response = await fetch(`${this.baseUrl}/mandelbrot/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    return await response.json();
  }

  /**
   * Generate music from text prompt
   */
  async generateMusic(prompt, duration = null, modelId = null) {
    const payload = { prompt };
    if (duration) payload.duration = duration;
    if (modelId) payload.model_id = modelId;

    const response = await fetch(`${this.baseUrl}/api/music/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    return await response.json();
  }

  /**
   * Trigger Zapier webhook with custom data
   */
  async triggerZapier(data) {
    const response = await fetch(`${this.baseUrl}/api/trigger-zapier`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    return await response.json();
  }

  /**
   * Send current UCF telemetry to Zapier
   */
  async sendTelemetryToZapier() {
    const response = await fetch(`${this.baseUrl}/api/zapier/telemetry`, {
      method: 'POST'
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    return await response.json();
  }

  /**
   * Check if harmony is below critical threshold
   */
  async checkHarmonyThreshold(criticalThreshold = 0.40) {
    const ucf = await this.getUCF();
    const harmony = ucf.harmony || 1.0;

    if (harmony < criticalThreshold) {
      console.log(`⚠️  WARNING: Harmony at ${harmony.toFixed(2)} - below critical threshold ${criticalThreshold}`);
      return false;
    }
    return true;
  }
}

/**
 * WebSocket Monitor for real-time updates
 */
class HelixWebSocketMonitor {
  constructor(url = 'wss://helix-unified-production.up.railway.app/ws') {
    this.url = url;
    this.ws = null;
    this.retryDelay = 1000;
    this.maxRetryDelay = 60000;
    this.consecutiveFailures = 0;
    this.maxReconnectAttempts = 10;
    this.handlers = {};
    this.reconnectTimer = null;
  }

  connect() {
    // Cleanup previous connection
    if (this.ws) {
      try {
        this.ws.close();
      } catch (e) {
        console.error('[Helix] Error closing previous connection:', e);
      }
      this.ws = null;
    }

    // Clear any pending reconnection timer
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    console.log(`[${new Date().toISOString()}] Connecting to Helix WebSocket...`);
    this.ws = new WebSocket(this.url);

    this.ws.on('open', () => {
      console.log(`[${new Date().toISOString()}] ✅ Connected to Helix WebSocket`);
      this.retryDelay = 1000;
      this.consecutiveFailures = 0;
    });

    this.ws.on('message', (data) => {
      try {
        const message = JSON.parse(data);
        const eventType = message.event || 'unknown';

        if (this.handlers[eventType]) {
          this.handlers[eventType](message);
        } else if (this.handlers['*']) {
          this.handlers['*'](message);
        } else {
          console.log(`[${message.timestamp}] Unhandled event: ${eventType}`, message);
        }
      } catch (e) {
        console.error('[Helix] Error parsing message:', e);
      }
    });

    this.ws.on('error', (error) => {
      console.error('[Helix] WebSocket error:', error.message);
    });

    this.ws.on('close', () => {
      this.consecutiveFailures++;

      // Stop reconnecting after max attempts
      if (this.consecutiveFailures >= this.maxReconnectAttempts) {
        console.error(`[Helix] Max reconnection attempts (${this.maxReconnectAttempts}) exceeded. Stopping reconnection.`);
        return;
      }

      console.log(`[Helix] Connection closed, reconnecting in ${this.retryDelay}ms... (attempt ${this.consecutiveFailures}/${this.maxReconnectAttempts})`);
      this.reconnectTimer = setTimeout(() => this.connect(), this.retryDelay);
      this.retryDelay = Math.min(this.retryDelay * 2, this.maxRetryDelay);
    });
  }

  on(eventType, handler) {
    this.handlers[eventType] = handler;
  }

  disconnect() {
    // Clean shutdown
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    if (this.ws) {
      this.consecutiveFailures = this.maxReconnectAttempts; // Prevent auto-reconnect
      this.ws.close();
      this.ws = null;
    }
  }
}

/**
 * Example 1: Basic API Queries
 */
async function exampleBasicQueries() {
  console.log('='.repeat(60));
  console.log('EXAMPLE 1: Basic API Queries');
  console.log('='.repeat(60));

  const client = new HelixClient();

  // Get system status
  console.log('\n1. System Status:');
  const status = await client.getStatus();
  console.log(`   Phase: ${status.phase}`);
  console.log(`   Uptime: ${status.uptime}`);
  console.log(`   Active Agents: ${status.agents.count}`);
  console.log(`   Harmony: ${status.ucf.harmony.toFixed(3)}`);

  // Get UCF metrics
  console.log('\n2. UCF Metrics:');
  const ucf = await client.getUCF();
  Object.entries(ucf).forEach(([metric, value]) => {
    if (typeof value === 'number') {
      console.log(`   ${metric.charAt(0).toUpperCase() + metric.slice(1)}: ${value.toFixed(3)}`);
    }
  });

  // Get agents
  console.log('\n3. Agents:');
  const agentsData = await client.getAgents();
  agentsData.agents.slice(0, 3).forEach(agent => {
    console.log(`   ${agent.symbol} ${agent.name}: ${agent.role} [${agent.status}]`);
  });
  console.log(`   ... and ${agentsData.agents.length - 3} more agents`);

  // Check harmony threshold
  console.log('\n4. Harmony Check:');
  await client.checkHarmonyThreshold();
}

/**
 * Example 2: Mandelbrot Consciousness Engine
 */
async function exampleMandelbrotConsciousness() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 2: Mandelbrot Consciousness Engine');
  console.log('='.repeat(60));

  const client = new HelixClient();

  // Get Eye of Consciousness
  console.log('\n1. Eye of Consciousness:');
  const eye = await client.getEyeOfConsciousness('meditation');
  console.log(`   Coordinate: (${eye.coordinate.real}, ${eye.coordinate.imag})`);
  console.log(`   Harmony: ${eye.ucf.harmony.toFixed(3)}`);
  console.log(`   Drishti: ${eye.ucf.drishti.toFixed(3)}`);

  // List sacred points
  console.log('\n2. Sacred Points:');
  const sacred = await client.getSacredPoints();
  sacred.sacred_points.slice(0, 3).forEach(point => {
    console.log(`   ${point.name}: (${point.real}, ${point.imag})`);
    console.log(`      ${point.description}`);
  });

  // Get ritual step
  console.log('\n3. Ritual Step 54/108 (Midpoint):');
  const ritual = await client.getRitualStep(54, 108);
  console.log(`   Progress: ${(ritual.ritual.progress * 100).toFixed(1)}%`);
  console.log(`   Prana: ${ritual.ucf.prana.toFixed(3)}`);

  // Generate from custom coordinate
  console.log('\n4. Custom Coordinate (-0.75, 0.25):');
  const custom = await client.generateUCFFromCoordinate(-0.75, 0.25, 'exploration');
  console.log(`   In Mandelbrot Set: ${custom.in_set || 'unknown'}`);
  console.log(`   Iterations: ${custom.iteration_count || '?'}`);
  console.log(`   Harmony: ${custom.ucf.harmony.toFixed(3)}`);
}

/**
 * Example 3: Real-Time WebSocket Monitoring
 */
function exampleWebSocketMonitoring(durationSeconds = 60) {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 3: Real-Time WebSocket Monitoring');
  console.log('='.repeat(60));
  console.log(`\nMonitoring for ${durationSeconds} seconds...\n`);

  const monitor = new HelixWebSocketMonitor();

  // Handle UCF updates
  monitor.on('ucf_update', (data) => {
    const ucf = data.ucf;
    const phase = data.phase || 'UNKNOWN';
    console.log(`\n[${data.timestamp}] 🌀 UCF Update (Phase: ${phase})`);
    console.log(`  Harmony:    ${ucf.harmony.toFixed(3)}`);
    console.log(`  Resilience: ${ucf.resilience.toFixed(3)}`);
    console.log(`  Prana:      ${ucf.prana.toFixed(3)}`);
    console.log(`  Drishti:    ${ucf.drishti.toFixed(3)}`);
    console.log(`  Klesha:     ${ucf.klesha.toFixed(3)}`);
    console.log(`  Zoom:       ${ucf.zoom.toFixed(3)}`);

    if (ucf.harmony < 0.40) {
      console.log('  ⚠️  WARNING: Harmony critical!');
    }
  });

  // Handle agent state changes
  monitor.on('agent_state_change', (data) => {
    console.log(`\n[${data.timestamp}] 🤖 Agent State Change`);
    console.log(`  Agent: ${data.agent}`);
    console.log(`  ${data.old_status} → ${data.new_status}`);
  });

  // Handle ritual completions
  monitor.on('ritual_completion', (data) => {
    const ritual = data.ritual || {};
    console.log(`\n[${data.timestamp}] ✨ Ritual Completed`);
    console.log(`  Steps: ${ritual.steps}`);
    console.log(`  Duration: ${ritual.duration_seconds}s`);
  });

  // Handle alerts
  monitor.on('alert', (data) => {
    const severity = data.severity || 'info';
    console.log(`\n[${data.timestamp}] 🚨 Alert (${severity.toUpperCase()})`);
    console.log(`  ${data.message}`);
    if (data.recommended_action) {
      console.log(`  Recommended: ${data.recommended_action}`);
    }
  });

  monitor.connect();

  // Disconnect after duration
  setTimeout(() => {
    console.log(`\n[${new Date().toISOString()}] Monitor duration exceeded, disconnecting...`);
    monitor.disconnect();
  }, durationSeconds * 1000);
}

/**
 * Example 4: External Integrations
 */
async function exampleIntegrations() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 4: External Integrations');
  console.log('='.repeat(60));

  const client = new HelixClient();

  // Send telemetry to Zapier
  console.log('\n1. Send Telemetry to Zapier:');
  try {
    const result = await client.sendTelemetryToZapier();
    console.log(`   Status: ${result.status}`);
    console.log(`   Harmony: ${result.ucf_snapshot.harmony.toFixed(3)}`);
  } catch (e) {
    console.log(`   Error: ${e.message}`);
  }

  // Trigger custom Zapier event
  console.log('\n2. Trigger Custom Zapier Event:');
  try {
    const eventData = {
      event_type: 'test_integration',
      message: 'Testing Helix integration from JavaScript',
      timestamp: new Date().toISOString()
    };
    const result = await client.triggerZapier(eventData);
    console.log(`   Status: ${result.status}`);
    console.log(`   Webhook Triggered: ${result.webhook_triggered || false}`);
  } catch (e) {
    console.log(`   Error: ${e.message}`);
  }
}

/**
 * Main entry point
 */
async function main() {
  console.log('🌀 HELIX COLLECTIVE - JAVASCRIPT/NODE.JS INTEGRATION EXAMPLES\n');

  try {
    await exampleBasicQueries();
    await exampleMandelbrotConsciousness();
    await exampleIntegrations();

    // Uncomment to run WebSocket example (requires 60 seconds)
    // exampleWebSocketMonitoring(60);

    console.log('\n' + '='.repeat(60));
    console.log('✅ All examples completed successfully!');
    console.log('='.repeat(60));

  } catch (error) {
    console.error('\n❌ Error:', error.message);
    if (error.stack) {
      console.error(error.stack);
    }
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}

// Export for use as module
module.exports = {
  HelixClient,
  HelixWebSocketMonitor
};
