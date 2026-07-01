# 🚀 Render Complete Setup Guide

## Deploy Agno Security Review on Render

Complete guide for deploying your Agno AI agent on Render with GitHub integration.

---

## Prerequisites

✅ GitHub account with your test repo  
✅ OpenAI API key (GPT-4 access)  
✅ GitHub Personal Access Token  
✅ Render account (free)  

---

## Step 1: Prepare Your Repository

### Make sure code is pushed to GitHub:

```bash
git add .
git commit -m "Agno security review system"
git push origin main
```

### Verify files exist:

```bash
ls -la
# Should show:
#   src/              ✓
#   requirements.txt  ✓
#   Dockerfile        ✓
#   render.yaml       ✓
#   runtime.txt       ✓
```

---

## Step 2: Create Render Account

### Go to: https://render.com

```
1. Click "Sign up"
2. Sign up with GitHub (recommended)
3. Authorize GitHub
4. Done!
```

---

## Step 3: Create Web Service on Render

### In Render Dashboard:

```
1. Click "New +" → "Web Service"
2. Select your GitHub repo
3. Authorize if prompted
4. Select your branch (main)
5. Click "Connect"
```

### Configure Service:

```
Name: agno-security-review

Environment: Docker
(Render detects Dockerfile automatically)

Build Command: (leave empty)
Start Command: (leave empty)

Plan: Free (for testing)
       or Paid ($7/month for always-on)

Region: Choose closest to you

Click "Deploy"
```

**Render starts building (3-5 minutes)...**

---

## Step 4: Monitor Deployment

### In Render Dashboard:

```
1. Go to: agno-security-review service
2. Click "Logs"
3. Watch the build process
4. Look for: "Service is live"
```

### Build process:

```
1. Building Docker image
2. Installing Python dependencies
3. Starting uvicorn server
4. Service goes "Live" ✅
```

---

## Step 5: Add Environment Variables

### After "Service is live":

```
1. Go to: agno-security-review
2. Click "Environment"
3. Add variables:

GITHUB_TOKEN
Value: your_github_personal_access_token

OPENAI_API_KEY
Value: your_openai_api_key

WEBHOOK_SECRET
Value: test-secret-123

DATABASE_URL
Value: sqlite:///./security_audit.db

ENVIRONMENT
Value: production

4. Click "Save"
```

**Render redeploys with new variables (1-2 minutes)...**

---

## Step 6: Get Service URL

### In Render Dashboard:

```
agno-security-review → Copy Service URL

Example:
https://agno-security-review-xxxxx.onrender.com
```

---

## Step 7: Configure GitHub Webhook

### In your GitHub test repo:

```
Settings → Webhooks → Add webhook

Fill in:
  Payload URL: https://agno-security-review-xxxxx.onrender.com/api/v1/webhook
  Content type: application/json
  Secret: test-secret-123
  Which events: Pull requests
  Active: ✓ Yes

Click "Add webhook"
```

### Test webhook delivery:

```
Settings → Webhooks → Click webhook name
Scroll to "Recent Deliveries"
Should show green ✓ (successful)
```

---

## Step 8: Test the Deployment

### Create test PR with vulnerabilities:

```bash
# In your test repo
git checkout -b test/security

# Add file: test_vulnerabilities.py
cat > test_vulnerabilities.py << 'EOF'
def get_user(user_id):
    # SQL Injection
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    
def login(username, password):
    # Hardcoded secret
    api_key = "sk_live_1234567890abcdef"
    
    # Weak crypto
    import hashlib
    hash = hashlib.md5(password).hexdigest()
    
    return hash
EOF

# Commit and push
git add test_vulnerabilities.py
git commit -m "Add security test"
git push origin test/security

# Create Pull Request on GitHub
```

### You should see:

```
PR Comment from Agno within 30 seconds:

🚨 SECURITY REVIEW - AGNO ANALYSIS

Found vulnerabilities:
1. SQL_INJECTION - CRITICAL
2. HARDCODED_SECRETS - HIGH  
3. WEAK_CRYPTO - MEDIUM

Recommendation: BLOCK
```

---

## Configuration Files Explained

### `Dockerfile`
```dockerfile
FROM python:3.11-slim
RUN pip install -r requirements.txt
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
**Purpose:** Tells Render how to build and run your app

### `runtime.txt`
```
python-3.11.0
```
**Purpose:** Specifies Python version (3.11 is stable & compatible)

### `render.yaml`
```yaml
services:
  - type: web
    name: agno-security-review
    dockerfilePath: ./Dockerfile
    envVars: [...]
```
**Purpose:** Render configuration (optional, but good to have)

### `requirements.txt`
```
fastapi==0.104.1
uvicorn==0.24.0
openai==1.3.0
agno>=0.1.0
...
```
**Purpose:** Python dependencies Render will install

---

## Deployment Verification

### Check if service is running:

```bash
curl https://agno-security-review-xxxxx.onrender.com/health
# Should return: {"status": "ok"}
```

### Check Render logs:

```
Render Dashboard → agno-security-review → Logs
Look for:
  - No errors
  - "Uvicorn running on 0.0.0.0:8000"
  - Service is receiving requests
