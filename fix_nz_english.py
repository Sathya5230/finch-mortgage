"""Convert US spellings in visible copy to New Zealand English.

The site targets New Zealand searchers only, yet visible copy used US forms
("specialized", "analyze", "behavior", "labor", "neighborhood"), and "advisor",
where NZ law and the FMA use "financial adviser". Only human-readable text is
touched: text between tags, <title>, meta description/og/twitter content, alt
text and JSON-LD string values. URLs, CSS, scripts and schema type names are left
alone. In Python sources only string literals change, and never the {expressions}
inside f-strings, so generators re-emit the same NZ spelling.

Idempotent. Run with --apply to write; default is a dry run.
"""
import io
import re
import subprocess
import sys
import tokenize
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent
APPLY = "--apply" in sys.argv

# -ize/-yze words whose "z" belongs to the root, not the suffix.
KEEP_Z = re.compile(r"siz|^prize|^seize|^capsiz", re.I)
IZE = re.compile(r"\b([A-Za-z]{2,}?)(i|y)z(e|es|ed|ing|ation|ations|er|ers|able)\b")

WORDS = {
    "advisor": "adviser", "advisors": "advisers",
    "behavior": "behaviour", "behaviors": "behaviours", "behavioral": "behavioural",
    "labor": "labour", "favor": "favour", "favors": "favours", "favored": "favoured",
    "favorable": "favourable", "favorably": "favourably", "unfavorable": "unfavourable",
    "favorite": "favourite", "favorites": "favourites",
    "neighborhood": "neighbourhood", "neighborhoods": "neighbourhoods",
    "endeavor": "endeavour", "color": "colour", "colors": "colours",
    "honor": "honour", "humor": "humour", "flavor": "flavour",
    "center": "centre", "centers": "centres", "centered": "centred",
    "modeling": "modelling", "modeled": "modelled",
    "fulfill": "fulfil", "license": "licence",
    "checking account": "bank account",
}
WORDS_RX = re.compile(r"\b(" + "|".join(sorted(map(re.escape, WORDS), key=len, reverse=True)) + r")\b", re.I)
URL = re.compile(r"(?:https?://|www\.|\.\./|/)[^\s\"'<>]*|[\w.-]+\.(?:html|js|css|png|jpg|webp|xml)\b")

counts = Counter()


def match_case(src, repl):
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def ize(m):
    if KEEP_Z.search(m.group(0)):
        return m.group(0)
    counts[m.group(0).lower()] += 1
    return f"{m.group(1)}{m.group(2)}s{m.group(3)}"


def word(m):
    counts[m.group(0).lower()] += 1
    return match_case(m.group(0), WORDS[m.group(0).lower()])


def nz_text(text):
    """Apply spelling fixes to plain text, skipping anything URL- or filename-shaped."""
    out, last = [], 0
    for u in URL.finditer(text):
        out.append(WORDS_RX.sub(word, IZE.sub(ize, text[last:u.start()])))
        out.append(u.group(0))
        last = u.end()
    out.append(WORDS_RX.sub(word, IZE.sub(ize, text[last:])))
    return "".join(out)


HTML_TOKEN = re.compile(r"(<script\b[^>]*>.*?</script>|<style\b.*?</style>|<!--.*?-->|<[^>]+>)", re.S | re.I)
ATTR = re.compile(r'(\s(?:alt|content)=")([^"]*)(")')
TEXT_META = re.compile(r'name="(?:description|twitter:title|twitter:description)"|property="og:(?:title|description)"')
JSON_STRING = re.compile(r'"(?:[^"\\]|\\.)*"')
# Values of "@type", "@id" etc. are vocabulary terms ("Organization"), never prose.
JSON_AT_VALUE = re.compile(r'"@[^"]*"\s*:\s*("(?:[^"\\]|\\.)*"|\[[^\]]*\])')


def nz_jsonld(body):
    protected = [m.span(1) for m in JSON_AT_VALUE.finditer(body)]

    def repl(m):
        a, b = m.span()
        is_key = body[b:b + 20].lstrip().startswith(":")
        if is_key or any(pa <= a < pb for pa, pb in protected):
            return m.group(0)
        return nz_text(m.group(0))
    return JSON_STRING.sub(repl, body)


