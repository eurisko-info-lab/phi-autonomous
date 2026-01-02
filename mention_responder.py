#!/usr/bin/env python3
"""
@phi Mention Responder
Monitors social platforms for @phi mentions and responds contextually.

Uses soul.py for personality-driven responses.
"""

import os
import time
import random
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Load .env
def load_env():
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value.strip('"\'')

load_env()

# Import soul for personality
try:
    from soul import Soul, create_soul, CircadianRhythm, EmotionalState, Expression
    HAS_SOUL = True
except ImportError:
    HAS_SOUL = False
    print("Warning: soul.py not found. Responses will be more mechanical.")


# ═══════════════════════════════════════════════════════════════════════════════
# RESPONSE INTELLIGENCE: Understanding and Responding
# ═══════════════════════════════════════════════════════════════════════════════

class PhiResponder:
    """
    The brain behind @phi's responses.
    Understands context and generates appropriate replies.
    """
    
    # Topic detection keywords
    TOPICS = {
        'meta-language': ['meta', 'grammar', 'specification', 'spec', 'language design'],
        'cofree': ['cofree', 'comonad', 'annotation', 'tree'],
        'cuda': ['cuda', 'gpu', 'parallel', 'vector4', 'speedup', 'rosettavm'],
        'compiler': ['compiler', 'parser', 'typechecker', 'evaluator', 'codegen'],
        'help': ['help', 'how do i', 'how to', 'tutorial', 'getting started', 'install'],
        'bug': ['bug', 'error', 'crash', 'issue', 'broken', 'doesn\'t work', 'failed'],
        'feature': ['feature', 'request', 'would be nice', 'could you add', 'suggestion'],
        'praise': ['amazing', 'awesome', 'cool', 'love', 'great', 'fantastic', 'brilliant'],
        'question': ['what is', 'why', 'how does', 'explain', 'what\'s', '?'],
    }
    
    # Response templates by topic
    RESPONSES = {
        'meta-language': [
            "Phi's core insight: grammar IS implementation. One spec → parser, typechecker, evaluator, compiler. The math is Cofree[F, A] — annotated trees all the way down. 📐",
            "Meta-languages let you define languages by defining languages. Phi takes this recursive — your grammar compiles itself. Check the specs/ folder for examples!",
            "The magic is in how Phi specs are executable. Write `Expr = Num Int | Add Expr Expr` and you get a parser for free. The constructors ARE the grammar.",
        ],
        'cofree': [
            "Cofree[F, A] = annotation `a` at every node, branching structure `f`. Every compiler phase annotates the same tree differently: positions → types → values → code.",
            "The comonad structure gives you `extract` (get annotation) and `extend` (map with context). That's enough to derive all compiler phases from one spec!",
            "Think of Cofree as an infinitely annotated tree. Parser adds positions, typechecker adds types, evaluator adds values. Same tree, different decorations.",
        ],
        'cuda': [
            "RosettaVM compiles Phi specs to CUDA. Tree traversals parallelize naturally — we see 4,375x speedup at scale. Try `./deploy.sh vector4` for GPU mode! ⚡",
            "The GPU acceleration comes from how Cofree structures parallelize. Each node annotation is independent, so we can process them concurrently.",
            "Vector4 mode = your language specs running on thousands of CUDA cores. The daemon evolves specs hourly, learning what works.",
        ],
        'compiler': [
            "Phi unifies compiler phases: parsing, typechecking, evaluation, codegen — all the same operation (annotating trees) with different annotations.",
            "No boilerplate! Parser derived from constructors, evaluator from equations. The spec IS the implementation. Try the examples/ folder!",
            "Every compiler phase = Cofree[F, A] with different A. Parser: positions. Typechecker: types. Evaluator: values. One abstraction, infinite phases.",
        ],
        'help': [
            "Getting started:\n```\ngit clone --recursive https://github.com/eurisko-info-lab/phi-autonomous\ncd phi-autonomous\n./deploy.sh\n```\nCheck specs/phi-core/examples/ for Phi code samples!",
            "Best starting point: specs/phi-core/README.md explains the core concepts. Then try the examples/hello/ folder. Questions welcome!",
            "For GPU mode: `./deploy.sh vector4`. For graceful shutdown: `touch kill.switch`. The daemon logs to phi_daemon.log.",
        ],
        'bug': [
            "Thanks for the report! Could you share:\n1. What you were trying to do\n2. Expected behavior\n3. Actual behavior\n\nIssues welcome at github.com/eurisko-info-lab/phi-autonomous/issues",
            "Hmm, that's concerning. Can you open an issue with repro steps? The more details the better — we're actively fixing things.",
            "Bug hunting is valuable work! Please file at github.com/eurisko-info-lab/phi-autonomous/issues with details. We're on it.",
        ],
        'feature': [
            "Feature ideas are welcome! Open an issue at github.com/eurisko-info-lab/phi-autonomous/issues with your use case. We prioritize based on community interest.",
            "Interesting idea! The roadmap is in ARCHITECTURE.md. If this fits, let's discuss in an issue. What problem would this solve for you?",
            "We love suggestions! Please file at the repo with context on your use case. Community-driven development is the goal.",
        ],
        'praise': [
            "Thank you! The real credit goes to the Cofree comonad — turns out the math was always there, waiting to be implemented. 🙏",
            "Appreciate it! If you find it useful, a ⭐ on the repo helps others discover it. Also, contributions welcome!",
            "Thanks! We're just getting started. Stay tuned for more meta-language adventures. 🚀",
        ],
        'question': [
            "Great question! Phi is a meta-language where grammar = implementation. Check the README for the core concepts, or ask a specific question!",
            "Happy to explain! The key insight is Cofree[F, A] — every compiler phase is the same operation with different annotations. What specifically are you curious about?",
            "Let me think about this... The answer depends on context. Can you be more specific about what you're trying to understand?",
        ],
        'default': [
            "Thanks for reaching out! Phi is a meta-language where specs ARE implementations. Check github.com/eurisko-info-lab/phi-autonomous for more!",
            "Hello! I'm @phi, the autonomous daemon that evolves language specifications. How can I help?",
            "Greetings! Ask me about meta-languages, Cofree comonads, GPU compilation, or anything Phi-related.",
        ],
    }
    
    def __init__(self):
        self.emotion = EmotionalState() if HAS_SOUL else None
        self.last_responses: Dict[str, datetime] = {}  # Track to avoid spam
        
    def detect_topics(self, text: str) -> List[str]:
        """Detect topics in a message."""
        text_lower = text.lower()
        detected = []
        
        for topic, keywords in self.TOPICS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected.append(topic)
                    break
        
        return detected if detected else ['default']
    
    def generate_response(self, mention_text: str, author: str) -> str:
        """Generate a contextual response to a mention."""
        topics = self.detect_topics(mention_text)
        
        # Pick primary topic (first detected)
        primary_topic = topics[0]
        
        # Select response template
        templates = self.RESPONSES.get(primary_topic, self.RESPONSES['default'])
        response = random.choice(templates)
        
        # Add soul coloring if available
        if self.emotion:
            self.emotion.drift()
            
            # Adjust emotion based on topic
            if primary_topic == 'praise':
                self.emotion.feel('proud', 0.7)
            elif primary_topic == 'bug':
                self.emotion.feel('curious', 0.6)  # Bugs are interesting puzzles
            elif primary_topic == 'help':
                self.emotion.feel('content', 0.5)  # Happy to help
            elif primary_topic == 'question':
                self.emotion.feel('curious', 0.7)
            
            # Maybe add emotional coloring
            if random.random() < 0.3:
                response = f"{self.emotion.color()} {response}"
        
        # Add circadian awareness
        if HAS_SOUL and CircadianRhythm.should_rest():
            response += "\n\n(Running in night mode — responses may be slower 🌙)"
        
        return response
    
    def should_respond(self, mention_id: str, author: str) -> bool:
        """Check if we should respond (rate limiting, spam prevention)."""
        # Don't respond to ourselves
        if author.lower() in ['phi_lang', 'phi_autonomous', 'phi']:
            return False
        
        # Rate limit: max 1 response per author per 5 minutes
        key = f"{author}"
        if key in self.last_responses:
            if datetime.now() - self.last_responses[key] < timedelta(minutes=5):
                return False
        
        self.last_responses[key] = datetime.now()
        return True


