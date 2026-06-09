# AGENTS.md - Claude Agent Configuration

This file documents how Claude AI agents can be used to assist with Elder Care Assistant development and operations.

## Overview

Claude agents extend the capabilities of the Elder Care Assistant project by automating code review, testing, documentation, and development workflows. These agents are designed to work within Claude Code and can be customized for specific development tasks.

## Table of Contents

1. [Available Agents](#available-agents)
2. [Agent Capabilities](#agent-capabilities)
3. [Configuration](#configuration)
4. [Usage Examples](#usage-examples)
5. [Best Practices](#best-practices)
6. [Integration Points](#integration-points)
7. [Troubleshooting](#troubleshooting)

---

## Available Agents

### 1. Code Review Agent

**Purpose**: Automated code review for pull requests and commits

**Triggers**:
- When code changes are submitted
- Before merging to main branch
- On-demand via Claude Code interface

**Capabilities**:
- Syntax validation
- Security vulnerability scanning
- Performance analysis
- Style guide compliance checking
- Documentation review
- Test coverage analysis

**Configuration**:
```
Agent: code-review
Scope: app/
Rules:
  - Enforce PEP 8 compliance
  - Check for hardcoded secrets
  - Verify type hints present
  - Validate error handling
  - Check SQL injection prevention
```

### 2. Testing Agent

**Purpose**: Automated test generation and validation

**Triggers**:
- New feature implementation
- Bug fixes
- Refactoring tasks
- Before deployments

**Capabilities**:
- Generate unit tests
- Create integration tests
- Test coverage analysis
- Identify untested code paths
- Execute test suite
- Report coverage metrics

**Configuration**:
```
Agent: testing
Scope: app/, tests/
Rules:
  - Minimum 80% coverage required
  - All endpoints must have tests
  - Security tests for auth endpoints
  - Database tests use real PostgreSQL
  - No hardcoded test data
```

### 3. Documentation Agent

**Purpose**: Keep documentation in sync with code

**Triggers**:
- API endpoint changes
- Schema modifications
- Configuration changes
- New features added

**Capabilities**:
- Generate API documentation
- Update README sections
- Keep examples current
- Validate documentation links
- Create changelog entries
- Generate migration guides

**Configuration**:
```
Agent: documentation
Scope: README.md, USER_MANUAL.md, .instructions.md
Rules:
  - Auto-generate API docs from OpenAPI spec
  - Update feature docs when routes change
  - Keep examples functional
  - Flag deprecated features
  - Generate upgrade guides
```

### 4. Security Agent

**Purpose**: Continuous security scanning and hardening

**Triggers**:
- On every commit
- Before production deployment
- Dependency updates
- Configuration changes

**Capabilities**:
- Scan for OWASP vulnerabilities
- Check for hardcoded secrets
- Validate authentication flows
- Audit database queries
- Check encryption usage
- Verify security headers

**Configuration**:
```
Agent: security
Scope: Full repository
Rules:
  - Block commits with secrets
  - Require HTTPS for external APIs
  - Validate JWT implementation
  - Check for SQL injection risks
  - Audit sensitive data handling
  - Verify CORS configuration
```

### 5. Performance Agent

**Purpose**: Monitor and optimize application performance

**Triggers**:
- Database query changes
- Algorithm implementations
- API endpoint modifications
- Dependency updates

**Capabilities**:
- Query optimization analysis
- Identify N+1 query problems
- Cache opportunity detection
- Memory leak analysis
- Load testing suggestions
- Bottleneck identification

**Configuration**:
```
Agent: performance
Scope: app/services/, app/database/
Rules:
  - Flag unindexed queries
  - Detect missing pagination
  - Identify cache opportunities
  - Check for excessive queries
  - Verify connection pooling
```

### 6. Health Specialist Agent

**Purpose**: Healthcare-specific compliance and safety review

**Triggers**:
- Health data handling code
- Chat/AI integration changes
- Emergency feature modifications
- Data privacy implementations

**Capabilities**:
- Verify HIPAA compliance
- Check data retention policies
- Validate audit logging
- Review consent management
- Audit medical advice safeguards
- Check patient data encryption

**Configuration**:
```
Agent: health-specialist
Scope: app/api/routes/health.py, app/api/routes/chat.py
Rules:
  - Health data must be encrypted at rest
  - Audit logs required for PII access
  - Chat must include medical disclaimers
  - Data retention policies enforced
  - Consent tracking mandatory
```

---

## Agent Capabilities

### Code Analysis

Agents can analyze code for:
- **Style Compliance**: PEP 8, naming conventions, structure
- **Type Safety**: Type hints, type checking, mypy validation
- **Error Handling**: Exception catching, error responses
- **Security Issues**: SQL injection, XSS, authentication bypass
- **Performance**: Query optimization, caching, async patterns
- **Testing**: Test coverage, edge case coverage, mocking

### Automation

Agents can automate:
- **Commit Checking**: Validate commits before pushing
- **PR Analysis**: Review pull requests automatically
- **Documentation Updates**: Keep docs in sync with code
- **Test Generation**: Create test skeletons
- **Release Notes**: Generate changelogs
- **Migration Scripts**: Create database migrations

### Reporting

Agents can generate:
- **Security Reports**: Vulnerability summaries
- **Coverage Reports**: Test coverage metrics
- **Performance Reports**: Optimization recommendations
- **Compliance Reports**: HIPAA/GDPR compliance status
- **Quality Metrics**: Code quality scores
- **Change Logs**: Automated changelogs

---

## Configuration

### Global Agent Settings

Configure agents in `.claude/settings.json`:

```json
{
  "agents": {
    "enabled": true,
    "autoReview": {
      "enabled": true,
      "triggers": ["commit", "pull_request"],
      "rules": "app/"
    },
    "autoTest": {
      "enabled": true,
      "minimumCoverage": 80,
      "triggers": ["feature", "bugfix"]
    },
    "autoDocumentation": {
      "enabled": true,
      "updateOnChange": ["models", "schemas", "routes"]
    },
    "security": {
      "enabled": true,
      "scanSecrets": true,
      "hipaaCheck": true
    },
    "performance": {
      "enabled": true,
      "analyzeQueries": true,
      "detectMemoryLeaks": true
    }
  }
}
```

### Per-Feature Configuration

Configure specific agents for features:

```json
{
  "agents": {
    "health": {
      "agent": "health-specialist",
      "strictMode": true,
      "requireAuditLog": true,
      "encryptionRequired": true
    },
    "chat": {
      "agent": "security",
      "requireMedicalDisclaimer": true,
      "auditConversations": true
    },
    "reminders": {
      "agent": "testing",
      "minimumCoverage": 90,
      "requireIntegrationTests": true
    }
  }
}
```

### Enable/Disable Specific Agents

```bash
# Enable code review agent
claude-code config set agents.code-review.enabled true

# Disable performance agent temporarily
claude-code config set agents.performance.enabled false

# Set minimum coverage to 90%
claude-code config set agents.testing.minimumCoverage 90
```

---

## Usage Examples

### Example 1: Code Review Before Commit

```bash
# Check code before committing
claude-code review-code app/api/routes/health.py

# Output:
# ✅ Type hints: All functions have type hints
# ⚠️  Security: 2 potential SQL injection risks (review required)
# ❌ Coverage: New functions lack tests (80 → 76%)
# ✅ PEP 8: Compliant
```

### Example 2: Generate Tests for New Endpoint

```bash
# Auto-generate tests for new endpoint
claude-code generate-tests app/api/routes/health.py

# Creates: tests/test_health.py with:
# - Test for GET /api/v1/health/status
# - Test for POST /api/v1/health/checkin
# - Test for invalid data handling
# - Test for authentication
# - Test for database errors
```

### Example 3: Security Scan Before Deployment

```bash
# Full security scan
claude-code security-scan

# Output:
# HIPAA Compliance: ✅ PASS
# Secrets Detection: ✅ PASS (0 secrets found)
# SQL Injection Risk: ❌ FAIL (2 issues in query building)
# Authentication: ✅ PASS
# Data Encryption: ✅ PASS
# CORS Config: ❌ FAIL (overly permissive)

# Recommendations:
# 1. Use parameterized queries in app/services/services.py:145
# 2. Restrict CORS origins in config.py
```

### Example 4: Performance Analysis

```bash
# Analyze performance for chat feature
claude-code analyze-performance app/api/routes/chat.py

# Output:
# Query Analysis:
#   ⚠️  N+1 query detected: line 45
#   ✅ Indexes present on user_id, created_at
#   💡 Suggestion: Cache chat history
#
# Caching Opportunities:
#   - Model configurations (currently queried on each request)
#   - User preferences (requested in every endpoint)
#
# Recommendations:
#   1. Use Redis for model caching (estimated 200ms improvement)
#   2. Implement pagination for long conversations
```

### Example 5: Documentation Sync

```bash
# Update documentation for API changes
claude-code sync-docs

# Output:
# Found 3 API changes:
#   ✅ POST /api/v1/health/checkin - Updated README
#   ✅ GET /api/v1/reminders - Added example
#   ⚠️  /api/v1/family/members - Deprecated (flagged for migration guide)
#
# Generated: CHANGELOG.md entry
```

### Example 6: Healthcare Compliance Check

```bash
# Verify HIPAA compliance
claude-code health-check

# Output:
# HIPAA Compliance Report:
#   Data Encryption: ✅ PASS
#   Access Logging: ✅ PASS
#   Data Retention: ⚠️  Policy not documented
#   Patient Consent: ✅ PASS
#   Breach Notification: ✅ PASS
#
# Issues:
#   1. Document data retention policy in config
#   2. Add automated cleanup for expired data
```

---

## Best Practices

### When to Use Agents

✅ **Use agents for**:
- Automated security scanning before commits
- Test generation for new features
- Performance analysis of complex queries
- Documentation updates after API changes
- Compliance verification before deployment
- Code review suggestions for PRs

❌ **Don't use agents for**:
- Making architectural decisions
- Writing business logic
- Complex debugging
- Understanding project context
- Making policy decisions
- Final security approvals

### Agent Workflow

```
Developer writes code
        ↓
Run agent review → Agent provides feedback
        ↓
Developer addresses issues
        ↓
Run agent verify → Agent confirms fixes
        ↓
Developer commits with confidence
```

### Handling Agent Recommendations

1. **For security issues**: Always fix before merging
2. **For performance suggestions**: Evaluate impact before implementing
3. **For documentation**: Accept if accurate, request revision if not
4. **For test generation**: Review and modify as needed
5. **For style issues**: Auto-fix if possible, or manually correct

### Running Agents Locally

```bash
# Before pushing to GitHub
claude-code run-agents --all

# For specific agent
claude-code run-agents --agent security

# With detailed output
claude-code run-agents --verbose

# In CI/CD pipeline
claude-code run-agents --fail-on-error
```

---

## Integration Points

### Git Hooks

Agents can integrate with git hooks:

```bash
# .git/hooks/pre-commit (enabled by default)
claude-code review-code --staged

# .git/hooks/pre-push
claude-code security-scan

# .git/hooks/commit-msg
claude-code validate-commit-message
```

### GitHub Actions (CI/CD)

```yaml
name: Automated Agent Review
on: [pull_request]
jobs:
  agents:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Code Review
        run: claude-code review-code
      
      - name: Security Scan
        run: claude-code security-scan
      
      - name: Test Coverage
        run: claude-code check-coverage --minimum 80
      
      - name: Performance Check
        run: claude-code analyze-performance
```

### Pre-Deployment Checklist

```bash
# Automated deployment checklist
claude-code pre-deploy-check

# Verifies:
# ✅ Security scan passed
# ✅ Test coverage >= 80%
# ✅ No hardcoded secrets
# ✅ Documentation updated
# ✅ Performance acceptable
# ✅ HIPAA compliance verified
```

---

## Troubleshooting

### Agent Not Running

**Problem**: Agent doesn't execute on commit

**Solutions**:
1. Check if agents are enabled: `claude-code config get agents.enabled`
2. Verify git hooks are installed: `ls -la .git/hooks/`
3. Check agent configuration: `claude-code config get agents`
4. Run manually: `claude-code run-agents --verbose`

### False Positives

**Problem**: Agent flags non-issues

**Solution**:
1. Review the agent's findings
2. If incorrect, note the context
3. Update agent rules if needed: `claude-code config set agents.rules.xxxx false`
4. Report false positives to maintain accuracy

### Performance Slow

**Problem**: Agent review takes too long

**Solutions**:
1. Reduce scope: `claude-code review-code app/api/` (instead of full app)
2. Disable non-critical agents: `claude-code config set agents.performance.enabled false`
3. Run agents asynchronously: `claude-code run-agents --async`

### Agent Fails on Large Files

**Problem**: Agent crashes on very large files (>5000 lines)

**Solutions**:
1. Split large files into smaller modules
2. Run agent on specific routes: `claude-code review-code app/api/routes/`
3. Use `--simplified` mode: `claude-code review-code --simplified`

### Conflicting Agent Feedback

**Problem**: Two agents give contradictory advice

**Solution**:
1. Review both findings carefully
2. Prioritize: Security > Performance > Style
3. Use human judgment for final decision
4. Document the decision for future reference

---

## Advanced Configuration

### Custom Agent Rules

Create `.claude/agents/custom.json`:

```json
{
  "rules": {
    "health-data": {
      "pattern": "app/models/models.py",
      "checks": [
        "encryption_required",
        "audit_logging",
        "data_retention"
      ]
    },
    "authentication": {
      "pattern": "app/middleware/auth.py",
      "checks": [
        "no_hardcoded_secrets",
        "token_expiration",
        "rate_limiting"
      ]
    }
  }
}
```

### Agent Plugins

Extend agent capabilities with plugins:

```python
# .claude/agents/plugins/healthcare_compliance.py
class HealthcareCompliancePlugin:
    def __init__(self):
        self.name = "Healthcare Compliance"
        self.version = "1.0"
    
    def check_hipaa_compliance(self, code):
        """Verify HIPAA compliance requirements."""
        # Implementation
        pass
    
    def check_data_encryption(self, code):
        """Verify encryption of health data."""
        # Implementation
        pass
```

---

## Support & Resources

- **Documentation**: See .instructions.md
- **Configuration**: `.claude/settings.json`
- **Examples**: `.claude/agents/examples/`
- **Issues**: Report via GitHub issues
- **Discussion**: Create a GitHub discussion

## Feedback

Have suggestions for improving agents? 
- Submit feedback in Claude Code
- Create an issue with `agent:` label
- Discuss in team channels

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06 | Initial agent configuration |

---

**Last Updated**: 2026-06-09

For questions or more information, see:
- [README.md](README.md) - Project overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guidelines
- [.instructions.md](.instructions.md) - Code patterns and architecture
- [USER_MANUAL.md](USER_MANUAL.md) - User documentation
