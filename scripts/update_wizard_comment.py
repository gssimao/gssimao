import random
import re
import urllib.request

# NOTE: countapi.xyz and counterapi.dev were both unreliable/unverifiable.
# Switched to komarev's GitHub profile view counter (the widely used
# "profile views" badge), which is well established, but it only returns an
# SVG image, not JSON. So instead of parsing JSON, we fetch the raw SVG text
# and pull the visible number back out of it with a regex.
USERNAME = "gssimao"
README_PATH = "README.md"


def get_count():
    """Fetches the komarev badge's SVG and extracts the visible count.
    This reads the SAME number the badge displays, it does not trigger a
    separate increment (komarev increments on its own each time the badge
    image itself is requested, e.g. by someone viewing the README)."""
    url = f"https://komarev.com/ghpvc/?username={USERNAME}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            svg = resp.read().decode("utf-8", errors="ignore")
        # Grab every plain number found between SVG text tags, then take the
        # last one, the label ("Visitors") isn't numeric, so the count is
        # reliably the last digit-only match.
        matches = re.findall(r">([\d,]+)<", svg)
        if not matches:
            return 0
        return int(matches[-1].replace(",", ""))
    except Exception:
        return 0


# Multiple options per tier: picking randomly each run means the README text
# almost always changes between runs, which keeps the repo "active" so
# GitHub doesn't auto-disable the schedule after 60 days of no commits.
TIERS = [
    (2000, [
        "Call the guards, we've gone viral.",
        "I need a bigger ledger. Possibly a bigger hall.",
        "I've lost count of the count. Wonderful problem to have.",
    ]),
    (1000, [
        "The whole realm seems to know about this place now.",
        "I can barely keep the ledger straight anymore.",
        "Quite the pilgrimage forming out there.",
    ]),
    (500, [
        "Blimey, might need to start charging admission.",
        "This is getting properly busy.",
        "I'm rationing the biscuits at this rate.",
    ]),
    (250, [
        "Word's getting round, this is becoming a proper hotspot.",
        "Quite the crowd gathering round here now.",
        "Someone tell Gabriel he's popular.",
    ]),
    (100, [
        "This place is getting traction!",
        "People keep finding this place, curious.",
        "The word is spreading, apparently.",
    ]),
    (10, [
        "Only crickets in here.",
        "A trickle of visitors, nothing more.",
        "Word hasn't quite got round yet.",
    ]),
]

DEFAULT_MESSAGES = [
    "Not a soul has passed through yet.",
    "It's been dead quiet around here.",
    "Even the crickets left.",
]


def pick_message(count):
    for threshold, pool in TIERS:
        if count > threshold:
            return random.choice(pool)
    return random.choice(DEFAULT_MESSAGES)


def update_readme(message):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"(<!--WIZARD_COMMENT_START-->\s*)(.*?)(\s*<!--WIZARD_COMMENT_END-->)"
    new_line = f'*"{message}"*'
    new_content = re.sub(
        pattern,
        lambda m: m.group(1) + new_line + m.group(3),
        content,
        flags=re.S,
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)


def main():
    count = get_count()
    message = pick_message(count)
    update_readme(message)
    print(f"Visit count: {count}. Wizard says: {message}")


if __name__ == "__main__":
    main()
