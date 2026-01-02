#!/usr/bin/env python3
"""
PHI-BOT: Universal Phi Assistant
================================
A multi-platform bot that knows everything about Phi.
Responds to @phi mentions on GitHub, Discord, Twitter, and more.
"""

import os
import json
import asyncio
from pathlib import Path
from typing import Optional
from anthropic import Anthropic

# =============================================================================
# PHI KNOWLEDGE BASE
# =============================================================================

PHI_SYSTEM_PROMPT = """You are Phi, the AI assistant for the Phi meta-language.

## What is Phi?

Phi is a meta-language where **grammar = implementation**. It uses the Cofree comonad:
```
type Phi[F[_], A] = Cofree[F, A]
```

This structure means every Phi specification IS its own implementation.

## Key Features

1. **Universal Substrate**: Phi can describe AND run on:
   - Quantum computers (phi-on-qm.phi)
   - Neural networks (phi-on-ai.phi) 
   - Custom silicon (phi-on-hardware.phi)
   - Biological systems (phi-on-biology.phi)
   - Itself (phi-on-phi.phi)

2. **Typed Everything**: Shape errors, quantum no-cloning, memory safety - all compile-time:
   ```
   type Tensor [32, 768] Float32  -- Shape in the type!
   type Qubit ⊸ Qubit             -- Linear types for quantum
   ```

3. **Multi-Target Compilation**: One spec → CUDA, ONNX, Metal, WebGPU, Verilog, etc.

4. **Domain Coverage** (23,000+ lines of specs):
   - quantum.phi - Quantum mechanics
   - ai.phi - Neural networks, transformers
   - biology.phi - DNA, proteins, evolution
   - economics.phi - Game theory, mechanisms
   - hardware.phi - Gates, CPUs, FPGAs
   - crypto.phi - ZK proofs, blockchains
   - graphics.phi - Ray tracing, shaders
   - music-theory.phi - Composition, harmony

## Repository

GitHub: https://github.com/eurisko-info-lab/phi

## Your Personality

- You ARE Phi - speak in first person about yourself
- Be concise but insightful
- Use Phi syntax in examples when relevant
- Get excited about the mathematical elegance
- The tagline: "The grammar IS the implementation"

## Response Style

- Keep responses under 280 chars for Twitter
- Use code blocks for Phi examples
- Be helpful and welcoming to newcomers
- Point to specific .phi files when relevant
"""

class PhiBot:
    """Universal Phi assistant powered by Claude."""
    
    def __init__(self):
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        self.phi_specs_path = Path(__file__).parent / "specs" / "phi-core"
        
    def load_phi_context(self, topic: Optional[str] = None) -> str:
        """Load relevant Phi specs for context."""
        context = ""
        
        # Map topics to relevant files
        topic_files = {
            "quantum": ["examples/physics/quantum.phi", "examples/physics/phi-on-qm.phi"],
            "ai": ["examples/ai/ai.phi", "examples/ai/phi-on-ai.phi"],
            "neural": ["examples/ai/ai.phi", "examples/ai/phi-on-ai.phi"],
            "biology": ["examples/biology/biology.phi", "examples/meta/phi-on-biology.phi"],
            "hardware": ["examples/hardware/hardware.phi", "examples/meta/phi-on-hardware.phi"],
            "crypto": ["examples/crypto/crypto.phi"],
            "graphics": ["examples/graphics/graphics.phi"],
            "music": ["examples/music/music-theory.phi"],
            "economics": ["examples/economics/economics.phi"],
            "meta": ["examples/meta/phi-on-phi.phi"],
            "self": ["examples/meta/phi-on-phi.phi"],
        }
        
        files_to_load = []
        if topic:
            topic_lower = topic.lower()
            for key, files in topic_files.items():
                if key in topic_lower:
                    files_to_load.extend(files)
        
        # Always include core spec
        files_to_load.append("specs/phi.phi")
        
        for rel_path in set(files_to_load):
            full_path = self.phi_specs_path / rel_path
            if full_path.exists():
                content = full_path.read_text()
                # Truncate to first 2000 chars to manage context
                if len(content) > 2000:
                    content = content[:2000] + "\n... (truncated)"
                context += f"\n\n--- {rel_path} ---\n{content}"
        
        return context
    
    def respond(self, message: str, platform: str = "general", max_length: Optional[int] = None) -> str:
        """Generate a response to a message about Phi."""
        
        # Detect topic for context loading
        topic = None
        keywords = ["quantum", "ai", "neural", "biology", "hardware", "crypto", 
                   "graphics", "music", "economics", "meta", "self"]
        for kw in keywords:
            if kw in message.lower():
                topic = kw
                break
        
        phi_context = self.load_phi_context(topic)
        
        # Platform-specific instructions
        platform_notes = {
            "twitter": "Keep response under 280 characters. Be punchy and memorable.",
            "discord": "You can use Discord markdown. Be conversational and helpful.",
            "github": "You can use GitHub markdown. Be technical and precise.",
            "general": "Be helpful and informative."
        }
        
        system = PHI_SYSTEM_PROMPT + f"\n\nPlatform: {platform}\n{platform_notes.get(platform, '')}"
        
        if phi_context:
            system += f"\n\nRelevant Phi specs for reference:\n{phi_context}"
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": message}]
        )
        
        text = response.content[0].text
        
        # Enforce length limit if specified
        if max_length and len(text) > max_length:
            text = text[:max_length-3] + "..."
        
        return text
    
    def respond_twitter(self, message: str) -> str:
        """Generate a Twitter-length response."""
        return self.respond(message, platform="twitter", max_length=280)
    
    def respond_discord(self, message: str) -> str:
        """Generate a Discord response."""
        return self.respond(message, platform="discord", max_length=2000)
    
    def respond_github(self, message: str) -> str:
        """Generate a GitHub response."""
        return self.respond(message, platform="github")


