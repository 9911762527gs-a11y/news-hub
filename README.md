# News Hub - 100% FREE AI-Generated News Reels with Oggy & Jack

**Automatically fetch Indian news, generate funny Hindi dialogue scripts for Oggy & Jack cartoon characters, create animated videos, and upload to social media platforms - ALL FOR FREE!**

✅ **Zero Cost** | ✅ **No Paid APIs** | ✅ **Open Source** | ✅ **Fully Automated**

---

## 🎯 What It Does

1. **📰 Fetches Latest Indian News** (FREE via RSS feeds)
   - Google News (English & Hindi)
   - NDTV, The Hindu, Indian Express, Times of India
   - BBC India, and more
   - Auto-categorizes: Politics, Tech, Sports, Entertainment, Business, etc.

2. **🎭 AI Script Generation** (FREE via Groq or Ollama)
   - **Groq API**: 30,000 tokens/day FREE (Llama 3, Mixtral)
   - **OR Ollama**: Run local AI models (100% offline, completely free)
   - Generates funny **Hindi dialogue** between Oggy & Jack
   - Personalities: Oggy (lazy cat) & Jack (cunning cockroach)

3. **🎥 Video Generation** (FREE)
   - **Edge TTS**: Microsoft's FREE text-to-speech for Hindi voices
   - **MoviePy**: FREE video editing library
   - **9:16 vertical format** (1080x1920) - perfect for all platforms
   - Indian location backgrounds (India Gate, Taj Mahal, etc.)
   - Animated characters with subtitles

4. **📤 Auto-Upload to Social Media** (FREE)
   - **YouTube**: FREE API tier (10,000 units/day)
   - **Twitter/X**: FREE OAuth 1.0a (legacy API)
   - **Instagram**: FREE via Instaloader (unofficial)
   - **Facebook**: FREE Graph API

5. **⏰ Scheduled Execution** (FREE)
   - Runs automatically at configured times
   - Default: 3 reels/day at 8AM, 2PM, 7PM IST

---

## 💰 Cost Breakdown

| Service | Cost | Daily Limit | What You Get |
|---------|------|-------------|--------------|
| Groq API | **$0** | 30,000 tokens | ~50-100 scripts |
| Ollama | **$0** | Unlimited | Local AI, offline |
| Edge TTS | **$0** | Unlimited | Hindi voice generation |
| YouTube API | **$0** | 10,000 units | ~100 uploads |
| Twitter API v1.1 | **$0** | Standard limits | Free uploads |
| Instagram (Instaloader) | **$0** | Rate limited | Free uploads |
| Facebook Graph API | **$0** | Standard limits | Free uploads |
| RSS Feeds | **$0** | Unlimited | News fetching |

**🎉 TOTAL COST: $0 (with free tier limits)**

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Microsoft Edge browser (for TTS)
- Optional: Ollama (if not using Groq)

### Installation

```bash
cd news-hub

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies (all FREE)
pip install -e .

# Copy and configure environment
cp .env.example .env
nano .env  # Edit with your keys
```

### Choose Your FREE AI Option

#### Option A: Groq API (Recommended - 30K tokens/day free)
1. Get FREE API key: https://console.groq.com/
2. Add to `.env`:
   ```
   GROQ_API_KEY=gsk_xxxxx
   USE_OLLAMA=false
   ```

#### Option B: Ollama (100% Local - No API Key)
1. Install Ollama: https://ollama.ai/
2. Pull a model:
   ```bash
   ollama pull llama3:8b-instruct
   # or
   ollama pull mixtral:8x7b-instruct
   ```
3. Add to `.env`:
   ```
   USE_OLLAMA=true
   # No API key needed!
   ```

### Configure Social Media (All FREE)

#### YouTube
1. Create app: https://console.cloud.google.com/
2. Enable YouTube Data API v3
3. Create OAuth credentials
4. Authenticate and get tokens

#### Twitter/X (FREE OAuth 1.0a)
1. Create app: https://developer.twitter.com/
2. Use **Essential Access** (FREE)
3. Get API keys (v1.1 - OAuth 1.0a)

#### Instagram (FREE via Instaloader)
```bash
# Option 1: Login once (saves session)
instaloader --login YOUR_USERNAME

# Option 2: Add to .env
IG_USERNAME=your_username
IG_PASSWORD=your_password
```

#### Facebook (FREE)
1. Create Facebook App: https://developers.facebook.com/
2. Get Page Access Token
3. Add to `.env`:
   ```
   FB_PAGE_ID=your_page_id
   FB_ACCESS_TOKEN=your_access_token
   ```

---

## 📋 Usage

### Generate and Upload Reels

```bash
# Generate 3 reels and upload to all platforms
news-hub

# Generate 5 reels without uploading (test mode)
news-hub --count 5 --no-upload

# Only generate scripts (test AI)
news-hub --skip-video
```

### Run Scheduler (Fully Automated)

```bash
# Auto-runs at configured times (default: 8AM, 2PM, 7PM IST)
news-hub-scheduler
```

### Manual Testing

```python
# Test news fetching
from news_hub.pipeline.news_fetcher import get_top_stories
stories = get_top_stories(count=1)
print(stories[0].title)

# Test script generation
from news_hub.pipeline.script_generator import ScriptGenerator
generator = ScriptGenerator(use_groq=True)
script = generator.generate_script(stories[0], "India Gate Delhi")
print(script)

# Test video generation
from news_hub.pipeline.video_generator import VideoGenerator
vg = VideoGenerator()
reel = vg.generate_reel(script)
print(f"Generated: {reel}")
```

---

## 🎬 Project Structure

