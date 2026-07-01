# News Hub - n8n Automation Workflows

This directory contains workflows and tools to automate your News Hub business using n8n.

## Quick Start

### Option 1: Simple Execute Command Workflow (RECOMMENDED)

**Prerequisites:**
- n8n installed and running at `http://localhost:5678`

**Steps:**
1. Open n8n at `http://localhost:5678`
2. Click **"Import from File"**
3. Select `news-hub-workflow.json` from this directory
4. Click **"Import"**
5. **Activate** the workflow

**That's it!** The workflow will:
- Run at 8AM, 2PM, 7PM IST daily
- Execute your News Hub pipeline
- Generate and upload 1 reel automatically

---

### Option 2: API Server + HTTP Request Workflow

For more advanced control, use the API server approach:

**1. Start API Server:**
```bash
cd /Users/devil/Desktop/revision/news-hub/n8n_workflows
pip install flask
python api_server.py
```

**2. Import Workflow:**
- Import `news-hub-http-workflow.json` (create this separately)
- The workflow will call your API endpoints

---

## Workflow Files

### `news-hub-workflow.json`
- **Trigger:** Cron schedule (8AM, 2PM, 7PM IST)
- **Action:** Executes `news-hub --count 1` command
- **Result:** Auto-generates and uploads 1 reel

### `api_server.py`
- Flask API server on port 8000
- Endpoints:
  - `POST /api/generate-reel` - Generate 1 reel from news data
  - `POST /api/generate-multiple` - Generate multiple reels

---

## Installing n8n

### Method 1: Docker (Recommended)
```bash
# Install Docker Desktop first: https://www.docker.com/products/docker-desktop/
# Then run:
docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n
```

### Method 2: npm
```bash
# Fix permissions first
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) /usr/local/lib/node_modules

# Install n8n
npm install -g n8n --legacy-peer-deps

# Start n8n
n8n start
```

### Method 3: yarn
```bash
npm install -g yarn
yarn global add n8n
n8n start
```

---

## Access n8n

After installation, open your browser to:
**http://localhost:5678**

---

## Troubleshooting

### npm Permission Errors
```bash
# Run these commands
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) /usr/local/lib/node_modules
rm -rf ~/.npm
npm cache clean --force
```

### Docker Not Running
- Make sure Docker Desktop is open and running
- Check for the whale icon in your menu bar

### n8n Not Starting
- Check logs in Terminal
- Try: `n8n start --debug`

---

## Customizing the Workflow

To edit the workflow in n8n:
1. Open n8n at `http://localhost:5678`
2. Click on your workflow
3. Drag nodes to reposition
4. Click on nodes to edit parameters
5. **Save** and **Activate**

---

## Advanced: Social Media Upload Nodes

To add individual social media uploads (instead of using your Python script):

1. **YouTube Upload**
   - Add "YouTube" node
   - Connect after video generation
   - Add your YouTube credentials

2. **Instagram Upload**
   - Add "Instagram" node
   - Use Instaloader credentials

3. **Facebook Upload**
   - Add "Facebook" node
   - Add your Page ID and Access Token

4. **Twitter Upload**
   - Add "Twitter" node
   - Add your API keys

---

## Support

- n8n Documentation: https://docs.n8n.io/
- News Hub Issues: Check `output/news_hub.log`

---

**Enjoy your automated News Hub pipeline!** 🚀
