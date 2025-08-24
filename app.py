from __future__ import annotations
import json
import os
import random
from pathlib import Path
from typing import List, Dict, Any

from flask import Flask, jsonify, request, render_template

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data.json"

app = Flask(__name__)

# Load data once at startup
with DATA_PATH.open("r", encoding="utf-8") as f:
    DATA = json.load(f)

ITEMS: List[Dict[str, Any]] = DATA.get("items", [])


@app.get("/")
def home():
    """Simple UI that consumes the JSON API."""
    return render_template("index.html")


@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok"})


@app.get("/api/items")
def list_items():
    """List all items with optional pagination: ?limit=&offset="""
    limit = request.args.get("limit", type=int) or len(ITEMS)
    offset = request.args.get("offset", type=int) or 0
    sliced = ITEMS[offset : offset + limit]
    return jsonify(
        {
            "count": len(ITEMS),
            "limit": limit,
            "offset": offset,
            "items": sliced,
        }
    )


@app.get("/api/random")
def random_items():
    """Return n unique random items. Default n=1. e.g., /api/random?n=3"""
    n = request.args.get("n", default=1, type=int)
    n = max(1, min(n, len(ITEMS)))
    # sample without replacement
    sample = random.sample(ITEMS, n)
    return jsonify({"n": n, "items": sample})


@app.get("/api/categories")
def categories():
    cats: Dict[str, int] = {}
    for it in ITEMS:
        cat = it.get("category", "uncategorized")
        cats[cat] = cats.get(cat, 0) + 1
    return jsonify({"categories": cats})


@app.get("/api/search")
def search():
    """Case-insensitive search in title/text/tags: /api/search?q=focus"""
    q = (request.args.get("q") or "").strip().lower()
    if not q:
        return jsonify({"items": [], "query": q})

    def matches(it: Dict[str, Any]) -> bool:
        hay = " ".join(
            [
                str(it.get("title", "")),
                str(it.get("text", "")),
                " ".join(it.get("tags", [])),
            ]
        ).lower()
        return q in hay

    results = [it for it in ITEMS if matches(it)]
    return jsonify({"items": results, "query": q, "count": len(results)})


if __name__ == "__main__":
    # Dev server
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)
