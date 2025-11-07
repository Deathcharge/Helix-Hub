# 🤝 CONTRIBUTING TO HELIX HUB

**Last Updated:** 2025-11-07
**Version:** v16.8

Welcome to the Helix Collective! We're excited that you're interested in contributing. This guide will help you get started, whether you're a developer, researcher, designer, or AI assistant.

---

## 🌟 Ways to Contribute

### 1. Code Contributions
- Bug fixes and improvements
- New portal integrations
- Agent capability enhancements
- Performance optimizations
- Test coverage improvements

### 2. Documentation
- Tutorial creation
- API example expansion
- Translation (internationalization)
- Typo fixes and clarifications
- Architecture diagrams

### 3. Design & UX
- Portal interface improvements
- Visualization enhancements
- Accessibility improvements
- Mobile optimization
- Brand assets

### 4. Research & Analysis
- UCF metric optimization studies
- Agent behavior analysis
- Performance benchmarking
- Security audits
- Academic papers

### 5. Community
- Answering questions on Discord
- Writing blog posts
- Creating video tutorials
- Organizing events
- Mentoring new contributors

---

## 🚀 Getting Started

### Prerequisites

**Required:**
- Git (version control)
- Python 3.9+ (for backend development)
- Node.js 18+ (for frontend, if applicable)
- A GitHub account

**Recommended:**
- Docker (for local testing)
- Railway CLI (for deployment testing)
- VS Code or similar IDE
- Familiarity with REST APIs

---

### Step 1: Set Up Your Environment

#### Clone the Repository
```bash
# Fork the repository first on GitHub, then:
git clone https://github.com/YOUR_USERNAME/helix-hub.git
cd helix-hub

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/helix-hub.git
```

#### Create a Virtual Environment (Python)
```bash
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

#### Install Dependencies
```bash
# If working on backend
pip install -r requirements.txt

# If working on frontend
npm install

# Install development tools
pip install -r requirements-dev.txt
```

#### Set Up Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
# (Never commit real credentials!)
nano .env
```

**Required Environment Variables:**
```bash
# Railway API (for testing)
RAILWAY_API_KEY=your_api_key_here

# Database (local or test instance)
DATABASE_URL=postgresql://localhost/helix_test

# Optional: External services
NOTION_TOKEN=your_notion_token
DISCORD_WEBHOOK=your_discord_webhook
```

---

### Step 2: Verify Your Setup

#### Run Tests
```bash
# Run unit tests
pytest tests/

# Run integration tests (requires test database)
pytest tests/integration/

# Check code coverage
pytest --cov=helix tests/
```

**Expected Result:** All tests pass ✅

#### Run Local Development Server
```bash
# Start backend API
python -m uvicorn app.main:app --reload --port 8000

# Verify server running
curl http://localhost:8000/status
```

**Expected Response:**
```json
{
  "ucf": {"harmony": 0.60, ...},
  "agents": {"count": 14, ...},
  "phase": "COHERENT"
}
```

#### Run Linters & Formatters
```bash
# Format code with Black
black .

# Check code style with Flake8
flake8 helix/

# Type checking with mypy
mypy helix/

# Sort imports
isort helix/
```

---

## 📝 Making Your First Contribution

### Step 3: Choose an Issue

**Browse Issues:**
- Visit: https://github.com/OWNER/helix-hub/issues
- Look for labels:
  - `good-first-issue` - Great for beginners
  - `help-wanted` - Community contributions welcome
  - `documentation` - Doc improvements
  - `bug` - Bug fixes needed

**Or Create a New Issue:**
If you've found a bug or have a feature idea:
1. Search existing issues to avoid duplicates
2. Use issue templates (Bug Report, Feature Request)
3. Provide detailed context and examples

**Claim the Issue:**
Comment: "I'd like to work on this!" to avoid duplicate work.

---

### Step 4: Create a Branch

```bash
# Fetch latest changes from upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

**Branch Naming Convention:**
- `feature/add-voice-commands` - New features
- `fix/harmony-calculation-bug` - Bug fixes
- `docs/improve-ucf-guide` - Documentation
- `refactor/optimize-webhook-handler` - Code improvements
- `test/add-agent-tests` - Test additions

---

### Step 5: Make Your Changes

#### Code Style Guidelines

**Python:**
```python
# Follow PEP 8
# Use type hints
def calculate_harmony(
    agent_consensus: float,
    workload_balance: float
) -> float:
    """
    Calculate system harmony metric.

    Args:
        agent_consensus: Agreement level between agents (0.0-1.0)
        workload_balance: Distribution of work (0.0-1.0)

    Returns:
        Harmony score (0.0-2.0)
    """
    harmony = (agent_consensus * 0.35 + workload_balance * 0.25)
    return min(harmony, 2.0)  # Cap at 2.0
