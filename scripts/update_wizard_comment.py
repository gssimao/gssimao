import json
import re
import urllib.request

NAMESPACE = "gssimao-github-readme"
KEY = "visits"
README_PATH = "README.md"


def get_count():
    """Reads the current count WITHOUT incrementing it (the badge in the
    README does the incrementing every time someone views the page)."""
    url = f"https://api.countapi.xyz/get/{NAMESPACE}/{KEY}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.load(resp)
            return int(data.get("value") or 0)
    except Exception:
        return 0


def pick_message(count):
    tiers = [
        (2000, "Call the guards, we've gone viral."),
        (1000, "The whole realm seems to know about this place now."),
        (500, "Blimey, might need to start charging admission."),
        (250, "Word's getting round, this is becoming a proper hotspot."),
        (100, "This place is getting traction!"),
        (10, "Only crickets in here."),
    ]
    for threshold, message in tiers:
        if count > threshold:
            return message
    return "Not a soul has passed through yet."


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
