"""SwingVision API — login, fetch, parse. Token cached in memory."""
from __future__ import annotations
import math
import os
import re
import uuid as _uuid
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import requests

API = "https://api.swing.tennis/v1"
CREDS = Path(__file__).parent.parent / "swingvision_creds.txt"

_auth: dict = {}   # {uuid, token}


# ── Auth ──────────────────────────────────────────────────────────────────────

def _headers() -> dict:
    return {
        "User-Agent": "SwingVision/11.9.58",
        "Accept":     "application/json",
        "Authorization": f"{_auth['uuid']}:{_auth['token']}",
        "Device-UUID": str(_uuid.uuid4()),
    }


def _load_creds() -> tuple[str, str]:
    """Credentials from environment variables first (works on Render),
    falling back to a local swingvision_creds.txt file (works locally)."""
    user = os.environ.get("SWINGVISION_USERNAME")
    pwd = os.environ.get("SWINGVISION_PASSWORD")
    if user and pwd:
        return user, pwd
    if not CREDS.exists():
        raise FileNotFoundError(
            "SwingVision credentials missing — set SWINGVISION_USERNAME and "
            "SWINGVISION_PASSWORD environment variables, or create swingvision_creds.txt"
        )
    lines = CREDS.read_text(encoding="utf-8").strip().splitlines()
    return lines[0], lines[1]


def login() -> dict:
    global _auth
    username, password = _load_creds()
    r = requests.post(f"{API}/login",
                      json={"username": username, "password": password},
                      headers={"Accept": "application/json",
                                "Content-Type": "application/json"},
                      timeout=15)
    r.raise_for_status()
    d = r.json()["data"]
    _auth = {"uuid": d["user_uuid"], "token": d["access_token_secret"]}
    return _auth


def _ensure_auth() -> None:
    if not _auth:
        login()


def _get(path: str, **kw) -> Any:
    _ensure_auth()
    r = requests.get(f"{API}{path}", headers=_headers(), timeout=15, **kw)
    if r.status_code == 401:
        login()
        r = requests.get(f"{API}{path}", headers=_headers(), timeout=15, **kw)
    r.raise_for_status()
    return r.json()


# ── URL parsing ───────────────────────────────────────────────────────────────

def extract_match_id(url: str) -> str | None:
    m = re.search(r"swing\.vision/matches/([a-zA-Z0-9_\-]+)", url)
    return m.group(1) if m else None


# ── Fetch raw data ────────────────────────────────────────────────────────────

def fetch_match(mid: str) -> dict:
    return _get(f"/matches/{mid}").get("data", {})


def fetch_shots(mid: str) -> list[dict]:
    return _get(f"/matches/{mid}/shots").get("data", [])


def fetch_fresh_video_url(mid: str) -> str | None:
    data = fetch_match(mid)
    vids = data.get("match_videos") or data.get("pending_match_videos") or []
    return vids[0].get("video_url") if vids else None


# ── Parse session ─────────────────────────────────────────────────────────────

def parse_session(mid: str) -> dict:
    """Fetch match + shots and return unified stats dict."""
    match  = fetch_match(mid)
    shots  = fetch_shots(mid)
    # "pending" = solo/practice session (no opponent) — treat as host
    host   = [s for s in shots if s.get("player") in ("host", "pending")]

    date  = (match.get("started_at") or "")[:10]
    total = match.get("host_shot_count", len(host))
    in_n  = match.get("host_shot_in", 0)
    vids  = match.get("match_videos") or match.get("pending_match_videos") or []
    video_url = vids[0].get("video_url") if vids else None

    return {
        "match_id":   mid,
        "date":       date,
        "shots":      total,
        "rallies":    len({s.get("pid") for s in shots if s.get("pid")}),
        "video_url":  video_url,
        "in_pct":     round(in_n / total * 100, 1) if total else 0,
        "strokes":    _stroke_stats(host),
        "spin":       _spin_stats(host),
        "directions": _direction_stats(host),
        "zones":      _zone_stats(host),
    }


def analyze_opponent(mid: str) -> dict:
    """Stats for the guest (opponent) player."""
    shots = fetch_shots(mid)
    guest = [s for s in shots if s.get("player") == "guest"]
    if not guest:
        return {}
    buckets: dict[str, list] = defaultdict(list)
    for s in guest:
        st = _stroke(s)
        if st:
            buckets[st].append(s)
    result = {}
    for stroke, lst in buckets.items():
        speeds = [_speed(s) for s in lst if _speed(s) > 5]
        in_c   = sum(1 for s in lst if _in(s))
        spins  = Counter(s.get("spin_type","") for s in lst)
        result[stroke] = {
            "count": len(lst),
            "avg_speed": round(sum(speeds)/len(speeds), 1) if speeds else 0,
            "in_pct": round(in_c/len(lst)*100, 1),
            "spin": spins.most_common(1)[0][0] if spins else "flat",
        }
    dirs = Counter(
        s.get("bounce_location_lat","") for s in guest if s.get("bounce_location_lat")
    )
    return {"strokes": result, "total": len(guest), "dirs": dict(dirs.most_common(4))}


# ── Internal helpers ──────────────────────────────────────────────────────────

def _speed(s: dict) -> float:
    hv = s.get("hit_velocity")
    if hv and len(hv) == 3:
        return round(math.sqrt(sum(x**2 for x in hv)) * 3.6, 1)
    return 0.0


def _in(s: dict) -> bool:
    return s.get("net_type") == "over" and s.get("bounce_location") is not None


def _stroke(s: dict, right_handed: bool = True) -> str:
    ht = s.get("hit_type", "")
    if ht == "feed":              return ""
    if "serve" in ht:             return "Serve"
    if ht == "volley":            return "Volley"
    if ht in ("overhead","smash"):return "Overhead"
    w = s.get("hit_wing", "")
    if w == "right": return "Forehand" if right_handed else "Backhand"
    if w == "left":  return "Backhand" if right_handed else "Forehand"
    return ""


def _stroke_stats(shots: list) -> dict:
    buckets: dict[str, list] = defaultdict(list)
    for s in shots:
        st = _stroke(s)
        if st:
            buckets[st].append(s)
    result = {}
    for stroke, lst in buckets.items():
        speeds = [_speed(s) for s in lst if _speed(s) > 5]
        in_c   = sum(1 for s in lst if _in(s))
        result[stroke] = {
            "count":     len(lst),
            "avg_speed": round(sum(speeds)/len(speeds), 1) if speeds else 0,
            "max_speed": round(max(speeds), 1) if speeds else 0,
            "in_pct":    round(in_c/len(lst)*100, 1) if lst else 0,
        }
    return result


def _spin_stats(shots: list) -> dict:
    buckets: dict[str, Counter] = defaultdict(Counter)
    for s in shots:
        st = _stroke(s)
        sp = s.get("spin_type", "")
        if st and sp:
            buckets[st][sp] += 1
    return {
        stroke: {k: round(v/sum(c.values())*100, 1) for k, v in c.items()}
        for stroke, c in buckets.items()
    }


def _direction_stats(shots: list) -> dict:
    overall = Counter(
        s.get("bounce_location_lat","") for s in shots if s.get("bounce_location_lat")
    )
    return dict(overall.most_common(6))


def _zone_stats(shots: list) -> dict:
    depth = Counter(s.get("bounce_location_long","") for s in shots if s.get("bounce_location_long"))
    hit_d = Counter(s.get("hit_location_long","")    for s in shots if s.get("hit_location_long"))
    return {"bounce_depth": dict(depth), "hit_depth": dict(hit_d)}
