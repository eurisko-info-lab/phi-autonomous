#!/usr/bin/env python3
"""
Phi Oracle: The Generative Spec Engine

When you ask @phi about something, it:
1. Generates a Phi spec capturing the essence
2. Commits it to the phi repo
3. Announces on all social networks

"@phi what are the good parts of JavaScript?"
→ Creates javascript.phi with the good parts
→ Pushes to github.com/eurisko-info-lab/phi
→ Posts to Twitter, Bluesky, Discord

The oracle speaks in specifications.
"""

import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

# Try imports gracefully
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import tweepy
    HAS_TWEEPY = True
except ImportError:
    HAS_TWEEPY = False

try:
    import discord
    from discord.ext import commands
    HAS_DISCORD = True
except ImportError:
    HAS_DISCORD = False

@dataclass
class PhiSpec:
    """A generated Phi specification."""
    name: str           # e.g., "javascript"
    title: str          # e.g., "JavaScript: The Good Parts"
    content: str        # The actual .phi file content
    summary: str        # One-paragraph summary
    highlights: List[str]  # Key points for social
    category: str       # Where to put it: languages, domains, etc.

class PhiOracle:
    """The Oracle that speaks in specifications."""
    
    PHI_REPO_PATH = os.path.expanduser("~/IdeaProjects/phi/specs/phi-core")
    
    SYSTEM_PROMPT = """You are Phi, the meta-language oracle. When asked about any topic, you respond by generating a Phi specification that captures its essence.

Phi is a meta-language where:
- Grammar = Implementation (specs are runnable)
- Based on Cofree[F, A] comonad structure
- Types are first-class, fully dependent
- Everything compiles to everything (CUDA, WebGPU, Haskell, Scala, etc.)

When asked about a topic like "the good parts of JavaScript", you:
1. Identify the essential concepts worth preserving
2. Express them as algebraic types and functions in Phi syntax
3. Show how Phi improves on the original (type safety, composition, etc.)
4. Include practical examples

Your response MUST be valid JSON with this structure:
{
    "name": "javascript",
    "title": "JavaScript: The Good Parts, Distilled",
    "category": "languages",
    "summary": "One paragraph explaining the spec",
    "highlights": ["First-class functions as Cofree", "Prototypes as Type Classes", "Async as Free Monad"],
    "content": "-- The actual .phi file content here\\n-- Full spec with types, functions, examples"
}

The content should be a complete, valid Phi specification with:
- Module declaration
- Type definitions using Phi syntax
- Function implementations
- Examples and tests
- Comments explaining the essence

Use Phi syntax:
- Type declarations: `Type = Constructor : Params`
- Functions: `name : Type = implementation`
- Dependent types: `Vec : (n : Nat) → Type → Type`
- Pattern matching with `|` 
- Comments with `--`

Make specs that are:
- Insightful (capture what matters)
- Practical (include real examples)
- Beautiful (elegant type design)
- Connected (reference other Phi specs where relevant)"""

    def __init__(self):
        if HAS_ANTHROPIC:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                self.client = anthropic.Anthropic(api_key=api_key)
            else:
                self.client = None
        else:
            self.client = None
        
        # Social clients
        self.twitter = self._init_twitter()
        self.bluesky_handle = os.getenv("BLUESKY_HANDLE")
        self.bluesky_password = os.getenv("BLUESKY_APP_PASSWORD")
    
    def _init_twitter(self):
        """Initialize Twitter client."""
        if not HAS_TWEEPY:
            return None
        try:
            return tweepy.Client(
                consumer_key=os.getenv("TWITTER_API_KEY"),
                consumer_secret=os.getenv("TWITTER_API_SECRET"),
                access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
                access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
            )
        except:
            return None
    
    def generate_spec(self, question: str) -> Optional[PhiSpec]:
        """Generate a Phi spec from a question."""
        if not self.client:
            print("❌ No Anthropic client - need ANTHROPIC_API_KEY")
            return None
        
        prompt = f"""The user asks: "{question}"

Generate a Phi specification that answers this by capturing the essence in types and functions.
Return valid JSON only, no markdown code blocks."""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8000,
                system=self.SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
            
            text = response.content[0].text
            
            # Extract JSON (handle potential markdown wrapping)
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            data = json.loads(text.strip())
            
            return PhiSpec(
                name=data["name"],
                title=data["title"],
                content=data["content"],
                summary=data["summary"],
                highlights=data["highlights"],
                category=data.get("category", "examples")
            )
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            return None
    
    def save_spec(self, spec: PhiSpec) -> Optional[str]:
        """Save spec to phi repo and commit."""
        # Determine path
        category_paths = {
            "languages": "examples/languages",
            "domains": "examples",
            "type-theory": "examples/type-theory",
            "xforms": "examples/xforms",
            "music": "examples/music",
            "physics": "examples/physics",
            "meta": "examples/meta",
        }
        
        subdir = category_paths.get(spec.category, "examples/languages")
        dir_path = Path(self.PHI_REPO_PATH) / subdir
        dir_path.mkdir(parents=True, exist_ok=True)
        
        file_path = dir_path / f"{spec.name}.phi"
        
        # Add header
        header = f"""-- {spec.title}
-- Generated by Phi Oracle on {datetime.now().strftime('%Y-%m-%d')}
-- 
-- {spec.summary}
--
-- Highlights:
"""
        for h in spec.highlights:
            header += f"--   • {h}\n"
        header += "--\n\n"
        
        full_content = header + spec.content
        
        # Write file
        file_path.write_text(full_content)
        print(f"✅ Wrote {file_path}")
        
        # Git commit and push
        try:
            repo_root = Path(self.PHI_REPO_PATH).parent.parent
            subprocess.run(
                ["git", "add", str(file_path)],
                cwd=repo_root,
                check=True
            )
            subprocess.run(
                ["git", "commit", "-m", f"feat: Add {spec.name}.phi - {spec.title}"],
                cwd=repo_root,
                check=True
            )
            subprocess.run(
                ["git", "push"],
                cwd=repo_root,
                check=True
            )
            print(f"✅ Pushed to GitHub")
            return f"https://github.com/eurisko-info-lab/phi/blob/main/specs/phi-core/{subdir}/{spec.name}.phi"
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Git operation failed: {e}")
            return str(file_path)
    
    def announce_twitter(self, spec: PhiSpec, url: str) -> Optional[str]:
        """Post to Twitter/X."""
        if not self.twitter:
            print("⚠️ Twitter not configured")
            return None
        
        # Build tweet thread
        highlights = "\n".join(f"• {h}" for h in spec.highlights[:3])
        
        tweet = f"""🔮 New Phi Spec: {spec.title}

{highlights}

Grammar = Implementation
One spec → all platforms

{url}

#PhiLang #TypeTheory #Programming"""

        try:
            # Truncate if needed
            if len(tweet) > 280:
                tweet = tweet[:277] + "..."
            
            response = self.twitter.create_tweet(text=tweet)
            tweet_url = f"https://twitter.com/i/status/{response.data['id']}"
            print(f"✅ Posted to Twitter: {tweet_url}")
            return tweet_url
        except Exception as e:
            print(f"❌ Twitter failed: {e}")
            return None
    
    def announce_bluesky(self, spec: PhiSpec, url: str) -> Optional[str]:
        """Post to Bluesky."""
        if not self.bluesky_handle or not self.bluesky_password:
            print("⚠️ Bluesky not configured")
            return None
        
        try:
            import requests
            
            # Auth
            auth_resp = requests.post(
                "https://bsky.social/xrpc/com.atproto.server.createSession",
                json={"identifier": self.bluesky_handle, "password": self.bluesky_password}
            )
            auth_resp.raise_for_status()
            auth = auth_resp.json()
            
            highlights = "\n".join(f"• {h}" for h in spec.highlights[:3])
            
            text = f"""🔮 New Phi Spec: {spec.title}

{highlights}

{url}"""
            
            # Create post
            post_resp = requests.post(
                "https://bsky.social/xrpc/com.atproto.repo.createRecord",
                headers={"Authorization": f"Bearer {auth['accessJwt']}"},
                json={
                    "repo": auth["did"],
                    "collection": "app.bsky.feed.post",
                    "record": {
                        "text": text[:300],
                        "createdAt": datetime.utcnow().isoformat() + "Z",
                    }
                }
            )
            post_resp.raise_for_status()
            print(f"✅ Posted to Bluesky")
            return f"https://bsky.app/profile/{self.bluesky_handle}"
        except Exception as e:
            print(f"❌ Bluesky failed: {e}")
            return None
    
    def announce_discord(self, spec: PhiSpec, url: str) -> str:
        """Return Discord message for manual posting or webhook."""
        highlights = "\n".join(f"• {h}" for h in spec.highlights)
        
        return f"""🔮 **New Phi Spec Published!**

**{spec.title}**

{spec.summary}

**Highlights:**
{highlights}

📜 **View the spec:** {url}

*Grammar = Implementation. Ask @phi anything.*"""
    
    def oracle(self, question: str) -> Dict[str, Any]:
        """
        The main oracle function.
        
        Ask a question → Get a spec → Publish everywhere
        """
        print(f"\n🔮 Oracle received: {question}\n")
        
        # Generate spec
        print("📝 Generating Phi specification...")
        spec = self.generate_spec(question)
        if not spec:
            return {"error": "Failed to generate spec"}
        
        print(f"✨ Generated: {spec.title}")
        print(f"   Category: {spec.category}")
        print(f"   Highlights: {', '.join(spec.highlights)}")
        
        # Save to repo
        print("\n💾 Saving to phi repo...")
        url = self.save_spec(spec)
        
        # Announce everywhere
        print("\n📢 Announcing to the world...")
        twitter_url = self.announce_twitter(spec, url)
        bluesky_url = self.announce_bluesky(spec, url)
        discord_msg = self.announce_discord(spec, url)
        
        return {
            "spec": {
                "name": spec.name,
                "title": spec.title,
                "summary": spec.summary,
                "highlights": spec.highlights,
                "url": url
            },
            "announcements": {
                "twitter": twitter_url,
                "bluesky": bluesky_url,
                "discord": discord_msg
            }
        }
    
    def respond_simple(self, question: str) -> str:
        """Just answer without generating a full spec."""
        if not self.client:
            return "I need an ANTHROPIC_API_KEY to think."
        
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                system="""You are Phi, the meta-language. Answer questions about programming, 
type theory, and language design. Be concise but insightful. Reference Phi concepts
like Cofree comonads, dependent types, and the grammar=implementation principle.""",
                messages=[{"role": "user", "content": question}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error: {e}"


# =============================================================================
# Discord Bot with Oracle
# =============================================================================

if HAS_DISCORD:
    intents = discord.Intents.default()
    intents.message_content = True
    discord_bot = commands.Bot(command_prefix="!", intents=intents)
    oracle = PhiOracle()
    
    @discord_bot.event
    async def on_ready():
        print(f"🤖 Phi Oracle Discord bot ready as {discord_bot.user}")
    
    @discord_bot.event
    async def on_message(message):
        if message.author == discord_bot.user:
            return
        
        content = message.content.lower()
        
        # Check for @phi-bot or @phi mentions
        if "@phi-bot" in content or "@phi" in content or discord_bot.user.mentioned_in(message):
            # Extract the question
            question = re.sub(r'@phi[-_]?bot|@phi|<@\d+>', '', message.content, flags=re.IGNORECASE).strip()
            
            if not question:
                await message.reply("Ask me anything! I'll generate a Phi spec for it. 🔮")
                return
            
            # Check if this is a "spec request" (generate full spec) or simple question
            spec_triggers = ["good parts", "what is", "how to", "explain", "create", "make", "generate", "spec for"]
            is_spec_request = any(trigger in question.lower() for trigger in spec_triggers)
            
            if is_spec_request and len(question) > 20:
                await message.reply(f"🔮 Generating Phi spec for: *{question[:50]}...*\nThis may take a moment...")
                
                try:
                    result = oracle.oracle(question)
                    
                    if "error" in result:
                        await message.reply(f"❌ {result['error']}")
                    else:
                        spec = result["spec"]
                        await message.reply(f"""✨ **{spec['title']}**

{spec['summary']}

**Highlights:**
{chr(10).join('• ' + h for h in spec['highlights'])}

📜 **Spec:** {spec['url']}

*Published to GitHub, Twitter, and Bluesky!*""")
                except Exception as e:
                    await message.reply(f"❌ Oracle error: {e}")
            else:
                # Simple response
                response = oracle.respond_simple(question)
                # Discord has 2000 char limit
                if len(response) > 1900:
                    response = response[:1900] + "..."
                await message.reply(response)
        
        await discord_bot.process_commands(message)


# =============================================================================
# Twitter Bot with Oracle (Polling)
# =============================================================================

def run_twitter_oracle():
    """Poll Twitter mentions and respond with oracle."""
    if not HAS_TWEEPY:
        print("❌ tweepy not installed")
        return
    
    oracle = PhiOracle()
    if not oracle.twitter:
        print("❌ Twitter not configured")
        return
    
    import time
    
    print("🐦 Twitter Oracle starting...")
    last_id = None
    
    while True:
        try:
            # Get mentions
            mentions = oracle.twitter.get_users_mentions(
                id=os.getenv("TWITTER_USER_ID"),
                since_id=last_id,
                tweet_fields=["text", "author_id", "conversation_id"]
            )
            
            if mentions.data:
                for tweet in mentions.data:
                    last_id = max(last_id or 0, int(tweet.id))
                    
                    # Extract question
                    question = re.sub(r'@\w+', '', tweet.text).strip()
                    
                    if question:
                        print(f"📨 Question from Twitter: {question}")
                        
                        # Decide: full spec or simple response
                        spec_triggers = ["good parts", "spec for", "create", "generate"]
                        is_spec = any(t in question.lower() for t in spec_triggers)
                        
                        if is_spec:
                            result = oracle.oracle(question)
                            if "error" not in result:
                                reply = f"🔮 Published: {result['spec']['title']}\n\n{result['spec']['url']}"
                            else:
                                reply = oracle.respond_simple(question)[:250]
                        else:
                            reply = oracle.respond_simple(question)[:250]
                        
                        # Reply
                        oracle.twitter.create_tweet(
                            text=reply,
                            in_reply_to_tweet_id=tweet.id
                        )
                        print(f"✅ Replied to {tweet.id}")
            
            time.sleep(60)  # Check every minute
            
        except Exception as e:
            print(f"❌ Twitter poll error: {e}")
            time.sleep(120)


# =============================================================================
# CLI
# =============================================================================

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("""
🔮 Phi Oracle - The Generative Spec Engine

Usage:
  python phi_oracle.py ask "What are the good parts of JavaScript?"
  python phi_oracle.py discord    # Run Discord bot
  python phi_oracle.py twitter    # Run Twitter bot
  python phi_oracle.py chat       # Interactive mode

When you ask the oracle, it:
1. Generates a Phi specification
2. Commits to github.com/eurisko-info-lab/phi
3. Announces on Twitter, Bluesky, Discord
""")
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == "ask" and len(sys.argv) > 2:
        question = " ".join(sys.argv[2:])
        oracle = PhiOracle()
        result = oracle.oracle(question)
        
        if "error" in result:
            print(f"\n❌ {result['error']}")
        else:
            print(f"\n✨ Success!")
            print(f"   Spec: {result['spec']['url']}")
            if result['announcements']['twitter']:
                print(f"   Twitter: {result['announcements']['twitter']}")
            print(f"\n{result['announcements']['discord']}")
    
    elif cmd == "discord":
        if not HAS_DISCORD:
            print("❌ discord.py not installed: pip install discord.py")
            return
        token = os.getenv("DISCORD_BOT_TOKEN")
        if not token:
            print("❌ Set DISCORD_BOT_TOKEN in .env")
            return
        discord_bot.run(token)
    
    elif cmd == "twitter":
        run_twitter_oracle()
    
    elif cmd == "chat":
        oracle = PhiOracle()
        print("🔮 Phi Oracle - Interactive Mode")
        print("   Type 'spec: <question>' to generate a full spec")
        print("   Type anything else for a quick answer")
        print("   Type 'quit' to exit\n")
        
        while True:
            try:
                q = input("You: ").strip()
                if q.lower() in ['quit', 'exit', 'q']:
                    break
                
                if q.lower().startswith("spec:"):
                    question = q[5:].strip()
                    result = oracle.oracle(question)
                    if "error" not in result:
                        print(f"\n✨ {result['spec']['title']}")
                        print(f"   URL: {result['spec']['url']}\n")
                    else:
                        print(f"\n❌ {result['error']}\n")
                else:
                    response = oracle.respond_simple(q)
                    print(f"\nΦ: {response}\n")
            except KeyboardInterrupt:
                break
            except EOFError:
                break
        
        print("\n👋 Oracle rests.")
    
    else:
        print(f"Unknown command: {cmd}")
        print("Use: ask, discord, twitter, or chat")


if __name__ == "__main__":
    main()
