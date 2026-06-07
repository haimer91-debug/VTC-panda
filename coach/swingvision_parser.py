"""Parse SwingVision CSV/JSON exports into normalized dicts."""
import csv
import json
from pathlib import Path
from datetime import datetime


COLUMN_ALIASES = {
    # SwingVision CSV headers (various export formats)
    "shot": "shot_type", "type": "shot_type", "stroke": "shot_type",
    "speed": "speed_kmh", "ball speed": "speed_kmh", "mph": "speed_mph",
    "spin": "spin_rpm", "topspin": "spin_rpm",
    "dir": "direction", "placement": "direction",
    "depth": "depth",
    "result": "outcome", "outcome": "outcome", "in/out": "outcome",
    "date": "date", "time": "date",
}


def _normalize_row(row: dict) -> dict:
    out = {}
    for k, v in row.items():
        key = COLUMN_ALIASES.get(k.strip().lower(), k.strip().lower())
        out[key] = v.strip() if isinstance(v, str) else v

    # Convert mph → kmh if needed
    if "speed_mph" in out and "speed_kmh" not in out:
        try:
            out["speed_kmh"] = round(float(out["speed_mph"]) * 1.60934, 1)
        except (ValueError, TypeError):
            pass

    # Numeric coercions
    for field in ("speed_kmh", "spin_rpm"):
        if field in out and out[field] not in (None, ""):
            try:
                out[field] = float(out[field])
            except (ValueError, TypeError):
                out[field] = None

    # Date default
    if "date" not in out or not out["date"]:
        out["date"] = datetime.now().strftime("%Y-%m-%d")
    else:
        # try to normalise to YYYY-MM-DD
        raw = str(out["date"])
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
            try:
                out["date"] = datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
                break
            except ValueError:
                continue

    return out


def parse_csv(path: str | Path) -> list[dict]:
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(_normalize_row(dict(row)))
    return rows


