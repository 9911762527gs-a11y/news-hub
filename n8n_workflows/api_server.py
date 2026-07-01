"""
Simple Flask API Server for News Hub
Allows n8n to call your pipeline via HTTP
"""

from flask import Flask, request, jsonify
import subprocess
import json
import os
import sys

# Add news_hub to path
sys.path.insert(0, '/Users/devil/Desktop/revision/news-hub')

app = Flask(__name__)

@app.route('/api/generate-reel', methods=['POST'])
def generate_reel():
    """Generate a single reel from news data"""
    try:
        data = request.json
        news_title = data.get('title', '')
        news_desc = data.get('description', '')
        
        # Run the news-hub command
        cmd = [
            'python', '-m', 'news_hub.main',
            '--count', '1',
            '--title', news_title,
            '--description', news_desc
        ]
        
        result = subprocess.run(
            cmd,
            cwd='/Users/devil/Desktop/revision/news-hub',
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            # Parse output to find video path
            output = result.stdout
            # Look for "Created scene video:" or similar
            if "output" in output and ".mp4" in output:
                # Extract video path
                lines = output.split('\n')
                for line in lines:
                    if ".mp4" in line and "output" in line:
                        video_path = line.split("output/")[-1].strip()
                        return jsonify({
                            "status": "success",
                            "video_path": f"/Users/devil/Desktop/revision/news-hub/output/{video_path}",
                            "title": news_title,
                            "description": f"{news_desc[:500]}",
                            "caption": f"🎬 {news_title}\n\n#NewsHub #India #OggyAndJack"
                        })
            
            return jsonify({
                "status": "success",
                "message": "Reel generated successfully",
                "title": news_title
            })
        else:
            return jsonify({
                "status": "error",
                "error": result.stderr
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/generate-multiple', methods=['POST'])
def generate_multiple():
    """Generate multiple reels"""
    try:
        data = request.json
        count = data.get('count', 1)
        
        cmd = [
            'python', '-m', 'news_hub.main',
            '--count', str(count)
        ]
        
        result = subprocess.run(
            cmd,
            cwd='/Users/devil/Desktop/revision/news-hub',
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0:
            return jsonify({
                "status": "success",
                "output": result.stdout,
                "count": count
            })
        else:
            return jsonify({
                "status": "error",
                "error": result.stderr
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("News Hub API Server starting on http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)
