# 🤖 Agno Agentic Framework - Security Review System

## What You're Building

**Real autonomous agents** using **Agno framework** that:

✅ **Think independently** - Multi-step reasoning  
✅ **Use tools** - Call functions autonomously  
✅ **Collaborate** - Multiple agents working together  
✅ **Learn context** - Remember analysis history  
✅ **Make decisions** - Autonomous workflow  

---

## System Architecture

```
GitHub PR Created
    ↓
Webhook triggers API
    ↓
CODE ANALYZER AGENT
├─ Tool: parse_code_diff()
├─ Tool: detect_sql_injection()
├─ Tool: detect_hardcoded_secrets()
├─ Tool: detect_weak_crypto()
├─ Tool: detect_xss()
├─ Tool: detect_command_injection()
└─ Analyzes code autonomously
    ↓
VULNERABILITY ANALYST AGENT
├─ Receives findings from Code Analyzer
├─ Deep analysis of each vulnerability
├─ Provides attack scenarios
├─ Suggests fixes
└─ Rates severity
    ↓
Generates Report
    ↓
Posts PR Comment
```

---

## How Agno Agents Work

### **1. Agent Definition**

```python
code_analyzer_agent = Agent(
    name="CodeAnalyzerAgent",
    role="Security Code Analyzer",
    model=OpenAIChat(id="gpt-4"),
    tools=[
        parse_code_diff,
        detect_sql_injection,
        detect_hardcoded_secrets,
        detect_weak_crypto,
        detect_xss,
        detect_command_injection,
        detect_path_traversal,
    ],
    instructions="You are an expert security..."
)
```

### **2. Agent Reasoning Flow**

```
User: "Analyze this code for vulnerabilities"
    ↓
Agent thinks: "I need to parse the code first"
    ↓
Agent calls: parse_code_diff() tool
    ↓
Agent receives: Code additions parsed
    ↓
Agent thinks: "Now I'll check for SQL injection"
    ↓
Agent calls: detect_sql_injection() tool
    ↓
Agent receives: "CRITICAL: SQL Injection detected"
    ↓
Agent thinks: "Let me check other vulnerabilities"
    ↓
Agent calls: detect_hardcoded_secrets() tool
    ↓
... (continues for all vulnerability types)
    ↓
Agent synthesizes: All findings into report
    ↓
Agent returns: Structured analysis
```

### **3. Tool Calling (Autonomous)**

Agents call tools **on their own** - no hard-coded logic!

```python
# Tools the agent can use:
def detect_sql_injection(code: str) -> str:
    """Check for SQL injection vulnerabilities."""
    if re.search(r'["\']SELECT.*\s\+\s', code):
        return "CRITICAL: SQL Injection detected"
    return "No SQL injection patterns found"

# Agent decides WHEN and HOW to use it!
# Developer doesn't control flow - agent does!
```

---

## Multi-Agent System

### **Stage 1: Code Analyzer Agent**

```
Input: Raw code diff
Role: Find vulnerabilities
Tools: 7 different security checks
Output: List of vulnerabilities found
```

### **Stage 2: Vulnerability Analyst Agent**

```
Input: Vulnerabilities from Code Analyzer
Role: Deep analysis
Tasks:
  - Explain security risk
  - Provide attack scenario
  - Suggest fix with code
  - Rate severity
  - Reference CWE
Output: Detailed findings with remediation
```

### **Stage 3: Recommendation**

```
Input: All findings
Decision:
  - CRITICAL or HIGH found? → BLOCK PR
  - MEDIUM or LOW only? → REVIEW
  - No issues? → APPROVE
```

---

## Example: Agno Agent in Action

### **Scenario: PR with SQL Injection**

```python
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    return db.execute(query)
```

### **Code Analyzer Agent Flow:**

```
1. Agent thinks: "I need to analyze code"
2. Calls: parse_code_diff() 
   → Returns: Code parsed
3. Agent thinks: "Let me check each vulnerability"
4. Calls: detect_sql_injection()
   → Returns: "CRITICAL: SQL Injection detected"
5. Calls: detect_hardcoded_secrets()
   → Returns: "No hardcoded secrets found"
6. Calls: detect_weak_crypto()
   → Returns: "No weak crypto patterns found"
... (checks others)
7. Agent thinks: "I found 1 critical issue"
8. Returns: SQL_INJECTION finding
```

### **Vulnerability Analyst Agent Flow:**

```
1. Agent receives: SQL_INJECTION finding
2. Agent thinks: "I need to analyze this deeply"
3. Generates: 
   - Explanation: "String concatenation in SQL query"
   - Attack: "SELECT * FROM users WHERE id = '1' OR '1'='1'"
   - Fix: "Use parameterized: SELECT * FROM users WHERE id = %s"
   - CWE: "CWE-89"
   - Severity: "CRITICAL"
4. Returns: Detailed analysis
```

### **PR Comment Posted:**

