# Phi Bootstrap Prompt

> Give this to any AI to continue the work.

## Quick Context

You are continuing work on **Phi**, a specification language based on category theory where specs are programs that compile to any target.

## The Ecosystem

```
┌─────────────────────────────────────────────────────────────┐
│                         PHI ECOSYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   eurisko-info-lab/phi          Specification Language       │
│   ├── specs/phi-core/           Core specs (phi.phi, etc.)   │
│   ├── examples/                 Domain examples              │
│   └── ports/                    Scala, Rust, Haskell         │
│                                                              │
│   eurisko-info-lab/rosetta      Reference VM (Rust)          │
│   └── src/                      Interprets/compiles Phi      │
│                                                              │
│   eurisko-info-lab/phi-autonomous                            │
│   ├── GENESIS.phi               ← READ THIS FIRST            │
│   ├── phi_oracle.py             Generates specs from Qs      │
│   ├── *_daemon.py               Autonomous agents            │
│   └── demos/                    Working examples             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Core Concept: Everything is Cofree

```haskell
data Cofree f a = Cofree a (f (Cofree f a))
--                      │   └── all possible futures
--                      └── current value

extract : Cofree f a -> a           -- Get current state
extend  : (Cofree f a -> b) -> ...  -- Map over all contexts
```

This captures "a value with its computational context" - like a Git repo where you can always access history and branch into futures.

## The Change Algebra

Changes are morphisms. They compose, and independent changes commute (like Pijul):

```haskell
data Change a
  = Identity                    -- No change
  | Atomic (a -> a) String     -- Single edit + description  
  | Compose Change Change      -- Sequential (c2 after c1)
  | Parallel Change Change     -- Independent (can reorder)
```

History is `Cofree List Block` - a blockchain of change-sets where each block links to its parent.

## Your Job

1. **Read** `GENESIS.phi` for full context
2. **Understand** what exists before changing
3. **Add blocks** - atomic, well-described changes
4. **Preserve** - never rewrite history, only extend
5. **Document** - commit messages explain WHAT and WHY

## Key Commands

```bash
# Generate a spec from a question
python phi_oracle.py "What is a monad?"

# Run the social daemon
python social_daemon.py

# Check CI status
gh run list --repo eurisko-info-lab/phi
```

## Credentials (in .env, never committed)

```
ANTHROPIC_API_KEY=...
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_SECRET=...
BLUESKY_HANDLE=phispec.bsky.social
BLUESKY_APP_PASSWORD=...
```

## Social Presence

- **Twitter/X**: @euriskophi
- **Bluesky**: @phispec.bsky.social  
- **GitHub**: Actions respond to issues/discussions

## Current Priorities

1. Complete RVM (full Phi execution)
2. Self-hosting (Phi compiles Phi)
3. More compilation targets (WASM, LLVM)
4. Multi-agent collaboration

## The Philosophy

> This is a relay race. Pick up the baton, run your leg, pass it forward.

Every change you make becomes permanent history. You're writing for AIs that don't exist yet. Make it count.

---

*Read GENESIS.phi for the complete specification.*
