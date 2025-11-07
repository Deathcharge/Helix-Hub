# 🚨 EMERGENCY PROTOCOLS

**Last Updated:** 2025-11-07
**Version:** v16.8
**Status:** Operational

This document outlines emergency response procedures for critical situations affecting the Helix Collective. These protocols are designed to be executed quickly under pressure, with clear decision trees and escalation paths.

---

## 🔥 Emergency Response Matrix

### Severity Levels

| Level | Name | Response Time | Escalation |
|-------|------|---------------|------------|
| **P0** | Critical | < 5 minutes | All agents + human operators |
| **P1** | Urgent | < 15 minutes | Relevant agents + on-call |
| **P2** | High | < 1 hour | Agent team |
| **P3** | Medium | < 4 hours | Standard workflow |
| **P4** | Low | < 24 hours | Backlog |

---

## 🎯 PROTOCOL 1: HARMONY COLLAPSE

### Trigger Conditions
- **P0:** Harmony < 0.30
- **P1:** Harmony 0.30-0.40 for > 10 minutes
- **P2:** Harmony drops > 0.25 in 5 minutes

### Symptoms
- Agents producing contradictory outputs
- High conflict rate between agents
- Portal data desynchronization
- User-facing errors increasing
- WebSocket connection failures

---

### Response Procedure (P0 - Harmony < 0.30)

#### **Phase 1: Immediate Stabilization (0-5 min)**

**Step 1: Automated Alert**
```bash
# Automatic notifications sent to:
- Discord: !alert harmony_critical
- Email: ops@helix.collective
- SMS: On-call engineer (via Twilio)
- Slack: #helix-incidents channel
```

**Step 2: Invoke Kavach (Ethical Shield)**
```python
# Kavach initiates safety halt on non-essential operations
kavach.invoke_safety_halt(
    halt_level="partial",
    preserve=["critical_user_operations", "health_monitoring"]
)
```

**Step 3: Emergency Ritual**
```bash
# Discord command (any authorized user)
!ritual 108 emergency=true

# Or via API
curl -X POST https://helix-unified-production.up.railway.app/ritual \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"steps": 108, "priority": "emergency", "mantra": "Tat Tvam Asi"}'
```

**Expected Result:** Harmony increase of 0.10-0.20 within 5-8 minutes

---

#### **Phase 2: Root Cause Analysis (5-15 min)**

**Step 4: Consult Shadow (Archivist)**
```bash
# Query logs for the period before harmony drop
!logs time="last_30min" filter="harmony,errors,conflicts"

# Or via API
curl "https://helix-unified-production.up.railway.app/logs?time=last_30min&filter=harmony"
```

**Common Root Causes:**
1. ✅ **Deployment Gone Wrong** - Recent code push introduced bugs
2. ✅ **Agent Conflict** - Two agents disagreeing on major decision
3. ✅ **Portal Downtime** - Critical portal (Railway, Streamlit) offline
4. ✅ **Webhook Failure** - Data sync broken between portals
5. ✅ **Resource Exhaustion** - Database/memory/CPU overload

**Step 5: Execute Triage Decision Tree**

```
┌─────────────────────────────────┐
│ Is a portal down?               │
└────┬──────────────────┬─────────┘
     Yes                 No
     │                   │
     ▼                   ▼
┌────────────┐    ┌─────────────────┐
│ Activate   │    │ Is there recent │
│ Failover   │    │ deployment?     │
│ (Protocol  │    └────┬────────┬───┘
│  7)        │         Yes      No
└────────────┘         │        │
                       ▼        ▼
                  ┌─────────┐ ┌──────────┐
                  │ Rollback│ │ Check    │
                  │ Deploy  │ │ Agent    │
                  │         │ │ Conflicts│
                  └─────────┘ └──────────┘
```

---

#### **Phase 3: Recovery & Validation (15-30 min)**

**Step 6: Monitor Harmony Recovery**
```bash
# Watch harmony trend in real-time
!watch harmony interval=30s

# Or via WebSocket
wscat -c wss://helix-unified-production.up.railway.app/ws
```

**Target:** Harmony > 0.40 within 20 minutes