```
🚨 SECURITY REVIEW - AGNO AGENTS ANALYSIS

Found 1 Vulnerability:

❌ CRITICAL - SQL_INJECTION
CWE: CWE-89
Confidence: 95%

Why: String concatenation in SQL query allows injection

Attack Scenario:
  Input: ' OR '1'='1
  Result: SELECT * FROM users WHERE id = '' OR '1'='1'
  Impact: Bypasses authentication, dumps database

Fix:
  # ❌ VULNERABLE
  query = "SELECT * FROM users WHERE id = '" + user_id + "'"
  
  # ✅ SECURE
  query = "SELECT * FROM users WHERE id = %s"
  db.execute(query, (user_id,))

✅ Recommendation: BLOCK - Fix before merge
```

---

## Your Agents' Capabilities

### **Agent 1: Code Analyzer**
- **Name:** CodeAnalyzerAgent
- **Role:** Security Code Analyzer
- **Tools:** 8 vulnerability detectors
- **Decision:** "What vulnerabilities exist?"

### **Agent 2: Vulnerability Analyst**
- **Name:** VulnerabilityAnalystAgent
- **Role:** Security Vulnerability Analyst
- **Decision:** "How to fix this? What's the attack? How severe?"

### **Both Use:**
- **Model:** GPT-4 (intelligent reasoning)
- **Framework:** Agno (agent orchestration)
- **Method:** Autonomous tool calling

---

## Key Differences: Agno vs Direct API

### **Without Agno (Direct API)**
```python
# Developer controls EVERYTHING
response = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}]
)
# One call, one response
# No reasoning chains
# No tool autonomy
```

### **With Agno (Framework)**
```python
# Agent controls the workflow
agent.run("Analyze this code")
# Agent decides:
#   1. What to do first
#   2. Which tools to use
#   3. When to use them
#   4. How to combine results
# Multi-step reasoning
# Autonomous decisions
```

---

## Architecture Benefits

| Feature | Agno | Direct API |
|---------|------|-----------|
| **Reasoning** | Multi-step ✅ | Single call ❌ |
| **Tool autonomy** | Autonomous ✅ | Manual ❌ |
| **Workflow** | Flexible ✅ | Rigid ❌ |
| **Reliability** | Higher ✅ | Lower ❌ |
| **Scalability** | Easy ✅ | Hard ❌ |
| **Debuggability** | Clear ✅ | Opaque ❌ |

---

## Installation & Setup

### **Requirements**

```
phi==2.2.0              # Agno framework
phi-core==2.2.0         # Core components
openai==1.3.0           # GPT-4 access
```

### **Environment Variables**

```bash
OPENAI_API_KEY=sk_test_...
GITHUB_TOKEN=ghp_...
WEBHOOK_SECRET=test-secret-123
```

---

## Running Your System

### **1. Local Testing**

```python
from src.agents.security_analyzer import security_analyzer

code_diff = """
+ def get_user(user_id):
+     query = "SELECT * FROM users WHERE id = '" + user_id + "'"
+     return db.execute(query)
"""

result = security_analyzer.analyze(code_diff)
print(result)
```

### **2. Live on Render**

```
GitHub PR → Webhook → API → Agno Agents → Analysis → Comment
```

---

## Example Output

```json
{
  "total_issues": 1,
  "critical": 1,
  "high": 0,
  "medium": 0,
  "findings": [
    {
      "type": "SQL_INJECTION",
      "severity": "CRITICAL",
      "explanation": "String concatenation in SQL query",
      "attack_scenario": "Attacker inputs SQL to bypass authentication",
      "fix": "Use parameterized queries",
      "cwe": "CWE-89"
    }
  ],
  "recommendation": "BLOCK",
  "analysis_time": 2.34
}
```

---

## Deployment on Render

```bash
# 1. Push to GitHub
git add .
git commit -m "Agno agentic security review system"
git push origin main

# 2. On Render
# → New Web Service
# → Select repo
# → Environment: Python
# → Add secrets
# → Deploy!
```

---

## Next: Extend Your System

### **Add More Agents**

```python
# Performance Agent
performance_agent = Agent(
    name="PerformanceAgent",
    role="Performance Analyzer",
    tools=[check_n_plus_one, check_loops, check_recursion],
)

# Compliance Agent
compliance_agent = Agent(
    name="ComplianceAgent",
    role="Compliance Checker",
    tools=[check_gdpr, check_hipaa, check_sox],
)

# All agents work together!
```

### **Add More Tools**

```python
def check_authentication(code: str) -> str:
    """New tool - check auth patterns."""
    ...

# Add to agent
code_analyzer_agent.tools.append(check_authentication)
# Agent automatically learns to use it!
```

---

## Why Agno is Perfect for This

✅ **Autonomous agents** make independent security decisions  
✅ **Tool calling** enables modular vulnerability checks  
✅ **Multi-step reasoning** provides thorough analysis  
✅ **Scalable** - add agents and tools without changing code  
✅ **Production-ready** - enterprise-grade framework  

---

## Your System is Now:

```
✅ Agno Agentic Framework
✅ Multi-agent architecture
✅ Autonomous tool calling
✅ Production-ready
✅ Scalable design
✅ Ready to deploy
```

**This is TRUE AI agent architecture!** 🚀

---

## Deploy Now!

```bash
git push origin main
# Then on Render:
# New Web Service → Select repo → Deploy!
```

**Your Agno-powered security review system is ready!** 🤖