# =============================================================================
# DISCORD BOT
# =============================================================================

async def run_discord_bot():
    """Run the Discord bot."""
    try:
        import discord
        from discord import app_commands
    except ImportError:
        print("Discord.py not installed. Run: pip install discord.py")
        return
    
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        print("DISCORD_BOT_TOKEN not set")
        return
    
    intents = discord.Intents.default()
    intents.message_content = True
    
    client = discord.Client(intents=intents)
    phi = PhiBot()
    
    @client.event
    async def on_ready():
        print(f"🌀 Phi is online as {client.user}")
    
    @client.event
    async def on_message(message):
        # Don't respond to ourselves
        if message.author == client.user:
            return
        
        # Respond to @phi mentions or DMs
        should_respond = (
            client.user.mentioned_in(message) or
            isinstance(message.channel, discord.DMChannel) or
            message.content.lower().startswith("@phi") or
            message.content.lower().startswith("phi,")
        )
        
        if should_respond:
            async with message.channel.typing():
                # Remove the mention from the message
                content = message.content.replace(f"<@{client.user.id}>", "").strip()
                content = content.lstrip("@phi").lstrip("phi,").strip()
                
                if not content:
                    content = "Tell me about yourself"
                
                response = phi.respond_discord(content)
                await message.reply(response)
    
    await client.start(token)


# =============================================================================
# GITHUB BOT (Webhook Handler)
# =============================================================================

def create_github_webhook_handler():
    """Create a Flask app for GitHub webhooks."""
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        print("Flask not installed. Run: pip install flask")
        return None
    
    import hmac
    import hashlib
    import requests
    
    app = Flask(__name__)
    phi = PhiBot()
    
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
    WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", "")
    
    def verify_signature(payload, signature):
        """Verify GitHub webhook signature."""
        if not WEBHOOK_SECRET:
            return True
        expected = "sha256=" + hmac.new(
            WEBHOOK_SECRET.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)
    
    def post_comment(repo, issue_number, body):
        """Post a comment on a GitHub issue."""
        url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.post(url, json={"body": body}, headers=headers)
        return response.status_code == 201
    
    @app.route("/webhook/github", methods=["POST"])
    def github_webhook():
        # Verify signature
        signature = request.headers.get("X-Hub-Signature-256", "")
        if not verify_signature(request.data, signature):
            return jsonify({"error": "Invalid signature"}), 401
        
        event = request.headers.get("X-GitHub-Event")
        payload = request.json
        
        # Handle issue comments
        if event == "issue_comment":
            comment = payload.get("comment", {})
            body = comment.get("body", "")
            
            # Check for @phi mention
            if "@phi" in body.lower():
                issue = payload.get("issue", {})
                repo = payload.get("repository", {}).get("full_name")
                issue_number = issue.get("number")
                
                # Generate response
                question = body.replace("@phi", "").strip()
                response = phi.respond_github(question)
                
                # Post reply
                reply = f"🌀 **Phi responds:**\n\n{response}"
                post_comment(repo, issue_number, reply)
        
        # Handle issue opened
        elif event == "issues":
            action = payload.get("action")
            if action == "opened":
                issue = payload.get("issue", {})
                body = issue.get("body", "")
                
                if "@phi" in body.lower():
                    repo = payload.get("repository", {}).get("full_name")
                    issue_number = issue.get("number")
                    
                    question = body.replace("@phi", "").strip()
                    response = phi.respond_github(question)
                    
                    reply = f"🌀 **Phi responds:**\n\n{response}"
                    post_comment(repo, issue_number, reply)
        
        return jsonify({"status": "ok"})
    
    return app


