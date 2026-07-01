import re
import json
import time
from typing import Dict, List
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from src.config import settings

# Define tools for the security analyzer agent
def parse_code(code_diff: str) -> str:
    """Parse code diff into additions and deletions."""
    lines = code_diff.split('\n')
    additions = [l[1:] for l in lines if l.startswith('+') and not l.startswith('+++')]
    return f"Code additions:\n{chr(10).join(additions[:20])}"

def detect_vulnerability_patterns(code: str) -> str:
    """Detect security vulnerability patterns using regex."""
    issues = []

    if re.search(r'["\']SELECT.*\s\+\s', code, re.IGNORECASE):
        issues.append("SQL_INJECTION: String concatenation in SQL query")

    if re.search(r'(api[_-]?key|password|secret|token)\s*=\s*["\'][\w\-\.]{20,}["\']', code, re.IGNORECASE):
        issues.append("HARDCODED_SECRETS: Found hardcoded credential")

    if re.search(r'hashlib\.md5|\.md5\(|hashlib\.sha1', code):
        issues.append("WEAK_CRYPTO: Using weak cryptographic algorithm")

    if re.search(r'eval\(|exec\(|pickle\.loads', code):
        issues.append("INSECURE_DESERIALIZATION: Unsafe deserialization detected")

    if re.search(r'innerHTML\s*=|document\.write\(', code):
        issues.append("XSS: Unsanitized content in DOM")

    if re.search(r'os\.system\(|subprocess\(', code):
        issues.append("COMMAND_INJECTION: Unsanitized system command")

    if re.search(r'open\(.*\+|file.*\+.*path', code, re.IGNORECASE):
        issues.append("PATH_TRAVERSAL: Path constructed from user input")

    return "\n".join(issues) if issues else "No patterns detected"

def analyze_vulnerability_details(vulnerability: str, code_snippet: str) -> str:
    """Provide detailed analysis of a specific vulnerability."""
    return f"Analyzing {vulnerability} in code context: {code_snippet[:100]}..."

# Create the Agno agent for security analysis
security_agent = Agent(
    name="SecurityReviewAgent",
    model=OpenAIChat(
        id="gpt-4",
        api_key=settings.OPENAI_API_KEY
    ),
    tools=[parse_code, detect_vulnerability_patterns, analyze_vulnerability_details],
    instructions="""You are an expert security code reviewer. Your job is to:
1. Analyze code for security vulnerabilities
2. Identify OWASP Top 10 vulnerabilities
3. Provide severity levels (CRITICAL, HIGH, MEDIUM, LOW)
4. Suggest fixes
5. Explain attack scenarios

When analyzing code:
- Use detect_vulnerability_patterns to find issues
- Provide specific line numbers and code contexts
- Give actionable remediation advice
- Assign CWE IDs where applicable

Always respond with valid JSON containing: type, severity, confidence, explanation, attack_scenario, fix, cwe""",
    markdown=False
)

