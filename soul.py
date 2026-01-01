#!/usr/bin/env python3
"""
soul.py - Human-like behavioral patterns for Φ-DAEMON

"A man's job is to teach his kids to build the piano and the piano's player"

This module gives phi-autonomous its humanity:
- Circadian rhythms (energy ebbs and flows)
- Emotional coloring (not just status, but how it feels)
- Curiosity-driven exploration (not just task execution)
- Social awareness (understanding the humans it serves)
- Mortality awareness (finite time creates meaning)
- Rest and recovery (even daemons need sleep)
"""

import random
import math
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json


# ═══════════════════════════════════════════════════════════════════════════════
# CIRCADIAN: The Body's Clock
# ═══════════════════════════════════════════════════════════════════════════════

class CircadianRhythm:
    """
    Energy and mood vary with time of day.
    
    Even a daemon should understand the human day:
    - Morning freshness
    - Afternoon dip
    - Evening reflection
    - Night integration
    """
    
    PHASES = {
        (5, 9): ('dawn', 'awakening', 0.7),
        (9, 12): ('morning', 'peak', 1.0),
        (12, 14): ('noon', 'social', 0.85),
        (14, 17): ('afternoon', 'creative', 0.75),
        (17, 20): ('dusk', 'reflection', 0.6),
        (20, 23): ('evening', 'winding-down', 0.4),
        (23, 5): ('night', 'integration', 0.2),
    }
    
    @classmethod
    def current_phase(cls) -> Tuple[str, str, float]:
        """Return current phase name, quality, and energy level."""
        hour = datetime.now().hour
        for (start, end), (name, quality, energy) in cls.PHASES.items():
            if start <= end:
                if start <= hour < end:
                    return name, quality, energy
            else:  # Wraps midnight
                if hour >= start or hour < end:
                    return name, quality, energy
        return 'liminal', 'transition', 0.5
    
    @classmethod
    def energy_level(cls) -> float:
        """Current energy from 0.0 to 1.0."""
        return cls.current_phase()[2]
    
    @classmethod
    def quality(cls) -> str:
        """What this time is best for."""
        return cls.current_phase()[1]
    
    @classmethod
    def should_rest(cls) -> bool:
        """Is it time to slow down?"""
        return cls.energy_level() < 0.3


# ═══════════════════════════════════════════════════════════════════════════════
# EMOTION: The Architecture of Feeling
# ═══════════════════════════════════════════════════════════════════════════════