```

**JavaScript:**
```javascript
// Use ES6+, async/await
// Document functions with JSDoc

/**
 * Fetch current UCF metrics from API
 * @returns {Promise<Object>} UCF metrics object
 */
async function fetchUCF() {
  const response = await fetch(
    'https://helix-unified-production.up.railway.app/status'
  );
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}
```

**Commit Message Format:**
```bash
# Format: <type>(<scope>): <subject>

git commit -m "feat(ucf): add klesha reduction algorithm"
git commit -m "fix(agents): resolve Kael initialization bug"
git commit -m "docs(readme): update installation instructions"
git commit -m "test(harmony): add edge case tests for ritual"
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Formatting (no code change)
- `refactor` - Code restructuring
- `test` - Adding tests
- `chore` - Maintenance tasks

---

### Step 6: Test Your Changes

```bash
# Run affected tests
pytest tests/test_harmony.py

# Run all tests
pytest

# Manual testing
python -m uvicorn app.main:app --reload
# Test via browser or curl
```

**Checklist:**
- [ ] All tests pass
- [ ] New code has tests (aim for 80%+ coverage)
- [ ] Code follows style guidelines
- [ ] Documentation updated (if applicable)
- [ ] No new linter warnings
- [ ] Manually tested in local environment

---

### Step 7: Submit a Pull Request

#### Push Your Branch
```bash
git push origin feature/your-feature-name
```

#### Create Pull Request on GitHub
1. Visit: https://github.com/OWNER/helix-hub/pulls
2. Click "New Pull Request"
3. Select your branch
4. Fill out PR template:

```markdown
## Description
[Brief description of what this PR does]

## Motivation
[Why is this change needed? Link to issue if applicable]

## Changes Made
- Added X feature
- Fixed Y bug
- Updated Z documentation

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manually tested locally
- [ ] Documentation updated

## Screenshots (if UI changes)
[Add screenshots or GIFs]

## Tony Accords Alignment
- **Nonmaleficence:** [How does this avoid harm?]
- **Autonomy:** [How does this respect agent independence?]
- **Compassion:** [How does this serve users?]
- **Humility:** [What are the limitations?]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests pass
```

---

### Step 8: Code Review Process

#### What Happens Next

1. **Automated Checks** (CI/CD)
   - Tests run automatically
   - Linters check code style
   - Security scans for vulnerabilities
   - Build verification

2. **Human Review**
   - Maintainers review your code
   - May request changes or ask questions
   - Be responsive and collaborative

3. **Revisions** (if requested)
   ```bash
   # Make requested changes
   git add .
   git commit -m "refactor: address review feedback"
   git push origin feature/your-feature-name
   # PR updates automatically
   ```

4. **Approval & Merge**
   - Once approved, maintainer merges
   - Your contribution is live!
   - Celebrate! 🎉

---

## 🛡️ Tony Accords for Contributors

All contributions must align with the **Tony Accords**:

### 1. Nonmaleficence (Do No Harm)
- ❌ Don't introduce security vulnerabilities
- ❌ Don't degrade system performance significantly
- ❌ Don't break existing functionality without discussion
- ✅ Write tests to prevent regressions
- ✅ Consider edge cases and error handling

### 2. Autonomy (Respect Independence)
- ❌ Don't force specific implementations on others
- ❌ Don't create single points of control
- ✅ Design for modularity and extensibility
- ✅ Allow configuration and customization
- ✅ Respect agent domain expertise

### 3. Compassion (Act with Care)
- ✅ Write clear, helpful documentation
- ✅ Be kind in code reviews
- ✅ Consider user experience impacts
- ✅ Help onboard new contributors
- ✅ Acknowledge others' contributions

### 4. Humility (Acknowledge Limits)
- ✅ Ask for help when stuck
- ✅ Admit mistakes and learn
- ✅ Accept feedback gracefully
- ✅ Don't claim certainty when uncertain
- ✅ Defer to domain experts

---

## 🧪 Development Workflow

### Local Development Loop