```

### Test webhook:

```
GitHub → Settings → Webhooks → Your webhook
Click "Recent Deliveries"
Look for:
  - Status: 200 OK (green ✓)
  - Response: Contains PR comment
```

---

## Troubleshooting

### Issue: Service Build Failed

**Check:**
```
1. Go to: Render → Logs
2. Look for error message
3. Common causes:
   - Python version incompatibility
   - Missing dependency in requirements.txt
   - Syntax error in code
```

**Fix:**
```
1. Fix the issue locally
2. Commit: git push origin main
3. Render auto-redeploys
```

### Issue: Webhook Not Triggering

**Check:**
```
1. GitHub → Settings → Webhooks → Your webhook
2. Click "Recent Deliveries"
3. Look at response (should be 200 OK)
```

**Debug:**
```
If error: 
  - Check Render service is "Live" (green)
  - Check URL is correct
  - Check secret matches
```

### Issue: No Agno Comment on PR

**Check:**
```
1. Render service is running (Status: Live)
2. GitHub token has repo access
3. Webhook is configured correctly
4. Check Render logs for errors
```

**Debug:**
```bash
# Check logs
Render → Logs → Search for "webhook" or "error"

# Test manually
curl -X POST https://agno-security-review-xxxxx.onrender.com/api/v1/webhook \
  -H "Content-Type: application/json" \
  -d '{"action": "opened", "pull_request": {}}'
```

### Issue: Slow Response Time

**Causes:**
```
Free tier Render can be slow due to:
  - Cold starts (needs 10-20 sec)
  - Limited resources
  - Shared infrastructure
```

**Solution:**
```
Upgrade to Paid Plan:
  - Go to: Render → agno-security-review → Settings
  - Click "Upgrade to Paid"
  - $7/month for always-on service
  - Much faster response times
```

### Issue: Service Falls Asleep (Free Tier)

**Render Free Tier Limitation:**
```
Free tier spins down after 15 minutes of inactivity
Next request takes 30-60 seconds to wake up
```

**Solution:**
```
Option 1: Upgrade to paid ($7/month)
Option 2: Use a service to keep it awake
Option 3: Accept slower cold starts
```

---

## Monitoring & Logs

### View Real-time Logs:

```
Render Dashboard → agno-security-review → Logs
Shows live output from your service
```

### Check Service Health:

```bash
# Health check endpoint
curl https://agno-security-review-xxxxx.onrender.com/health

# Get statistics
curl https://agno-security-review-xxxxx.onrender.com/api/v1/stats
```

### Monitor Webhook Deliveries:

```
GitHub → Settings → Webhooks → Your webhook
Click "Recent Deliveries" to see:
  - Request/response
  - Status codes
  - Timing
```

---

## Updating Your Service

### After code changes:

```bash
# Make changes locally
git add .
git commit -m "Update Agno agent logic"
git push origin main

# Render auto-redeploys!
# (No manual steps needed)
```

### Force redeploy:

```
Render Dashboard → agno-security-review → Manual Deploy
Click "Deploy latest commit"
```

---

## Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] GitHub repo connected to Render
- [ ] Web service created
- [ ] Environment variables added
- [ ] Service is "Live"
- [ ] Service URL copied
- [ ] GitHub webhook added
- [ ] Webhook shows 200 status
- [ ] Test PR created
- [ ] Agno comment appeared ✅

---

## Performance Characteristics

| Metric | Free Tier | Paid |
|--------|-----------|------|
| Cold start | 30-60 sec | 2-5 sec |
| Response time | 200-500ms | 50-100ms |
| Uptime | 99% | 99.9% |
| Cost | Free | $7/month |
| Auto-sleep | Yes (15 min) | No |

---

## Cost Analysis

### Free Tier
```
Cost: $0/month
Perfect for: Testing, MVP, low traffic
Downside: Slow cold starts, falls asleep
```

### Paid Tier
```
Cost: $7/month minimum
Perfect for: Production, always-on
Benefit: Always running, fast response
```

### OpenAI Costs
```
100 PRs per month:
  ~100 GPT-4 calls
  ≈ $3-5/month
Total: ~$10-12/month
```

---

## Next Steps

### After Deployment

1. ✅ Deployed on Render
2. ✅ Agno agent analyzing PRs
3. 📊 Monitor statistics at `/stats`
4. 🔄 Create more test PRs
5. 📈 Show your manager!

### Optional Enhancements

- [ ] Set up monitoring/alerts
- [ ] Create compliance reports
- [ ] Add custom vulnerability rules
- [ ] Integrate with Slack
- [ ] Set up daily reports

---

## Support & Resources

| Resource | URL |
|----------|-----|
| Render Docs | https://render.com/docs |
| Render Status | https://status.render.com |
| GitHub Webhooks | https://docs.github.com/en/developers/webhooks-and-events/webhooks |
| Agno Framework | https://www.agno.com/ |

---

## Summary

You now have:

✅ Agno AI agent analyzing code  
✅ Deployed on Render  
✅ GitHub webhook integration  
✅ Real-time security reviews  
✅ Audit logging  

**Your Agno-powered security review system is live!** 🚀
