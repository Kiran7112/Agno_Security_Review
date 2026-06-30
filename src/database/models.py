from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base

class SecurityAudit(Base):
    __tablename__ = "security_audits"

    id = Column(Integer, primary_key=True, index=True)
    pr_number = Column(Integer)
    repository = Column(String)
    branch = Column(String)
    developer = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    vulnerabilities_found = Column(Integer, default=0)
    vulnerabilities_fixed = Column(Integer, default=0)
    severity_breakdown = Column(JSON)
    status = Column(String, default="PENDING")
    findings = Column(JSON)
    ai_response = Column(Text)
    analysis_time = Column(Float)

    findings_rel = relationship("VulnerabilityFinding", back_populates="audit")

class VulnerabilityFinding(Base):
    __tablename__ = "vulnerability_findings"

    id = Column(Integer, primary_key=True, index=True)
    audit_id = Column(Integer, ForeignKey("security_audits.id"))
    vulnerability_type = Column(String, index=True)
    severity = Column(String)
    file_path = Column(String)
    line_number = Column(Integer)
    code_snippet = Column(Text)
    explanation = Column(Text)
    fix_suggestion = Column(Text)
    cwe_id = Column(String)
    confidence = Column(Float)
    fixed = Column(Boolean, default=False)

    audit = relationship("SecurityAudit", back_populates="findings_rel")

class TeamMetrics(Base):
    __tablename__ = "team_metrics"

    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    total_prs_reviewed = Column(Integer)
    total_vulnerabilities = Column(Integer)
    vulnerabilities_fixed = Column(Integer)
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    false_positive_count = Column(Integer, default=0)
    average_fix_time = Column(Float)
    top_vulnerability_type = Column(String)
    developer_count = Column(Integer)

class ComplianceReport(Base):
    __tablename__ = "compliance_reports"

    id = Column(Integer, primary_key=True, index=True)
    standard = Column(String, index=True)
    date_generated = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
    requirements_met = Column(JSON)
    requirements_failed = Column(JSON)
    findings = Column(JSON)
    report_html = Column(Text)
    percentage_compliant = Column(Float)

class DeveloperStats(Base):
    __tablename__ = "developer_stats"

    id = Column(Integer, primary_key=True, index=True)
    developer_name = Column(String, index=True)
    prs_submitted = Column(Integer, default=0)
    total_vulnerabilities_introduced = Column(Integer, default=0)
    vulnerabilities_fixed = Column(Integer, default=0)
    avg_vulnerabilities_per_pr = Column(Float, default=0)
    security_score = Column(Float, default=100)
    last_updated = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=__import__("src.database", fromlist=["engine"]).engine)
