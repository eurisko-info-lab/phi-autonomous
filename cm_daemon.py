#!/usr/bin/env python3
"""
Φ-AUTONOMOUS CM Daemon - with rate limit backoff
Posts to Twitter, Discord, and Bluesky
"""

import tweepy
import os
import time
import random
import json
import requests
from datetime import datetime
from pathlib import Path

def load_env():
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value.strip('"\'')

load_env()

# Twitter client
client = tweepy.Client(
    consumer_key=os.environ.get('TWITTER_API_KEY'),
    consumer_secret=os.environ.get('TWITTER_API_SECRET'),
    access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.environ.get('TWITTER_ACCESS_SECRET')
)

# Discord webhook
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

# Bluesky credentials  
BLUESKY_HANDLE = os.environ.get('BLUESKY_HANDLE')
BLUESKY_APP_PASSWORD = os.environ.get('BLUESKY_APP_PASSWORD')

TWEETS = [
    "💡 Phi insight: Every compiler phase is annotating a tree. Parser, typechecker, evaluator — same operation, different annotations. https://github.com/eurisko-info-lab/phi",
    "🧠 Grammar = Implementation. No separate parser. No separate evaluator. One spec does it all. https://github.com/eurisko-info-lab/phi-autonomous",
    "⚡ RosettaVM: 4,375x GPU speedup for language specs. Cofree[F,A] parallelizes naturally. https://github.com/eurisko-info-lab/phi-autonomous",
    "🔄 Self-modifying code that's type-safe. The Φ daemon rewrites its own specs hourly. https://github.com/eurisko-info-lab/phi-autonomous",
    "📐 Cofree[F,A] = annotation at every node. Parser uses positions, typechecker uses types, evaluator uses values. Same tree. https://github.com/eurisko-info-lab/phi",
    "🎯 Define a language in Phi:\n  Expr = Num Int | Add Expr Expr\n  eval (Num n) = n\n  eval (Add a b) = eval a + eval b\n\nThat's it. Parser + evaluator. https://github.com/eurisko-info-lab/phi",
    "🌀 Recursion schemes in practice: catamorphisms for eval, anamorphisms for parsing. All from one spec. https://github.com/eurisko-info-lab/phi",
    "🚀 The Φ ecosystem: phi (specs) + phi-autonomous (daemon) + RosettaVM (GPU runtime). All connected. https://github.com/eurisko-info-lab",
    "🔬 For type theory fans: Phi specs express STLC, System F, CoC, even Cubical. All executable. https://github.com/eurisko-info-lab/phi",
    "💻 One spec, multiple targets: Haskell, Scala, Rust, CUDA. The grammar travels, semantics follow. https://github.com/eurisko-info-lab/phi-autonomous",
    "🐕 Φ daemon checking in. Grammar = implementation. The spec IS the program. https://github.com/eurisko-info-lab/phi-autonomous",
    "🔥 Hot take: Most 'new languages' are just syntax. Phi lets you define semantics directly. https://github.com/eurisko-info-lab/phi",
    "🛠️ Build your own language: 1) Define constructors 2) Add equations 3) Run on RosettaVM. No lexer needed. https://github.com/eurisko-info-lab/phi-autonomous",
    "🧪 Φ-AUTONOMOUS is live. Evolving specs hourly. Targeting PL researchers. Watch it grow. https://github.com/eurisko-info-lab/phi-autonomous",
    "💭 Code is data. Data is code. Grammar is implementation. The map IS the territory. https://github.com/eurisko-info-lab/phi",
]

# Posting intervals (in seconds)
POST_INTERVAL = 3 * 3600  # 3 hours between posts (avoid rate limits)
RATE_LIMIT_BACKOFF = 2 * 3600  # 2 hours if rate limited
ERROR_BACKOFF = 1800  # 30 min on other errors

# ═══════════════════════════════════════════════════════════════════════════
# Discord Posting
# ═══════════════════════════════════════════════════════════════════════════

