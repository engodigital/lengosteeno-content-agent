#!/usr/bin/env python3
"""
Scraping deterministico via RSS (nessun AI coinvolto in questo step).
Legge scraper/feeds.json, prende gli articoli delle ultime N ore da ogni
feed, e stampa un JSON su stdout con i candidati grezzi. La selezione
dell'angolo/rilevanza resta a valle (skill), qui c'e' solo raccolta dati.

Uso:
    python3 fetch_news.py [--hours 48] [--filone hosteleria|marketing]
"""
import argparse
import json
import ssl
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

FEEDS_PATH = Path(__file__).parent / "feeds.json"
USER_AGENT = "Mozilla/5.0 (compatible; LengosteenoContentBot/1.0)"

try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()


def fetch_feed(url: str, timeout: int = 15) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as resp:
        return resp.read()


def parse_rss(xml_bytes: bytes, source_name: str):
    items = []
    root = ET.fromstring(xml_bytes)
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date_raw = item.findtext("pubDate")
        description = (item.findtext("description") or "").strip()

        pub_date = None
        if pub_date_raw:
            try:
                pub_date = parsedate_to_datetime(pub_date_raw)
                if pub_date.tzinfo is None:
                    pub_date = pub_date.replace(tzinfo=timezone.utc)
            except (TypeError, ValueError):
                pub_date = None

        items.append({
            "source": source_name,
            "title": title,
            "link": link,
            "description": description[:400],
            "published_at": pub_date.isoformat() if pub_date else None,
        })
    return items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hours", type=int, default=48,
                         help="Finestra temporale in ore (default: 48)")
    parser.add_argument("--filone", choices=["hosteleria", "marketing"],
                         default=None,
                         help="Filtra un solo filone. Default: entrambi")
    args = parser.parse_args()

    with open(FEEDS_PATH, encoding="utf-8") as f:
        feeds = json.load(f)

    filoni = [args.filone] if args.filone else list(feeds.keys())
    cutoff = datetime.now(timezone.utc) - timedelta(hours=args.hours)

    results = {"generated_at": datetime.now(timezone.utc).isoformat(),
               "window_hours": args.hours, "items": []}

    for filone in filoni:
        for feed in feeds.get(filone, []):
            try:
                xml_bytes = fetch_feed(feed["url"])
                items = parse_rss(xml_bytes, feed["name"])
            except Exception as exc:
                print(f"[warn] feed fallito: {feed['name']} ({exc})",
                      file=sys.stderr)
                continue

            for it in items:
                if it["published_at"] is None:
                    continue
                pub_dt = datetime.fromisoformat(it["published_at"])
                if pub_dt >= cutoff:
                    it["filone"] = filone
                    results["items"].append(it)

    results["items"].sort(key=lambda x: x["published_at"], reverse=True)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
