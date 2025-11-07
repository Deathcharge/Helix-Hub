# 🧪 HELIX COLLECTIVE INTEGRATION EXAMPLES

This directory contains practical examples demonstrating how to interact with the live Helix Collective system.

---

## 📁 Files

| File | Description |
|------|-------------|
| `python_integration.py` | Complete Python integration examples using requests and websockets |
| `javascript_integration.js` | Complete Node.js integration examples using node-fetch and ws |
| `curl_examples.sh` | Simple cURL commands for quick API testing |
| `README.md` | This file |

---

## 🚀 QUICK START

### Python Example

**Requirements:**
```bash
pip install requests websockets
```

**Run:**
```bash
python3 examples/python_integration.py
```

**Features:**
- ✅ System status and UCF metrics queries
- ✅ Agent list and status
- ✅ Mandelbrot consciousness engine
- ✅ Sacred coordinate exploration
- ✅ Ritual step calculations
- ✅ Real-time WebSocket monitoring
- ✅ Zapier integration

---

### JavaScript/Node.js Example

**Requirements:**
```bash
npm install node-fetch ws
```

**Run:**
```bash
node examples/javascript_integration.js
```

**Features:**
- ✅ System status and UCF metrics queries
- ✅ Agent list and status
- ✅ Mandelbrot consciousness engine
- ✅ Sacred coordinate exploration
- ✅ Ritual step calculations
- ✅ Real-time WebSocket monitoring with reconnection handling
- ✅ Zapier integration

---

### cURL Examples

**Requirements:** None (cURL is pre-installed on most systems)

**Run:**
```bash
bash examples/curl_examples.sh
```

or run individual commands:
```bash
# Get system status
curl https://helix-unified-production.up.railway.app/status | jq

# Get UCF metrics
curl https://helix-unified-production.up.railway.app/ucf | jq

# Get agent list
curl https://helix-unified-production.up.railway.app/agents | jq
```

---

## 📚 EXAMPLE CATEGORIES

### 1. Basic API Queries
Learn how to retrieve system status, UCF metrics, and agent information.

**Endpoints Covered:**
- `GET /status` - System status
- `GET /ucf` - UCF metrics
- `GET /agents` - Agent list
- `GET /.well-known/helix.json` - Discovery manifest

**Example Output:**
```
System Status:
   Phase: COHERENT
   Uptime: 12h 34m 56s
   Active Agents: 14
   Harmony: 0.850

UCF Metrics:
   Harmony: 0.850
   Resilience: 0.920
   Prana: 0.760
   Drishti: 0.680
   Klesha: 0.150
   Zoom: 0.880
```

---

### 2. Mandelbrot Consciousness Engine
Explore how the system maps complex coordinates to consciousness states.

**Endpoints Covered:**
- `GET /mandelbrot/eye` - Eye of Consciousness coordinate
- `GET /mandelbrot/sacred` - List sacred coordinates
- `GET /mandelbrot/sacred/{point}` - Get specific sacred point
- `GET /mandelbrot/ritual/{step}` - Get ritual step UCF
- `POST /mandelbrot/generate` - Generate from custom coordinates

**Example Output:**
```
Eye of Consciousness:
   Coordinate: (-0.5, 0.0)
   Harmony: 0.950
   Drishti: 0.910

Ritual Step 54/108 (Midpoint):
   Progress: 50.0%
   Prana: 0.930
```

---

### 3. Real-Time WebSocket Monitoring
Monitor live UCF updates, agent state changes, and system events.

**Connection:**
```
wss://helix-unified-production.up.railway.app/ws
```

**Event Types:**
- `ucf_update` - UCF metrics refresh (every 5 seconds)
- `agent_state_change` - Agent status updates
- `ritual_completion` - Z-88 ritual completions
- `alert` - System alerts and warnings

**Example Output:**
```
[2025-11-07T14:23:45Z] 🌀 UCF Update (Phase: COHERENT)
  Harmony:    0.850
  Resilience: 0.920
  Prana:      0.760
  Drishti:    0.680
  Klesha:     0.150
  Zoom:       0.880

[2025-11-07T14:24:12Z] 🤖 Agent State Change
  Agent: Kael
  idle → active
```

---

