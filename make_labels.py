"""
Turns my raw collected posts into labels.csv.

I copy pasted comments from r/cscareerquestions into
data/collected_posts.txt with a blank line between each one. This script
splits them up, throws out the ones I can't use, and writes the CSV with
the text/label/note columns the project asks for.

It leaves the label column empty on purpose. I fill that in myself.

Run it with:  python make_labels.py
"""

import csv
import re

SOURCE = "data/collected_posts.txt"
OUTPUT = "labels.csv"

# A comment shorter than this is things like "this" or "same here". There
# isn't enough in it to say whether it's advice, experience or a claim.
MIN_LENGTH = 60


def is_just_a_question(post):
    """Questions have no opinion in them so none of my three labels fit."""
    return post.rstrip().endswith("?") and len(post) < 200


def load_posts(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()

    # I separated posts with blank lines while I was copy pasting.
    return [block.strip() for block in re.split(r"\n\s*\n", raw) if block.strip()]


def main():
    posts = load_posts(SOURCE)
    print(f"read {len(posts)} posts from {SOURCE}")

    kept = []
    seen = set()
    too_short = questions = duplicates = 0

    for post in posts:
        if len(post) < MIN_LENGTH:
            too_short += 1
            continue
        if is_just_a_question(post):
            questions += 1
            continue

        # Same comment pasted twice by accident. The notebook checks for this
        # too but it's easier to fix here.
        fingerprint = post.lower()[:80]
        if fingerprint in seen:
            duplicates += 1
            continue
        seen.add(fingerprint)

        kept.append(post)

    print(f"  dropped {too_short} too short")
    print(f"  dropped {questions} that were only questions")
    print(f"  dropped {duplicates} duplicates")
    print(f"  keeping {len(kept)}")

    # newline="" is what the csv docs say to do, otherwise Windows puts blank
    # rows between everything.
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label", "note"])
        for post in kept:
            writer.writerow([post, "", ""])

    print(f"\nwrote {OUTPUT} with {len(kept)} rows, label column empty")

    if len(kept) < 200:
        print(f"that is {200 - len(kept)} short of 200, need to collect more")


if __name__ == "__main__":
    main()