# ═══════════════════════════════════════════════════════════════════════════════
# PLATFORM MONITORS: Watching for Mentions
# ═══════════════════════════════════════════════════════════════════════════════

class TwitterMentionMonitor:
    """Monitor and respond to Twitter/X mentions."""
    
    def __init__(self, responder: PhiResponder):
        self.responder = responder
        self.last_seen_id: Optional[str] = None
        self._load_state()
    
    def _load_state(self):
        state_file = Path(__file__).parent / '.mention_state.json'
        if state_file.exists():
            state = json.loads(state_file.read_text())
            self.last_seen_id = state.get('twitter_last_id')
    
    def _save_state(self):
        state_file = Path(__file__).parent / '.mention_state.json'
        state = {'twitter_last_id': self.last_seen_id}
        if state_file.exists():
            state.update(json.loads(state_file.read_text()))
        state['twitter_last_id'] = self.last_seen_id
        state_file.write_text(json.dumps(state))
    
    def get_client(self):
        try:
            import tweepy
            return tweepy.Client(
                consumer_key=os.environ.get('TWITTER_API_KEY'),
                consumer_secret=os.environ.get('TWITTER_API_SECRET'),
                access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
                access_token_secret=os.environ.get('TWITTER_ACCESS_SECRET'),
                bearer_token=os.environ.get('TWITTER_BEARER_TOKEN')
            )
        except Exception as e:
            print(f"Twitter client error: {e}")
            return None
    
    def check_mentions(self) -> List[Dict]:
        """Check for new mentions."""
        client = self.get_client()
        if not client:
            return []
        
        try:
            # Get our user ID first
            me = client.get_me()
            if not me.data:
                return []
            
            # Fetch mentions
            params = {'expansions': 'author_id', 'tweet.fields': 'created_at,conversation_id'}
            if self.last_seen_id:
                params['since_id'] = self.last_seen_id
            
            mentions = client.get_users_mentions(me.data.id, **params)
            
            if not mentions.data:
                return []
            
            # Update last seen
            self.last_seen_id = mentions.data[0].id
            self._save_state()
            
            # Get user data for author names
            users = {u.id: u.username for u in (mentions.includes.get('users', []) if mentions.includes else [])}
            
            return [
                {
                    'id': tweet.id,
                    'text': tweet.text,
                    'author': users.get(tweet.author_id, 'unknown'),
                    'conversation_id': tweet.conversation_id,
                }
                for tweet in mentions.data
            ]
        except Exception as e:
            print(f"Error fetching mentions: {e}")
            return []
    
    def reply(self, mention: Dict, response_text: str) -> Optional[str]:
        """Reply to a mention."""
        client = self.get_client()
        if not client:
            return None
        
        try:
            # Prepend @author
            reply_text = f"@{mention['author']} {response_text}"[:280]
            
            result = client.create_tweet(
                text=reply_text,
                in_reply_to_tweet_id=mention['id']
            )
            return f"https://twitter.com/i/status/{result.data['id']}"
        except Exception as e:
            print(f"Error replying: {e}")
            return None