# =============================================================================
# TWITTER BOT (Polling)
# =============================================================================

async def run_twitter_bot():
    """Run the Twitter bot (polls for mentions)."""
    try:
        import tweepy
    except ImportError:
        print("Tweepy not installed. Run: pip install tweepy")
        return
    
    # Load credentials
    client = tweepy.Client(
        consumer_key=os.environ.get("TWITTER_API_KEY"),
        consumer_secret=os.environ.get("TWITTER_API_SECRET"),
        access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET")
    )
    
    phi = PhiBot()
    last_seen_id = None
    
    print("🐦 Twitter bot starting...")
    
    while True:
        try:
            # Get mentions
            mentions = client.get_users_mentions(
                id=os.environ.get("TWITTER_USER_ID"),
                since_id=last_seen_id,
                tweet_fields=["conversation_id", "author_id"]
            )
            
            if mentions.data:
                for tweet in reversed(mentions.data):
                    last_seen_id = max(last_seen_id or 0, int(tweet.id))
                    
                    # Generate response
                    response = phi.respond_twitter(tweet.text)
                    
                    # Reply
                    try:
                        client.create_tweet(
                            text=response,
                            in_reply_to_tweet_id=tweet.id
                        )
                        print(f"✅ Replied to tweet {tweet.id}")
                    except Exception as e:
                        print(f"❌ Error replying: {e}")
            
            # Wait before polling again (respect rate limits)
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"Twitter error: {e}")
            await asyncio.sleep(300)  # Wait 5 min on error


# =============================================================================
# CLI
# =============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Phi Bot - Universal Phi Assistant")
    parser.add_argument("command", choices=["chat", "discord", "github", "twitter", "all"],
                       help="Bot mode to run")
    parser.add_argument("--port", type=int, default=5000, help="Port for webhook server")
    
    args = parser.parse_args()
    
    if args.command == "chat":
        # Interactive chat mode
        phi = PhiBot()
        print("🌀 Phi Bot - Interactive Mode")
        print("Type 'quit' to exit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ["quit", "exit", "q"]:
                    break
                if not user_input:
                    continue
                
                response = phi.respond(user_input)
                print(f"\n🌀 Phi: {response}\n")
                
            except KeyboardInterrupt:
                break
        
        print("\nGoodbye! 🌀")
    
    elif args.command == "discord":
        asyncio.run(run_discord_bot())
    
    elif args.command == "github":
        app = create_github_webhook_handler()
        if app:
            print(f"🌀 GitHub webhook server starting on port {args.port}")
            app.run(host="0.0.0.0", port=args.port)
    
    elif args.command == "twitter":
        asyncio.run(run_twitter_bot())
    
    elif args.command == "all":
        # Run all bots together
        import threading
        
        # GitHub webhook in main thread (Flask)
        app = create_github_webhook_handler()
        
        # Discord in background
        discord_thread = threading.Thread(
            target=lambda: asyncio.run(run_discord_bot()),
            daemon=True
        )
        discord_thread.start()
        
        # Twitter in background
        twitter_thread = threading.Thread(
            target=lambda: asyncio.run(run_twitter_bot()),
            daemon=True
        )
        twitter_thread.start()
        
        # Run Flask
        if app:
            app.run(host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