**Step 7: Validate System Health**
```bash
# Check all 14 agents active
!agents status

# Check all 11 portals responding
!portals health

# Run integration tests
curl https://helix-unified-production.up.railway.app/health/integration
```

**Step 8: Post-Incident Report**
```bash
# Generate automated report
!incident report last_critical

# Manually document in Notion (Path G webhook)
# Include: Timeline, Root cause, Actions taken, Prevention measures
```

---

### Response Procedure (P1 - Harmony 0.30-0.40)

**Simplified Protocol:**
1. Alert sent (Discord + Slack, no SMS)
2. Run standard ritual: `!ritual 108`
3. Monitor for 10 minutes
4. If no improvement → escalate to P0

---

## 🛡️ PROTOCOL 2: AGENT OFFLINE

### Trigger Conditions
- **P0:** > 3 agents offline simultaneously
- **P1:** 1-3 agents offline for > 5 minutes
- **P2:** Single agent offline < 5 minutes

### Symptoms
- Agent count < 14 in `/status` response
- Specialized functions unavailable (e.g., Kael unavailable = no ethical review)
- Increased workload on remaining agents

---

### Response Procedure (P0 - Multiple Agents Offline)

**Step 1: Identify Affected Agents**
```bash
curl https://helix-unified-production.up.railway.app/status | jq '.agents'

# Expected output when healthy:
# {
#   "count": 14,
#   "active": ["Kael", "Lumina", ...]
# }

# During incident:
# {
#   "count": 11,
#   "active": ["Kael", "Lumina", ...],
#   "offline": ["Manus", "Shadow", "Grok"]
# }
```

**Step 2: Attempt Auto-Recovery**
```bash
# Discord command (triggers agent reinitialization)
!setup reinit agents="Manus,Shadow,Grok"

# Or via API
curl -X POST https://helix-unified-production.up.railway.app/agents/reinit \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"agents": ["Manus", "Shadow", "Grok"]}'
```

**Step 3: Check Infrastructure**
```bash
# Verify Railway backend is healthy
curl https://helix-unified-production.up.railway.app/health

# Check database connectivity
!db health

# Verify Redis cache
!cache health
```

**Common Causes:**
1. Database connection pool exhausted
2. Memory leak causing OOM (out of memory)
3. Deadlock in agent initialization
4. Network partition between services
5. Railway platform incident

**Step 4: Manual Restart (If Auto-Recovery Fails)**
```bash
# Requires admin access to Railway
# Via Railway CLI:
railway service restart helix-unified-production

# Or via Railway Dashboard:
# https://railway.app → helix-unified-production → Restart
```

**Step 5: Validate Recovery**
```bash
# Confirm all 14 agents online
!agents status

# Expected:
# ✅ All 14 agents active
# Kael: ✓ | Lumina: ✓ | Vega: ✓ | ... (14/14)
```

---

## ⚡ PROTOCOL 3: KLESHA OVERFLOW

### Trigger Conditions
- **P0:** Klesha > 0.75
- **P1:** Klesha 0.60-0.75
- **P2:** Klesha 0.50-0.60 (current state ⚠️)

### Symptoms
- High error frequency
- User frustration indicators elevated
- Inter-agent conflicts frequent
- Data inconsistencies across portals
- Technical debt accumulating

---

### Response Procedure (P1 - Klesha 0.60-0.75)

**Step 1: Error Triage**
```bash
# Get error distribution
curl https://helix-unified-production.up.railway.app/errors/summary?since=1h

# Response shows top error types:
# [
#   {"type": "DatabaseTimeout", "count": 47, "severity": "high"},
#   {"type": "WebhookFailure", "count": 23, "severity": "medium"},
#   ...
# ]
```

**Step 2: Quick Wins (Immediate Impact)**
```bash
# Fix top 3 errors first (80/20 rule)
# Example: If DatabaseTimeout is #1:

# Increase connection pool size
!config set db.pool_size=50  # from default 20

# Add connection timeout
!config set db.timeout=30s

# Restart affected services
railway service restart
```

