#!/usr/bin/env python3
"""
Φ-AUTONOMOUS CM Daemon - with rate limit backoff
"""

import tweepy
import os
import time
import random
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

client = tweepy.Client(
    consumer_key=os.environ.get('TWITTER_API_KEY'),
    consumer_secret=os.environ.get('TWITTER_API_SECRET'),
    access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.environ.get('TWITTER_ACCESS_SECRET')
)

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

def post_tweet():
    kill_switch = Path(__file__).parent / 'kill.switch'
    if kill_switch.exists():
        print(f"[{datetime.now()}] kill.switch detected. Halting.")
        return False, 0
    
    tweet = random.choice(TWEETS)
    try:
        response = client.create_tweet(text=tweet[:280])
        print(f"[{datetime.now()}] ✅ Bark! https://twitter.com/i/status/{response.data['id']}")
        return True, 3600  # Success: wait 1 hour
    except tweepy.TooManyRequests:
        print(f"[{datetime.now()}] ⏳ Rate limited. Backing off 20 min...")
        return True, 1200  # Rate limit: wait 20 min
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Error: {e}")
        return True, 600  # Other error: wait 10 min

def main():
    print(f"[{datetime.now()}] 🐕 Φ CM Daemon started. Will bark hourly.")
    print(f"[{datetime.now()}] Touch 'kill.switch' to stop.")
    
    while True:
        keep_going, wait_time = post_tweet()
        if not keep_going:
            break
        time.sleep(wait_time)

if __name__ == '__main__':
    main()
