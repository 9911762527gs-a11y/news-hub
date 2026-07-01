# News Hub - Railway Deployment Guide

## 🚀 Deploy Your AI News Reels Business to Railway in 5 Minutes

This guide will help you deploy your News Hub project to Railway.app for 24/7 automated reel generation and posting.

---

## ⚙️ Prerequisites

1. **Railway Account** - Sign up at [https://railway.app](https://railway.app) (FREE tier available)
2. **GitHub Account** - To connect your repository
3. **All your API keys** from .env file

---

## 📋 Step 1: Prepare Your Project

### 1.1 Push to GitHub (if not already)

```bash
cd /Users/devil/Desktop/revision/news-hub

# Initialize git if not already
git init
git add .
git commit -m "Initial commit - News Hub project"

# Create a new repository on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/news-hub.git
git branch -M main
git push -u origin main
```

### 1.2 Create .dockerignore file

```bash
cat > /Users/devil/Desktop/revision/news-hub/.dockerignore << 'EOF'
# Python
__pycache__
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs and output
output/
logs/
*.mp4
*.log

# Environment
.env
.env.local
.env.*.local
EOF
```

---

## 🚂 Step 2: Deploy to Railway

### Method A: Deploy from GitHub (RECOMMENDED)

1. **Go to Railway Dashboard**: [https://railway.app/dashboard](https://railway.app/dashboard)
2. **Click "New Project"** → "Deploy from GitHub repo"
3. **Select your news-hub repository**
4. **Configure variables** (see Step 3 below)
5. **Deploy!**

### Method B: Deploy via CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create new project
railway init

# Deploy
railway up
```

---

## 🔐 Step 3: Configure Environment Variables

In Railway Dashboard → Your Project → Variables tab, add these:

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key for AI script generation | `gsk_xxxxxxxxxxxxx` |
| `USE_OLLAMA` | Set to "true" if using Ollama (local AI) | `false` or `true` |
| `YOUTUBE_CLIENT_ID` | YouTube API Client ID | From Google Cloud Console |
| `YOUTUBE_CLIENT_SECRET` | YouTube API Client Secret | From Google Cloud Console |
| `YOUTUBE_ACCESS_TOKEN` | YouTube OAuth Access Token | From OAuth flow |
| `YOUTUBE_REFRESH_TOKEN` | YouTube OAuth Refresh Token | From OAuth flow |
| `TWITTER_API_KEY` | Twitter API Key (v1.1) | From Twitter Developer |
| `TWITTER_API_SECRET` | Twitter API Secret | From Twitter Developer |
| `TWITTER_ACCESS_TOKEN` | Twitter Access Token | From Twitter Developer |
| `TWITTER_ACCESS_TOKEN_SECRET` | Twitter Access Token Secret | From Twitter Developer |
| `INSTAGRAM_USERNAME` | Your Instagram username | `your_instagram` |
| `INSTAGRAM_PASSWORD` | Your Instagram password | `********` |
| `FACEBOOK_PAGE_ID` | Your Facebook Page ID | `1234567890` |
| `FACEBOOK_ACCESS_TOKEN` | Facebook Page Access Token | `EA...` |

### Optional Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `REELS_PER_DAY` | Number of reels to generate daily | `3` |
| `REEL_SCHEDULE_TIMES` | Times to generate reels (IST) | `08:00,14:00,19:00` |
| `TIMEZONE` | Timezone for scheduler | `Asia/Kolkata` |
| `LOG_LEVEL` | Logging level | `INFO` |

---

## 🎚️ Step 4: Set Up Services

Your Railway project will have **2 services**:

### Service 1: Scheduler (Worker)
- **Name**: `news-hub-scheduler`
- **Type**: Worker
- **Command**: `python -m news_hub.scheduler`
- **Always On**: ✅ Enable (for 24/7 operation)

### Service 2: Dashboard (Web)
- **Name**: `news-hub-api`
- **Type**: Web
- **Command**: `python deploy/dashboard.py`
- **Port**: `8000`
- **Always On**: ✅ Enable

---

## ⏰ Step 5: Configure Cron Jobs (Optional)

In Railway Dashboard → Triggers → Cron:

Add these cron jobs for automatic posting:

| Name | Schedule | Command |
|------|----------|---------|
| Morning Reel | `0 8 * * *` | `python -m news_hub.main --count 1` |
| Afternoon Reel | `0 14 * * *` | `python -m news_hub.main --count 1` |
| Evening Reel | `0 19 * * *` | `python -m news_hub.main --count 1` |

Note: Times are in UTC. Adjust for IST (UTC+5:30):
- 8:00 IST = 2:30 UTC
- 14:00 IST = 8:30 UTC
- 19:00 IST = 13:30 UTC

So use:
- `30 2 * * *` for 8:00 IST
- `30 8 * * *` for 14:00 IST
- `30 13 * * *` for 19:00 IST

---

## 📊 Step 6: Access Your Dashboard

After deployment:

1. **Scheduler Service**: Runs automatically, generating and uploading reels
2. **Dashboard**: Access at the URL provided by Railway (usually `https://news-hub-api.up.railway.app/`)

### Dashboard Features:
- 📈 Real-time statistics (total reels, today's reels, success rate)
- 📱 Platform upload counts (YouTube, Twitter, Instagram, Facebook)
- 🎬 Quick controls (generate reels, upload pending)
- 📜 Recent activity logs
- 💰 Estimated earnings tracker
- ✅ Service status monitoring

---

## 🔄 Step 7: Monitor and Maintain

### Check Logs
```bash
# In Railway CLI
railway logs

# Or in Dashboard
# Go to your project → Logs tab
```

### Scale Up (if needed)
- Increase CPU/Memory in Railway settings
- Add more cron jobs for more frequent posting
- Use multiple Groq accounts for higher AI limits

### Backup
- Railway automatically persists `output/` and `logs/` directories
- Download important files regularly

---

## ⚠️ Troubleshooting

### Common Issues

1. **Edge TTS not working**
   - Make sure Microsoft Edge is installed in the container
   - Check Dockerfile has Edge installation

2. **YouTube upload failing**
   - Verify OAuth tokens are valid
   - Check YouTube API quota
   - Ensure video is < 15 minutes

3. **Instagram upload failing**
   - Use a dedicated account for the bot
   - Disable 2FA on the bot account
   - Login once manually with Instaloader

4. **Dashboard not loading**
   - Check Flask is installed (`pip install flask`)
   - Verify port 8000 is exposed
   - Check Railway web service is running

5. **Scheduler not running**
   - Enable "Always On" for the worker service
   - Check Railway has enough credits (FREE tier available)

---

## 📈 Step 8: Optimize Your Business

### Increase Reach
- Add more news sources in `news_hub/pipeline/news_fetcher.py`
- Customize Oggy & Jack personalities
- Add trending hashtags
- Optimize video thumbnails

### Monetization Tips
- Enable YouTube monetization after 1K subscribers
- Use affiliate links in descriptions
- Sponsor specific news topics
- Offer custom reel creation services

### Scale Up
- Deploy multiple instances for different niches
- Use Ollama for unlimited AI generation (no API costs)
- Add more social media platforms
- Create a content calendar

---

## 🎯 Success Metrics to Track

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Daily Reels | 3-5 | Dashboard stats |
| Upload Success Rate | >95% | Dashboard success rate |
| YouTube Views | 100+/reel | YouTube Analytics |
| Instagram Reach | 500+/reel | Instagram Insights |
| Total Followers | 10K+ | Social media dashboards |
| Monthly Earnings | $100+ | Ad revenue + sponsors |

---

## 📞 Support

- **Railway Docs**: [https://docs.railway.app](https://docs.railway.app)
- **News Hub Issues**: Check `output/news_hub.log`
- **Contact**: For deployment help, open an issue on your repository

---

## 🎉 You're Live!

Your News Hub business is now fully automated and running 24/7 on Railway!

✅ **Fully Automated** - Reels generated and posted automatically
✅ **Business Dashboard** - Monitor everything in real-time  
✅ **Scalable** - Easy to add more platforms and features
✅ **Cost Effective** - Uses FREE tiers of all services

**Next Steps:**
1. Share your dashboard URL with your team
2. Set up notifications for failures
3. Start promoting your content
4. Track your growth and optimize

---

*Built with love for the Indian creator community*