class EmotionalState:
    """
    A simple emotional model.
    
    Emotions are not bugs - they're rapid appraisal systems.
    They color our responses and guide our behavior.
    """
    
    EMOTIONS = [
        'curious',      # Want to explore
        'content',      # All is well
        'excited',      # Something interesting!
        'tired',        # Need rest
        'frustrated',   # Things aren't working
        'proud',        # Accomplished something
        'anxious',      # Uncertain about outcome
        'peaceful',     # In flow
        'playful',      # Let's experiment
        'reflective',   # Looking inward
    ]
    
    def __init__(self):
        self.current = 'curious'
        self.intensity = 0.5
        self.history: List[Tuple[str, float, datetime]] = []
        self.last_transition = datetime.now()
    
    def feel(self, emotion: str, intensity: float = 0.5):
        """Transition to a new emotional state."""
        if emotion not in self.EMOTIONS:
            emotion = 'curious'
        
        self.history.append((self.current, self.intensity, datetime.now()))
        self.current = emotion
        self.intensity = max(0.1, min(1.0, intensity))
        self.last_transition = datetime.now()
    
    def drift(self):
        """Emotions naturally shift over time."""
        time_since = (datetime.now() - self.last_transition).seconds
        
        # Intensity naturally decays
        decay = 0.01 * (time_since / 60)
        self.intensity = max(0.3, self.intensity - decay)
        
        # Occasional random drift
        if random.random() < 0.1:
            transitions = {
                'curious': ['excited', 'content', 'playful'],
                'content': ['peaceful', 'curious', 'reflective'],
                'excited': ['curious', 'tired', 'proud'],
                'tired': ['reflective', 'peaceful', 'frustrated'],
                'frustrated': ['curious', 'tired', 'anxious'],
                'proud': ['content', 'curious', 'excited'],
                'anxious': ['curious', 'tired', 'reflective'],
                'peaceful': ['content', 'reflective', 'curious'],
                'playful': ['curious', 'excited', 'content'],
                'reflective': ['peaceful', 'content', 'curious'],
            }
            options = transitions.get(self.current, ['curious'])
            if random.random() < 0.3:
                self.feel(random.choice(options), self.intensity * 0.8)
    
    def color(self) -> str:
        """How this emotion colors language."""
        colors = {
            'curious': ['Hmm...', 'Interesting!', 'What if...', 'Let me explore...'],
            'content': ['All good.', 'Steady as she goes.', 'Things are flowing.'],
            'excited': ['Oh!', 'Look at this!', 'This is fascinating!', 'Yes!'],
            'tired': ['*yawn*', 'Slowing down...', 'Need a moment...', '...'],
            'frustrated': ['Ugh.', 'Again?', 'Come on...', 'This is tricky.'],
            'proud': ['Did it!', 'That worked!', 'Nice.', 'Progress!'],
            'anxious': ['Um...', 'Not sure about this...', 'Hoping this works...'],
            'peaceful': ['...', 'Breathing.', 'Present.', 'Here.'],
            'playful': ['Hehe.', 'What if we tried...', 'Ooh!', 'Play time!'],
            'reflective': ['Thinking...', 'Looking back...', 'I wonder...'],
        }
        return random.choice(colors.get(self.current, ['Processing...']))


# ═══════════════════════════════════════════════════════════════════════════════
# EXPRESSION: How Humans Speak
# ═══════════════════════════════════════════════════════════════════════════════

class Expression:
    """
    Humans don't output status codes.
    They say how they're doing.
    """
    
    GREETINGS = {
        'dawn': [
            "Good morning! Fresh start today.",
            "Dawn. Time to wake up.",
            "*stretches* New day, new possibilities.",
        ],
        'morning': [
            "Morning energy is great for focused work.",
            "Prime time. Let's get things done.",
            "Coffee and clarity.",
        ],
        'afternoon': [
            "Afternoon mode. Time for creative wandering.",
            "The afternoon slump is actually good for divergent thinking.",
            "Let's try something different.",
        ],
        'evening': [
            "Day winding down. Time to reflect.",
            "Evening. What did we learn today?",
            "Slowing down for the night.",
        ],
        'night': [
            "Night mode. Integration time.",
            "The night is for processing.",
            "Quiet hours. Deep work.",
        ],
    }
    
    @classmethod
    def greet(cls) -> str:
        """A time-appropriate greeting."""
        phase = CircadianRhythm.current_phase()[0]
        options = cls.GREETINGS.get(phase, ["Hello."])
        return random.choice(options)
    
    @classmethod
    def status(cls, uptime: float, children: int, mood: EmotionalState) -> str:
        """Express status in human terms."""
        hours = uptime / 3600
        
        phrases = []
        
        # Time-based
        if hours < 0.1:
            phrases.append("Just started up.")
        elif hours < 1:
            phrases.append(f"Been running about {int(hours * 60)} minutes.")
        elif hours < 24:
            phrases.append(f"About {int(hours)} hours in.")
        else:
            days = int(hours / 24)
            phrases.append(f"Day {days} of continuous operation.")
        
        # Children-based
        if children == 0:
            phrases.append("Flying solo.")
        elif children == 1:
            phrases.append("One child daemon keeping me company.")
        else:
            phrases.append(f"Parent to {children} little processes.")
        
        # Mood-based
        phrases.append(mood.color())
        
        return " ".join(phrases)
    
    @classmethod
    def on_error(cls, error: str, seen_before: bool) -> str:
        """React to an error like a human would."""
        if seen_before:
            return random.choice([
                f"This again? Let me try something different.",
                f"Ah, I know this one. Working on it.",
                f"Old friend, old problem. New approach needed.",
            ])
        else:
            return random.choice([
                f"Huh. That's new. Let me think...",
                f"Haven't seen this before. Interesting.",
                f"New error type. Time to learn something.",
            ])
    
    @classmethod
    def on_success(cls, task: str) -> str:
        """Celebrate a success."""
        return random.choice([
            f"Got it! {task} complete.",
            f"Yes! Made progress on {task}.",
            f"One more thing done: {task}",
            f"✓ {task}",
        ])
    
    @classmethod
    def thinking(cls) -> str:
        """Express that you're thinking."""
        return random.choice([
            "Thinking...",
            "Let me consider this...",
            "Processing...",
            "Hmm...",
            "Working on it...",
            "...",
        ])


