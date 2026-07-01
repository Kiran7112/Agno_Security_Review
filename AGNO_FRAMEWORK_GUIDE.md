# 🤖 Agno AI Framework - Security Review Agent

## What is Agno?

**Agno** (https://www.agno.com/) is an AI agent framework for building autonomous agents with:
- ✅ **Multi-step reasoning** - Agents think through problems step-by-step
- ✅ **Tool calling** - Agents use custom functions as tools
- ✅ **Memory** - Agents remember context and past interactions
- ✅ **State management** - Track agent state and workflow
- ✅ **Autonomous execution** - Agents work independently without constant prompting

---

## Our Architecture

### **What Changed**

Instead of calling OpenAI directly in code, we now use **Agno agents** that:

1. **Define Tools** - Functions agents can call
2. **Create Agent** - Define behavior and instructions
3. **Agent Runs** - Uses multi-step reasoning to analyze security

### **Before (Direct OpenAI)**
```python
# ❌ Old approach
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
```

### **After (Agno Framework)**
```python
# ✅ New approach with Agno
agent = Agent(
    model=OpenAIChat(id="gpt-4"),
    tools=[parse_code, detect_patterns, analyze_details],
    instructions="You are a security expert..."
)
response = agent.run(prompt)
```

---

## Agno Agent Components

### **1. Tools** - Functions the agent can use

```python
def detect_vulnerability_patterns(code: str) -> str:
    """Tool: Detect security patterns in code."""
    issues = []
    if re.search(r'SELECT.*\+', code):
        issues.append("SQL_INJECTION detected")
    return "\n".join(issues)
```

**The agent can call this tool autonomously!**

### **2. Model** - LLM powering the agent

```python
model=OpenAIChat(
    id="gpt-4",
    api_key=settings.OPENAI_API_KEY
)
```

### **3. Instructions** - Agent behavior/role

```python
instructions="""You are an expert security code reviewer.
When analyzing code:
1. Use detect_vulnerability_patterns tool
2. Identify OWASP Top 10 vulnerabilities
3. Provide severity levels
4. Suggest fixes
"""
```

### **4. Agent** - Puts it all together

```python
security_agent = Agent(
    name="SecurityReviewAgent",
    model=model,
    tools=[tool1, tool2, tool3],
    instructions="..."
)
```

---

## How It Works - Security Analysis Flow

### **Step 1: GitHub Webhook Triggered**
```
PR Created on GitHub
    ↓
GitHub sends webhook to our API
    ↓
/api/v1/webhook receives data
```

### **Step 2: Agno Agent Analyzes**
```
Code diff extracted
    ↓
Agent receives prompt: "Analyze this code for vulnerabilities"
    ↓
Agent calls tools:
  1. parse_code()
  2. detect_vulnerability_patterns()
  3. analyze_vulnerability_details()
    ↓
Agent reasons through findings
    ↓
Agent generates JSON response
```

### **Step 3: Results Posted**
```
Vulnerabilities identified
    ↓
Comment formatted
    ↓
Posted to PR
    ↓
Developer sees Agno recommendations
```

---

## Tools Our Agent Uses

### **1. parse_code(code_diff: str) -> str**
- Parses git diff
- Extracts additions/deletions
- Returns formatted code

### **2. detect_vulnerability_patterns(code: str) -> str**
- Regex-based detection
- Finds SQL injection, XSS, secrets, etc.
- Returns list of patterns found

### **3. analyze_vulnerability_details(vulnerability: str, code: str) -> str**
- Deep analysis of specific issue
- Returns detailed information

**The agent decides which tools to use and in what order!**

---

## Agent Decision Making

Agno agents use **reasoning chains**. For security analysis:

```
Agent Reasoning:
1. Receive: "Analyze this code for vulnerabilities"
2. Think: "I should first parse the code"
3. Action: Call parse_code() tool
4. Think: "Now detect patterns"
5. Action: Call detect_vulnerability_patterns() tool
6. Think: "For critical issues, I need details"
7. Action: Call analyze_vulnerability_details() tool
8. Conclude: "Found 3 vulnerabilities, recommending BLOCK"
9. Return: JSON with findings
```

**This is autonomous reasoning - no hardcoded steps!**

---

## Configuration

### `src/agents/security_analyzer.py`

```python
# Define tools
def parse_code(code_diff: str) -> str: ...
def detect_vulnerability_patterns(code: str) -> str: ...
def analyze_vulnerability_details(vulnerability: str, code: str) -> str: ...

# Create Agno agent
security_agent = Agent(
    name="SecurityReviewAgent",
    model=OpenAIChat(id="gpt-4", api_key=OPENAI_API_KEY),
    tools=[parse_code, detect_vulnerability_patterns, analyze_vulnerability_details],
    instructions="..."
)

# Use in SecurityAnalyzer class
class SecurityAnalyzer:
    def __init__(self):
        self.agent = security_agent
    
    def analyze(self, code_diff: str) -> dict:
        # Agent analyzes automatically
        response = self.agent.run(prompt)
```

---

## Advantages of Agno Framework

### **vs. Direct OpenAI Calls**

| Feature | Direct OpenAI | Agno Framework |
|---------|---------------|----------------|
| **Reasoning** | Single prompt/response | Multi-step reasoning |
| **Tool use** | Manual function calls | Autonomous tool selection |
| **State** | Must track manually | Built-in state management |
| **Memory** | Not included | Built-in context memory |
| **Autonomy** | No (step by step) | Yes (agent decides) |
| **Reliability** | Depends on prompt | More robust |
| **Extensibility** | Hardcoded logic | Add tools dynamically |

---

## Example: Agno Agent in Action

### **Scenario: PR with SQL Injection**

**Code submitted:**
```python
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    return db.execute(query)
```

**Agent flow:**
```
1. Agent receives code for security review
2. Agent: "I need to parse and analyze this"
3. Agent calls: parse_code() 
   → Returns formatted code
4. Agent calls: detect_vulnerability_patterns()
   → Returns "SQL_INJECTION: String concatenation"
5. Agent calls: analyze_vulnerability_details()
   → Returns "CRITICAL, CWE-89, Attack: SELECT * FROM users..."
6. Agent reasons: "This is CRITICAL, recommend BLOCK"
7. Agent returns: {
     "type": "SQL_INJECTION",
     "severity": "CRITICAL",
     "recommendation": "BLOCK",
     "fix": "Use parameterized query: db.execute(...)"
   }
```

**Result: PR comment with Agno's analysis**

---

## Extending the Agent

### **Add New Tool**

```python
def check_authentication(code: str) -> str:
    """New tool: Check authentication patterns."""
    if "request.user" not in code:
        return "Missing authentication check"
    return "Authentication check found"

# Add to agent
security_agent = Agent(
    ...
    tools=[parse_code, detect_patterns, analyze_details, check_authentication],
    ...
)
```

**Agent automatically learns to use new tool!**

---

## Integration with FastAPI

### **In `src/api/routes.py`**

```python
from src.agents.security_analyzer import security_analyzer

@router.post("/api/v1/webhook")
async def webhook(payload: dict):
    # Extract code diff from GitHub
    code_diff = get_diff_from_github(payload)
    
    # Use Agno agent to analyze
    result = security_analyzer.analyze(code_diff)
    
    # Format and post comment
    comment = format_pr_comment(result)
    post_github_comment(comment)
```

**Seamless integration!**

---

## Agno Framework Benefits for Security

### **Why Agno is Perfect for Security Review**

1. **Multi-step reasoning**
   - Security requires nuanced analysis
   - Agno agents think through problems
   - Better accuracy than single prompts

2. **Tool autonomy**
   - Agent decides which analysis to run
   - Can combine multiple checks
   - Adapts to code type

3. **Memory**
   - Remember past vulnerabilities
   - Learn from patterns
   - Improve over time

4. **Explainability**
   - Track agent's reasoning steps
   - Know why finding was flagged
   - Better for security audits

5. **Scalability**
   - Handle complex analyses
   - Support multiple PR reviews
   - Parallel agent execution

---

## Deployment (Same as Before)

**Firebase + Google Cloud Run deployment works the same!**

```bash
# Deploy to Cloud Run
gcloud run deploy agno-security-review --source .

# Agent runs on Cloud Run
# GitHub → Webhook → API → Agno Agent → Analysis → PR Comment
```

---

## Next Steps

### **Use the Agno Agent**

1. ✅ Install: Agno framework added to `requirements.txt`
2. ✅ Code: `src/agents/security_analyzer.py` uses Agno
3. ✅ Deploy: Firebase deployment handles it
4. ⏭️ Test: Create PR with bugs, see Agno analyze

### **Extend with More Tools**

```python
# Add tools like:
def check_cwe_database(vuln_type: str) -> str: ...
def suggest_remediation(issue: dict) -> str: ...
def check_compliance(code: str, standard: str) -> str: ...

# Agent will use them automatically!
```

---

## Documentation Files

| File | Purpose |
|------|---------|
| **AGNO_FRAMEWORK_GUIDE.md** | This file - Agno concepts |
| **FIREBASE_QUICK_START.md** | Deploy on Firebase |
| **FIREBASE_SETUP.md** | Complete setup |
| **README.md** | Features and usage |

---

## Agno Resources

- **Website:** https://www.agno.com/
- **GitHub:** https://github.com/agno-ai/agno
- **Docs:** https://docs.agno.com/
- **API Reference:** https://api.agno.com/

---

## Summary

You now have a **real Agno-powered security review system** that:

✅ Uses Agno framework (not custom OpenAI calls)
✅ Has autonomous agents with reasoning
✅ Calls tools independently
✅ Analyzes code intelligently
✅ Deploys on Firebase
✅ Scales automatically

**This is true AI agent architecture!** 🤖
