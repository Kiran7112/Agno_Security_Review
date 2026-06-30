import re
import json
import time
from typing import Dict, List
from openai import OpenAI
from src.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class SecurityAnalyzer:
    def __init__(self):
        self.model = "gpt-4"
        self.vulnerabilities = []

    def parse_code(self, code_diff: str) -> dict:
        lines = code_diff.split('\n')
        parsed = {
            "additions": [l[1:] for l in lines if l.startswith('+') and not l.startswith('+++')],
            "deletions": [l[1:] for l in lines if l.startswith('-') and not l.startswith('---')],
            "total_lines": len(lines)
        }
        return parsed

    def detect_patterns(self, code: str) -> List[dict]:
        issues = []

        # SQL Injection
        if re.search(r'["\']SELECT.*\s\+\s', code, re.IGNORECASE) or re.search(r'query.*\+.*user', code, re.IGNORECASE):
            issues.append({
                "type": "SQL_INJECTION",
                "confidence": 0.95,
                "severity": "CRITICAL",
                "pattern": "String concatenation in SQL query"
            })

        # Hardcoded Secrets
        if re.search(r'(api[_-]?key|password|secret|token|auth)\s*=\s*["\'][\w\-\.]{20,}["\']', code, re.IGNORECASE):
            issues.append({
                "type": "HARDCODED_SECRETS",
                "confidence": 0.98,
                "severity": "HIGH",
                "pattern": "Hardcoded credential or API key"
            })

        # Weak Cryptography
        if re.search(r'hashlib\.md5|\.md5\(|hashlib\.sha1', code):
            issues.append({
                "type": "WEAK_CRYPTO",
                "confidence": 0.90,
                "severity": "MEDIUM",
                "pattern": "Using weak cryptographic algorithm"
            })

        # Insecure Deserialization
        if re.search(r'eval\(|exec\(|pickle\.loads|pickle\.load', code):
            issues.append({
                "type": "INSECURE_DESERIALIZATION",
                "confidence": 0.92,
                "severity": "CRITICAL",
                "pattern": "Unsafe deserialization/execution"
            })

        # XSS Vulnerability
        if re.search(r'innerHTML\s*=|document\.write\(|innerHTML\s*\+=', code):
            issues.append({
                "type": "XSS",
                "confidence": 0.85,
                "severity": "HIGH",
                "pattern": "Unsanitized content in DOM"
            })

        # Command Injection
        if re.search(r'os\.system\(|subprocess\(|exec\(', code):
            issues.append({
                "type": "COMMAND_INJECTION",
                "confidence": 0.88,
                "severity": "CRITICAL",
                "pattern": "Unsanitized system command"
            })

        # Path Traversal
        if re.search(r'open\(.*\+|file.*\+.*path', code, re.IGNORECASE):
            issues.append({
                "type": "PATH_TRAVERSAL",
                "confidence": 0.80,
                "severity": "HIGH",
                "pattern": "Path constructed from user input"
            })

        return issues

    def generate_ai_explanation(self, code: str, vulnerability_type: str, pattern: str) -> dict:
        prompt = f"""
Analyze this code for {vulnerability_type} vulnerability:

Pattern detected: {pattern}
Code context:
{code[:500]}

Provide a JSON response with:
{{
    "is_vulnerable": true/false,
    "reason": "why this is vulnerable",
    "attack_scenario": "realistic attack example",
    "fix": "corrected code",
    "explanation": "developer-friendly explanation",
    "cwe": "CWE-ID"
}}

Be concise and accurate. Return valid JSON only.
"""

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=600
            )

            response_text = response.choices[0].message.content
            return json.loads(response_text)
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

        # Filter out false positives
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
