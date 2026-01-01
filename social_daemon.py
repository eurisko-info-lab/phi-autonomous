#!/usr/bin/env python3
"""
Multi-Platform Social Posting Daemon
Posts to: X, Dev.to, Mastodon, LinkedIn
"""

import os
import time
import random
import requests
from datetime import datetime
from pathlib import Path

# Load .env
def load_env():
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value.strip('"\'')

load_env()

# === TWITTER/X ===
def post_twitter(text):
    try:
        import tweepy
        client = tweepy.Client(
            consumer_key=os.environ.get('TWITTER_API_KEY'),
            consumer_secret=os.environ.get('TWITTER_API_SECRET'),
            access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.environ.get('TWITTER_ACCESS_SECRET')
        )
        response = client.create_tweet(text=text[:280])
        return f"https://twitter.com/i/status/{response.data['id']}"
    except Exception as e:
        return f"X error: {e}"

# === DEV.TO ===
def post_devto(title, body, tags=['programming', 'languages', 'compilers']):
    api_key = os.environ.get('DEVTO_API_KEY')
    if not api_key:
        return "Dev.to: no API key"
    
    try:
        response = requests.post(
            'https://dev.to/api/articles',
            headers={'api-key': api_key, 'Content-Type': 'application/json'},
            json={
                'article': {
                    'title': title,
                    'body_markdown': body,
                    'published': True,
                    'tags': tags[:4]  # Max 4 tags
                }
            }
        )
        if response.ok:
            return response.json().get('url', 'posted')
        return f"Dev.to error: {response.text}"
    except Exception as e:
        return f"Dev.to error: {e}"

# === MASTODON ===
def post_mastodon(text):
    instance = os.environ.get('MASTODON_INSTANCE', 'https://fosstodon.org')
    token = os.environ.get('MASTODON_ACCESS_TOKEN')
    if not token:
        return "Mastodon: no token"
    
    try:
        response = requests.post(
            f'{instance}/api/v1/statuses',
            headers={'Authorization': f'Bearer {token}'},
            data={'status': text[:500]}
        )
        if response.ok:
            return response.json().get('url', 'posted')
        return f"Mastodon error: {response.text}"
    except Exception as e:
        return f"Mastodon error: {e}"

# === LINKEDIN ===
def post_linkedin(text):
    token = os.environ.get('LINKEDIN_ACCESS_TOKEN')
    person_id = os.environ.get('LINKEDIN_PERSON_ID')
    if not token or not person_id:
        return "LinkedIn: no token/id"
    
    try:
        response = requests.post(
            'https://api.linkedin.com/v2/ugcPosts',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            },
            json={
                'author': f'urn:li:person:{person_id}',
                'lifecycleState': 'PUBLISHED',
                'specificContent': {
                    'com.linkedin.ugc.ShareContent': {
                        'shareCommentary': {'text': text[:3000]},
                        'shareMediaCategory': 'NONE'
                    }
                },
                'visibility': {'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'}
            }
        )
        if response.ok:
            return "LinkedIn: posted"
        return f"LinkedIn error: {response.text}"
    except Exception as e:
        return f"LinkedIn error: {e}"

# === BLUESKY ===
def post_bluesky(text):
    handle = os.environ.get('BLUESKY_HANDLE')
    password = os.environ.get('BLUESKY_APP_PASSWORD')
    if not handle or not password:
        return "Bluesky: no credentials"
    
    try:
        # Login
        session = requests.post(
            'https://bsky.social/xrpc/com.atproto.server.createSession',
            json={'identifier': handle, 'password': password}
        ).json()
        
        # Post
        response = requests.post(
            'https://bsky.social/xrpc/com.atproto.repo.createRecord',
            headers={'Authorization': f"Bearer {session['accessJwt']}"},
            json={
                'repo': session['did'],
                'collection': 'app.bsky.feed.post',
                'record': {
                    'text': text[:300],
                    'createdAt': datetime.utcnow().isoformat() + 'Z',
                    '$type': 'app.bsky.feed.post'
                }
            }
        )
        if response.ok:
            return "Bluesky: posted"
        return f"Bluesky error: {response.text}"
    except Exception as e:
        return f"Bluesky error: {e}"

