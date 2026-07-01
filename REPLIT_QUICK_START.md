# ⚡ Replit Quick Start (3 Steps Only)

## You're Already Halfway There! ✅

You pushed to GitHub and imported to Replit. Perfect!

---

## Step 1: Add Secrets (2 minutes)

**In Replit:**
```
Left sidebar → Secrets (lock icon)

Add:
1. GITHUB_TOKEN = your_github_token
2. OPENAI_API_KEY = your_openai_key
3. WEBHOOK_SECRET = test-secret
```

---

## Step 2: Run (1 click!)

**In Replit:**
```
Click: RUN button (top)

Wait 30 seconds...

You see:
"Uvicorn running on http://0.0.0.0:8000"

✅ Done!
```

---

## Step 3: Test (5 minutes)

### Get Your URL

```
Replit shows at top:
https://agno-security-xyz.replit.dev
```

### Add GitHub Webhook

```
GitHub repo → Settings → Webhooks → Add

Payload URL: https://agno-security-xyz.replit.dev/api/v1/webhook
Content type: application/json
Secret: test-secret
Events: Pull requests
Active: ✓

Save!
```

### Create Test PR

```
Your test app:
1. Create branch with buggy code
2. Create PR
3. Wait 30 seconds
4. See Agno comment ✅
```

---

## That's It! 🚀

**3 Steps. Done. Running on Replit!**

Your API is live at:
```
https://agno-security-xyz.replit.dev/api/v1/webhook
```

Test your buggy app now! 🎉
