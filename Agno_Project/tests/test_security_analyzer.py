import pytest
from src.agents.security_analyzer import SecurityAnalyzer

@pytest.fixture
def analyzer():
    return SecurityAnalyzer()

def test_sql_injection_detection(analyzer):
    code = 'query = "SELECT * FROM users WHERE id = " + user_input'
    issues = analyzer.detect_patterns(code)
    assert any(issue["type"] == "SQL_INJECTION" for issue in issues)

def test_hardcoded_secret_detection(analyzer):
    code = 'API_KEY = "sk_live_1234567890abcdef"'
    issues = analyzer.detect_patterns(code)
    assert any(issue["type"] == "HARDCODED_SECRETS" for issue in issues)

def test_weak_crypto_detection(analyzer):
    code = 'hashlib.md5(password).hexdigest()'
    issues = analyzer.detect_patterns(code)
    assert any(issue["type"] == "WEAK_CRYPTO" for issue in issues)

def test_xss_detection(analyzer):
    code = 'element.innerHTML = user_input'
    issues = analyzer.detect_patterns(code)
    assert any(issue["type"] == "XSS" for issue in issues)

def test_parse_code_diff(analyzer):
    diff = """
    - old_code = 1
    + new_code = 2
    """
    parsed = analyzer.parse_code(diff)
    assert len(parsed["additions"]) > 0
    assert len(parsed["deletions"]) > 0

def test_safe_code_no_issues(analyzer):
    code = '''
    def safe_function():
        user_input = request.args.get("id")
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_input,))
        return result
    '''
    issues = analyzer.detect_patterns(code)
    assert len(issues) == 0