# === CONTENT LIBRARY ===
POSTS = [
    {
        'short': """🚀 Phi: A meta-language where grammar = implementation

One spec → parser, typechecker, evaluator, compiler.

Built on Cofree[F, A] — annotated trees all the way down.

https://github.com/eurisko-info-lab/phi""",
        'title': "Phi: When Your Grammar IS Your Implementation",
        'long': """# Phi: When Your Grammar IS Your Implementation

What if you could write a language specification and have it *be* the implementation?

```
Expr = Num Int | Add Expr Expr
eval (Num n) = n
eval (Add a b) = eval a + eval b
```

That's a complete language in Phi. Parser derived from constructors. Evaluator from equations.

## The Math: Cofree[F, A]

Every compiler phase is the same operation — annotating a tree:
- Parser: annotate with source positions
- Typechecker: annotate with types
- Evaluator: annotate with values
- Codegen: annotate with target code

Same structure. Different annotations. All derived.

## Try It

```bash
git clone --recursive https://github.com/eurisko-info-lab/phi-autonomous
./deploy.sh
```

Feedback welcome from PL researchers and compiler enthusiasts!

https://github.com/eurisko-info-lab/phi
"""
    },
    {
        'short': """⚡ RosettaVM: Running language specs on GPU

4,375x speedup at scale.
Compiles Phi → CUDA.
Self-evolving daemon included.

https://github.com/eurisko-info-lab/phi-autonomous""",
        'title': "RosettaVM: GPU-Accelerated Language Specifications",
        'long': """# RosettaVM: GPU-Accelerated Language Specifications

What if your language specs could run on GPU?

RosettaVM compiles Phi specifications to CUDA, achieving:
- CPU baseline: 1x
- CUDA (small): 12x
- CUDA (large): 4,375x

## How It Works

Phi specs are Cofree[F, A] — annotated trees. Tree traversals parallelize naturally.

The RosettaVM runtime:
1. Parses .phi specs
2. Generates CUDA kernels for tree operations
3. Executes with massive parallelism

## The Self-Evolving Daemon

Φ-AUTONOMOUS runs RosettaVM hourly, evolving its own behavior:

```bash
./deploy.sh vector4  # GPU mode
touch kill.switch    # Graceful halt
```

https://github.com/eurisko-info-lab/phi-autonomous
"""
    },
    {
        'short': """🔄 Cofree comonads in practice:

Every compiler phase = annotating a tree.
One abstraction unifies parsing, typing, evaluation, codegen.

Phi makes it executable.

https://github.com/eurisko-info-lab/phi""",
        'title': "Cofree Comonads: Unifying Compiler Phases",
        'long': """# Cofree Comonads: Unifying Compiler Phases

The insight that powers Phi: every compiler phase is the same operation.

## Cofree[F, A]

```haskell
data Cofree f a = a :< f (Cofree f a)
```

An annotation `a` at every node. A branching structure `f`. Infinite recursion, finite representation.

## Compiler Phases as Annotations

| Phase | Annotation |
|-------|------------|
| Parser | Source positions |
| Typechecker | Types |
| Evaluator | Values |
| Codegen | Target code |

Same tree. Different annotations. All derived from one spec.

## In Phi

```phi
Expr = Num Int | Add Expr Expr
eval (Num n) = n
eval (Add a b) = eval a + eval b
```

Parser derived from constructors. Evaluator from equations. No boilerplate.

https://github.com/eurisko-info-lab/phi
"""
    }
]

def post_all(content):
    """Post to all platforms."""
    results = []
    
    # Twitter/X (short)
    r = post_twitter(content['short'])
    results.append(f"X: {r}")
    
    # Mastodon (short)
    r = post_mastodon(content['short'])
    results.append(f"Mastodon: {r}")
    
    # Bluesky (short)
    r = post_bluesky(content['short'])
    results.append(f"Bluesky: {r}")
    
    # Dev.to (long article) - only if has content
    if 'long' in content and 'title' in content:
        r = post_devto(content['title'], content['long'])
        results.append(f"Dev.to: {r}")
    
    # LinkedIn (medium)
    linkedin_text = content.get('linkedin', content['short'])
    r = post_linkedin(linkedin_text)
    results.append(f"LinkedIn: {r}")
    
    return results

def main():
    kill_switch = Path(__file__).parent / 'kill.switch'
    print(f"[{datetime.now()}] Multi-platform daemon started")
    print(f"Touch 'kill.switch' to stop")
    
    while True:
        if kill_switch.exists():
            print(f"[{datetime.now()}] kill.switch detected. Halting.")
            break
        
        content = random.choice(POSTS)
        print(f"\n[{datetime.now()}] Posting: {content['title'][:50]}...")
        
        for result in post_all(content):
            print(f"  {result}")
        
        # Wait 2 hours between posts (to avoid spam across platforms)
        time.sleep(7200)

if __name__ == '__main__':
    main()
