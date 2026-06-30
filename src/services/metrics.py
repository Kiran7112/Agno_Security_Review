from typing import Dict, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.database.models import SecurityAudit, DeveloperStats, TeamMetrics

class MetricsService:
    @staticmethod
    def get_statistics(db: Session) -> Dict:
        audits = db.query(SecurityAudit).all()

        total_issues = sum(a.vulnerabilities_found for a in audits)
        critical = sum(a.severity_breakdown.get("critical", 0) for a in audits)
        high = sum(a.severity_breakdown.get("high", 0) for a in audits)
        medium = sum(a.severity_breakdown.get("medium", 0) for a in audits)

        return {
            "total_reviews": len(audits),
            "total_issues": total_issues,
            "critical": critical,
            "high": high,
            "medium": medium,
            "average_issues_per_pr": total_issues / len(audits) if audits else 0,
            "blocked_prs": len([a for a in audits if a.status == "BLOCKED"]),
            "approved_prs": len([a for a in audits if a.status == "APPROVED"])
        }

    @staticmethod
    def get_developer_metrics(db: Session, developer_name: str) -> Dict:
        audits = db.query(SecurityAudit).filter(
            SecurityAudit.developer == developer_name
        ).all()

        total_issues = sum(a.vulnerabilities_found for a in audits)

        return {
            "developer": developer_name,
            "prs_submitted": len(audits),
            "total_vulnerabilities": total_issues,
            "average_per_pr": total_issues / len(audits) if audits else 0,
            "critical_count": sum(a.severity_breakdown.get("critical", 0) for a in audits),
            "high_count": sum(a.severity_breakdown.get("high", 0) for a in audits),
            "medium_count": sum(a.severity_breakdown.get("medium", 0) for a in audits),
            "security_score": 100 - min(total_issues * 5, 50)  # Simple scoring
        }

    @staticmethod
    def get_trends(db: Session, days: int = 30) -> Dict:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        audits = db.query(SecurityAudit).filter(
            SecurityAudit.timestamp >= start_date,
            SecurityAudit.timestamp <= end_date
        ).all()

        daily_data = {}
        for audit in audits:
            date_key = audit.timestamp.strftime("%Y-%m-%d")
            if date_key not in daily_data:
                daily_data[date_key] = {
                    "reviews": 0,
                    "issues": 0,
                    "critical": 0,
                    "high": 0,
                    "medium": 0
                }

            daily_data[date_key]["reviews"] += 1
            daily_data[date_key]["issues"] += audit.vulnerabilities_found
            daily_data[date_key]["critical"] += audit.severity_breakdown.get("critical", 0)
            daily_data[date_key]["high"] += audit.severity_breakdown.get("high", 0)
            daily_data[date_key]["medium"] += audit.severity_breakdown.get("medium", 0)

        return {
            "period_days": days,
            "daily_data": daily_data,
            "trend": "improving" if len(audits) > 0 else "no_data"
        }

    @staticmethod
    def get_vulnerability_breakdown(db: Session) -> Dict:
        audits = db.query(SecurityAudit).all()

        breakdown = {}
        for audit in audits:
            for finding in audit.findings or []:
                vuln_type = finding.get("type", "Unknown")
                if vuln_type not in breakdown:
                    breakdown[vuln_type] = 0
                breakdown[vuln_type] += 1

        return {
            "vulnerability_types": breakdown,
            "total_unique_types": len(breakdown),
            "most_common": max(breakdown.items(), key=lambda x: x[1])[0] if breakdown else "N/A"
        }

    @staticmethod
    def get_team_leaderboard(db: Session) -> List[Dict]:
        developers = db.query(DeveloperStats).order_by(
            DeveloperStats.security_score.desc()
        ).all()

        leaderboard = []
        for i, dev in enumerate(developers, 1):
            leaderboard.append({
                "rank": i,
                "developer": dev.developer_name,
                "security_score": dev.security_score,
                "prs_submitted": dev.prs_submitted,
                "vulnerabilities": dev.total_vulnerabilities_introduced,
                "avg_per_pr": dev.avg_vulnerabilities_per_pr
            })

        return leaderboard

    @staticmethod
    def get_roi_metrics(db: Session) -> Dict:
        audits = db.query(SecurityAudit).all()

        total_time_saved = sum(a.analysis_time for a in audits) / 3600  # Convert to hours
        developer_hourly_rate = 150
        money_saved = total_time_saved * developer_hourly_rate

        return {
            "total_reviews": len(audits),
            "total_analysis_hours": total_time_saved,
            "developer_hourly_rate": developer_hourly_rate,
            "estimated_savings": money_saved,
            "annual_projection": money_saved * 12 if len(audits) > 0 else 0,
            "vulnerabilities_prevented": len([a for a in audits if a.status == "BLOCKED"])
        }
