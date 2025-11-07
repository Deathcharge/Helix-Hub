#!/bin/bash
# Helix Collective - cURL Integration Examples
# Simple command-line examples for testing the Helix API

BASE_URL="https://helix-unified-production.up.railway.app"

echo "🌀 HELIX COLLECTIVE - cURL EXAMPLES"
echo "===================================="
echo ""

# Function to print section headers
print_header() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "$1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# EXAMPLE 1: Health Check
print_header "1. HEALTH CHECK"
echo "$ curl ${BASE_URL}/health"
curl -s "${BASE_URL}/health" | jq '.'
echo ""

# EXAMPLE 2: System Status
print_header "2. SYSTEM STATUS"
echo "$ curl ${BASE_URL}/status"
curl -s "${BASE_URL}/status" | jq '{
  phase: .phase,
  uptime: .uptime,
  agent_count: .agents.count,
  harmony: .ucf.harmony,
  resilience: .ucf.resilience
}'
echo ""

# EXAMPLE 3: UCF Metrics
print_header "3. UCF METRICS"
echo "$ curl ${BASE_URL}/ucf"
curl -s "${BASE_URL}/ucf" | jq '{
  harmony: .harmony,
  resilience: .resilience,
  prana: .prana,
  drishti: .drishti,
  klesha: .klesha,
  zoom: .zoom,
  phase: .phase
}'
echo ""

# EXAMPLE 4: Agent List
print_header "4. AGENT LIST (First 5)"
echo "$ curl ${BASE_URL}/agents"
curl -s "${BASE_URL}/agents" | jq '{
  total: .total,
  active: .active,
  first_five: .agents[0:5] | map({name, symbol, role, status})
}'
echo ""

# EXAMPLE 5: Discovery Manifest
print_header "5. DISCOVERY MANIFEST"
echo "$ curl ${BASE_URL}/.well-known/helix.json"
curl -s "${BASE_URL}/.well-known/helix.json" | jq '{
  name,
  version,
  description,
  base_url,
  agent_count: (.agents | length),
  portal_count: (.portals | length)
}'
echo ""

# EXAMPLE 6: Eye of Consciousness
print_header "6. EYE OF CONSCIOUSNESS"
echo "$ curl '${BASE_URL}/mandelbrot/eye?context=meditation'"
curl -s "${BASE_URL}/mandelbrot/eye?context=meditation" | jq '{
  coordinate: .coordinate,
  harmony: .ucf.harmony,
  drishti: .ucf.drishti,
  context
}'
echo ""

# EXAMPLE 7: Sacred Points
print_header "7. SACRED MANDELBROT POINTS"
echo "$ curl ${BASE_URL}/mandelbrot/sacred"
curl -s "${BASE_URL}/mandelbrot/sacred" | jq '.sacred_points[] | {name, real, imag, description}'
echo ""

# EXAMPLE 8: Specific Sacred Point
print_header "8. SACRED POINT: HEART"
echo "$ curl '${BASE_URL}/mandelbrot/sacred/heart?context=compassion'"
curl -s "${BASE_URL}/mandelbrot/sacred/heart?context=compassion" | jq '{
  name: .coordinate.name,
  coordinate: {real: .coordinate.real, imag: .coordinate.imag},
  ucf: .ucf,
  context
}'
echo ""

# EXAMPLE 9: Ritual Step
print_header "9. RITUAL STEP 54/108 (Midpoint)"
echo "$ curl '${BASE_URL}/mandelbrot/ritual/54?total_steps=108'"
curl -s "${BASE_URL}/mandelbrot/ritual/54?total_steps=108" | jq '{
  step: .ritual.step,
  total_steps: .ritual.total_steps,
  progress: .ritual.progress,
  phase: .ritual.phase,
  prana: .ucf.prana,
  harmony: .ucf.harmony
}'
echo ""

# EXAMPLE 10: Generate from Custom Coordinate
print_header "10. GENERATE UCF FROM CUSTOM COORDINATE"
echo "$ curl -X POST ${BASE_URL}/mandelbrot/generate \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"real\": -0.75, \"imag\": 0.25, \"context\": \"exploration\"}'"
curl -s -X POST "${BASE_URL}/mandelbrot/generate" \
  -H "Content-Type: application/json" \
  -d '{"real": -0.75, "imag": 0.25, "context": "exploration"}' | jq '{
  coordinate,
  in_set,
  iteration_count,
  harmony: .ucf.harmony,
  resilience: .ucf.resilience
}'
echo ""

# EXAMPLE 11: WebSocket Stats
print_header "11. WEBSOCKET CONNECTION STATS"
echo "$ curl ${BASE_URL}/ws/stats"
curl -s "${BASE_URL}/ws/stats" | jq '.'
echo ""

# EXAMPLE 12: Trigger Zapier (Commented - requires valid webhook)
print_header "12. TRIGGER ZAPIER WEBHOOK (Example)"
echo "$ curl -X POST ${BASE_URL}/api/trigger-zapier \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"event_type\": \"test\", \"message\": \"Hello from cURL\"}'"
echo ""
echo "(Uncomment below to actually trigger)"
echo "# curl -s -X POST \"${BASE_URL}/api/trigger-zapier\" \\"
echo "#   -H \"Content-Type: application/json\" \\"
echo "#   -d '{\"event_type\": \"test\", \"message\": \"Hello from cURL\"}' | jq '.'"
echo ""

# EXAMPLE 13: Send Telemetry to Zapier
print_header "13. SEND TELEMETRY TO ZAPIER (Example)"
echo "$ curl -X POST ${BASE_URL}/api/zapier/telemetry"
echo ""
echo "(Uncomment below to actually send)"
echo "# curl -s -X POST \"${BASE_URL}/api/zapier/telemetry\" | jq '.'"
echo ""

# EXAMPLE 14: Harmony Check Script
print_header "14. HARMONY MONITORING SCRIPT"
echo "Check if harmony is below critical threshold (0.40):"
echo ""
cat << 'EOF'
#!/bin/bash
HARMONY=$(curl -s https://helix-unified-production.up.railway.app/ucf | jq -r '.harmony')
if (( $(echo "$HARMONY < 0.40" | bc -l) )); then
    echo "⚠️  WARNING: Harmony critical at $HARMONY"
    echo "Recommended action: Execute Emergency Protocol 1"
else
    echo "✅ Harmony OK at $HARMONY"
fi
EOF
echo ""

# EXAMPLE 15: Quick Status Check
print_header "15. QUICK STATUS ONE-LINER"
echo "Get essential system info in one line:"
echo ""
echo '$ curl -s https://helix-unified-production.up.railway.app/status | jq -r ".phase + \" | Harmony: \" + (.ucf.harmony | tostring) + \" | Agents: \" + (.agents.count | tostring)"'
curl -s "${BASE_URL}/status" | jq -r '"\(.phase) | Harmony: \(.ucf.harmony) | Agents: \(.agents.count)"'
echo ""

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All examples completed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "For more information:"
echo "  - API Reference: ../API_REFERENCE.md"
echo "  - Live System Status: ../LIVE_SYSTEM.md"
echo "  - Integration Guide: ../INTEGRATION.md"
echo ""