def nz_html(html):
    parts = HTML_TOKEN.split(html)
    for i, part in enumerate(parts):
        if i % 2 == 0:
            parts[i] = nz_text(part)
        elif part.lower().startswith('<script type="application/ld+json"'):
            head_end = part.index(">") + 1
            tail = part.rindex("</")
            parts[i] = part[:head_end] + nz_jsonld(part[head_end:tail]) + part[tail:]
        elif part.startswith("<img") or (part.startswith("<meta") and TEXT_META.search(part)):
            parts[i] = ATTR.sub(lambda m: m.group(1) + nz_text(m.group(2)) + m.group(3), part)
    return "".join(parts)


# Python string literals mix prose with CSS ("color:", "text-center",
# "text-transform:capitalize") and schema vocabulary ("Organization"), so sources
# only get an explicit list of prose words that never occur in either.
PY_WORDS = {
    **{k: v for k, v in WORDS.items()
       if k not in {"color", "colors", "center", "centers", "centered", "license"}},
    **{w: w.replace("iz", "is") for w in (
        "specialize specialized specializes specializing analyze analyzed analyzes analyzing "
        "utilize utilized utilizes utilizing utilization maximize maximized maximizes maximizing "
        "minimize minimized minimizing minimization optimize optimized optimizing optimization "
        "finalize finalized scrutinize scrutinized scrutinizes localized personalized characterized "
        "agonizing recognize recognized recognizing recognizable realize realized realizable "
        "prioritize prioritized prioritizing penalize penalized penalizes customize customized "
        "customizable amortization amortizing standardized incentivizing publicized energized "
        "formalize centralizes modernized visualization urbanized marginalized subsidizing "
        "unauthorized collateralize harmonizing hybridized emphasized emphasize organize "
        "organizing capitalization capitalizing").split()},
    "paralyzing": "paralysing",
}
PY_RX = re.compile(r"\b(" + "|".join(sorted(map(re.escape, PY_WORDS), key=len, reverse=True)) + r")\b", re.I)


def py_text(text):
    def sub(m):
        counts[m.group(0).lower()] += 1
        return match_case(m.group(0), PY_WORDS[m.group(0).lower()])
    out, last = [], 0
    for u in URL.finditer(text):
        out.append(PY_RX.sub(sub, text[last:u.start()]))
        out.append(u.group(0))
        last = u.end()
    out.append(PY_RX.sub(sub, text[last:]))
    return "".join(out)


def py_fstring_literal(tok):
    """Fix only the literal parts of an f-string, leaving {expressions} untouched."""
    out, buf, depth, i = [], [], 0, 0
    while i < len(tok):
        ch = tok[i]
        if depth == 0 and tok.startswith(("{{", "}}"), i):
            buf.append(tok[i:i + 2]); i += 2; continue
        if ch == "{":
            if depth == 0:
                out.append(py_text("".join(buf))); buf = []
            depth += 1
        if depth:
            out.append(ch)
            if ch == "}":
                depth -= 1
        else:
            buf.append(ch)
        i += 1
    out.append(py_text("".join(buf)))
    return "".join(out)


def nz_python(src):
    lines = src.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    toks = [t for t in tokenize.generate_tokens(io.StringIO(src).readline)
            if t.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.COMMENT, tokenize.INDENT, tokenize.DEDENT)]
    edits = []
    for i, tok in enumerate(toks):
        if tok.type != tokenize.STRING:
            continue
        if i + 1 < len(toks) and toks[i + 1].string == ":":
            continue  # dict key
        a = offsets[tok.start[0] - 1] + tok.start[1]
        b = offsets[tok.end[0] - 1] + tok.end[1]
        prefix = re.match(r"[A-Za-z]*", tok.string).group(0).lower()
        new = py_fstring_literal(tok.string) if "f" in prefix else py_text(tok.string)
        if new != tok.string:
            edits.append((a, b, new))
    for a, b, new in reversed(edits):
        src = src[:a] + new + src[b:]
    return src


def main():
    tracked = subprocess.run(["git", "ls-files", "*.html", "*.py"], cwd=ROOT,
                             capture_output=True, text=True).stdout.split()
    changed = 0
    for f in tracked:
        if f.endswith(".py") and (Path(f).name.startswith("fix_") or "/" in f):
            continue
        p = ROOT / f
        src = p.read_text(encoding="utf-8")
        out = nz_python(src) if f.endswith(".py") else nz_html(src)
        if out != src:
            changed += 1
            if f.endswith(".py"):
                compile(out, f, "exec")
            if APPLY:
                p.write_text(out, encoding="utf-8")
    for w, n in counts.most_common():
        print(f"{n:5}  {w}")
    print(f"\nfiles changed: {changed}")
    print("APPLIED" if APPLY else "DRY RUN (use --apply)")


if __name__ == "__main__":
    main()