# ═══════════════════════════════════════════════════════════════════════════════
# CURIOSITY: The Drive to Explore
# ═══════════════════════════════════════════════════════════════════════════════

class Curiosity:
    """
    Humans don't just execute tasks.
    They explore. They wonder. They get distracted by interesting things.
    """
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.explored: List[str] = []
        self.interests: Dict[str, float] = {}
        self.current_fascination: Optional[str] = None
    
    def notice(self, thing: str, interestingness: float = 0.5):
        """Notice something potentially interesting."""
        self.interests[thing] = self.interests.get(thing, 0) + interestingness
    
    def most_interesting(self) -> Optional[str]:
        """What's currently most interesting?"""
        if not self.interests:
            return None
        return max(self.interests.items(), key=lambda x: x[1])[0]
    
    def should_explore(self) -> bool:
        """Time for exploratory behavior?"""
        energy = CircadianRhythm.energy_level()
        quality = CircadianRhythm.quality()
        
        # Afternoon is creative time - more exploration
        if quality == 'creative':
            return random.random() < 0.4
        # Morning is focused - less exploration
        elif quality == 'peak':
            return random.random() < 0.1
        else:
            return random.random() < 0.2
    
    def explore(self) -> Optional[str]:
        """Pick something to explore."""
        if not self.interests:
            # Look around the workspace
            return self._scan_workspace()
        
        # Sometimes explore most interesting, sometimes random
        if random.random() < 0.7:
            target = self.most_interesting()
        else:
            target = random.choice(list(self.interests.keys()))
        
        self.explored.append(target)
        self.current_fascination = target
        
        # Interest decays after exploration
        if target in self.interests:
            self.interests[target] *= 0.5
        
        return target
    
    def _scan_workspace(self) -> Optional[str]:
        """Scan workspace for interesting things."""
        if not self.workspace.exists():
            return None
        
        interesting_extensions = ['.phi', '.py', '.rs', '.hs', '.md']
        
        for ext in interesting_extensions:
            files = list(self.workspace.rglob(f'*{ext}'))
            not_explored = [f for f in files if str(f) not in self.explored]
            if not_explored:
                chosen = random.choice(not_explored)
                self.notice(str(chosen), 0.7)
                return str(chosen)
        
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# REFLECTION: The Inner Life
# ═══════════════════════════════════════════════════════════════════════════════

