from typing import Dict
from sqlalchemy.orm import Session
from src.agents.security_analyzer import security_analyzer
from src.database.crud import AuditCRUD, MetricsCRUD
from src.database.models import SecurityAudit

class AnalysisService:
    @staticmethod
    def analyze_pr(code_diff: str, pr_info: Dict, db: Session) -> Dict:
        analysis_result = security_analyzer.analyze(code_diff)

        audit_data = {
            "pr_number": pr_info["number"],
            "repository": pr_info["repo"],
            "branch": pr_info["branch"],
            "developer": pr_info["author"],
            "vulnerabilities_found": analysis_result["total_issues"],
            "severity_breakdown": {
                "critical": analysis_result["critical"],
                "high": analysis_result["high"],
                "medium": analysis_result["medium"]
            },
            "findings": analysis_result["findings"],
            "status": analysis_result["recommendation"],
            "analysis_time": analysis_result.get("analysis_time", 0)
        }

        audit = AuditCRUD.create_audit(db, audit_data)

        MetricsCRUD.update_developer_stats(db, pr_info["author"], {
            "prs_submitted": 1,
            "total_vulnerabilities_introduced": analysis_result["total_issues"]
        })

        return {
            "audit_id": audit.id,
            "analysis": analysis_result,
            "audit": audit
        }
