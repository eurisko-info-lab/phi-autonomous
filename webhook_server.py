#!/usr/bin/env python3
"""
GitHub Webhook → Twitter Bot
Receives push events from eurisko-info-lab org and tweets them.
"""

from flask import Flask, request, jsonify
import tweepy
import os
import hmac
import hashlib
from pathlib import Path

app = Flask(__name__)

def load_env():
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value.strip('"\'')

load_env()

def get_twitter_client():
    return tweepy.Client(
        consumer_key=os.environ.get('TWITTER_API_KEY'),
        consumer_secret=os.environ.get('TWITTER_API_SECRET'),
        access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.environ.get('TWITTER_ACCESS_SECRET')
    )

def verify_signature(payload, signature):
    secret = os.environ.get('GITHUB_WEBHOOK_SECRET', '').encode()
    if not secret:
        return True  # No secret configured, skip verification
    expected = 'sha256=' + hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)

@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    # Verify signature
    signature = request.headers.get('X-Hub-Signature-256', '')
    if not verify_signature(request.data, signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    event = request.headers.get('X-GitHub-Event')
    payload = request.json
    
    if event == 'push':
        repo = payload.get('repository', {}).get('full_name', 'unknown')
        commits = payload.get('commits', [])
        if commits:
            commit = commits[-1]  # Latest commit
            message = commit.get('message', '').split('\n')[0][:100]
            author = commit.get('author', {}).get('name', 'unknown')
            url = payload.get('repository', {}).get('html_url', '')
            
            tweet = f"""🔄 Push to {repo}

{message}

by {author}

{url}"""
            
            try:
                client = get_twitter_client()
                response = client.create_tweet(text=tweet[:280])
                print(f"✅ Tweeted push: {response.data['id']}")
                return jsonify({'status': 'tweeted', 'id': response.data['id']})
            except Exception as e:
                print(f"❌ Tweet failed: {e}")
                return jsonify({'error': str(e)}), 500
    
    return jsonify({'status': 'ignored', 'event': event})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
