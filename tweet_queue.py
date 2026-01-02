#!/usr/bin/env python3
"""
Tweet queue - posts when rate limit allows
Run with: nohup python3 tweet_queue.py &
"""

import tweepy
from pathlib import Path
import time
from datetime import datetime

# Load env
env = {}
for line in Path('/home/patrick/IdeaProjects/phi-autonomous/.env').read_text().splitlines():
    if '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1)
        env[k] = v.strip('"\'')

def get_client():
    return tweepy.Client(
        consumer_key=env['TWITTER_API_KEY'],
        consumer_secret=env['TWITTER_API_SECRET'],
        access_token=env['TWITTER_ACCESS_TOKEN'],
        access_token_secret=env['TWITTER_ACCESS_SECRET']
    )

# Queue of tweets to post
QUEUE = [
    """@elonmusk 

Phi: a meta-language where grammar = implementation.

• Shape errors in AI → compile-time errors
• Linear types enforce no-cloning (quantum)
• One spec → CUDA, ONNX, Metal, WebGPU

Better than PyTorch. Better than Qiskit.

github.com/eurisko-info-lab/phi""",

    """PyTorch shape errors at 3am? 

In Phi, Tensor [32, 768] is a TYPE.
Wrong dimensions = won't compile.

Your loss function can't be NaN if your code can't run wrong shapes.

github.com/eurisko-info-lab/phi""",
]

def post_with_retry(tweet, max_retries=50, delay=300):
    """Keep trying until rate limit resets"""
    client = get_client()
    
    for attempt in range(max_retries):
        try:
            response = client.create_tweet(text=tweet)
            return f"✅ Posted: https://twitter.com/i/status/{response.data['id']}"
        except tweepy.TooManyRequests:
            print(f"[{datetime.now()}] Rate limited, waiting {delay}s... (attempt {attempt+1}/{max_retries})")
            time.sleep(delay)
        except Exception as e:
            return f"❌ Failed: {e}"
    
    return "❌ Max retries exceeded"

if __name__ == '__main__':
    log = Path('/home/patrick/IdeaProjects/phi-autonomous/tweet_queue.log')
    
    for i, tweet in enumerate(QUEUE):
        print(f"\n[{datetime.now()}] Posting tweet {i+1}/{len(QUEUE)}...")
        result = post_with_retry(tweet)
        print(result)
        log.write_text(log.read_text() + f"\n[{datetime.now()}] {result}" if log.exists() else f"[{datetime.now()}] {result}")
        
        if "✅" in result:
            time.sleep(60)  # Wait 1 min between successful posts
    
    print("\n✅ Queue complete!")
