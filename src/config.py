import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your-secret-key")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./security_audit.db")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    OWASP_TOP_10 = {
        "SQL_INJECTION": "CWE-89",
        "XSS": "CWE-79",
        "HARDCODED_SECRETS": "CWE-798",
        "WEAK_CRYPTO": "CWE-327",
        "INSECURE_DESERIALIZATION": "CWE-502",
        "BROKEN_AUTHENTICATION": "CWE-287",
        "SENSITIVE_DATA_EXPOSURE": "CWE-200",
        "COMMAND_INJECTION": "CWE-78",
        "PATH_TRAVERSAL": "CWE-22",
        "ACCESS_CONTROL": "CWE-639"
    }

    COMPLIANCE_STANDARDS = {
        "SOC2": ["encryption", "access_control", "audit_logging"],
        "HIPAA": ["data_protection", "access_control", "audit_logging"],
        "GDPR": ["data_protection", "consent", "privacy"],
        "PCI-DSS": ["network_security", "password_management", "encryption"]
    }

settings = Settings()
