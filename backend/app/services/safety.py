import re

# Conservative keyword tripwire; not a clinical detector and not a substitute for human review.
CRISIS_PATTERNS = [
    r"\bkill myself\b", r"\bend my life\b", r"\bsuicid(?:e|al)\b",
    r"\bwant to die\b", r"\bhurt myself\b", r"\bself[- ]harm\b",
]
CRISIS_NOTICE = ("I'm sorry you're facing this. Your immediate safety matters more than anything else. "
                 "If you may act on these thoughts or are in immediate danger, contact local emergency services now, "
                 "move near a trusted person, and tell them directly what is happening. If you're in India, 112 is the emergency number. "
                 "I can stay with you while you reach out, but I can't provide emergency care.")

def may_be_crisis(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in CRISIS_PATTERNS)