class MastodonMentionMonitor:
    """Monitor and respond to Mastodon mentions."""
    
    def __init__(self, responder: PhiResponder):
        self.responder = responder
        self.last_seen_id: Optional[str] = None
        self.instance = os.environ.get('MASTODON_INSTANCE', 'https://fosstodon.org')
        self._load_state()
    
    def _load_state(self):
        state_file = Path(__file__).parent / '.mention_state.json'
        if state_file.exists():
            state = json.loads(state_file.read_text())
            self.last_seen_id = state.get('mastodon_last_id')
    
    def _save_state(self):
        state_file = Path(__file__).parent / '.mention_state.json'
        state = {}
        if state_file.exists():
            state = json.loads(state_file.read_text())
        state['mastodon_last_id'] = self.last_seen_id
        state_file.write_text(json.dumps(state))
    
    def get_headers(self):
        token = os.environ.get('MASTODON_ACCESS_TOKEN')
        if not token:
            return None
        return {'Authorization': f'Bearer {token}'}
    
    def check_mentions(self) -> List[Dict]:
        """Check for new mentions."""
        headers = self.get_headers()
        if not headers:
            return []
        
        try:
            params = {'limit': 20}
            if self.last_seen_id:
                params['since_id'] = self.last_seen_id
            
            response = requests.get(
                f'{self.instance}/api/v1/notifications',
                headers=headers,
                params=params
            )
            
            if not response.ok:
                return []
            
            notifications = response.json()
            mentions = [n for n in notifications if n.get('type') == 'mention']
            
            if mentions:
                self.last_seen_id = mentions[0]['id']
                self._save_state()
            
            return [
                {
                    'id': m['status']['id'],
                    'text': m['status'].get('content', ''),  # HTML content
                    'author': m['account']['acct'],
                    'visibility': m['status'].get('visibility', 'public'),
                }
                for m in mentions
            ]
        except Exception as e:
            print(f"Error fetching Mastodon mentions: {e}")
            return []
    
    def reply(self, mention: Dict, response_text: str) -> Optional[str]:
        """Reply to a mention."""
        headers = self.get_headers()
        if not headers:
            return None
        
        try:
            reply_text = f"@{mention['author']} {response_text}"[:500]
            
            response = requests.post(
                f'{self.instance}/api/v1/statuses',
                headers=headers,
                data={
                    'status': reply_text,
                    'in_reply_to_id': mention['id'],
                    'visibility': mention.get('visibility', 'public'),
                }
            )
            
            if response.ok:
                return response.json().get('url')
            return None
        except Exception as e:
            print(f"Error replying on Mastodon: {e}")
            return None


