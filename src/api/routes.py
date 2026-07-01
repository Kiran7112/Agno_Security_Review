from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.database import get_db
from src.database.crud import AuditCRUD, ComplianceCRUD
from src.services.metrics import MetricsService
from src.services.reporting import ReportingService
from src.api.webhooks import WebhookVerifier
from src.services.analysis import AnalysisService
from src.integrations.github import github_manager

router = APIRouter(prefix="/api/v1", tags=["security"])

@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "agno-security-review"}

@router.post("/webhook")
async def github_webhook(request: Request, db: Session = Depends(get_db)):
    try:
        data = await WebhookVerifier.extract_webhook_data(request)

        if data.get("action") not in ["opened", "synchronize"]:
            return {"status": "skipped", "reason": "not_pr_event"}

        pr_number = data["pull_request"]["number"]
        repo_name = data["repository"]["full_name"]

        pr_info = github_manager.get_pr_info(repo_name, pr_number)
        if not pr_info:
            return {"status": "error", "message": "Could not fetch PR info"}

        pr_info["repo"] = repo_name

        analysis_result = AnalysisService.analyze_pr(pr_info["diff"], pr_info, db)

        comment = ReportingService.format_pr_comment(analysis_result["analysis"])
        github_manager.post_comment(repo_name, pr_number, comment)

        return {
            "status": "success",
            "pr_number": pr_number,
            "issues_found": analysis_result["analysis"]["total_issues"],
            "recommendation": analysis_result["analysis"]["recommendation"]
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/audits")
async def list_audits(db: Session = Depends(get_db), limit: int = 100):
    audits = db.query(__import__("src.database.models", fromlist=["SecurityAudit"]).SecurityAudit).limit(limit).all()

    return [
        {
            "pr_number": a.pr_number,
            "repository": a.repository,
            "developer": a.developer,
            "timestamp": a.timestamp.isoformat(),
            "issues_found": a.vulnerabilities_found,
            "status": a.status
        }
        for a in audits
    ]

@router.get("/audits/{pr_number}")
async def get_audit(pr_number: int, db: Session = Depends(get_db)):
    audit = db.query(__import__("src.database.models", fromlist=["SecurityAudit"]).SecurityAudit).filter(
        __import__("src.database.models", fromlist=["SecurityAudit"]).SecurityAudit.pr_number == pr_number
    ).first()

    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")

    return {
        "pr_number": audit.pr_number,
        "repository": audit.repository,
        "developer": audit.developer,
        "timestamp": audit.timestamp.isoformat(),
        "issues_found": audit.vulnerabilities_found,
        "status": audit.status,
        "findings": audit.findings,
        "analysis_time": audit.analysis_time
    }

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    return MetricsService.get_statistics(db)

@router.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)):
    return {
        "statistics": MetricsService.get_statistics(db),
        "trends": MetricsService.get_trends(db, days=30),
        "vulnerabilities": MetricsService.get_vulnerability_breakdown(db),
        "roi": MetricsService.get_roi_metrics(db)
    }

@router.get("/metrics/developer/{developer_name}")
async def get_developer_metrics(developer_name: str, db: Session = Depends(get_db)):
    return MetricsService.get_developer_metrics(db, developer_name)

@router.get("/metrics/leaderboard")
async def get_leaderboard(db: Session = Depends(get_db)):
    return {"leaderboard": MetricsService.get_team_leaderboard(db)}

@router.get("/compliance")
async def list_compliance_reports(db: Session = Depends(get_db)):
    reports = ComplianceCRUD.get_compliance_reports(db)

    return [
        {
            "standard": r.standard,
            "date": r.date_generated.isoformat(),
            "percentage_compliant": r.percentage_compliant,
            "status": r.status
        }
        for r in reports
    ]

@router.get("/compliance/{standard}")
async def get_compliance_report(standard: str, db: Session = Depends(get_db)):
    report = ComplianceCRUD.get_latest_compliance(db, standard)

    if not report:
        raise HTTPException(status_code=404, detail="Compliance report not found")

    return {
        "standard": report.standard,
        "date": report.date_generated.isoformat(),
        "status": report.status,
        "percentage_compliant": report.percentage_compliant,
        "requirements_met": report.requirements_met,
        "requirements_failed": report.requirements_failed,
        "findings": report.findings
    }

@router.post("/compliance/{standard}/generate")
async def generate_compliance_report(standard: str, db: Session = Depends(get_db)):
    if standard not in ["SOC2", "HIPAA", "GDPR", "PCI-DSS"]:
        raise HTTPException(status_code=400, detail="Invalid compliance standard")

    report_data = ReportingService.generate_compliance_report(db, standard)

    return {
        "status": "generated",
        "standard": standard,
        "report": report_data
    }

@router.get("/reports/daily")
async def get_daily_report(db: Session = Depends(get_db)):
    report_html = ReportingService.generate_daily_report(db, days=1)

    return {
        "type": "daily",
        "date": __import__("datetime", fromlist=["datetime"]).datetime.utcnow().isoformat(),
        "report": report_html
    }