```
news-hub/
├── news_hub/
│   ├── __init__.py
│   ├── config/
│   │   ├── settings.py      # Loads .env (FREE APIs only)
│   │   └── characters.py    # Oggy & Jack definitions
│   ├── pipeline/
│   │   ├── news_fetcher.py   # FREE RSS feeds
│   │   ├── script_generator.py # FREE AI (Groq/Ollama)
│   │   ├── video_generator.py # FREE (Edge TTS + MoviePy)
│   │   └── social_uploader.py # FREE uploads
│   ├── main.py               # CLI entry point
│   └── scheduler.py          # Auto-scheduler
├── assets/
│   ├── backgrounds/          # Indian locations
│   ├── characters/           # Oggy & Jack images
│   └── fonts/                # Hindi fonts
├── output/                  # Generated videos
├── .env.example              # FREE API keys template
├── pyproject.toml           # Dependencies (all FREE)
└── README.md
```

---

## 🎭 Characters

### Oggy
- **Type**: Blue cartoon cat (chubby)
- **Personality**: Lazy, loves sleeping, easily angered, naive but kind-hearted
- **Voice**: Hindi male (hi-IN-MadhurNeural) - deep and slow
- **Catchphrase**: "Arre yaar..."

### Jack
- **Type**: Green cartoon cockroach (tall, thin)
- **Personality**: Cunning, intelligent, mischievous, always planning trouble
- **Voice**: Hindi female (hi-IN-SwaraNeural) - fast and sarcastic
- **Catchphrase**: "Oggy, tu toh..."

---

## 📊 Free Tier Limits & Recommendations

| Service | Daily Limit | Recommendation |
|---------|-------------|----------------|
| Groq | 30,000 tokens | ~60 scripts (50 tokens each) |
| YouTube | 10,000 units | ~100 uploads |
| Twitter | Standard | ~100 tweets |
| Instagram | Rate limited | ~50 posts |
| Facebook | Standard | ~100 posts |

**With 3 reels/day:**
- Groq: ~150 tokens/reel = 450 tokens/day (well within 30K limit)
- YouTube: 3 uploads/day = 300 units/month (well within 10K limit)
- **You can easily run 24/7 with 3 reels/day!**

---

## 🔧 Customization

### Add New News Sources
Edit `news_hub/pipeline/news_fetcher.py`:
```python
RSS_FEEDS = {
    "new_source": "https://rss.news-site.com/india",
    ...
}
```

### Add More Indian Locations
Edit `news_hub/config/characters.py`:
```python
LOCATIONS = [
    ...
    "Mumbai Local Train",
    "Himalayas Snow Mountain",
]
```

### Change Voice Settings
Edit `news_hub/config/characters.py`:
```python
OGGY = Character(
    ...
    voice_name="hi-IN-MadhurNeural",
    voice_rate="-10%",  # Slower for lazy Oggy
)
```

### Change Schedule Times
Edit `.env`:
```
REEL_SCHEDULE_TIMES=07:00,12:00,17:00,20:00
```

---

## ⚠️ Important Notes

### Instagram Upload
- **Instaloader** is unofficial and may be rate-limited by Instagram
- For production, consider using **manual upload** or **browser automation**
- Create a **dedicated Instagram account** for this bot

### Twitter/X Upload
- **OAuth 1.0a** (v1.1 API) is still FREE
- **Essential Access** tier is enough for basic uploading
- Rate limits: ~300 tweets/day

### YouTube Upload
- **10,000 units/day** is shared across all YouTube API calls
- Each upload costs ~1,600 units
- You can do ~6 uploads/day on free tier (or use multiple accounts)

### Groq API
- **30,000 tokens/day** is per account
- Llama 3 8B uses ~10-15 tokens per word
- Each script (~200 words) = ~1,500-2,000 tokens
- You can generate ~15-20 scripts/day on free tier

**Solution for higher volume:**
- Use **Ollama** (local) for unlimited script generation
- Use **multiple Groq accounts** if needed
- Use **different YouTube channels** for more uploads

---

## 🛠️ Dependencies (All FREE)

```toml
# All these packages are FREE to install and use
- feedparser      # RSS feed parsing
- requests       # HTTP requests
- python-dotenv  # .env file loading
- edge-tts       # Microsoft Edge TTS (FREE)
- moviepy        # Video editing (FREE)
- pillow         # Image processing (FREE)
- schedule       # Task scheduling (FREE)
- tweepy         # Twitter API (FREE)
- groq           # Groq API client (FREE tier)
- instaloader    # Instagram upload (FREE)
- google-api-python-client  # YouTube API (FREE)
```

---

## 📚 Troubleshooting

### "Groq API key not configured"
- Get FREE key: https://console.groq.com/
- Or use Ollama: `USE_OLLAMA=true`

### "Edge TTS not working"
- Install Microsoft Edge browser
- Or install Edge WebView on Linux

### "YouTube upload failed"
- Check API quota: https://console.cloud.google.com/
- Verify tokens are still valid
- Ensure video is < 15 minutes

### "Instagram upload failed"
- Try: `instaloader --login YOUR_USERNAME` first
- Check if 2FA is enabled (disable for bot account)
- Use a dedicated account for the bot

### "Twitter upload failed"
- Verify OAuth 1.0a keys are correct
- Check if API v1.1 is still accessible
- Try with a different Twitter account

---

## 📜 License

MIT License - Free for personal and commercial use

---

## 🤝 Contributing

Pull requests are welcome! Help improve:
- Better AI prompts
- More Indian news sources
- Better video effects
- More social platforms

---

## 🙏 Support

For issues and questions:
1. Check this README
2. Check the logs in `output/news_hub.log`
3. Open an issue on the repository

---

**Built with ❤️ for the Indian creator community**

**100% FREE. No hidden costs. No subscriptions. Just pure automation.**