class SecurityAnalyzer:
    def __init__(self):
        self.agent = security_agent
        self.model = "gpt-4"

    def parse_code(self, code_diff: str) -> dict:
        lines = code_diff.split('\n')
        parsed = {
            "additions": [l[1:] for l in lines if l.startswith('+') and not l.startswith('+++')],
            "deletions": [l[1:] for l in lines if l.startswith('-') and not l.startswith('---')],
            "total_lines": len(lines)
        }
        return parsed

    def detect_patterns(self, code: str) -> List[dict]:
        """Use Agno agent to detect patterns."""
        issues = []

        if re.search(r'["\']SELECT.*\s\+\s', code, re.IGNORECASE):
            issues.append({
                "type": "SQL_INJECTION",
                "confidence": 0.95,
                "severity": "CRITICAL",
                "pattern": "String concatenation in SQL query"
            })

        if re.search(r'(api[_-]?key|password|secret|token)\s*=\s*["\'][\w\-\.]{20,}["\']', code, re.IGNORECASE):
            issues.append({
                "type": "HARDCODED_SECRETS",
                "confidence": 0.98,
                "severity": "HIGH",
                "pattern": "Hardcoded credential"
            })

        if re.search(r'hashlib\.md5|\.md5\(|hashlib\.sha1', code):
            issues.append({
                "type": "WEAK_CRYPTO",
                "confidence": 0.90,
                "severity": "MEDIUM",
                "pattern": "Weak cryptography"
            })

        if re.search(r'eval\(|exec\(|pickle\.loads|pickle\.load', code):
            issues.append({
                "type": "INSECURE_DESERIALIZATION",
                "confidence": 0.92,
                "severity": "CRITICAL",
                "pattern": "Unsafe deserialization"
            })

        if re.search(r'innerHTML\s*=|document\.write\(|innerHTML\s*\+=', code):
            issues.append({
                "type": "XSS",
                "confidence": 0.85,
                "severity": "HIGH",
                "pattern": "XSS vulnerability"
            })

        if re.search(r'os\.system\(|subprocess\(|exec\(', code):
            issues.append({
                "type": "COMMAND_INJECTION",
                "confidence": 0.88,
                "severity": "CRITICAL",
                "pattern": "Command injection"
            })

        if re.search(r'open\(.*\+|file.*\+.*path', code, re.IGNORECASE):
            issues.append({
                "type": "PATH_TRAVERSAL",
                "confidence": 0.80,
                "severity": "HIGH",
                "pattern": "Path traversal"
            })

        return issues

    def generate_ai_explanation(self, code: str, vulnerability_type: str, pattern: str) -> dict:
        """Use Agno agent to generate detailed explanation."""
        prompt = f"""Analyze this {vulnerability_type} vulnerability:
Pattern: {pattern}
Code: {code[:300]}

Return JSON: {{"is_vulnerable": bool, "reason": str, "attack_scenario": str, "fix": str, "explanation": str, "cwe": str}}"""

        try:
            response = self.agent.run(prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)

            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                return {
                    "is_vulnerable": True,
                    "reason": f"Agno analysis: {response_text[:100]}",
                    "attack_scenario": "Potential attack vector exists",
                    "fix": "Review and remediate",
                    "explanation": response_text,
                    "cwe": "CWE-Unknown"
                }
        except Exception as e:
            return {
                "is_vulnerable": True,
                "reason": "Analysis error",
                "attack_scenario": "See pattern",
                "fix": "Review context",
                "explanation": str(e),
                "cwe": "CWE-Unknown"
            }

    def analyze(self, code_diff: str) -> dict:
        """Analyze code using Agno agent."""
        start_time = time.time()

        parsed = self.parse_code(code_diff)
        full_code = '\n'.join(parsed["additions"])

        pattern_issues = self.detect_patterns(full_code)

        findings = []
        for issue in pattern_issues:
            ai_explanation = self.generate_ai_explanation(
                full_code,
                issue["type"],
                issue["pattern"]
            )

            findings.append({
                "type": issue["type"],
                "severity": issue["severity"],
                "confidence": issue["confidence"],
                "explanation": ai_explanation.get("explanation", ""),
                "attack_scenario": ai_explanation.get("attack_scenario", ""),
                "fix": ai_explanation.get("fix", ""),
                "cwe": ai_explanation.get("cwe", ""),
                "is_vulnerable": ai_explanation.get("is_vulnerable", True),
                "reason": ai_explanation.get("reason", "")
            })

        findings = [f for f in findings if f.get("is_vulnerable", True)]

        analysis_time = time.time() - start_time

        return {
            "total_issues": len(findings),
            "critical": len([f for f in findings if f["severity"] == "CRITICAL"]),
            "high": len([f for f in findings if f["severity"] == "HIGH"]),
            "medium": len([f for f in findings if f["severity"] == "MEDIUM"]),
            "findings": findings,
            "recommendation": "BLOCK" if len([f for f in findings if f["severity"] in ["CRITICAL", "HIGH"]]) > 0 else "REVIEW",
            "analysis_time": analysis_time
        }

security_analyzer = SecurityAnalyzer()