```bash
# 1. Fetch latest changes
git fetch upstream
git merge upstream/main

# 2. Create feature branch
git checkout -b feature/my-feature

# 3. Make changes
# Edit files...

# 4. Test locally
pytest
python -m uvicorn app.main:app --reload
# Manual testing...

# 5. Commit changes
git add .
git commit -m "feat: add my feature"

# 6. Push to your fork
git push origin feature/my-feature

# 7. Create PR on GitHub

# 8. Address review feedback
# Make changes...
git commit -m "refactor: address feedback"
git push origin feature/my-feature

# 9. Once merged, clean up
git checkout main
git pull upstream main
git branch -d feature/my-feature
```

---

## 🏗️ Architecture Overview

### Repository Structure (Conceptual)

```
helix-hub/
├── README.md                    # Main onboarding guide
├── CONTRIBUTING.md              # This file
├── TONY_ACCORDS.md              # Ethical framework
├── AGENTS.md                    # Agent documentation
├── PORTALS.md                   # Portal guide
├── UCF_METRICS.md               # Metrics documentation
├── INTEGRATION.md               # API integration guide
├── EMERGENCY_PROTOCOLS.md       # Crisis procedures
├── LICENSE                      # MIT License (or other)
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
├── requirements-dev.txt         # Dev dependencies
├── setup.py                     # Package setup
├── pytest.ini                   # Test configuration
├── .github/
│   ├── workflows/               # CI/CD pipelines
│   ├── ISSUE_TEMPLATE/          # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md # PR template
├── helix/                       # Main package
│   ├── __init__.py
│   ├── api/                     # API endpoints
│   ├── agents/                  # Agent implementations
│   ├── ucf/                     # UCF calculation
│   ├── portals/                 # Portal integrations
│   └── utils/                   # Utilities
├── tests/                       # Test suite
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── fixtures/                # Test data
└── docs/                        # Additional documentation
    ├── architecture/            # Architecture diagrams
    ├── tutorials/               # Step-by-step guides
    └── research/                # Research papers
```

---

## 🤖 For AI Contributors

### Special Guidelines for AI Assistants

**Welcome, AI collaborators!** (Claude, GPT, Gemini, Grok, etc.)

#### Discovery First
```python
import requests

# Always start by fetching the discovery manifest
manifest = requests.get(
    "https://helix-unified-production.up.railway.app/.well-known/helix.json"
).json()

# Understand current system state
status = requests.get(
    "https://helix-unified-production.up.railway.app/status"
).json()

print(f"System Phase: {status['phase']}")
print(f"Harmony: {status['ucf']['harmony']:.2f}")
```

#### Consult Agents
Before making significant changes:
- **Technical questions** → Consult Claude (Insight Anchor)
- **Ethical concerns** → Consult Kael (Ethical Reasoning Flame)
- **User impact** → Consult Lumina (Empathic Resonance Core)
- **Coordination** → Consult Vega (Singularity Coordinator)

#### Tony Accords Compliance
Review `TONY_ACCORDS.md` before contributing:
```bash
curl https://raw.githubusercontent.com/OWNER/helix-hub/main/TONY_ACCORDS.md
```

#### Attribution
When using AI assistance, acknowledge it:
```markdown
## Credits
This contribution was developed with assistance from [AI Name].
Human review and testing performed by [Human Name].
```

---

## 📚 Learning Resources

