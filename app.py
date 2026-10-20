from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app) 

@app.route('/api/get_link', methods=['POST'])
def get_link():
    data = request.json
    url = data.get('url')
    quality = data.get('quality', '720')
    
    try:
        cmd = ["yt-dlp", "-f", f"best[height<={quality}]", "--get-url", url]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        direct_url = result.stdout.strip()
        
        if not direct_url:
            return jsonify({"status": "error", "message": "Link nahi mila"})
            
        return jsonify({"status": "success", "url": direct_url})
    except Exception as e:
        return jsonify({"status": "error", "message": "YouTube ne block kiya ya link galat hai."})

if __name__ == '__main__':
    app.run(port=5000)