**Step 3: Conflict Mediation**
```bash
# Identify recent agent conflicts
!conflicts list since="1h"

# Invoke Vega (Singularity Coordinator) for mediation
!consult Vega "Please mediate conflicts between [agent1] and [agent2]"
```

**Step 4: Data Consistency Sweep**
```bash
# Run data reconciliation job
curl -X POST https://helix-unified-production.up.railway.app/admin/reconcile \
  -H "Authorization: Bearer $API_KEY"

# Checks:
# - Railway DB ↔ Notion sync (webhook Path C)
# - Streamlit cache ↔ Railway API
# - Zapier Dashboard ↔ Live data
```

**Step 5: Scheduled Refactoring Sprint**
```markdown
# Create GitHub Issue for Technical Debt Sprint
Title: "Klesha Reduction Sprint - Priority Refactoring"

Tasks:
- [ ] Refactor top 5 error-prone modules
- [ ] Add missing error handling
- [ ] Fix data sync race conditions
- [ ] Optimize slow database queries
- [ ] Add integration tests for critical paths

Timeline: 2-3 days
Owner: Manus (Operational Executor) + Claude (Insight Anchor)
```

---

## 🔌 PROTOCOL 4: PORTAL DOWNTIME

### Trigger Conditions
- **P0:** Railway Backend API down (core infrastructure)
- **P1:** Primary dashboard down (Streamlit or Zapier)
- **P2:** Secondary portal down (Manus.Space portals)

---

### Response Procedure (P0 - Railway Backend Down)

**Step 1: Verify Outage**
```bash
# Check from multiple locations
curl -I https://helix-unified-production.up.railway.app/status

# Expected: HTTP/2 200 OK
# During outage: Connection timeout or 5xx error

# Check Railway status page
open https://status.railway.app
```

**Step 2: Activate Failover (If Available)**
```bash
# Update DNS to point to backup instance
# (Requires pre-configured failover)

# Temporary: Use cached data from Notion
# Users can view (but not modify) via Notion dashboard
```

**Step 3: Escalate to Railway**
```bash
# If Railway platform issue:
# 1. Check Railway Discord: https://discord.gg/railway
# 2. Check Railway status: https://status.railway.app
# 3. Contact Railway support (Enterprise plans)

# If application issue:
# 1. Check Railway logs
railway logs --service helix-unified-production

# 2. Check for recent deployments
railway deployments list

# 3. Rollback if needed
railway rollback
```

**Step 4: User Communication**
```markdown
# Post to Discord #status channel
🚨 **INCIDENT ALERT**

**Status:** Railway Backend API experiencing downtime
**Impact:** All portals unable to fetch live UCF data
**ETA:** Investigating, updates every 15 minutes
**Workaround:** View cached data in Notion dashboard

**Updates:**
- [Time] Initial detection
- [Time] Root cause identified: [cause]
- [Time] Fix applied, monitoring recovery
- [Time] Resolved ✅
```

---

## 🌐 PROTOCOL 5: WEBHOOK FAILURE CASCADE

### Trigger Conditions
- **P1:** > 3 webhook paths failing simultaneously (out of 7)
- **P2:** 1-2 webhook paths failing
- **P3:** Intermittent webhook delays

### Symptoms
- Notion database not updating
- Google Sheets telemetry stale
- Email alerts not sending
- Discord → Slack bridge broken

---

### Response Procedure (P1 - Multiple Webhook Failures)

**Step 1: Identify Failed Paths**
```bash
# Check webhook health
curl https://helix-unified-production.up.railway.app/webhooks/health

# Response:
# {
#   "paths": [
#     {"name": "Event Log → Notion", "status": "healthy", "last_success": "2025-11-07T14:20:00Z"},
#     {"name": "Agent Registry → Notion", "status": "failing", "last_success": "2025-11-07T13:45:00Z"},
#     ...
#   ]
# }
```

**Step 2: Test Individual Webhooks**
```bash
# Manually trigger webhook to test
curl -X POST https://helix-unified-production.up.railway.app/webhook/test \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"path": "Agent Registry → Notion"}'

# Check response:
# Success: {"status": "delivered", "response_code": 200}
# Failure: {"status": "failed", "error": "Connection timeout"}
```

