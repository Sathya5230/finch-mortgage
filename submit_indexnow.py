"""Submit sitemap URLs to IndexNow (Bing, Yandex, Seznam, Naver).

Bing's index feeds ChatGPT search and Copilot, so this matters for AI visibility.
Run only after a deploy, once the key file is reachable on the live site:
    python3 submit_indexnow.py            # dry run: list what would be sent
    python3 submit_indexnow.py --send     # submit every sitemap URL
    python3 submit_indexnow.py --send blog/some-post locations/x   # submit specific paths
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

HOST = "www.finchmortgages.co.nz"
BASE = f"https://{HOST}"
ROOT = Path(__file__).resolve().parent
KEY = next(p.stem for p in ROOT.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}", p.stem))


def urls_from_args(args):
    if args:
        return [f"{BASE}/{a.strip('/')}" for a in args]
    return re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text())


def main():
    send = "--send" in sys.argv
    urls = urls_from_args([a for a in sys.argv[1:] if a != "--send"])
    print(f"{len(urls)} URLs, key {KEY}")
    if not send:
        print("\n".join(urls[:10]), "\n... dry run; add --send to submit")
        return
    key_url = f"{BASE}/{KEY}.txt"
    with urllib.request.urlopen(key_url, timeout=20) as r:
        if r.read().decode().strip() != KEY:
            sys.exit(f"{key_url} does not serve the key yet; deploy first")
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": key_url, "urlList": urls}).encode()
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        print("IndexNow response:", r.status)


if __name__ == "__main__":
    main()
