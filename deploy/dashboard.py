"""
News Hub Business Dashboard
Real-time monitoring, analytics, and control for your AI news reels business
"""

from flask import Flask, render_template_string, jsonify, request
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Project root
PROJECT_ROOT = Path("/app")
OUTPUT_DIR = PROJECT_ROOT / "output"
LOGS_DIR = PROJECT_ROOT / "logs"

# HTML Template (inline for simplicity, no external file needed)
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News Hub Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }
        
        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }
        
        .stat-card h3 {
            color: #667eea;
            font-size: 1.1em;
            margin-bottom: 10px;
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
        }
        
        .stat-label {
            color: #999;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        .controls {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .controls h2 {
            color: #667eea;
            margin-bottom: 20px;
        }
        
        .control-buttons {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
            transform: scale(1.05);
        }
        
        .btn-danger {
            background: #ff4757;
            color: white;
        }
        
        .btn-danger:hover {
            background: #ff3742;
            transform: scale(1.05);
        }
        
        .btn-success {
            background: #2ed573;
            color: white;
        }
        
        .btn-success:hover {
            background: #27ae60;
            transform: scale(1.05);
        }
        
        .recent-activity {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .recent-activity h2 {
            color: #667eea;
            margin-bottom: 20px;
        }
        
        .activity-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .activity-item {
            padding: 15px;
            border-left: 4px solid #667eea;
            margin-bottom: 15px;
            background: #f8f9fa;
            border-radius: 0 8px 8px 0;
        }
        
        .activity-item.success {
            border-left-color: #2ed573;
        }
        
        .activity-item.error {
            border-left-color: #ff4757;
        }
        
        .activity-time {
            color: #999;
            font-size: 0.85em;
        }
        
        .activity-message {
            color: #333;
            margin-top: 5px;
        }
        
        .platform-stats {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .platform-stats h2 {
            color: #667eea;
            margin-bottom: 20px;
        }
        
        .platform-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        
        .platform-card {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .platform-icon {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .platform-name {
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .platform-count {
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #667eea;
            font-size: 1.2em;
        }
        
        .status {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }
        
        .status-online {
            background: #d4edda;
            color: #155724;
        }
        
        .status-offline {
            background: #f8d7da;
            color: #721c24;
        }
        
        @media (max-width: 768px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }
            .control-buttons {
                flex-direction: column;
            }
            .btn {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📰 News Hub Dashboard</h1>
            <p>AI-Generated News Reels with Oggy & Jack | 100% Automated Business</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>📊 Total Reels Generated</h3>
                <div class="stat-value" id="total-reels">0</div>
                <div class="stat-label">All time</div>
            </div>
            <div class="stat-card">
                <h3>🎬 Today's Reels</h3>
                <div class="stat-value" id="today-reels">0</div>
                <div class="stat-label">Last 24 hours</div>
            </div>
            <div class="stat-card">
                <h3>✅ Upload Success Rate</h3>
                <div class="stat-value" id="success-rate">0%</div>
                <div class="stat-label">Last 7 days</div>
            </div>
            <div class="stat-card">
                <h3>💰 Estimated Earnings</h3>
                <div class="stat-value" id="earnings">$0</div>
                <div class="stat-label">This month</div>
            </div>
        </div>
        
        <div class="controls">
            <h2>⚙️ Quick Controls</h2>
            <div class="control-buttons">
                <button class="btn btn-primary" onclick="generateReel()">
                    🎥 Generate 1 Reel Now
                </button>
                <button class="btn btn-primary" onclick="generateMultiple()">
                    🎬 Generate 3 Reels
                </button>
                <button class="btn btn-success" onclick="uploadAll()">
                    📤 Upload Pending
                </button>
                <button class="btn btn-danger" onclick="clearLogs()">
                    🗑️ Clear Old Logs
                </button>
            </div>
        </div>
        
        <div class="platform-stats">
            <h2>📱 Social Media Platforms</h2>
            <div class="platform-grid">
                <div class="platform-card">
                    <div class="platform-icon">📺</div>
                    <div class="platform-name">YouTube</div>
                    <div class="platform-count" id="youtube-count">0</div>
                </div>
                <div class="platform-card">
                    <div class="platform-icon">🐦</div>
                    <div class="platform-name">Twitter/X</div>
                    <div class="platform-count" id="twitter-count">0</div>
                </div>
                <div class="platform-card">
                    <div class="platform-icon">📸</div>
                    <div class="platform-name">Instagram</div>
                    <div class="platform-count" id="instagram-count">0</div>
                </div>
                <div class="platform-card">
                    <div class="platform-icon">👍</div>
                    <div class="platform-name">Facebook</div>
                    <div class="platform-count" id="facebook-count">0</div>
                </div>
            </div>
        </div>
        
        <div class="recent-activity">
            <h2>📜 Recent Activity <span class="status status-online" id="service-status">● LIVE</span></h2>
            <div class="activity-list" id="activity-list">
                <div class="loading">Loading activity...</div>
            </div>
        </div>
    </div>
    
    <script>
        // Auto-refresh data every 30 seconds
        const refreshInterval = 30000;
        
        // Fetch statistics
        async function fetchStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                
                document.getElementById('total-reels').textContent = data.total_reels || 0;
                document.getElementById('today-reels').textContent = data.today_reels || 0;
                document.getElementById('success-rate').textContent = data.success_rate || '0%';
                document.getElementById('earnings').textContent = data.earnings || '$0';
                
                document.getElementById('youtube-count').textContent = data.youtube_uploads || 0;
                document.getElementById('twitter-count').textContent = data.twitter_uploads || 0;
                document.getElementById('instagram-count').textContent = data.instagram_uploads || 0;
                document.getElementById('facebook-count').textContent = data.facebook_uploads || 0;
                
                document.getElementById('service-status').textContent = data.service_online ? '● LIVE' : '● OFFLINE';
                document.getElementById('service-status').className = data.service_online ? 'status status-online' : 'status status-offline';
            } catch (error) {
                console.error('Error fetching stats:', error);
            }
        }
        
        // Fetch activity logs
        async function fetchActivity() {
            try {
                const response = await fetch('/api/activity');
                const activities = await response.json();
                
                const list = document.getElementById('activity-list');
                
                if (activities.length === 0) {
                    list.innerHTML = '<div class="loading">No recent activity</div>';
                    return;
                }
                
                list.innerHTML = activities.slice(0, 20).map(activity => `
                    <div class="activity-item ${activity.success ? 'success' : 'error'}">
                        <div class="activity-time">${activity.time}</div>
                        <div class="activity-message">${activity.message}</div>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Error fetching activity:', error);
            }
        }
        
        // Generate a single reel
        async function generateReel() {
            showLoading('Generating 1 reel...');
            try {
                const response = await fetch('/api/generate?count=1');
                const data = await response.json();
                
                if (data.success) {
                    showNotification('✅ Reel generated successfully!', 'success');
                    fetchStats();
                    fetchActivity();
                } else {
                    showNotification('❌ Error: ' + (data.error || 'Unknown error'), 'error');
                }
            } catch (error) {
                showNotification('❌ Error generating reel', 'error');
            }
            hideLoading();
        }
        
        // Generate multiple reels
        async function generateMultiple() {
            showLoading('Generating 3 reels...');
            try {
                const response = await fetch('/api/generate?count=3');
                const data = await response.json();
                
                if (data.success) {
                    showNotification('✅ 3 reels generated successfully!', 'success');
                    fetchStats();
                    fetchActivity();
                } else {
                    showNotification('❌ Error: ' + (data.error || 'Unknown error'), 'error');
                }
            } catch (error) {
                showNotification('❌ Error generating reels', 'error');
            }
            hideLoading();
        }
        
        // Upload all pending reels
        async function uploadAll() {
            showLoading('Uploading pending reels...');
            try {
                const response = await fetch('/api/upload');
                const data = await response.json();
                
                if (data.success) {
                    showNotification('✅ Upload started! Check logs for progress', 'success');
                    fetchStats();
                    fetchActivity();
                } else {
                    showNotification('❌ Error: ' + (data.error || 'Unknown error'), 'error');
                }
            } catch (error) {
                showNotification('❌ Error uploading reels', 'error');
            }
            hideLoading();
        }
        
        // Clear old logs
        async function clearLogs() {
            if (!confirm('Are you sure you want to clear old logs?')) return;
            
            showLoading('Clearing logs...');
            try {
                const response = await fetch('/api/clear-logs', { method: 'POST' });
                const data = await response.json();
                
                if (data.success) {
                    showNotification('✅ Old logs cleared!', 'success');
                    fetchActivity();
                } else {
                    showNotification('❌ Error: ' + (data.error || 'Unknown error'), 'error');
                }
            } catch (error) {
                showNotification('❌ Error clearing logs', 'error');
            }
            hideLoading();
        }
        
        // Show loading state
        function showLoading(message) {
            const btns = document.querySelectorAll('.btn');
            btns.forEach(btn => {
                btn.disabled = true;
                btn.textContent = message;
            });
        }
        
        // Hide loading state
        function hideLoading() {
            const btns = document.querySelectorAll('.btn');
            btns.forEach(btn => {
                btn.disabled = false;
            });
            document.querySelector('.btn-primary').textContent = '🎥 Generate 1 Reel Now';
            document.querySelectorAll('.btn-primary')[1].textContent = '🎬 Generate 3 Reels';
            document.querySelector('.btn-success').textContent = '📤 Upload Pending';
            document.querySelector('.btn-danger').textContent = '🗑️ Clear Old Logs';
        }
        
        // Show notification
        function showNotification(message, type) {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                padding: 15px 25px;
                background: ${type === 'success' ? '#2ed573' : '#ff4757'};
                color: white;
                border-radius: 8px;
                font-weight: 600;
                z-index: 10000;
                animation: slideIn 0.3s ease;
            `;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }
        
        // Initialize
        fetchStats();
        fetchActivity();
        setInterval(fetchStats, refreshInterval);
        setInterval(fetchActivity, refreshInterval);
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template_string(DASHBOARD_HTML)


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()}), 200


@app.route('/api/stats')
def get_stats():
    """Get business statistics"""
    try:
        # Count generated reels
        reels = list(OUTPUT_DIR.glob("*.mp4"))
        total_reels = len(reels)
        
        # Count today's reels
        today = datetime.now().date()
        today_reels = sum(1 for r in reels if r.stat().st_ctime >= datetime(today.year, today.month, today.day).timestamp())
        
        # Count uploads from logs
        youtube_uploads = count_uploads("YouTube")
        twitter_uploads = count_uploads("Twitter")
        instagram_uploads = count_uploads("Instagram")
        facebook_uploads = count_uploads("Facebook")
        
        total_uploads = youtube_uploads + twitter_uploads + instagram_uploads + facebook_uploads
        total_attempts = total_uploads + count_uploads("failed")
        success_rate = f"{int((total_uploads / max(total_attempts, 1)) * 100)}%" if total_attempts > 0 else "0%"
        
        # Simple earnings estimation (adjust based on your monetization)
        # Assuming $0.01 per view, 1000 views per reel
        earnings = f"${total_reels * 10}"  # Placeholder - adjust with real data
        
        # Check if service is online
        service_online = True
        
        return jsonify({
            "total_reels": total_reels,
            "today_reels": today_reels,
            "success_rate": success_rate,
            "earnings": earnings,
            "youtube_uploads": youtube_uploads,
            "twitter_uploads": twitter_uploads,
            "instagram_uploads": instagram_uploads,
            "facebook_uploads": facebook_uploads,
            "service_online": service_online
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({
            "total_reels": 0,
            "today_reels": 0,
            "success_rate": "0%",
            "earnings": "$0",
            "youtube_uploads": 0,
            "twitter_uploads": 0,
            "instagram_uploads": 0,
            "facebook_uploads": 0,
            "service_online": False
        }), 500


@app.route('/api/activity')
def get_activity():
    """Get recent activity from logs"""
    try:
        log_file = LOGS_DIR / "news_hub.log"
        if not log_file.exists():
            return jsonify([])
        
        activities = []
        with open(log_file, 'r') as f:
            lines = f.readlines()[-100:]  # Last 100 lines
            
            for line in reversed(lines):
                line = line.strip()
                if not line:
                    continue
                
                # Parse log line
                success = "✓" in line or "success" in line.lower() or "generated" in line.lower()
                error = "✗" in line or "error" in line.lower() or "failed" in line.lower()
                
                if success or error:
                    activities.append({
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "message": line[:150],  # Truncate long messages
                        "success": success
                    })
                
                if len(activities) >= 20:
                    break
        
        return jsonify(activities)
    except Exception as e:
        logger.error(f"Error reading activity: {e}")
        return jsonify([]), 500


@app.route('/api/generate')
def generate_reels():
    """Generate reels via subprocess"""
    count = int(request.args.get('count', 1))
    
    try:
        import subprocess
        cmd = ["python", "-m", "news_hub.main", "--count", str(count)]
        
        result = subprocess.run(
            cmd,
            cwd="/app",
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0:
            return jsonify({"success": True, "output": result.stdout})
        else:
            return jsonify({"success": False, "error": result.stderr}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/upload', methods=['POST'])
def upload_reels():
    """Upload pending reels"""
    try:
        import subprocess
        cmd = ["python", "-m", "news_hub.main", "--upload-only"]
        
        result = subprocess.run(
            cmd,
            cwd="/app",
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0:
            return jsonify({"success": True, "output": result.stdout})
        else:
            return jsonify({"success": False, "error": result.stderr}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/clear-logs', methods=['POST'])
def clear_logs():
    """Clear old log files"""
    try:
        # Keep last 7 days of logs
        for log_file in LOGS_DIR.glob("*.log"):
            if (datetime.now() - datetime.fromtimestamp(log_file.stat().st_mtime)).days > 7:
                log_file.unlink()
        
        return jsonify({"success": True, "message": "Old logs cleared"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def count_uploads(platform):
    """Count uploads from log files"""
    count = 0
    log_file = LOGS_DIR / "news_hub.log"
    
    if log_file.exists():
        with open(log_file, 'r') as f:
            for line in f:
                if platform.lower() in line.lower() and ("upload" in line.lower() or "✓" in line):
                    count += 1
    
    return count


if __name__ == '__main__':
    print("=" * 60)
    print("News Hub Dashboard starting...")
    print("=" * 60)
    print(f"Dashboard URL: http://localhost:8000")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Logs directory: {LOGS_DIR}")
    print("=" * 60)
    
    # Create directories if they don't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    app.run(host='0.0.0.0', port=8000, debug=False)
