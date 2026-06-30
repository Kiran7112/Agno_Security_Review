# ⚡ Render Quick Start (5 Steps Only)

## Deploy to Render in 10 Minutes!

---

## Step 1: Create Account (2 minutes)

```
1. Go: https://render.com
2. Sign up with GitHub (easiest!)
3. Authorize GitHub
```

---

## Step 2: Deploy (5 minutes)

```
Render Dashboard:

1. Click "New +" → "Web Service"
2. Select your GitHub repo
3. Click "Connect"
4. Fill in:
   - Name: agno-security-review
   - Build Command: pip install -r requirements.txt
   - Start Command: python src/main.py
5. Click "Deploy"

Wait 2-3 minutes...
```

---

## Step 3: Add Secrets (2 minutes)

```
While deploying:

Environment tab → Add:

1. GITHUB_TOKEN = your_token
2. OPENAI_API_KEY = your_key
3. WEBHOOK_SECRET = test-secret

Save!
```

---

## Step 4: Get URL (1 minute)

```
When deployed:
Shows: https://agno-security-review.onrender.com

Copy this URL!
```

---

## Step 5: Test (2 minutes)

```
GitHub repo Settings → Webhooks → Add

Payload URL: https://agno-security-review.onrender.com/api/v1/webhook
Secret: test-secret
Events: Pull requests
Active: ✓

Create test PR → See Agno comment ✅
```

---

## That's It! 🚀

**Live in 10 minutes with Render!**

Better than Replit:
- ✅ Auto-deploys from GitHub
- ✅ Better performance
- ✅ Always on (even free tier)
- ✅ Real production ready
- ✅ No manual clicking Run
