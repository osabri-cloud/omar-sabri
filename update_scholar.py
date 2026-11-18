"""Fetch Omar Sabri's Google Scholar profile through SerpAPI and write scholar.json.

Runs daily from .github/workflows/update-scholar.yml. Needs the SERPAPI_KEY secret.
Uses only the Python standard library, so nothing has to be installed.
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

AUTHOR_ID = "XtvII74AAAAJ"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scholar.json")


def fetch(api_key):
    params = {
        "engine": "google_scholar_author",
        "author_id": AUTHOR_ID,
        "hl": "en",
        "num": "100",          # up to 100 articles in a single search
        "api_key": api_key,
    }
    url = "https://serpapi.com/search.json?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def metric(table, name):
    """cited_by.table is a list of one-key dicts, e.g. {"h_index": {"all": 13, "since_2021": 11}}."""
    for row in table or []:
        if name in row:
            values = row[name]
            since_key = next((k for k in values if k != "all"), None)
            return {
                "all": values.get("all"),
                "since": values.get(since_key) if since_key else None,
                "since_year": int(since_key.split("_")[-1]) if since_key and since_key.split("_")[-1].isdigit() else None,
            }
    return {"all": None, "since": None, "since_year": None}


def to_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def normalise(raw):
    author = raw.get("author", {})
    cited = raw.get("cited_by", {})
    table = cited.get("table", [])
    articles = []
    for a in raw.get("articles", []):
        articles.append({
            "title": a.get("title", "").strip(),
            "authors": a.get("authors", ""),
            "venue": a.get("publication", ""),
            "year": to_int(a.get("year")),
            "cites": to_int((a.get("cited_by") or {}).get("value")) or 0,
            "link": a.get("link", ""),
        })
    return {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "https://scholar.google.com/citations?user=" + AUTHOR_ID,
        "name": author.get("name", "Omar Sabri"),
        "affiliation": author.get("affiliations", ""),
        "interests": [i.get("title") for i in author.get("interests", []) if i.get("title")],
        "citations": metric(table, "citations"),
        "h_index": metric(table, "h_index"),
        "i10_index": metric(table, "i10_index"),
        "citations_per_year": [
            {"year": to_int(g.get("year")), "citations": to_int(g.get("citations")) or 0}
            for g in cited.get("graph", []) if to_int(g.get("year"))
        ],
        "articles": articles,
    }


def main():
    key = os.environ.get("SERPAPI_KEY")
    if not key:
        sys.exit("SERPAPI_KEY is not set. Add it under Settings > Secrets and variables > Actions.")
    raw = fetch(key)
    if raw.get("error"):
        sys.exit("SerpAPI error: " + raw["error"])
    data = normalise(raw)
    # Refuse to overwrite good data with an empty or broken response.
    if not data["articles"] or data["citations"]["all"] is None:
        sys.exit("Response had no articles or citation table; keeping the previous data.")
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Saved %d articles, %s citations, h-index %s" % (
        len(data["articles"]), data["citations"]["all"], data["h_index"]["all"]))


if __name__ == "__main__":
    main()
