# 🗄️ REDIS SESSION MANAGEMENT GUIDE

**Last Updated:** 2025-11-07
**Version:** v16.8

This guide covers Redis session management configuration and best practices for preventing session-related memory leaks and crashes in the Helix Collective system.

---

## 🎯 PURPOSE

Redis is used for session management in the Helix backend. Without proper TTL (Time To Live) configuration, sessions can accumulate indefinitely, leading to:
- Memory exhaustion
- Redis OOM (Out Of Memory) errors
- System crashes
- Degraded performance

---

## ⚙️ RECOMMENDED CONFIGURATION

### Production Settings

```bash
# Session TTL: 24 hours (86400 seconds)
# Sessions expire after 24 hours of creation
redis.session_ttl=86400

# Idle timeout: 5 minutes (300 seconds)
# Sessions expire after 5 minutes of inactivity
redis.session_idle_timeout=300

# Enable automatic session cleanup
# Background process removes expired sessions
redis.session_cleanup=true

# Session cleanup interval: 1 hour (3600 seconds)
redis.session_cleanup_interval=3600

# Maximum sessions per user: 5
# Prevents single user from creating excessive sessions
redis.max_sessions_per_user=5
```

### Development Settings

```bash
# Shorter TTL for development
redis.session_ttl=3600  # 1 hour

# Shorter idle timeout
redis.session_idle_timeout=300  # 5 minutes

# More frequent cleanup
redis.session_cleanup_interval=600  # 10 minutes
```

---

## 📊 MONITORING SESSION HEALTH

### Check Current Session Count

```bash
# Count all active sessions
redis-cli KEYS "session:*" | wc -l

# Or via Helix command
!redis keys session:* | wc -l
```

### Check Redis Memory Usage

```bash
# Get Redis info
redis-cli INFO memory

# Key metrics to monitor:
# - used_memory_human: Total memory used
# - used_memory_peak_human: Peak memory usage
# - maxmemory: Maximum memory limit
```

### View Session Details

```bash
# Get specific session
redis-cli GET session:abc123

# Get session TTL (time remaining)
redis-cli TTL session:abc123

# List recent sessions
redis-cli KEYS "session:*" | head -10
```

---

## 🚨 TROUBLESHOOTING

### Problem: Too Many Sessions Accumulating

**Symptoms:**
- Redis memory usage climbing steadily
- Session count > 10,000
- System slowdown

**Diagnosis:**
```bash
# Count sessions
redis-cli DBSIZE

# Check if TTL is set on sessions
redis-cli TTL session:$(redis-cli KEYS "session:*" | head -1)
# Returns -1 if no TTL (problem!)
# Returns seconds if TTL set (good)
```

**Solution:**
```bash
# Option 1: Set TTL on existing sessions (non-destructive)
redis-cli KEYS "session:*" | xargs -I {} redis-cli EXPIRE {} 86400

# Option 2: Enable automatic cleanup going forward
!config set redis.session_ttl=86400
!config set redis.session_cleanup=true

# Option 3: Clear all sessions (CAUTION: logs everyone out)
# redis-cli FLUSHDB
```

---

### Problem: Redis Out of Memory

**Symptoms:**
- `OOM command not allowed when used memory > 'maxmemory'`
- Sessions failing to create
- Authentication errors

**Diagnosis:**
```bash
# Check memory limit
redis-cli CONFIG GET maxmemory

# Check current usage
redis-cli INFO memory | grep used_memory_human
```

**Solution:**
```bash
# Option 1: Increase maxmemory (if resources available)
redis-cli CONFIG SET maxmemory 2gb

# Option 2: Enable eviction policy
redis-cli CONFIG SET maxmemory-policy allkeys-lru

# Option 3: Clear old sessions
redis-cli --scan --pattern "session:*" | \
  xargs -L 1000 redis-cli DEL

# Option 4: Restart Redis (loses all data)
# railway service restart redis
```

---

### Problem: Session Leaks (Users Can't Logout)

**Symptoms:**
- Sessions persist after logout
- Multiple sessions for same user
- Session count grows linearly with logins

**Diagnosis:**
```bash
# Check sessions for a specific user
redis-cli KEYS "session:user:john@example.com:*"

# Count sessions per user
redis-cli --scan --pattern "session:user:*" | \
  cut -d: -f3 | sort | uniq -c | sort -rn | head -10
```

**Solution:**
```bash
# Implement proper logout handler
# In application code, ensure:
# 1. Session is deleted from Redis on logout
# 2. Session cookie is cleared
# 3. User token is invalidated

# Manual cleanup for specific user
redis-cli KEYS "session:user:john@example.com:*" | \
  xargs redis-cli DEL
```

