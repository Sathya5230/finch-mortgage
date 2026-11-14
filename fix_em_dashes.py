"""Replace em dashes in page copy with ordinary punctuation.

The older pages used an em dash in almost every paragraph (about 2,200 across
the site), which reads as machine-written. This rewrites them the way an
editor would by hand:

- a pair of dashes around an aside becomes a pair of commas;
- a dash before a new clause that starts with a pronoun or article becomes a
  full stop;
- "Yes —" / "No —" becomes "Yes." / "No.";
- anything else becomes a comma, or a colon in titles and headings.

Applies to visible text, meta descriptions, titles and JSON-LD strings, so the
structured data keeps matching the page. Idempotent. Run with --apply to
write; --sample N prints N before/after pairs. Run after the generators.
"""
import random
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
APPLY = "--apply" in sys.argv
SAMPLE = int(sys.argv[sys.argv.index("--sample") + 1]) if "--sample" in sys.argv else 0

PRONOUNS = {"it", "it's", "this", "that", "that's", "they", "they're", "we", "we'll", "we're", "we've", "you", "you'll",
            "you're", "there", "there's", "here's", "if", "when", "once", "these", "those", "finch", "don't", "do",
            # imperatives that open a new instruction
            "ask", "get", "check", "see", "read", "use", "try", "talk", "speak", "compare", "book", "send", "call",
            "find", "learn", "contact", "start", "run", "tell"}
CONNECTORS = {"and", "but", "so", "or", "which", "with", "without", "from", "to", "for", "in", "on", "at", "as", "plus",
              "because", "even", "then", "not", "rather", "often", "just", "well", "whether", "where", "while",
              "since", "although", "though", "by", "like", "such", "than", "until", "unless", "after", "before", "about",
              "all", "both", "either", "especially", "sometimes", "now", "still", "also", "something", "nothing", "no"}
DASH = re.compile(r"\s*(?:—|\\u2014)\s*")
samples = []


def fix_sentence(text, heading):
    parts = DASH.split(text)
    if len(parts) == 1:
        return text
    if heading:
        return parts[0] + "".join((": " if i == 0 else ", ") + p for i, p in enumerate(parts[1:]))
    out = parts[0]
    n = len(parts) - 1
    for i, nxt in enumerate(parts[1:]):
        prev_word = re.findall(r"[\w']+", out[-12:])[-1:] or [""]
        first = (re.match(r"[\w']+", nxt) or [""])[0]
        ends_here = re.search(r"[.!?]", nxt)
        if not out.strip() or not nxt.strip():
            sep = " " if out.strip() and nxt.strip() else ""
        elif prev_word[0].lower() in ("yes", "no"):
            sep, nxt = ". ", nxt[:1].upper() + nxt[1:]
        elif n == 2 and i == 0 and not re.search(r"[.!?]", nxt):
            # An aside that is itself a list reads better in brackets than between commas.
            sep, nxt = (" (", nxt + ")") if "," in nxt else (", ", nxt)
        elif n == 2 and i == 1 and samples_pair_open[0]:
            sep = " " if out.endswith(")") else ", "
        elif first.lower() in ("how", "what", "why", "who") and re.search(r"\w$", out):
            sep = ": "
        elif first.lower() in PRONOUNS and re.search(r"\w$", out):
            sep, nxt = ". ", nxt[:1].upper() + nxt[1:]
        elif re.match(r"\d", nxt) or (first[:1].isupper() and not ends_here):
            sep = ": " if re.search(r"\w$", out) else " "
        elif first.lower() in CONNECTORS or first.lower().endswith(("ing", "ly")):
            sep = ", " if re.search(r"[\w)%'’\"]$", out) else " "
        elif len(nxt.split()) >= 5 and re.search(r"\w$", out):
            sep = ": "
        else:
            sep = ", " if re.search(r"[\w)%'’\"]$", out) else " "
        samples_pair_open[0] = (n == 2 and i == 0 and sep in (", ", " ("))
        out += sep + nxt
    return out


samples_pair_open = [False]


def fix_text(text, heading=False):
    if "—" not in text and "\\u2014" not in text:
        return text
    # Work sentence by sentence so paired dashes are matched within one sentence.
    pieces = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(])", text)
    fixed = " ".join(fix_sentence(p, heading) for p in pieces)
    lead = re.match(r"\s*", text).group(0)
    trail = re.search(r"\s*$", text).group(0)
    fixed = lead + fixed.strip() + trail if text.strip() else text
    if fixed != text and SAMPLE:
        samples.append((text.strip()[:260], fixed.strip()[:260]))
    return fixed


BLOCK = re.compile(r"(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>)", re.S)
HEAD_TAG = re.compile(r"<(title|h1|h2|h3|h4)\b[^>]*>.*?</\1>", re.S)
ATTR = re.compile(r'(<meta\b[^>]*?\bcontent=")([^"]*)(")')


def fix_markup(chunk):
    def heading(m):
        return re.sub(r">([^<]+)<", lambda t: ">" + fix_text(t.group(1), True) + "<", m.group(0))
    # "<strong>Label</strong> — text" is a labelled item; after a link or emphasis the dash was an aside.
    chunk = re.sub(r"(</(?:strong|b)>)\s*—\s*", r"\1: ", chunk)
    chunk = re.sub(r"(</(?:a|em|i|span)>)\s*—\s*", r"\1, ", chunk)
    chunk = HEAD_TAG.sub(heading, chunk)
    chunk = ATTR.sub(lambda m: m.group(1) + fix_text(m.group(2), "title" in m.group(1)) + m.group(3), chunk)
    return re.sub(r">([^<]+)<", lambda t: ">" + fix_text(t.group(1)) + "<", chunk)


def fix_jsonld(block):
    def val(m):
        key, text = m.group(1), m.group(2)
        return f'"{key}": "{fix_text(text, key in ("headline", "name"))}"'
    return re.sub(r'"(headline|name|description|text|alternativeHeadline)":\s*"((?:[^"\\]|\\.)*)"', val, block)


def fix_html(html):
    out = []
    for part in BLOCK.split(html):
        if part.startswith("<script") and "ld+json" in part[:60]:
            out.append(fix_jsonld(part))
        elif part.startswith(("<script", "<style")):
            out.append(part)
        else:
            out.append(fix_markup(part))
    return "".join(out)


def main():
    files = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT, capture_output=True, text=True,
                           check=True).stdout.splitlines()
    skip = ("node_modules/", "wordpress/", "output/", "scratch/", "docs/", "research/", "drafts/", "published/")
    changed = left = 0
    for rel in files:
        path = ROOT / rel
        if rel.startswith(skip) or not path.exists():
            continue
        src = path.read_text(encoding="utf-8")
        out = fix_html(src)
        left += out.count("—")
        if out != src:
            changed += 1
            if APPLY:
                path.write_text(out, encoding="utf-8")
    if SAMPLE:
        random.seed(7)
        for before, after in random.sample(samples, min(SAMPLE, len(samples))):
            print("-", before, "\n+", after, "\n")
    print(f"files changed: {changed}; em dashes left (comments, code): {left}")
    print("APPLIED" if APPLY else "DRY RUN (use --apply)")


if __name__ == "__main__":
    main()
