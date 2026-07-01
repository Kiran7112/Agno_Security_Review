import re
import json
import time
from typing import Dict, List
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.python import PythonTools
from src.config import settings

# ============================================================================
# SECURITY ANALYSIS TOOLS FOR AGENTS
# ============================================================================

def parse_code_diff(code_diff: str) -> str:
    """Parse code diff to extract additions."""
    lines = code_diff.split('\n')
    additions = [l[1:] for l in lines if l.startswith('+') and not l.startswith('+++')]
    return f"Code additions found:\n{chr(10).join(additions[:30])}"

def detect_sql_injection(code: str) -> str:
    """Check for SQL injection vulnerabilities."""
    if re.search(r'["\']SELECT.*\s\+\s', code, re.IGNORECASE) or \
       re.search(r'query.*\+.*user', code, re.IGNORECASE):
        return "CRITICAL: SQL Injection detected - String concatenation in SQL query"
    return "No SQL injection patterns found"

def detect_hardcoded_secrets(code: str) -> str:
    """Check for hardcoded secrets/credentials."""
    if re.search(r'(api[_-]?key|password|secret|token|auth)\s*=\s*["\'][\w\-\.]{20,}["\']',
                 code, re.IGNORECASE):
        return "HIGH: Hardcoded secret/API key detected in code"
    return "No hardcoded secrets found"

def detect_weak_crypto(code: str) -> str:
    """Check for weak cryptography."""
    if re.search(r'hashlib\.md5|\.md5\(|hashlib\.sha1', code):
        return "MEDIUM: Weak cryptographic algorithm detected (MD5/SHA1)"
    return "No weak crypto patterns found"

def detect_insecure_deserialization(code: str) -> str:
    """Check for insecure deserialization."""
    if re.search(r'eval\(|exec\(|pickle\.loads|pickle\.load', code):
        return "CRITICAL: Insecure deserialization/code execution detected"
    return "No deserialization vulnerabilities found"

def detect_xss(code: str) -> str:
    """Check for XSS vulnerabilities."""
    if re.search(r'innerHTML\s*=|document\.write\(|innerHTML\s*\+=', code):
        return "HIGH: XSS vulnerability detected - unsanitized content in DOM"
    return "No XSS patterns found"

def detect_command_injection(code: str) -> str:
    """Check for command injection."""
    if re.search(r'os\.system\(|subprocess\(|exec\(', code):
        return "CRITICAL: Command injection detected - unsanitized system command"
    return "No command injection patterns found"

def detect_path_traversal(code: str) -> str:
    """Check for path traversal vulnerabilities."""
    if re.search(r'open\(.*\+|file.*\+.*path', code, re.IGNORECASE):
        return "HIGH: Path traversal detected - path constructed from user input"
    return "No path traversal patterns found"

# ============================================================================
# CODE ANALYZER AGENT
# ============================================================================

code_analyzer_agent = Agent(
    name="CodeAnalyzerAgent",
    role="Security Code Analyzer",
    model=OpenAIChat(id="gpt-4", api_key=settings.OPENAI_API_KEY),
    tools=[
        parse_code_diff,
        detect_sql_injection,
        detect_hardcoded_secrets,
        detect_weak_crypto,
        detect_insecure_deserialization,
        detect_xss,
        detect_command_injection,
        detect_path_traversal,
    ],
    instructions="""You are an expert security code reviewer. Your job is to:
1. Parse code diffs to understand changes
2. Use all detection tools to find vulnerabilities
3. Analyze patterns and severity
4. Provide detailed explanations
5. Suggest fixes

When analyzing code:
- Use tools to detect specific vulnerability types
- Consider severity levels: CRITICAL, HIGH, MEDIUM, LOW
- Provide CWE IDs where applicable
- Suggest actionable remediation
- Format responses as structured JSON

Always be thorough and check for multiple vulnerability types.""",
    show_tool_calls=False,
    markdown=False,
)

# ============================================================================
# VULNERABILITY ANALYZER AGENT
# ============================================================================

vulnerability_analyst_agent = Agent(
    name="VulnerabilityAnalystAgent",
    role="Security Vulnerability Analyst",
    model=OpenAIChat(id="gpt-4", api_key=settings.OPENAI_API_KEY),
    instructions="""You are an expert security analyst. Given vulnerability findings:
1. Explain WHY each vulnerability is dangerous
2. Provide realistic attack scenarios
3. Suggest specific fixes with code examples
4. Rate severity (CRITICAL/HIGH/MEDIUM/LOW)
5. Reference CWE/OWASP standards

For each vulnerability:
- Explain the attack vector
- Show impact/consequence
- Provide remediated code
- Link to security standards""",
    show_tool_calls=False,
    markdown=False,
)

# ============================================================================
# SECURITY ANALYZER CLASS
# ============================================================================

