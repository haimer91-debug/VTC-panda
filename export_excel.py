"""Export all SwingVision data to a single Excel file."""
import json, sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd

DB = Path("coach.db")

def run():
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT match_id, date, shots, rallies, stats_json, note_json FROM sessions ORDER BY date"
    ).fetchall()
    conn.close()

    summary, strokes_rows, spin_rows, zones_rows = [], [], [], []

    for match_id, date, shots, rallies, stats_json, note_json in rows:
        s   = json.loads(stats_json or "{}")
        note = json.loads(note_json or "{}")

        # in_pct
        in_pct = (s.get("in_pct")
                  or s.get("in_out", {}).get("in_pct")
                  or 0)

        # speed — handle both formats
        def spd(stroke):
            v = s.get("strokes", {}).get(stroke, {}).get("avg_speed")
            if v: return v
            return s.get("speed", {}).get(stroke, {}).get("avg", 0)

        def ts(stroke):
            return s.get("spin", {}).get(stroke, {}).get("topspin", 0)

        def volley_count():
            return s.get("strokes", {}).get("Volley", {}).get("count", 0)

        def deep_pct():
            bd = s.get("zones", {}).get("bounce_depth", {})
            total = sum(bd.values()) or 1
            return round((bd.get("deep", 0) + bd.get("baseline", 0)) / total * 100, 1)

        summary.append({
            "תאריך": date,
            "מזהה": match_id,
            "מכות": shots,
            "ראלים": rallies,
            "% IN": in_pct,
            "% OUT": round(100 - in_pct, 1),
            "FH קמ\"ש": spd("Forehand"),
            "BH קמ\"ש": spd("Backhand"),
            "Topspin FH %": ts("Forehand"),
            "Topspin BH %": ts("Backhand"),
            "כדורים עמוקים %": deep_pct(),
            "כמות וולי": volley_count(),
            "יריב": note.get("opponent", ""),
            "סוג": note.get("type", ""),
            "תוצאה": note.get("score", ""),
            "הערות": note.get("free", ""),
        })

        for stroke, d in s.get("strokes", {}).items():
            strokes_rows.append({
                "תאריך": date,
                "מכה": stroke,
                "כמות": d.get("count", 0),
                "מהירות ממוצעת": d.get("avg_speed", d.get("avg", 0)),
                "מהירות מקס": d.get("max_speed", d.get("max", 0)),
                "% IN": d.get("in_pct", d.get("in_rate", 0)),
            })

        for stroke, spins in s.get("spin", {}).items():
            for spin_type, pct in spins.items():
                spin_rows.append({
                    "תאריך": date,
                    "מכה": stroke,
                    "ספין": spin_type,
                    "%": pct,
                })

        bd = s.get("zones", {}).get("bounce_depth", {})
        for zone, cnt in bd.items():
            zones_rows.append({"תאריך": date, "אזור נחיתה": zone, "כמות": cnt})

    out = Path("SwingVision_Data.xlsx")
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        pd.DataFrame(summary).to_excel(w, sheet_name="סיכום", index=False)
        if strokes_rows:
            pd.DataFrame(strokes_rows).to_excel(w, sheet_name="מכות", index=False)
        if spin_rows:
            pd.DataFrame(spin_rows).to_excel(w, sheet_name="ספין", index=False)
        if zones_rows:
            pd.DataFrame(zones_rows).to_excel(w, sheet_name="אזורי נחיתה", index=False)

    print(f"Saved: {out.absolute()} ({len(summary)} sessions)")

if __name__ == "__main__":
    run()