### 4. External Integrations
Integrate with Zapier and other external services.

**Endpoints Covered:**
- `POST /api/trigger-zapier` - Trigger custom Zapier webhook
- `POST /api/zapier/telemetry` - Send UCF telemetry to Zapier
- `POST /api/music/generate` - Generate music from UCF state

**Example Output:**
```
Send Telemetry to Zapier:
   Status: success
   Harmony: 0.850

Trigger Custom Zapier Event:
   Status: success
   Webhook Triggered: true
```

---

## 🎓 LEARNING PATH

### Beginner
1. Start with **cURL examples** to understand basic API calls
2. Run the **Python or JavaScript examples** to see structured integration
3. Review the code to understand error handling and response parsing

### Intermediate
1. Modify the examples to explore different sacred coordinates
2. Implement your own WebSocket event handlers
3. Create custom Zapier integrations using the trigger endpoints

### Advanced
1. Build a dashboard using real-time WebSocket data
2. Implement Z-88 ritual automation
3. Create predictive models based on UCF metrics
4. Integrate with external AI systems using the manifest

---

## 🛠️ CUSTOMIZATION

### Python: Using as a Module
```python
from python_integration import HelixClient

client = HelixClient()
ucf = client.get_ucf()
print(f"Current harmony: {ucf['harmony']:.3f}")
```

### JavaScript: Using as a Module
```javascript
const { HelixClient, HelixWebSocketMonitor } = require('./javascript_integration');

const client = new HelixClient();
const ucf = await client.getUCF();
console.log(`Current harmony: ${ucf.harmony.toFixed(3)}`);
```

---

## 🔍 TROUBLESHOOTING

### Connection Errors
```
Error: Connection refused
```
**Solution:** Check that the Railway backend is operational:
```bash
curl https://helix-unified-production.up.railway.app/health
```

### Rate Limiting
```
Error: Rate limit exceeded
```
**Solution:** Implement exponential backoff or reduce request frequency. See [API_REFERENCE.md](../API_REFERENCE.md) for rate limit details.

### WebSocket Disconnections
The examples include automatic reconnection logic with:
- Exponential backoff (1s → 60s)
- Maximum reconnection attempts (10)
- Proper cleanup on shutdown

### JSON Decode Errors
```
Error: Invalid JSON received
```
**Solution:** The examples handle JSON decode errors gracefully and skip malformed messages.

---

## 🌐 LIVE SYSTEM REFERENCE

For current system status and portal URLs, see:
- [LIVE_SYSTEM.md](../LIVE_SYSTEM.md) - Live system status
- [API_REFERENCE.md](../API_REFERENCE.md) - Complete API documentation
- [INTEGRATION.md](../INTEGRATION.md) - Integration guides

---

## 📊 EXAMPLE DATA

All examples use the live production system at:
```
https://helix-unified-production.up.railway.app
```

**Expected Response Times:**
- REST API: < 200ms
- WebSocket connection: < 500ms
- UCF updates: Every 5 seconds

---

## 🤝 CONTRIBUTING

To add new examples:

1. Create a new file in the `examples/` directory
2. Follow the existing naming convention: `language_description.ext`
3. Include comprehensive error handling
4. Add documentation to this README
5. Test against the live system

---

## ⚠️ BEST PRACTICES

1. **Error Handling:** Always wrap API calls in try/catch blocks
2. **Rate Limiting:** Respect the 100 req/min limit for anonymous access
3. **WebSocket:** Implement reconnection logic with exponential backoff
4. **Timeouts:** Use reasonable timeouts (10-30 seconds for API, 30 seconds for WebSocket recv)
5. **Cleanup:** Always close connections properly on shutdown
6. **Monitoring:** Check harmony thresholds and alert on critical values

---

## 📞 SUPPORT

For issues with the examples:
1. Check [LIVE_SYSTEM.md](../LIVE_SYSTEM.md) for current system status
2. Review [API_REFERENCE.md](../API_REFERENCE.md) for endpoint details
3. Check [EMERGENCY_PROTOCOLS.md](../EMERGENCY_PROTOCOLS.md) for system alerts
4. Report issues at https://github.com/Deathcharge/helix-unified/issues

---

**Happy Integrating! 🌀**