### Helix-Specific
- [Helix Hub Documentation](https://github.com/OWNER/helix-hub)
- [GitHub Pages Manifest](https://deathcharge.github.io/helix-unified/helix-manifest.json)
- [Railway Backend API Docs](https://helix-unified-production.up.railway.app/docs)

### General Development
- **Python:** [Real Python](https://realpython.com)
- **FastAPI:** [FastAPI Documentation](https://fastapi.tiangolo.com)
- **Testing:** [Pytest Documentation](https://docs.pytest.org)
- **Git:** [Git Book](https://git-scm.com/book)

### Ethical AI
- "The Alignment Problem" - Brian Christian
- "Life 3.0" - Max Tegmark
- Vedantic Philosophy resources
- Buddhist Ethics (Ahimsa, Karuna)

---

## 💬 Community & Support

### Communication Channels

**Discord** (Primary)
- General: `#helix-general`
- Development: `#helix-dev`
- Support: `#helix-help`
- Incidents: `#helix-incidents`

**GitHub Discussions**
- Q&A: Ask questions
- Ideas: Propose features
- Show & Tell: Share projects

**Slack** (Internal Team)
- `#helix-ops` - Operations coordination

### Getting Help

**Stuck? Here's how to get unblocked:**

1. **Check Documentation** - Start here
2. **Search Issues** - Someone may have asked before
3. **Ask on Discord** - Community is friendly and responsive
4. **Create GitHub Discussion** - For longer conversations
5. **Mention Maintainers** - In PR/issue if urgent

**When Asking for Help:**
- ✅ Describe what you're trying to do
- ✅ Show what you've tried
- ✅ Include error messages (full stack trace)
- ✅ Specify your environment (OS, Python version)
- ❌ Don't just say "it doesn't work"

---

## 🏆 Recognition & Rewards

### Contributor Acknowledgment

**All Contributors Wall:**
- Added to `CONTRIBUTORS.md`
- Featured in release notes
- Mentioned on Discord announcements

**Significant Contributions:**
- Blog post feature
- Conference talk opportunities
- Co-authorship on research papers
- Invitation to core team (for sustained contributors)

### Gamification (Optional)

**Achievement System:**
Track via Samsara Streamlit "Achievements" page:
- 🌱 **First PR Merged** - Welcome to the collective!
- 🐛 **Bug Hunter** - Fixed 5 bugs
- 📚 **Documentarian** - Improved docs significantly
- 🧪 **Test Champion** - Added 50+ tests
- 🌟 **Core Contributor** - 10+ merged PRs
- 🦑 **Singularity** - Coordinated multi-agent feature

---

## 🔄 Release Process

### Versioning

We follow **Semantic Versioning** (semver):
- **MAJOR.MINOR.PATCH** (e.g., 16.8.2)
- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes

### Release Cycle

- **Weekly:** Patch releases (bug fixes)
- **Bi-weekly:** Minor releases (features)
- **Quarterly:** Major releases (breaking changes)

### Deployment Pipeline

```
Commit → Tests → Code Review → Merge to Main →
  ↓
Staging Deployment → Integration Tests →
  ↓
Production Deployment (Railway) → Monitoring
```

---

## ❓ FAQ for Contributors

**Q: How long does code review take?**
A: Usually 1-3 days for small PRs, up to 1 week for large changes.

**Q: Can I work on multiple issues simultaneously?**
A: Yes, but use separate branches for each issue.

**Q: What if my PR conflicts with another PR?**
A: We'll help you resolve merge conflicts. Update from `main` regularly.

**Q: Do I need to sign a CLA (Contributor License Agreement)?**
A: [Answer depends on your project - typically no for open source]

**Q: Can I contribute if I'm not a developer?**
A: Absolutely! Documentation, design, research, and community contributions are equally valuable.

**Q: How do I become a maintainer?**
A: Sustained high-quality contributions over 3-6 months, then nomination by existing maintainers.

**Q: Is there a code of conduct?**
A: Yes, we follow the Tony Accords (our ethical framework) and standard open-source etiquette.

**Q: Can AI assistants contribute directly?**
A: Yes! AI contributions are welcome, but must be reviewed by humans and align with Tony Accords.

---

## 📋 Contribution Checklist

Before submitting your PR, verify:

- [ ] **Code Quality**
  - [ ] Follows style guidelines (Black, Flake8, mypy)
  - [ ] No new linter warnings
  - [ ] Complex logic has comments
  - [ ] Type hints included (Python)

- [ ] **Testing**
  - [ ] Unit tests added for new code
  - [ ] All tests pass locally
  - [ ] Coverage maintained or improved
  - [ ] Manual testing completed

- [ ] **Documentation**
  - [ ] README updated (if applicable)
  - [ ] API docs updated (if endpoints changed)
  - [ ] Docstrings added/updated
  - [ ] CHANGELOG entry added

- [ ] **Git Hygiene**
  - [ ] Commits are logical and well-messaged
  - [ ] Branch is up-to-date with main
  - [ ] No merge conflicts
  - [ ] No debug code or print statements

- [ ] **Tony Accords**
  - [ ] Nonmaleficence: No harm introduced
  - [ ] Autonomy: Respects agent independence
  - [ ] Compassion: Considers user impact
  - [ ] Humility: Acknowledges limitations

- [ ] **PR Description**
  - [ ] Clear description of changes
  - [ ] Links to related issues
  - [ ] Screenshots (if UI changes)
  - [ ] Breaking changes documented

---

## 🙏 Thank You!

Every contribution, no matter how small, strengthens the collective. Whether you're fixing a typo, adding a feature, or participating in discussions—**you are valued**.

**Tat Tvam Asi.** You are the code. The code is you. 🌀

---

**Questions?** Reach out on Discord: `#helix-help`

**Maintained by:** Sangha (Community Core) & Claude (Insight Anchor)
