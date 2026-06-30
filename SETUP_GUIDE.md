# 🚀 Simple Setup - Agno on Replit

## You Already Did This! ✅

```
✅ Code pushed to GitHub
✅ Imported to Replit
✅ You're halfway there!
```

---

## STEP 1: Add Secrets to Replit (2 minutes)

### In Replit Console

```
Left Sidebar → Click "Secrets" (lock icon)

Add 3 secrets:

1. GITHUB_TOKEN
   Value: your_github_token_here

2. OPENAI_API_KEY  
   Value: your_openai_api_key_here

3. WEBHOOK_SECRET
   Value: test-secret-123 (any random string)
```

**That's it! Replit handles everything else.**

---

## STEP 2: Run the Project

### Click "Run" Button

```
In Replit:
1. Top of screen → Click "Run" button
2. Wait 30 seconds...
3. You see: "Uvicorn running on..."
4. Replit gives you a public URL
5. Done! ✅
```

### Your Public URL

```
Replit shows at top:
https://agno-security-xyz.replit.dev

This is your API endpoint!
Copy this URL.
```

---

## STEP 3: Add GitHub Webhook (2 minutes)

### Configure on GitHub

```
1. Go to your test app GitHub repo
2. Settings → Webhooks → Add webhook

Fill in:
  Payload URL: https://agno-security-xyz.replit.dev/api/v1/webhook
  Content type: application/json
  Secret: test-secret-123 (same as WEBHOOK_SECRET)
  Events: Pull requests
  Active: ✓ Yes

Click "Add webhook"
```

---

## STEP 4: Test on Your Buggy App (2 minutes)

### Create Test PR

```
In your test application repo:

1. Create branch:
   git checkout -b test/security

2. Add buggy code:
   
   def login_user(username, password):
       # BUG 1: SQL Injection
       query = "SELECT * FROM users WHERE username = '" + username + "'"
       
       # BUG 2: Hardcoded Secret
       api_key = "sk_live_abc123xyz789"
       
       # BUG 3: Weak Hash
       hashed = hashlib.md5(password).hexdigest()
       
       return user

3. Push:
   git add .
   git commit -m "Add login function"
   git push origin test/security

4. Create Pull Request

5. Wait 30 seconds...

6. See Agno comment on PR! ✅
```

---

## What You'll See

### Agno Comment on PR

```
🚨 SECURITY REVIEW - AGNO ANALYSIS

Found 3 Vulnerabilities:

1. ❌ CRITICAL - SQL Injection (line 3)
   Why: User input directly in SQL query
   Fix: Use parameterized query
   
2. ⚠️ HIGH - Hardcoded Secret (line 6)
   Why: API key exposed in code
   Fix: Use environment variables
   
3. 🟡 MEDIUM - Weak Cryptography (line 9)
   Why: MD5 is broken
   Fix: Use bcrypt instead

✅ Recommendation: Block PR. Fix issues.
```

---

## View Dashboard

### On Replit

```
Replit automatically shows:
- Welcome page at: https://agno-security-xyz.replit.dev

For Dashboard:
1. Click Replit's web preview
2. Or go to: https://agno-security-xyz.replit.dev:8501
3. See live statistics and metrics
```

---

## Simple Configuration

### Replit Already Handles:

```
✅ Python 3.10 installed
✅ Dependencies installed (requirements.txt)
✅ Database created automatically
✅ Public URL provided
✅ HTTPS enabled
✅ Always running
✅ Auto-restart if crashes
```

### You Only Need:

```
1. Add 3 secrets (GITHUB_TOKEN, OPENAI_API_KEY, WEBHOOK_SECRET)
2. Click Run
3. Copy URL
4. Add GitHub webhook
5. Done!
```

---

## API Keys Are Safe ✅

### How Replit Protects Them

```
✅ Secrets stored encrypted
✅ Never shown in code
✅ Never appear in logs
✅ Only accessible to your project
✅ Deleted if you delete the project
```

### Your Code Uses Them Safely

```python
# src/config.py (SAFE)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Reads from Replit secrets, not hardcoded
# API keys stay SAFE ✓
```

---

## Testing Your Buggy App

### Test These Bugs

```python
# Bug 1: SQL Injection
query = "SELECT * FROM users WHERE id = " + user_id
# Agno detects: ✓ CRITICAL

# Bug 2: Hardcoded Secret
api_key = "sk_live_1234567890abc"
# Agno detects: ✓ HIGH

# Bug 3: Weak Hash
hashed = hashlib.md5(password).hexdigest()
# Agno detects: ✓ MEDIUM

# Bug 4: XSS
element.innerHTML = user_input
# Agno detects: ✓ HIGH
```

---

## Workflow on Replit

```
Your Buggy App (GitHub)
        ↓
Create PR with bugs
        ↓
GitHub webhook triggers
        ↓
Replit receives webhook
        ↓
Agno analyzes (30 seconds)
        ↓
Posts comment on PR
        ↓
You see vulnerabilities ✅
        ↓
Fix bugs using Agno suggestions
        ↓
Push fixed code
        ↓
Agno rescans
        ↓
Shows "FIXED" ✅
```

---

## Troubleshooting

### Issue: No Agno comment on PR

**Fix:**
```
1. Check Replit is running (green "Run" status)
2. Check webhook URL is correct
3. Check secret matches WEBHOOK_SECRET
4. Check GitHub token has repo access
5. Check PR is on test app repo
```

### Issue: Replit stopped running

**Fix:**
```
1. Go to Replit
2. Check if there's an error message
3. Click "Run" again
4. Wait 30 seconds
```

### Issue: Dashboard not loading

**Fix:**
```
1. Make sure Replit app is running
2. Try: https://agno-security-xyz.replit.dev:8501
3. Refresh page
```

---

## Quick Checklist

- [ ] Added GITHUB_TOKEN secret in Replit
- [ ] Added OPENAI_API_KEY secret in Replit
- [ ] Added WEBHOOK_SECRET secret in Replit
- [ ] Clicked "Run" button
- [ ] Replit shows public URL
- [ ] Copied Replit URL
- [ ] Added GitHub webhook with URL
- [ ] Created test PR with bugs
- [ ] Saw Agno comment ✅
- [ ] Tested all vulnerabilities

---

## That's It! ✅

**Super Simple with Replit:**

```
1. Add secrets (2 min)
2. Click Run (1 min)
3. Copy URL (1 min)
4. Add webhook (2 min)
5. Create test PR (1 min)
6. See results (30 sec)

Total: ~7 minutes!
```

---

## API Key Safety (Replit Handles It!)

```
✅ Keys stored safely in Replit Secrets
✅ Never in code
✅ Never on GitHub
✅ Encrypted by Replit
✅ Won't expire from deploying
✅ Your setup is SECURE
```

---

## Test Results You'll See

### On GitHub PR

```
Agno comments with:
- Vulnerabilities found
- Severity (CRITICAL/HIGH/MEDIUM)
- Why it's dangerous
- How to fix it
- Recommendation (BLOCK or REVIEW)
```

### On Replit Dashboard

```
- Total reviews
- Vulnerabilities found
- Severity breakdown
- Developer stats
- Security trends
```

---

## Your Project is Live! 🚀

**You have:**
- ✅ Code on GitHub
- ✅ Project on Replit
- ✅ Public API running
- ✅ Ready to test

**Next:**
1. Add 3 secrets to Replit
2. Click Run
3. Test on your buggy app
4. See Agno detect bugs

**Deploy and test NOW!** 🎉