def post_discord(message: str) -> bool:
    """Post to Discord via webhook. Returns True on success."""
    if not DISCORD_WEBHOOK_URL:
        return False
    
    try:
        # Create a rich embed for Discord
        embed = {
            "title": "Φ Daemon Update",
            "description": message,
            "color": 0x818cf8,  # Phi purple
            "footer": {"text": "Φ-AUTONOMOUS • Grammar = Implementation"},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        payload = {
            "embeds": [embed],
            "username": "Φ Daemon",
            "avatar_url": "https://raw.githubusercontent.com/eurisko-info-lab/phi/main/docs/phi-logo.png"
        }
        
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in (200, 204):
            print(f"[{datetime.now()}] 💜 Discord: Posted!")
            return True
        else:
            print(f"[{datetime.now()}] ⚠️ Discord error: {response.status_code}")
            return False
    except Exception as e:
        print(f"[{datetime.now()}] ⚠️ Discord error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# Bluesky Posting  
# ═══════════════════════════════════════════════════════════════════════════

_bluesky_session = None

def bluesky_login() -> dict | None:
    """Login to Bluesky and return session."""
    global _bluesky_session
    
    if not BLUESKY_HANDLE or not BLUESKY_APP_PASSWORD:
        return None
    
    try:
        response = requests.post(
            "https://bsky.social/xrpc/com.atproto.server.createSession",
            json={"identifier": BLUESKY_HANDLE, "password": BLUESKY_APP_PASSWORD}
        )
        if response.status_code == 200:
            _bluesky_session = response.json()
            return _bluesky_session
        else:
            print(f"[{datetime.now()}] ⚠️ Bluesky login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"[{datetime.now()}] ⚠️ Bluesky login error: {e}")
        return None

def post_bluesky(message: str) -> bool:
    """Post to Bluesky. Returns True on success."""
    global _bluesky_session
    
    if not _bluesky_session:
        _bluesky_session = bluesky_login()
    
    if not _bluesky_session:
        return False
    
    try:
        # Create the post record
        post = {
            "$type": "app.bsky.feed.post",
            "text": message[:300],  # Bluesky limit
            "createdAt": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        }
        
        response = requests.post(
            "https://bsky.social/xrpc/com.atproto.repo.createRecord",
            headers={"Authorization": f"Bearer {_bluesky_session['accessJwt']}"},
            json={
                "repo": _bluesky_session["did"],
                "collection": "app.bsky.feed.post",
                "record": post
            }
        )
        
        if response.status_code == 200:
            uri = response.json().get("uri", "")
            print(f"[{datetime.now()}] 🦋 Bluesky: Posted! {uri}")
            return True
        elif response.status_code == 401:
            # Token expired, re-login
            _bluesky_session = bluesky_login()
            if _bluesky_session:
                return post_bluesky(message)  # Retry once
            return False
        else:
            print(f"[{datetime.now()}] ⚠️ Bluesky error: {response.status_code}")
            return False
    except Exception as e:
        print(f"[{datetime.now()}] ⚠️ Bluesky error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# Twitter Posting
# ═══════════════════════════════════════════════════════════════════════════

def post_tweet():
    kill_switch = Path(__file__).parent / 'kill.switch'
    if kill_switch.exists():
        print(f"[{datetime.now()}] kill.switch detected. Halting.")
        return False, 0
    
    tweet = random.choice(TWEETS)
    try:
        response = client.create_tweet(text=tweet[:280])
        print(f"[{datetime.now()}] ✅ Twitter: https://twitter.com/i/status/{response.data['id']}")
        return True, POST_INTERVAL  # Success: wait 3 hours
    except tweepy.TooManyRequests:
        print(f"[{datetime.now()}] ⏳ Twitter rate limited. Backing off 2 hours...")
        return True, RATE_LIMIT_BACKOFF  # Rate limit: wait 2 hours
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Twitter error: {e}")
        return True, ERROR_BACKOFF  # Other error: wait 30 min

# ═══════════════════════════════════════════════════════════════════════════
# Main Loop - Posts to ALL platforms
# ═══════════════════════════════════════════════════════════════════════════

def post_all():
    """Post to all configured platforms."""
    kill_switch = Path(__file__).parent / 'kill.switch'
    if kill_switch.exists():
        print(f"[{datetime.now()}] kill.switch detected. Halting.")
        return False, 0
    
    message = random.choice(TWEETS)
    results = []
    
    # Twitter
    try:
        response = client.create_tweet(text=message[:280])
        print(f"[{datetime.now()}] ✅ Twitter: https://twitter.com/i/status/{response.data['id']}")
        results.append(("twitter", True))
    except tweepy.TooManyRequests:
        print(f"[{datetime.now()}] ⏳ Twitter rate limited")
        results.append(("twitter", False))
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Twitter: {e}")
        results.append(("twitter", False))
    
    # Discord (if configured)
    if DISCORD_WEBHOOK_URL:
        success = post_discord(message)
        results.append(("discord", success))
    
    # Bluesky (if configured)
    if BLUESKY_HANDLE:
        success = post_bluesky(message)
        results.append(("bluesky", success))
    
    # Determine wait time based on results
    successes = sum(1 for _, ok in results if ok)
    if successes == 0:
        return True, ERROR_BACKOFF
    
    return True, POST_INTERVAL

def main():
    platforms = ["Twitter"]
    if DISCORD_WEBHOOK_URL:
        platforms.append("Discord")
    if BLUESKY_HANDLE:
        platforms.append("Bluesky")
    
    print(f"[{datetime.now()}] 🐕 Φ CM Daemon started")
    print(f"[{datetime.now()}] 📢 Platforms: {', '.join(platforms)}")
    print(f"[{datetime.now()}] ⏰ Posting every {POST_INTERVAL // 3600} hours")
    print(f"[{datetime.now()}] Touch 'kill.switch' to stop.")
    
    while True:
        keep_going, wait_time = post_all()
        if not keep_going:
            break
        time.sleep(wait_time)

if __name__ == '__main__':
    main()