def parse_json(path: str | Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return [_normalize_row(r) for r in data]
    if isinstance(data, dict) and "shots" in data:
        return [_normalize_row(r) for r in data["shots"]]
    return [_normalize_row(data)]


def parse_excel(path: str | Path) -> list[dict]:
    """Parse a SwingVision .xlsx/.xls export (first sheet, header row)."""
    try:
        from openpyxl import load_workbook
    except ImportError as e:
        raise ImportError("openpyxl is required to parse Excel files (pip install openpyxl)") from e

    wb = load_workbook(filename=str(path), read_only=True, data_only=True)
    ws = wb.worksheets[0]
    rows_iter = ws.iter_rows(values_only=True)
    try:
        header = [str(h).strip() if h is not None else "" for h in next(rows_iter)]
    except StopIteration:
        return []

    rows = []
    for raw in rows_iter:
        if raw is None or all(v is None for v in raw):
            continue
        row = {header[i]: raw[i] for i in range(min(len(header), len(raw)))}
        rows.append(_normalize_row(row))
    return rows


# ── Session-summary export support ────────────────────────────────────────────
# SwingVision's "export sessions" file is one row PER SESSION (not per shot) —
# e.g. SwingVision_Data.xlsx with Hebrew headers: תאריך, מזהה, מכות, ראלים, % in,
# fh קמ"ש, bh קמ"ש, topspin fh %, topspin bh %, כמות וולי, יריב, סוג, תוצאה, הערות.
# This is the format real users will export and upload — map it straight into
# the same `session dict` shape that coach.swingvision.parse_session() returns,
# so it can be passed directly to db.save_session().

_SESSION_SUMMARY_MAP = {
    "תאריך": "date", "date": "date",
    "מזהה": "match_id", "match_id": "match_id", "id": "match_id", "מזהה משחק": "match_id",
    "מכות": "shots", "shots": "shots",
    "ראלים": "rallies", "rallies": "rallies",
    "% in": "in_pct", "%in": "in_pct", "in_pct": "in_pct", "in%": "in_pct",
    'fh קמ"ש': "fh_speed", "fh speed": "fh_speed",
    'bh קמ"ש': "bh_speed", "bh speed": "bh_speed",
    "topspin fh %": "fh_topspin", "topspin bh %": "bh_topspin",
    "כמות וולי": "volleys", "volleys": "volleys",
    "יריב": "opponent", "opponent": "opponent",
    "סוג": "type", "type": "type",
    "תוצאה": "score", "score": "score",
    "הערות": "notes", "notes": "notes",
}


def looks_like_session_summary(rows: list[dict]) -> bool:
    """Heuristic: does this file look like a per-session export (not per-shot)?"""
    if not rows:
        return False
    keys = {k.strip().lower() for k in rows[0].keys() if isinstance(k, str)}
    has_id    = bool(keys & {"מזהה", "match_id", "id", "מזהה משחק"})
    has_shots = bool(keys & {"מכות", "shots"})
    return has_id and has_shots


def _num(v, default=0):
    try:
        if v is None or v == "":
            return default
        return float(v)
    except (TypeError, ValueError):
        return default


def sessions_from_summary_rows(rows: list[dict]) -> list[dict]:
    """Convert per-session summary rows into session dicts ready for db.save_session.

    Output shape matches coach.swingvision.parse_session():
    {match_id, date, shots, rallies, in_pct, strokes, spin, video_url, note}
    """
    sessions = []
    for raw in rows:
        d: dict = {}
        for k, v in raw.items():
            if not isinstance(k, str):
                continue
            mapped = _SESSION_SUMMARY_MAP.get(k.strip().lower())
            if mapped:
                d[mapped] = v

        mid = d.get("match_id")
        if not mid:
            continue
        mid = str(mid).strip()

        in_pct = _num(d.get("in_pct"))
        strokes: dict = {}
        spin: dict = {}
        fh_spd, bh_spd = _num(d.get("fh_speed")), _num(d.get("bh_speed"))
        if fh_spd:
            strokes["Forehand"] = {"avg_speed": fh_spd, "in_pct": in_pct, "count": 0}
        if bh_spd:
            strokes["Backhand"] = {"avg_speed": bh_spd, "in_pct": in_pct, "count": 0}
        if "fh_topspin" in d:
            spin.setdefault("Forehand", {})["topspin"] = _num(d.get("fh_topspin"))
        if "bh_topspin" in d:
            spin.setdefault("Backhand", {})["topspin"] = _num(d.get("bh_topspin"))
        vols = d.get("volleys")
        if vols not in (None, ""):
            strokes["Volley"] = {"count": int(_num(vols))}

        sessions.append({
            "match_id":  mid,
            "date":      d.get("date") or "",
            "shots":     int(_num(d.get("shots"))),
            "rallies":   int(_num(d.get("rallies"))),
            "in_pct":    in_pct,
            "strokes":   strokes,
            "spin":      spin,
            "video_url": None,
            "note": {
                "opponent": str(d.get("opponent") or ""),
                "type":     str(d.get("type") or ""),
                "score":    str(d.get("score") or ""),
                "free":     str(d.get("notes") or ""),
            },
        })
    return sessions


def parse_file(path: str | Path) -> list[dict]:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return parse_csv(path)
    if suffix in (".json", ".jsonl"):
        return parse_json(path)
    if suffix in (".xlsx", ".xls", ".xlsm"):
        return parse_excel(path)
    raise ValueError(f"Unsupported file type: {path.suffix}")


def summarise_for_prompt(rows: list[dict]) -> str:
    """Convert parsed rows into a concise text summary for the AI prompt."""
    if not rows:
        return "אין נתוני SwingVision."

    total = len(rows)
    by_shot: dict[str, list] = {}
    for r in rows:
        shot = r.get("shot_type") or "לא ידוע"
        by_shot.setdefault(shot, []).append(r)

    lines = [f"סה\"כ {total} מכות נרשמו:"]
    for shot, shots in by_shot.items():
        speeds = [s["speed_kmh"] for s in shots if s.get("speed_kmh")]
        spins = [s["spin_rpm"] for s in shots if s.get("spin_rpm")]
        outcomes = [s.get("outcome", "") for s in shots]
        in_count = sum(1 for o in outcomes if "in" in str(o).lower())
        out_count = sum(1 for o in outcomes if "out" in str(o).lower() or "fault" in str(o).lower())

        line = f"  {shot} ({len(shots)} מכות)"
        if speeds:
            line += f" | מהירות ממוצעת: {sum(speeds)/len(speeds):.0f} קמ\"ש"
            line += f" (מקס: {max(speeds):.0f})"
        if spins:
            line += f" | ספין ממוצע: {sum(spins)/len(spins):.0f} rpm"
        if in_count + out_count > 0:
            pct = round(in_count / (in_count + out_count) * 100)
            line += f" | דיוק: {pct}%"
        lines.append(line)

    return "\n".join(lines)
