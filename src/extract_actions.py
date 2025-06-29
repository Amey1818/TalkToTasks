import re

ACTION_PATTERNS = {
    "assignment": r"\b(assign(ed)?|delegate(d)?)\b.*",
    "follow_up": r"\b(follow up|track|remind|review|check in)\b.*",
    "responsibility": r"\b(will|must|should|need to|responsible for)\b.*",
    "deadline": r"\b(by|before|due|on)\s+\b(\w+ \d{1,2}|\d{1,2}/\d{1,2})\b.*"
}

def extract_action_items(text):
    lines = text.split('\n')
    extracted = []

    for line in lines:
        for category, pattern in ACTION_PATTERNS.items():
            if re.search(pattern, line, re.IGNORECASE):
                extracted.append({
                    "action": line.strip(),
                    "type": category
                })
                break  # Don't double-tag the same line

    return extracted
