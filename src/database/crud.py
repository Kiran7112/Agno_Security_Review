from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from src.database.models import SecurityAudit, VulnerabilityFinding, TeamMetrics, ComplianceReport, DeveloperStats

class AuditCRUD:
    @staticmethod
    def create_audit(db: Session, audit_data: dict):
        audit = SecurityAudit(**audit_data)
        db.add(audit)
        db.commit()
        db.refresh(audit)
        return audit

    @staticmethod
    def get_audit_by_pr(db: Session, pr_number: int, repository: str):
        return db.query(SecurityAudit).filter(
            SecurityAudit.pr_number == pr_number,
            SecurityAudit.repository == repository
        ).first()

    @staticmethod
    def get_audits_by_date_range(db: Session, start_date: datetime, end_date: datetime):
        return db.query(SecurityAudit).filter(
            SecurityAudit.timestamp >= start_date,
            SecurityAudit.timestamp <= end_date
        ).all()

    @staticmethod
    def get_recent_audits(db: Session, days: int = 7):
        start_date = datetime.utcnow() - timedelta(days=days)
        return AuditCRUD.get_audits_by_date_range(db, start_date, datetime.utcnow())

class MetricsCRUD:
    @staticmethod
    def get_team_metrics(db: Session, team_name: str, days: int = 30):
        start_date = datetime.utcnow() - timedelta(days=days)
        return db.query(TeamMetrics).filter(
            TeamMetrics.team_name == team_name,
            TeamMetrics.date >= start_date
        ).all()

    @staticmethod
    def get_developer_stats(db: Session, developer_name: str):
        return db.query(DeveloperStats).filter(
            DeveloperStats.developer_name == developer_name
        ).first()

    @staticmethod
    def update_developer_stats(db: Session, developer_name: str, stats_data: dict):
        dev_stats = MetricsCRUD.get_developer_stats(db, developer_name)
        if dev_stats:
            for key, value in stats_data.items():
                setattr(dev_stats, key, value)
        else:
            dev_stats = DeveloperStats(developer_name=developer_name, **stats_data)
            db.add(dev_stats)
        db.commit()
        return dev_stats

class ComplianceCRUD:
    @staticmethod
    def create_compliance_report(db: Session, report_data: dict):
        report = ComplianceReport(**report_data)
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def get_compliance_reports(db: Session, standard: str = None):
        query = db.query(ComplianceReport)
        if standard:
            query = query.filter(ComplianceReport.standard == standard)
        return query.order_by(ComplianceReport.date_generated.desc()).all()

    @staticmethod
    def get_latest_compliance(db: Session, standard: str):
        return db.query(ComplianceReport).filter(
            ComplianceReport.standard == standard
        ).order_by(ComplianceReport.date_generated.desc()).first()