class SecurityAnalyzer:
    """Multi-agent security analysis system using Agno framework."""

    def __init__(self):
        self.code_analyzer = code_analyzer_agent
        self.vulnerability_analyst = vulnerability_analyst_agent
        self.model = "gpt-4"

    def parse_code(self, code_diff: str) -> dict:
        """Parse code diff."""
        lines = code_diff.split('\n')
        return {
            "additions": [l[1:] for l in lines if l.startswith('+') and not l.startswith('+++')],
            "deletions": [l[1:] for l in lines if l.startswith('-') and not l.startswith('---')],
            "total_lines": len(lines)
        }

    def analyze(self, code_diff: str) -> dict:
        """
        Multi-stage security analysis using Agno agents.

        Stage 1: Code analysis agent scans for vulnerabilities
        Stage 2: Vulnerability analyst provides detailed analysis
        Stage 3: Recommendations generated
        """
        start_time = time.time()

        # Parse code
        parsed = self.parse_code(code_diff)
        full_code = '\n'.join(parsed["additions"])

        if not full_code.strip():
            return {
                "total_issues": 0,
                "critical": 0,
                "high": 0,
                "medium": 0,
                "findings": [],
                "recommendation": "APPROVE",
                "analysis_time": time.time() - start_time
            }

        # Stage 1: Code Analyzer Agent scans for vulnerabilities
        analysis_prompt = f"""Analyze this code for ALL security vulnerabilities:

Code:
{full_code[:1000]}

Use ALL detection tools to check for:
- SQL Injection
- Hardcoded Secrets
- Weak Cryptography
- Insecure Deserialization
- XSS
- Command Injection
- Path Traversal

Report findings with severity levels."""

        try:
            analyzer_response = self.code_analyzer.run(analysis_prompt)
            analyzer_findings = str(analyzer_response)
        except Exception as e:
            analyzer_findings = f"Analysis error: {str(e)}"

        # Stage 2: Vulnerability Analyst provides detailed analysis
        analyst_prompt = f"""Based on these security findings:

{analyzer_findings}

For each vulnerability found:
1. Explain the security risk
2. Provide attack scenario
3. Suggest fix with code
4. Rate severity (CRITICAL/HIGH/MEDIUM/LOW)
5. Reference CWE ID

Format as JSON array with: type, severity, explanation, attack_scenario, fix, cwe"""

        try:
            analyst_response = self.vulnerability_analyst.run(analyst_prompt)
            findings_text = str(analyst_response)

            # Try to parse JSON from response
            try:
                # Extract JSON from response
                json_match = re.search(r'\[.*\]', findings_text, re.DOTALL)
                if json_match:
                    findings = json.loads(json_match.group())
                else:
                    findings = []
            except:
                findings = []
        except Exception as e:
            findings = []

        # Stage 3: Generate recommendations
        if not findings:
            findings = self._fallback_analysis(full_code)

        analysis_time = time.time() - start_time

        return {
            "total_issues": len(findings),
            "critical": len([f for f in findings if f.get("severity") == "CRITICAL"]),
            "high": len([f for f in findings if f.get("severity") == "HIGH"]),
            "medium": len([f for f in findings if f.get("severity") == "MEDIUM"]),
            "findings": findings,
            "recommendation": "BLOCK" if len([f for f in findings if f.get("severity") in ["CRITICAL", "HIGH"]]) > 0 else "REVIEW",
            "analysis_time": analysis_time
        }

    def _fallback_analysis(self, code: str) -> List[dict]:
        """Fallback pattern-based analysis if agent analysis fails."""
        findings = []

        # SQL Injection
        if re.search(r'["\']SELECT.*\s\+\s', code, re.IGNORECASE):
            findings.append({
                "type": "SQL_INJECTION",
                "severity": "CRITICAL",
                "explanation": "String concatenation in SQL query allows injection",
                "attack_scenario": "Attacker inputs SQL to bypass authentication",
                "fix": "Use parameterized queries/prepared statements",
                "cwe": "CWE-89"
            })

        # Hardcoded Secrets
        if re.search(r'(api[_-]?key|password|secret)\s*=\s*["\'][\w\-\.]{20,}["\']', code, re.IGNORECASE):
            findings.append({
                "type": "HARDCODED_SECRETS",
                "severity": "HIGH",
                "explanation": "Credentials exposed in source code",
                "attack_scenario": "Attacker finds exposed API key in repository",
                "fix": "Use environment variables or secrets manager",
                "cwe": "CWE-798"
            })

        # Weak Crypto
        if re.search(r'hashlib\.md5|\.md5\(', code):
            findings.append({
                "type": "WEAK_CRYPTO",
                "severity": "MEDIUM",
                "explanation": "MD5 is cryptographically broken",
                "attack_scenario": "Attacker cracks MD5 hash via rainbow tables",
                "fix": "Use bcrypt, scrypt, or PBKDF2 for passwords",
                "cwe": "CWE-327"
            })

        return findings

# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

security_analyzer = SecurityAnalyzer()