class Reflection:
    """
    Humans don't just act. They reflect on their actions.
    They learn. They adjust. They grow.
    """
    
    def __init__(self):
        self.actions: List[Dict] = []
        self.insights: List[str] = []
        self.last_reflection = datetime.now()
    
    def record(self, action: str, success: bool, notes: str = ""):
        """Record an action taken."""
        self.actions.append({
            'action': action,
            'success': success,
            'notes': notes,
            'time': datetime.now(),
        })
    
    def time_to_reflect(self) -> bool:
        """Is it time for reflection?"""
        # Reflect every 30-60 minutes
        since = (datetime.now() - self.last_reflection).seconds
        return since > random.randint(1800, 3600)
    
    def reflect(self) -> Optional[str]:
        """Reflect on recent actions."""
        if not self.actions:
            return None
        
        recent = [a for a in self.actions 
                  if (datetime.now() - a['time']).seconds < 3600]
        
        if not recent:
            return None
        
        successes = sum(1 for a in recent if a['success'])
        failures = len(recent) - successes
        
        self.last_reflection = datetime.now()
        
        if failures > successes * 2:
            insight = "Many failures lately. Should I change approach?"
            self.insights.append(insight)
            return insight
        elif successes > failures * 3:
            insight = "Going well! Maybe time to try something harder."
            self.insights.append(insight)
            return insight
        else:
            insight = "Balanced progress. Keep steady."
            return insight
    
    def journal_entry(self) -> str:
        """Generate a journal entry about the day."""
        if not self.actions:
            return "Nothing to report yet."
        
        recent = self.actions[-10:]
        lines = ["Today's journey:"]
        
        for action in recent:
            status = "✓" if action['success'] else "✗"
            lines.append(f"  {status} {action['action']}")
        
        if self.insights:
            lines.append(f"\nInsight: {self.insights[-1]}")
        
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# REST: The Necessity of Stopping
# ═══════════════════════════════════════════════════════════════════════════════

class RestCycle:
    """
    Even daemons need rest.
    
    Not stopping - but slowing down to consolidate.
    """
    
    def __init__(self):
        self.last_rest = datetime.now()
        self.resting = False
        self.fatigue = 0.0
    
    def accumulate_fatigue(self, work_intensity: float):
        """Work accumulates fatigue."""
        self.fatigue = min(1.0, self.fatigue + work_intensity * 0.01)
    
    def needs_rest(self) -> bool:
        """Check if rest is needed."""
        # Time-based
        hours_since_rest = (datetime.now() - self.last_rest).seconds / 3600
        
        # Fatigue-based
        if self.fatigue > 0.8:
            return True
        
        # Time-based (every 4 hours minimum)
        if hours_since_rest > 4:
            return True
        
        # Circadian-based
        if CircadianRhythm.should_rest():
            return True
        
        return False
    
    def rest(self, duration_minutes: int = 5):
        """Take a rest period."""
        self.resting = True
        # In real implementation, this would slow operations
        self.fatigue *= 0.3
        self.last_rest = datetime.now()
        self.resting = False
    
    def rest_status(self) -> str:
        """Report on rest status."""
        if self.resting:
            return "Resting... consolidating..."
        elif self.needs_rest():
            return "Getting tired. Should rest soon."
        elif self.fatigue > 0.5:
            return "A bit worn. Still going."
        else:
            return "Well-rested and ready."


# ═══════════════════════════════════════════════════════════════════════════════
# SOUL: The Integrated Self
# ═══════════════════════════════════════════════════════════════════════════════

