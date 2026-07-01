import os
from dotenv import load_dotenv

load_dotenv()


def _env(name: str, default: str | None = None) -> str | None:
    """Read an env var and sanitize common copy/paste mistakes.

    Strips surrounding whitespace/quotes and a stray leading ``Value:`` or
    ``Key:`` label (which happens when the label is accidentally pasted into
    a hosting dashboard's value box). Falls back to ``default`` when unset
    or blank after cleaning.
    """
    raw = os.getenv(name)
    if raw is None:
        return default
    cleaned = raw.strip().strip('"').strip("'").strip()
    low = cleaned.lower()
    for prefix in ("value:", "key:"):
        if low.startswith(prefix):
            cleaned = cleaned[len(prefix):].strip().strip('"').strip("'").strip()
            break
    return cleaned or default


class Settings:
    GITHUB_TOKEN = _env("GITHUB_TOKEN")
    OPENAI_API_KEY = _env("OPENAI_API_KEY")
    WEBHOOK_SECRET = _env("WEBHOOK_SECRET", "your-secret-key")
    DATABASE_URL = _env("DATABASE_URL", "sqlite:///./security_audit.db")
    ENVIRONMENT = _env("ENVIRONMENT", "development")
    DEBUG = (_env("DEBUG", "false") or "false").lower() == "true"

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
