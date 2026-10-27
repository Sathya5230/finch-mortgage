"""Rewrite internal links to extensionless URLs (Vercel cleanUrls).

Idempotent; run last in the post-generation pipeline, since generators still emit .html links.
External .html links are left untouched.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SITE = "https://www.finchmortgages.co.nz"
SKIP_DIRS = {"node_modules", "wordpress", "drafts", "output", "research", "rewrites",
             "published", "topics", "scratch", "examples", "docs", "context", ".git"}

URL_RE = re.compile(r"(?P<url>(?:https?://[A-Za-z0-9.-]+)?[A-Za-z0-9_./~-]*?)(?P<name>[A-Za-z0-9_-]+)\.html(?=[#?\"'\s<>)\],;`]|$)")


def fix(m):
    url, name = m.group("url"), m.group("name")
    if url.startswith("http") and not url.startswith(("https://www.finchmortgages.co.nz", "https://finchmortgages.co.nz")):
        return m.group(0)
    if name == "index":
        if url == "":
            return "./"
        if url.rstrip("/") in (SITE, "https://finchmortgages.co.nz"):
            return url if url.endswith("/") else url + "/"
        if url.endswith("/") and url.strip("./") and not url.endswith("../"):
            return url.rstrip("/")
        return url or "./"
    return url + name


def process(path):
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"Skipped non-UTF-8 file: {path}")
        return False
    new = URL_RE.sub(fix, text)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def main():
    targets = [p for p in ROOT.rglob("*")
               if p.suffix in {".html", ".xml", ".txt", ".md"} and p.is_file()
               and not any(d in SKIP_DIRS or d.startswith(".") for d in p.relative_to(ROOT).parts[:-1])
               and p.name not in {"CLAUDE.md", "README.md", "seo-machine-README.md",
                                  "seo-machine-QUICK-START.md", "data-sources-setup.md"}]
    changed = sum(process(p) for p in targets)
    print(f"Updated {changed} of {len(targets)} files")


if __name__ == "__main__":
    main()