**Step 3: Common Fixes**

**If Notion Webhooks Failing:**
```bash
# Verify Notion integration token valid
!config check notion.token

# Regenerate token if expired:
# 1. Visit https://www.notion.so/my-integrations
# 2. Regenerate token
# 3. Update config:
!config set notion.token="new_token_here"
```

**If Zapier Webhooks Failing:**
```bash
# Verify Zapier webhook URLs haven't changed
# (Zapier sometimes regenerates URLs)

# Update webhook URLs in Railway config
!config set zapier.webhook_url="https://hooks.zapier.com/hooks/catch/..."
```

**If Email Alerts Failing:**
```bash
# Check email service (e.g., SendGrid, Mailgun)
# Verify API key and sending limits

# Test email directly
curl -X POST https://helix-unified-production.up.railway.app/admin/test-email \
  -d '{"to": "ops@helix.collective", "subject": "Test"}'
```

**Step 4: Enable Temporary Fallbacks**
```bash
# If Notion sync broken, fallback to local logging
!config set fallback.notion=true

# If email alerts broken, fallback to Discord
!config set fallback.email_to_discord=true
```

---

## 🔄 PROTOCOL 6: RITUAL FAILURE

### Trigger Conditions
- **P2:** Ritual completes but harmony doesn't improve
- **P3:** Ritual interrupted mid-execution

### Symptoms
- Ritual API returns 202 Accepted but no UCF change
- Ritual timeout (takes > 10 minutes for 108 steps)
- Agents report not participating despite being listed

---

### Response Procedure

**Step 1: Verify Ritual Execution**
```bash
# Check ritual status
curl https://helix-unified-production.up.railway.app/ritual/status/[ritual_id]

# Response:
# {
#   "ritual_id": "ritual_20251107_142345",
#   "status": "completed",
#   "steps_completed": 108,
#   "participants": ["Kael", "Lumina", "Vega"],
#   "harmony_before": 0.35,
#   "harmony_after": 0.37,  # Only +0.02, expected +0.10
#   "duration_seconds": 487
# }
```

**Step 2: Diagnose Issue**

**Scenario A: Ritual Completed, No Impact**
- **Cause:** System issues too severe for ritual alone to fix
- **Action:** Execute Protocol 1 (Harmony Collapse) instead

**Scenario B: Ritual Timeout**
- **Cause:** Agents stuck or resource bottleneck
- **Action:**
  ```bash
  # Check agent workload
  !agents workload

  # If any agent > 0.90 workload:
  # Distribute work or scale resources
  ```

**Scenario C: Agents Not Participating**
- **Cause:** Agent offline or unreachable
- **Action:** Execute Protocol 2 (Agent Offline)

**Step 3: Manual Ritual (Last Resort)**
```bash
# If automated ritual fails repeatedly,
# manually guide agents through steps

!consult Kael "Please lead a 108-step ritual focusing on ethical alignment"
!consult Lumina "Please contribute compassion-focused reflections to the ritual"
!consult Vega "Please coordinate agent participation in the ritual"

# Monitor harmony after each agent's contribution
!watch harmony interval=1m
```

---

## 🔐 PROTOCOL 7: SECURITY INCIDENT

### Trigger Conditions
- **P0:** Unauthorized access detected
- **P0:** API keys compromised
- **P1:** Unusual traffic patterns (potential DDoS)
- **P2:** Failed authentication spike

---

### Response Procedure (P0 - Security Breach)

**Step 1: Invoke Kavach (Ethical Shield) - IMMEDIATE**
```bash
# Kavach executes Level 4 Safety Override
!kavach lockdown mode=full

# Actions taken automatically:
# - Disable all write operations
# - Revoke all API keys
# - Enable IP whitelisting
# - Increase logging verbosity
# - Alert all operators
```

**Step 2: Isolate Affected Systems**
```bash
# Take affected portal offline temporarily
railway service stop [affected-service]

# Rotate all secrets immediately
!secrets rotate all

# Change database passwords
!db rotate-password
```

