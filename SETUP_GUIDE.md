# 🚀 Simple Setup - Agno on Render

## You Already Did This! ✅

```
✅ Code pushed to GitHub
✅ Ready to deploy to Render
✅ Super easy!
```

---

## STEP 1: Create Render Account (2 minutes)

```
1. Go: https://render.com
2. Click "Sign up"
3. Sign up with GitHub (easiest!)
4. Authorize GitHub
5. Done!
```

---

## STEP 2: Deploy on Render (5 minutes)

### Create New Service

```
In Render Dashboard:
1. Click "New +" → "Web Service"
2. Select your GitHub repo (agno-project)
3. Click "Connect"
```

### Configure Service

```
Fill in:
Name: agno-security-review

Environment: Python 3

Build Command: pip install -r requirements.txt

Start Command: python src/main.py

Region: Choose closest to you
```

### Add Environment Variables

```
Click "Environment" tab

Add 3 variables:
1. GITHUB_TOKEN = your_github_token_here
2. OPENAI_API_KEY = your_openai_key_here
3. WEBHOOK_SECRET = test-secret-123

(Render encrypts them automatically!)
```

### Deploy

```
Click "Deploy"

Wait 2-3 minutes...

You see: "Your service is live"

Copy the URL shown
```

---

## STEP 3: Your Public URL

```
Render shows:
https://agno-security-review.onrender.com

This is your API endpoint!
```

---

## STEP 4: Add GitHub Webhook (2 minutes)

### Configure on GitHub

```
Go to your test app GitHub repo:
Settings → Webhooks → Add webhook

Fill in:
  Payload URL: https://agno-security-review.onrender.com/api/v1/webhook
  Content type: application/json
  Secret: test-secret-123
  Events: Pull requests
  Active: ✓ Yes

Click "Add webhook"
```

---

## STEP 5: Test on Your Buggy App (2 minutes)

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

4. Create Pull Request on GitHub

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

✅ Recommendation: Block PR
```

---

## API Keys Are Safe ✅

### How Render Protects Them

```
✅ Environment variables encrypted
✅ Never logged or visible
✅ Only your service can access
✅ Secure by default
```

---

## Simple Configuration

### Render Handles Everything:

```
✅ Python 3.10 installed
✅ Dependencies installed
✅ Database created
✅ SSL/HTTPS enabled
✅ Always running (unless free tier sleeps)
✅ Auto-restart if crashes
✅ Easy scaling
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

## Workflow on Render

```
Your Buggy App (GitHub)
        ↓
Create PR with bugs
        ↓
GitHub webhook triggers
        ↓
Render receives webhook
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

### Issue: Service won't deploy

**Fix:**
```
1. Check GitHub connection is authorized
2. Check requirements.txt is valid
3. Look at Render build logs
4. Check Python version is 3.10+
```

### Issue: No Agno comment on PR

**Fix:**
```
1. Check Render service is running (green "Live")
2. Check webhook URL is correct
3. Check secret matches WEBHOOK_SECRET
4. Check GitHub token has repo access
5. Look at Render logs
```

### Issue: Service keeps sleeping (free tier)

**Upgrade to paid plan:**
```
Render Dashboard → Settings
Click "Upgrade to paid"
($7/month for always-on)
```

---

## Quick Checklist

- [ ] Created Render account
- [ ] Connected GitHub repo
- [ ] Added GITHUB_TOKEN environment variable
- [ ] Added OPENAI_API_KEY environment variable
- [ ] Added WEBHOOK_SECRET environment variable
- [ ] Clicked Deploy
- [ ] Service says "Live"
- [ ] Copied Render URL
- [ ] Added GitHub webhook with URL
- [ ] Created test PR with bugs
- [ ] Saw Agno comment ✅
- [ ] Tested vulnerabilities detected ✅

---

## That's It! ✅

**Super Simple with Render:**

```
1. Create account (2 min)
2. Deploy from GitHub (5 min)
3. Add environment variables (2 min)
4. Add GitHub webhook (2 min)
5. Create test PR (1 min)
6. See results (30 sec)

Total: ~12 minutes!
```

---

## Why Render is Better Than Replit

| Feature | Render | Replit |
|---------|--------|--------|
| **Deploy** | Auto from GitHub | Manual |
| **Speed** | Fast startup | Can be slow |
| **Free tier** | ✅ Yes | ✅ Yes |
| **Always on** | $7/month | Hard to keep on |
| **Performance** | Better | Adequate |
| **Scaling** | Easy | Limited |
| **Production ready** | Yes | No |
| **Logs** | Detailed | Limited |

---

## Render URLs

| Service | URL |
|---------|-----|
| **Render Dashboard** | https://dashboard.render.com |
| **Your Service** | https://agno-security-review.onrender.com |
| **GitHub** | Your test app repo |

---

## Your Project is Live! 🚀

**You have:**
- ✅ Code on GitHub
- ✅ Deployed on Render
- ✅ Public API running 24/7
- ✅ Ready to test

**Next:**
1. Deploy on Render (5 min)
2. Add environment variables (2 min)
3. Test on your buggy app

**Deploy and test NOW!** 🎉
it 