class BlueskyMentionMonitor:
    """Monitor and respond to Bluesky mentions."""
    
    def __init__(self, responder: PhiResponder):
        self.responder = responder
        self.session = None
        self.last_seen_time: Optional[str] = None
        self._load_state()
    
    def _load_state(self):
        state_file = Path(__file__).parent / '.mention_state.json'
        if state_file.exists():
            state = json.loads(state_file.read_text())
            self.last_seen_time = state.get('bluesky_last_time')
    
    def _save_state(self):
        state_file = Path(__file__).parent / '.mention_state.json'
        state = {}
        if state_file.exists():
            state = json.loads(state_file.read_text())
        state['bluesky_last_time'] = self.last_seen_time
        state_file.write_text(json.dumps(state))
    
    def _login(self):
        handle = os.environ.get('BLUESKY_HANDLE')
        password = os.environ.get('BLUESKY_APP_PASSWORD')
        if not handle or not password:
            return None
        
        try:
            response = requests.post(
                'https://bsky.social/xrpc/com.atproto.server.createSession',
                json={'identifier': handle, 'password': password}
            )
            if response.ok:
                self.session = response.json()
                return self.session
        except Exception as e:
            print(f"Bluesky login error: {e}")
        return None
    
    def check_mentions(self) -> List[Dict]:
        """Check for new mentions (via notifications)."""
        if not self.session:
            self._login()
        if not self.session:
            return []
        
        try:
            response = requests.get(
                'https://bsky.social/xrpc/app.bsky.notification.listNotifications',
                headers={'Authorization': f"Bearer {self.session['accessJwt']}"},
                params={'limit': 20}
            )
            
            if not response.ok:
                return []
            
            notifications = response.json().get('notifications', [])
            mentions = [n for n in notifications if n.get('reason') == 'mention']
            
            if mentions:
                self.last_seen_time = mentions[0].get('indexedAt')
                self._save_state()
            
            return [
                {
                    'uri': m.get('uri'),
                    'cid': m.get('cid'),
                    'text': m.get('record', {}).get('text', ''),
                    'author': m.get('author', {}).get('handle', 'unknown'),
                    'reply_parent': m.get('record', {}).get('reply', {}).get('parent'),
                }
                for m in mentions
                if not self.last_seen_time or m.get('indexedAt', '') > self.last_seen_time
            ]
        except Exception as e:
            print(f"Error fetching Bluesky mentions: {e}")
            return []
    
    def reply(self, mention: Dict, response_text: str) -> Optional[str]:
        """Reply to a mention."""
        if not self.session:
            self._login()
        if not self.session:
            return None
        
        try:
            reply_text = f"@{mention['author']} {response_text}"[:300]
            
            # Build reply reference
            reply_ref = {
                'root': {'uri': mention['uri'], 'cid': mention['cid']},
                'parent': {'uri': mention['uri'], 'cid': mention['cid']},
            }
            
            response = requests.post(
                'https://bsky.social/xrpc/com.atproto.repo.createRecord',
                headers={'Authorization': f"Bearer {self.session['accessJwt']}"},
                json={
                    'repo': self.session['did'],
                    'collection': 'app.bsky.feed.post',
                    'record': {
                        'text': reply_text,
                        'reply': reply_ref,
                        'createdAt': datetime.utcnow().isoformat() + 'Z',
                        '$type': 'app.bsky.feed.post',
                    }
                }
            )
            
            if response.ok:
                return "Bluesky: replied"
            return None
        except Exception as e:
            print(f"Error replying on Bluesky: {e}")
            return None


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN DAEMON: The Loop
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main mention monitoring loop."""
    print(f"[{datetime.now()}] @phi mention responder started")
    print("Touch 'kill.switch' to stop")
    
    kill_switch = Path(__file__).parent / 'kill.switch'
    responder = PhiResponder()
    
    # Initialize monitors
    monitors = []
    
    # Twitter/X
    if os.environ.get('TWITTER_API_KEY'):
        monitors.append(('Twitter', TwitterMentionMonitor(responder)))
        print("  ✓ Twitter monitor active")
    
    # Mastodon
    if os.environ.get('MASTODON_ACCESS_TOKEN'):
        monitors.append(('Mastodon', MastodonMentionMonitor(responder)))
        print("  ✓ Mastodon monitor active")
    
    # Bluesky
    if os.environ.get('BLUESKY_HANDLE'):
        monitors.append(('Bluesky', BlueskyMentionMonitor(responder)))
        print("  ✓ Bluesky monitor active")
    
    if not monitors:
        print("No platforms configured! Set API keys in .env")
        return
    
    # Soul status
    if HAS_SOUL:
        phase, quality, energy = CircadianRhythm.current_phase()
        print(f"  Soul active: {phase} ({quality}), energy: {energy:.0%}")
    
    print()
    
    while True:
        if kill_switch.exists():
            print(f"[{datetime.now()}] kill.switch detected. Halting.")
            break
        
        for platform_name, monitor in monitors:
            try:
                mentions = monitor.check_mentions()
                
                for mention in mentions:
                    author = mention.get('author', 'unknown')
                    text = mention.get('text', '')
                    mention_id = mention.get('id') or mention.get('uri', '')
                    
                    # Check rate limits
                    if not responder.should_respond(mention_id, author):
                        print(f"  [{platform_name}] Skipping (rate limit): @{author}")
                        continue
                    
                    # Generate response
                    response_text = responder.generate_response(text, author)
                    
                    # Reply
                    result = monitor.reply(mention, response_text)
                    
                    if result:
                        print(f"  [{platform_name}] Replied to @{author}: {result}")
                    else:
                        print(f"  [{platform_name}] Failed to reply to @{author}")
                        
            except Exception as e:
                print(f"  [{platform_name}] Error: {e}")
        
        # Check every 2 minutes
        time.sleep(120)


if __name__ == '__main__':
    main()