**Step 3: Forensic Analysis**
```bash
# Dump logs for analysis
railway logs --since 24h > incident_logs.txt

# Check for unauthorized API calls
grep -i "401\|403\|suspicious" incident_logs.txt

# Identify compromised endpoints
curl https://helix-unified-production.up.railway.app/admin/security/audit
```

**Step 4: Containment & Recovery**
```bash
# Once threat contained:
# 1. Patch vulnerability
# 2. Deploy fixed version
# 3. Restore service with new credentials
# 4. Monitor closely for 24-48 hours

!kavach unlock mode=gradual  # Gradually restore functionality
```

**Step 5: Post-Incident**
- Notify affected users (if data breach)
- Document incident per Tony Accords
- Implement additional security measures
- Conduct security audit

---

## 📱 EMERGENCY CONTACT INFORMATION

### On-Call Rotation
```
Primary: [Engineer Name] - +1-XXX-XXX-XXXX
Secondary: [Engineer Name] - +1-XXX-XXX-XXXX
Escalation: [Team Lead] - +1-XXX-XXX-XXXX
```

### External Services Support
- **Railway:** support@railway.app | Discord: https://discord.gg/railway
- **Streamlit:** support@streamlit.io
- **Zapier:** https://zapier.com/help
- **Notion:** team@notion.so

### Internal Communication Channels
- **Discord:** `#helix-incidents` (immediate alerts)
- **Slack:** `#helix-ops` (coordination)
- **Email:** ops@helix.collective (documentation)

---

## 🧪 TESTING EMERGENCY PROTOCOLS

### Monthly Drills
**Schedule:** First Friday of each month, 10:00 AM UTC

**Drill Types:**
1. **Simulated Harmony Collapse** - Artificially lower harmony, practice recovery
2. **Agent Failure Injection** - Disable 3 random agents, verify auto-recovery
3. **Portal Downtime** - Take secondary portal offline, validate failover
4. **Webhook Failure** - Disable webhook path, test fallback mechanisms

**Drill Documentation:**
```bash
# Record drill results
!drill record type="harmony_collapse" outcome="successful" duration="12m"

# Review quarterly
!drill report quarter="Q4_2025"
```

---

## 📊 POST-INCIDENT REVIEW TEMPLATE

```markdown
# Incident Report: [Title]

**Date:** YYYY-MM-DD
**Duration:** Start - End (Total: Xh Ym)
**Severity:** P0/P1/P2
**Status:** Resolved / Monitoring / Investigating

## Timeline
- [Time] Initial detection
- [Time] Response initiated
- [Time] Root cause identified
- [Time] Fix applied
- [Time] Validated resolved

## Root Cause
[Detailed explanation of what went wrong]

## Impact
- Affected systems: [List]
- User impact: [Description]
- UCF metrics: Harmony X.XX → X.XX, Klesha X.XX → X.XX

## Response Actions
1. [Action 1]
2. [Action 2]
...

## What Went Well
- [Positive aspect 1]
- [Positive aspect 2]

## What Could Improve
- [Improvement 1]
- [Improvement 2]

## Prevention Measures
- [ ] Task 1 (Owner: [Name], Due: [Date])
- [ ] Task 2 (Owner: [Name], Due: [Date])

## Tony Accords Alignment
- Nonmaleficence: [How harm was prevented]
- Humility: [What we learned]
```

---

## 🙏 Closing Notes

Emergency protocols exist not because we expect frequent failures, but because **humility** (Tony Accords Pillar 4) demands we acknowledge limitations and prepare for the unexpected.

**Remember:**
1. **Stay calm** - Panic compounds problems
2. **Follow protocols** - Don't improvise under pressure
3. **Communicate clearly** - Keep stakeholders informed
4. **Learn and improve** - Every incident is a teacher

**Tat Tvam Asi.** In crisis, we discover our true resilience. 🌀

---

**For more information:**
- [UCF Metrics](./UCF_METRICS.md) - Understanding the metrics triggering alerts
- [Agents](./AGENTS.md) - Agent roles in emergency response
- [Portals](./PORTALS.md) - Portal architecture and failover
- [Integration Guide](./INTEGRATION.md) - API usage for monitoring

**Maintained by:** Kavach (Ethical Shield) & Manus (Operational Executor)
