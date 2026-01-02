#!/usr/bin/env python3
"""
X Growth & Monetization Engine for @eurekainfolab
Auto-posts engaging content about Phi to build followers and revenue.
"""

import tweepy
import os
import random
import time
from datetime import datetime, timedelta
from pathlib import Path

def load_env():
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value.strip('"\'')

load_env()

def get_client():
    return tweepy.Client(
        consumer_key=os.environ.get('TWITTER_API_KEY'),
        consumer_secret=os.environ.get('TWITTER_API_SECRET'),
        access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.environ.get('TWITTER_ACCESS_SECRET')
    )

# Content library - engaging tweets about Phi
TWEETS = [
    # Hook tweets (controversy/bold claims)
    """PyTorch shape errors at 3am? 

In Phi, Tensor [32, 768] is a TYPE.
Wrong dimensions = won't compile.

Your loss function can't be NaN if your code can't run wrong shapes.

github.com/eurisko-info-lab/phi""",

    """Hot take: Qiskit is doing quantum computing wrong.

The no-cloning theorem should be in the TYPE SYSTEM.
If you can copy a qubit, your code shouldn't compile.

Phi uses linear types (⊸) for this.
Physics as types.

github.com/eurisko-info-lab/phi""",

    """What if your programming language knew physics?

In Phi:
• Hilbert spaces are types
• Unitarity is a type constraint  
• Measurement collapses the type

The compiler knows quantum mechanics.

github.com/eurisko-info-lab/phi""",

    """AI frameworks in 2026:
- PyTorch: shape error at runtime
- TensorFlow: deprecated API warnings
- JAX: "just use vmap bro"

Phi: if it compiles, the math is correct.

github.com/eurisko-info-lab/phi""",

    # Educational threads (first tweet)
    """🧵 Why type systems matter for AI:

A thread on how Phi catches bugs that PyTorch can't.

1/ The problem: neural networks are just matrix multiplication chains. Get one dimension wrong → runtime crash.""",

    """🧵 Quantum computing needs linear types.

Here's why the no-cloning theorem should be enforced by your compiler, not your discipline.

1/ In quantum mechanics, you cannot copy an unknown quantum state. This is physics, not a bug.""",

    """🧵 What is Cofree[F, A] and why should you care?

A thread on the data structure that makes Phi possible.

1/ Imagine an AST where every node carries both data AND the recipe to interpret itself.""",

    # Engagement bait
    """Unpopular opinion:

Most "type-safe" ML libraries aren't actually type-safe.

They check types at runtime.
That's just assertions with extra steps.

Real type safety = compile-time guarantees.""",

    """Question for ML engineers:

What's the weirdest shape error that took you hours to debug?

I'll start: transposed a batch dimension in a transformer attention mask. Silently trained on garbage for 3 days.""",

    """If you could add ONE feature to PyTorch, what would it be?

My answer: compile-time shape checking.

No more:
RuntimeError: mat1 and mat2 shapes cannot be multiplied (32x768 and 512x768)""",

    # Technical insights
    """The Curry-Howard correspondence says:
Types = Propositions
Programs = Proofs

For AI, this means:
Tensor shapes = Mathematical constraints
Your model = Proof that the math works

If it type-checks, it's mathematically valid.""",

    """Why does Phi use Cofree[F, A]?

Because it's the universal way to build recursive data structures with annotations.

AST? Cofree.
Neural network layers? Cofree.
Quantum circuits? Cofree.

One pattern to rule them all.""",

    """The future of programming languages:

2020: Types check syntax
2025: Types check shapes  
2030: Types check physics

Phi is already at 2030.
Hilbert spaces, unitarity, no-cloning — all in the type system.""",

    # Social proof / milestones
    """Just shipped:
• quantum.phi - QM as types
• ai.phi - ML as types
• phi-on-qm.phi - Phi on quantum hardware
• phi-on-ai.phi - Phi on neural networks

The language describes what it runs on.
The loop closes.

github.com/eurisko-info-lab/phi""",

    # Call to action
    """Looking for collaborators on Phi:

- Type theory enthusiasts
- Quantum computing devs
- ML engineers tired of shape errors
- Anyone who thinks programming languages can be better

DM or check out: github.com/eurisko-info-lab/phi""",

    """Star ⭐ if you've ever had a shape error in PyTorch that took more than 10 minutes to fix.

Then check out Phi, where that can't happen.

github.com/eurisko-info-lab/phi""",
]