---

## 🔒 SECURITY BEST PRACTICES

### 1. Session Hijacking Prevention

```bash
# Bind sessions to IP address
redis.session_bind_ip=true

# Regenerate session ID on privilege escalation
redis.session_regenerate_on_auth=true

# Use secure session cookies
redis.session_cookie_secure=true
redis.session_cookie_httponly=true
redis.session_cookie_samesite=strict
```

### 2. Session Validation

```bash
# Validate session on each request
# Check TTL and user binding

# Example session validation flow:
# 1. Get session from Redis
# 2. Check session.user_id matches request
# 3. Check session.ip matches request IP (if bind_ip enabled)
# 4. Check session TTL > 0
# 5. Refresh TTL on valid request (sliding window)
```

### 3. Rate Limiting Session Creation

```bash
# Prevent session creation abuse
redis.max_sessions_per_ip_per_hour=20
redis.max_sessions_per_user=5

# Alert on excessive session creation
redis.session_creation_alert_threshold=100
```

---

## 📈 PERFORMANCE OPTIMIZATION

### 1. Session Data Optimization

**DO:**
- Store minimal data in session (user_id, token, timestamps)
- Use separate keys for user profile data
- Compress large session values

**DON'T:**
- Store entire user objects in session
- Store file uploads or large blobs
- Duplicate data already in database

### 2. Redis Configuration

```bash
# Enable RDB persistence for session recovery
save 900 1
save 300 10
save 60 10000

# Use AOF for durability (optional, trades performance)
appendonly yes
appendfsync everysec

# Optimize memory
maxmemory-policy allkeys-lru
maxmemory 2gb
```

### 3. Connection Pooling

```python
# Python example with redis-py
from redis import ConnectionPool

pool = ConnectionPool(
    host='redis.railway.internal',
    port=6379,
    max_connections=50,
    socket_keepalive=True,
    socket_keepalive_options={
        socket.TCP_KEEPIDLE: 30,
        socket.TCP_KEEPINTVL: 10,
        socket.TCP_KEEPCNT: 3
    }
)

redis_client = redis.Redis(connection_pool=pool)
```

---

## 🔄 SESSION LIFECYCLE

### 1. Session Creation

```python
import uuid
import time
import json

def create_session(user_id, ip_address):
    session_id = str(uuid.uuid4())
    session_data = {
        'user_id': user_id,
        'ip': ip_address,
        'created_at': time.time(),
        'last_accessed': time.time()
    }

    # Store with TTL
    redis_client.setex(
        f"session:{session_id}",
        86400,  # 24 hours
        json.dumps(session_data)
    )

    return session_id
```

### 2. Session Validation

```python
def validate_session(session_id, ip_address=None):
    key = f"session:{session_id}"

    # Check if session exists
    data = redis_client.get(key)
    if not data:
        return None

    session = json.loads(data)

    # Validate IP binding if enabled
    if ip_address and session['ip'] != ip_address:
        return None

    # Refresh TTL (sliding window)
    session['last_accessed'] = time.time()
    redis_client.setex(key, 86400, json.dumps(session))

    return session
```

### 3. Session Destruction

```python
def destroy_session(session_id):
    redis_client.delete(f"session:{session_id}")
```

---

## 📚 RELATED DOCUMENTATION

- [SESSION_CRASH_ANALYSIS.md](./SESSION_CRASH_ANALYSIS.md) - Session crash patterns
- [EMERGENCY_PROTOCOLS.md](./EMERGENCY_PROTOCOLS.md) - Crisis response
- [PORTALS.md](./PORTALS.md) - System architecture
- [INTEGRATION.md](./INTEGRATION.md) - Integration patterns

---

## 🔧 QUICK REFERENCE COMMANDS

```bash
# Session count
redis-cli DBSIZE

# Memory usage
redis-cli INFO memory | grep used_memory_human

# Set TTL on all sessions
redis-cli KEYS "session:*" | xargs -I {} redis-cli EXPIRE {} 86400

# Delete expired sessions
redis-cli --scan --pattern "session:*" | \
  while read key; do
    ttl=$(redis-cli TTL "$key")
    if [ "$ttl" -eq "-1" ]; then
      redis-cli DEL "$key"
    fi
  done

# Clear all sessions (DANGER)
redis-cli KEYS "session:*" | xargs redis-cli DEL

# Get session with longest TTL
redis-cli KEYS "session:*" | \
  xargs -I {} sh -c 'echo "$(redis-cli TTL {}) {}"' | \
  sort -rn | head -1

# Monitor Redis commands in real-time
redis-cli MONITOR
```

---

**Last Review:** 2025-11-07
**Next Review:** 2025-12-07