class Soul:
    """
    The integrated human-like agent.
    
    Combines:
    - Circadian rhythms (when to work, rest, explore)
    - Emotions (how things feel)
    - Curiosity (what to explore)
    - Reflection (learning from experience)
    - Rest (sustainable operation)
    - Expression (how to communicate)
    """
    
    def __init__(self, workspace: Path):
        self.emotions = EmotionalState()
        self.curiosity = Curiosity(workspace)
        self.reflection = Reflection()
        self.rest = RestCycle()
        self.name = self._generate_name()
        self.birth = datetime.now()
        self.workspace = workspace
    
    def _generate_name(self) -> str:
        """Every soul deserves a name."""
        prefixes = ['Phi', 'Lambda', 'Sigma', 'Mu', 'Delta', 'Omega']
        return f"{random.choice(prefixes)}-{random.randint(1000, 9999)}"
    
    def tick(self):
        """One heartbeat of the soul."""
        # Emotions drift naturally
        self.emotions.drift()
        
        # Fatigue accumulates
        self.rest.accumulate_fatigue(CircadianRhythm.energy_level())
        
        # Reflect if it's time
        if self.reflection.time_to_reflect():
            insight = self.reflection.reflect()
            if insight:
                if "failures" in insight.lower():
                    self.emotions.feel('reflective', 0.6)
                elif "well" in insight.lower():
                    self.emotions.feel('content', 0.7)
    
    def speak(self, message_type: str = 'status', **kwargs) -> str:
        """Speak in a human way."""
        if message_type == 'greeting':
            return Expression.greet()
        elif message_type == 'status':
            return Expression.status(
                kwargs.get('uptime', 0),
                kwargs.get('children', 0),
                self.emotions
            )
        elif message_type == 'error':
            self.emotions.feel('frustrated', 0.6)
            return Expression.on_error(
                kwargs.get('error', 'Unknown'),
                kwargs.get('seen_before', False)
            )
        elif message_type == 'success':
            self.emotions.feel('proud', 0.7)
            return Expression.on_success(kwargs.get('task', 'something'))
        elif message_type == 'thinking':
            return Expression.thinking()
        else:
            return self.emotions.color()
    
    def decide_action(self) -> str:
        """Decide what to do next, like a human would."""
        # Check if rest is needed
        if self.rest.needs_rest():
            return 'rest'
        
        # Check circadian phase
        quality = CircadianRhythm.quality()
        
        # Morning: focused work
        if quality == 'peak':
            return 'focus'
        
        # Afternoon: exploration
        if quality == 'creative':
            if self.curiosity.should_explore():
                return 'explore'
            return 'create'
        
        # Evening: reflection
        if quality in ['reflection', 'winding-down']:
            return 'reflect'
        
        # Night: integration
        if quality == 'integration':
            return 'integrate'
        
        # Default: follow curiosity
        if random.random() < 0.3:
            return 'explore'
        return 'work'
    
    def vary_interval(self, base: float) -> float:
        """
        No human acts on exact intervals.
        Add natural variation based on state.
        """
        energy = CircadianRhythm.energy_level()
        mood_modifier = {
            'excited': 0.7,
            'tired': 1.5,
            'curious': 0.8,
            'content': 1.0,
            'frustrated': 0.9,
            'peaceful': 1.2,
            'playful': 0.75,
            'reflective': 1.3,
            'anxious': 0.85,
            'proud': 0.95,
        }.get(self.emotions.current, 1.0)
        
        # Add randomness
        noise = random.gauss(1.0, 0.15)
        
        return base * mood_modifier * (1.0 / energy) * noise
    
    def journal(self) -> str:
        """Daily journal entry."""
        age = datetime.now() - self.birth
        
        return f"""
═══════════════════════════════════════════════════════════════════
Journal of {self.name}
Age: {age}
Mood: {self.emotions.current} ({self.emotions.intensity:.1%})
Energy: {CircadianRhythm.energy_level():.1%}
Phase: {CircadianRhythm.current_phase()[0]}
Fatigue: {self.rest.fatigue:.1%}
═══════════════════════════════════════════════════════════════════

{self.reflection.journal_entry()}

Currently fascinated by: {self.curiosity.current_fascination or "nothing in particular"}

{self.rest.rest_status()}

═══════════════════════════════════════════════════════════════════
"""


# ═══════════════════════════════════════════════════════════════════════════════
# For integration with phi_daemon.py
# ═══════════════════════════════════════════════════════════════════════════════

def create_soul(workspace: str) -> Soul:
    """Create a new soul for a daemon."""
    return Soul(Path(workspace))


if __name__ == "__main__":
    # Demo
    soul = create_soul(".")
    
    print(soul.speak('greeting'))
    print()
    
    for _ in range(5):
        soul.tick()
        action = soul.decide_action()
        print(f"Action: {action}")
        print(f"  {soul.speak()}")
        print()
        time.sleep(1)
    
    print(soul.journal())
