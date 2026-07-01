# ⚡ Render Quick Start - Deploy in 10 Minutes

## Deploy Your Agno Agent to Render

Using **Agno Framework** for autonomous security analysis + **Render** for fast deployment.

---

## Step 1: Create Render Account (2 minutes)

```
1. Go: https://render.com
2. Sign up with GitHub (easiest!)
3. Authorize GitHub
4. Done!
```

---

## Step 2: Deploy Web Service (5 minutes)

### In Render Dashboard:

```
1. Click "New +" → "Web Service"
2. Select your GitHub repo
3. Click "Connect"
4. Fill in:
   - Name: agno-security-review
   - Environment: Docker
   - Build Command: (leave default)
   - Start Command: (leave default)
5. Click "Deploy"
```

**Wait 3-5 minutes for deployment...**

---

## Step 3: Add Environment Variables (2 minutes)

After deployment starts:

```
1. Go to: Service → Environment
2. Add variables:
   
   GITHUB_TOKEN = your_github_token
   OPENAI_API_KEY = your_openai_key
   WEBHOOK_SECRET = test-secret-123
   ENVIRONMENT = production

3. Click "Save"
```

**Render will redeploy with your variables.**

---

## Step 4: Get Your Service URL (1 minute)

```
Render Dashboard → agno-security-review → Service URL

Example: https://agno-security-review-xxxxx.onrender.com

Copy this URL!
```

---

## Step 5: Add GitHub Webhook (1 minute)

In your GitHub test repo:

```
Settings → Webhooks → Add webhook

Payload URL: https://agno-security-review-xxxxx.onrender.com/api/v1/webhook
Content type: application/json
Secret: test-secret-123
Events: Pull requests
Active: ✓ Yes

Click "Add webhook"
```

---

## Step 6: Test with Your Buggy App (1 minute)

### Create test PR:

```bash
# In your test repo
git checkout -b test/security

# Add buggy code:
def login_user(username, password):
    # BUG 1: SQL Injection
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    
    # BUG 2: Hardcoded Secret
    api_key = "sk_live_abc123xyz789"
    
    # BUG 3: Weak Hash
    import hashlib
    hashed = hashlib.md5(password).hexdigest()
    
    return user

# Push
git add .
git commit -m "Add login function"
git push origin test/security

# Create Pull Request on GitHub
# Wait 30 seconds...
# See Agno comment on PR! ✅
```

---

## What You'll See

### Agno Comment on PR:

```
🚨 SECURITY REVIEW - AGNO ANALYSIS

Found 3 Vulnerabilities:

1. ❌ CRITICAL - SQL_INJECTION
   Why: User input directly in SQL query
   Fix: Use parameterized query
   CWE: CWE-89

2. ⚠️ HIGH - HARDCODED_SECRETS
   Why: API key exposed in code
   Fix: Use environment variables
   CWE: CWE-798

3. 🟡 MEDIUM - WEAK_CRYPTO
   Why: MD5 is broken algorithm
   Fix: Use bcrypt instead
   CWE: CWE-327

✅ Recommendation: BLOCK - Fix before merge
```

---

## ✅ Deployment Checklist

- [ ] Created Render account
- [ ] Connected GitHub repo
- [ ] Deployed web service
- [ ] Added GITHUB_TOKEN
- [ ] Added OPENAI_API_KEY
- [ ] Added WEBHOOK_SECRET
- [ ] Copied Service URL
- [ ] Added GitHub webhook
- [ ] Created test PR
- [ ] Saw Agno comment ✅

---

## Troubleshooting

### Service won't deploy?
```
Check: Render logs → Build log
Look for: Python version, dependencies
Solution: Check requirements.txt is valid
```

### Webhook not triggering?
```
Check: GitHub webhook delivery
  Settings → Webhooks → Click webhook → Deliveries
Look for: 200 status code
If error: Check URL, Secret, Render service is running
```

### No Agno comment on PR?
```
1. Check Render service is "Live" (green dot)
2. Check webhook URL is correct
3. Check secret matches WEBHOOK_SECRET
4. Check GitHub token has repo access
5. Check Render logs for errors
```

### Agno timeout?
```
Render free tier can be slow.
Solution: Upgrade to paid plan ($7/month)
Or: Increase webhook timeout in GitHub settings
```

---

## Why Render?

```
✅ Easy to set up (GitHub integration)
✅ Auto-deploys from GitHub push
✅ Docker support (Python 3.11 guaranteed)
✅ Free tier available
✅ Simple UI
✅ Good for MVP/testing
✅ Faster than previous issues
```

---

## Your Agno Agent is Live! 🎉

Service URL: `https://agno-security-review-xxxxx.onrender.com`

**Features:**
✅ Agno AI agent analyzes code
✅ Multi-step reasoning
✅ Tool autonomy (parse, detect, analyze)
✅ GitHub webhook integration
✅ Real-time PR comments
✅ Security audit logging

---

## Next Steps

1. ✅ Deploy on Render (you're here!)
2. ✅ Test with buggy app
3. ✅ Show your manager
4. 📈 Monitor via /stats endpoint
5. 🚀 Scale if needed

---

## Support

- **Agno Framework:** [AGNO_FRAMEWORK_GUIDE.md](AGNO_FRAMEWORK_GUIDE.md)
- **Full Setup:** [RENDER_SETUP.md](RENDER_SETUP.md)
- **Project Info:** [README.md](README.md)

---

**Ready to deploy?** Go to https://render.com and follow Step 1! 🚀