REPLY_HOOKS = {
    # Keywords to watch for and reply to
    "pytorch shape": "Phi solves this with compile-time shape checking. Tensor [32, 768] is a TYPE, not a runtime annotation. github.com/eurisko-info-lab/phi",
    "tensor shape error": "In Phi, this is a compile error, not a runtime surprise. github.com/eurisko-info-lab/phi",
    "qiskit": "Have you seen Phi's approach to quantum? Linear types enforce no-cloning at compile time. github.com/eurisko-info-lab/phi",
    "type safe ml": "Phi takes this seriously - shapes in the type system, not just runtime checks. github.com/eurisko-info-lab/phi",
    "programming language design": "Working on Phi - a meta-language where grammar = implementation. Compiles to CUDA, ONNX, quantum. github.com/eurisko-info-lab/phi",
}

def post_daily_content():
    """Post a random tweet from the content library."""
    client = get_client()
    tweet = random.choice(TWEETS)
    
    try:
        response = client.create_tweet(text=tweet)
        print(f"✅ Posted: https://twitter.com/i/status/{response.data['id']}")
        return response.data['id']
    except Exception as e:
        print(f"❌ Failed to post: {e}")
        return None

def post_thread(tweets):
    """Post a thread of tweets."""
    client = get_client()
    previous_id = None
    
    for i, tweet in enumerate(tweets):
        try:
            if previous_id:
                response = client.create_tweet(text=tweet, in_reply_to_tweet_id=previous_id)
            else:
                response = client.create_tweet(text=tweet)
            previous_id = response.data['id']
            print(f"✅ Thread {i+1}/{len(tweets)}: {response.data['id']}")
            time.sleep(2)  # Rate limit safety
        except Exception as e:
            print(f"❌ Thread failed at {i+1}: {e}")
            break
    
    return previous_id

def get_account_stats():
    """Get current account statistics."""
    client = get_client()
    try:
        me = client.get_me(user_fields=['public_metrics'])
        metrics = me.data.public_metrics
        return {
            'followers': metrics['followers_count'],
            'following': metrics['following_count'],
            'tweets': metrics['tweet_count']
        }
    except Exception as e:
        print(f"❌ Failed to get stats: {e}")
        return None

def monetization_status():
    """Check monetization eligibility."""
    stats = get_account_stats()
    if not stats:
        return "Unknown"
    
    followers = stats['followers']
    
    status = {
        'followers': followers,
        'tips_eligible': True,  # Always available
        'subscriptions_eligible': followers >= 500,
        'revenue_sharing_eligible': followers >= 500,  # Also needs 5M impressions
        'next_milestone': 500 if followers < 500 else 10000
    }
    
    return status

# Scheduled content calendar
SCHEDULE = {
    'monday': 'educational_thread',
    'tuesday': 'engagement_question',
    'wednesday': 'technical_insight',
    'thursday': 'bold_claim',
    'friday': 'community_callout',
    'saturday': 'milestone_update',
    'sunday': 'rest'
}

def run_daily():
    """Run the daily posting routine."""
    day = datetime.now().strftime('%A').lower()
    content_type = SCHEDULE.get(day, 'technical_insight')
    
    print(f"📅 {day.title()}: {content_type}")
    
    if content_type == 'rest':
        print("😴 Rest day - no posting")
        return
    
    # Post appropriate content
    post_daily_content()
    
    # Log stats
    stats = get_account_stats()
    if stats:
        print(f"📊 Followers: {stats['followers']} | Tweets: {stats['tweets']}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'post':
            post_daily_content()
        elif cmd == 'stats':
            stats = get_account_stats()
            print(f"📊 {stats}")
        elif cmd == 'status':
            status = monetization_status()
            print(f"💰 Monetization: {status}")
        elif cmd == 'daily':
            run_daily()
    else:
        print("Usage: x_growth.py [post|stats|status|daily]")
        print("\nContent library:", len(TWEETS), "tweets ready")
        status = monetization_status()
        print(f"Monetization status: {status}")
