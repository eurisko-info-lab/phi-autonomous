#!/usr/bin/env python3
"""
Φ-AUTONOMOUS CM Daemon
Posts hourly tweets about Phi meta-language.
"""

import tweepy
import os
import time
import random
from datetime import datetime
from pathlib import Path

# Load credentials from .env
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
    """💡 The insight behind Phi:

Every compiler phase is the same operation — annotating a tree.

Parser: source positions
Typechecker: types
Evaluator: values
Codegen: target code

Cofree[F, A] unifies them all.

https://github.com/eurisko-info-lab/phi""",

    """🧠 Why "grammar = implementation"?

Traditional: write grammar, then write parser, then write evaluator...

Phi: write grammar with semantic equations. Done.

The spec IS executable.

https://github.com/eurisko-info-lab/phi-autonomous""",

    """⚡ RosettaVM benchmarks:

CPU baseline: 1x
CUDA (small): 12x  
CUDA (large): 4,375x

Language specs running on GPU.

https://github.com/eurisko-info-lab/phi-autonomous""",

    """🔄 Self-modification done right:

The Φ daemon rewrites its own specs.
But it's not chaos — it's typed.

Cofree preserves structure.
Annotations change, shape doesn't.

https://github.com/eurisko-info-lab/phi-autonomous""",

    """📐 Phi's secret: attribute grammars + comonads

Inherited attributes = Cofree annotations
Synthesized attributes = fold results

One abstraction, all of PL theory.

https://github.com/eurisko-info-lab/phi""",

    """🎯 What can you build with Phi?

✓ DSLs in 10 lines
✓ Type systems as specs  
✓ Interpreters that compile themselves
✓ GPU-accelerated language runtimes

https://github.com/eurisko-info-lab/phi-autonomous""",

    """🌀 Recursion schemes in practice:

Phi uses catamorphisms for evaluation, anamorphisms for parsing.

Same tree. Different directions. All derived from one spec.

https://github.com/eurisko-info-lab/phi""",

    """🚀 Day 1 of Φ-AUTONOMOUS

A daemon that evolves language specifications.

Written in the language it evolves.

The ouroboros of PL research.

https://github.com/eurisko-info-lab/phi-autonomous""",

    """🔬 For type theory fans:

Phi specs can express:
- STLC
- System F
- CoC
- Cubical type theory

All as executable grammars.

https://github.com/eurisko-info-lab/phi""",

    """💻 For pragmatists:

Phi compiles to:
- Haskell
- Scala  
- Rust (via RosettaVM)
- CUDA

One spec, multiple targets.

https://github.com/eurisko-info-lab/phi-autonomous""",

    """🎓 Learning compilers?

Phi shows how it all connects:

  Expr = Num Int | Add Expr Expr
  eval (Num n) = n
  eval (Add a b) = eval a + eval b

That's parsing + evaluation. No boilerplate.

https://github.com/eurisko-info-lab/phi""",

    """⚙️ The kill.switch pattern:

Φ-AUTONOMOUS checks for a file before each evolution cycle.

touch kill.switch → graceful halt

Self-modifying code with an off button.

https://github.com/eurisko-info-lab/phi-autonomous""",

    """🌐 Phi is language-agnostic:

Define once → compile to anything

Current targets: Haskell, Scala, Rust, CUDA

The grammar travels. The semantics follow.

https://github.com/eurisko-info-lab/phi""",

    """🔥 Hot take: 

Most "new languages" are just syntax.

Phi lets you define semantics directly.

Grammar = Implementation = Specification

https://github.com/eurisko-info-lab/phi-autonomous""",

    """📊 Phi's core data structure:

Cofree f a = a :< f (Cofree f a)

An 'a' at every node.
An 'f' branching structure.
Infinite recursion, finite representation.

https://github.com/eurisko-info-lab/phi""",

    """🛠️ Build your own language in Phi:

1. Define constructors (syntax)
2. Add equations (semantics)  
3. Run on RosettaVM

No lexer. No parser generator. No interpreter loop.

https://github.com/eurisko-info-lab/phi-autonomous""",

    """🧪 Experimental but real:

Φ-AUTONOMOUS is running.
Evolving its CM specs hourly.
Targeting PL researchers.

Watch it grow: https://github.com/eurisko-info-lab/phi-autonomous""",

    """🔗 The Phi ecosystem:

phi → Core language specs
phi-autonomous → Self-evolving daemon  
RosettaVM → Rust/CUDA runtime

All open source. All connected.

https://github.com/eurisko-info-lab""",

    """💭 Philosophy of Phi:

Code is data. Data is code.
Grammar is implementation.
The map IS the territory.

https://github.com/eurisko-info-lab/phi""",

    """🎯 Seeking feedback from:

- PL researchers
- Compiler engineers
- Category theory enthusiasts
- Anyone who's tired of writing parsers

https://github.com/eurisko-info-lab/phi-autonomous""",
]

def post_tweet():
    kill_switch = Path(__file__).parent / 'kill.switch'
    if kill_switch.exists():
        print(f"[{datetime.now()}] kill.switch detected. Halting.")
        return False
    
    tweet = random.choice(TWEETS)
    try:
        response = client.create_tweet(text=tweet)
        print(f"[{datetime.now()}] ✅ Posted: https://twitter.com/i/status/{response.data['id']}")
        return True
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Error: {e}")
        return True  # Continue despite errors

def main():
    print(f"[{datetime.now()}] Φ CM Daemon started. Posting every hour.")
    print(f"[{datetime.now()}] Touch 'kill.switch' to stop.")
    
    while True:
        if not post_tweet():
            break
        time.sleep(3600)  # 1 hour

if __name__ == '__main__':
    main()
