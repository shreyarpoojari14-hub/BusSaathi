from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path("bussaathi.db")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bus_location (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                bus_id TEXT NOT NULL,
                route_name TEXT NOT NULL,
                lat REAL NOT NULL,
                lon REAL NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_type TEXT NOT NULL,
                note TEXT,
                created_at TEXT NOT NULL
            )
        """)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/driver")
def driver():
    return render_template("driver.html")

@app.route("/api/location", methods=["GET", "POST"])
def location():
    if request.method == "POST":
        data = request.get_json(force=True)
        required = ["lat", "lon"]
        if not all(k in data for k in required):
            return jsonify({"error": "lat and lon are required"}), 400
        bus_id = str(data.get("bus_id", "DEMO-01"))[:30]
        route_name = str(data.get("route_name", "Demo route"))[:80]
        updated_at = datetime.now(timezone.utc).isoformat()
        with db() as conn:
            conn.execute("""
                INSERT INTO bus_location (id, bus_id, route_name, lat, lon, updated_at)
                VALUES (1, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    bus_id=excluded.bus_id,
                    route_name=excluded.route_name,
                    lat=excluded.lat,
                    lon=excluded.lon,
                    updated_at=excluded.updated_at
            """, (bus_id, route_name, float(data["lat"]), float(data["lon"]), updated_at))
        return jsonify({"ok": True, "updated_at": updated_at})

    with db() as conn:
        row = conn.execute("SELECT * FROM bus_location WHERE id=1").fetchone()
    if not row:
        return jsonify({"available": False})
    age_seconds = (datetime.now(timezone.utc) -
                   datetime.fromisoformat(row["updated_at"])).total_seconds()
    if age_seconds <= 30:
        status = "LIVE"
    elif age_seconds <= 120:
        status = "DELAYED"
    else:
        status = "STALE"
    return jsonify({
        "available": True,
        "bus_id": row["bus_id"],
        "route_name": row["route_name"],
        "lat": row["lat"],
        "lon": row["lon"],
        "updated_at": row["updated_at"],
        "age_seconds": round(age_seconds),
        "status": status
    })

@app.route("/api/report", methods=["POST"])
def report():
    data = request.get_json(force=True)
    report_type = str(data.get("report_type", "Other"))[:60]
    note = str(data.get("note", ""))[:250]
    with db() as conn:
        conn.execute(
            "INSERT INTO reports (report_type, note, created_at) VALUES (?, ?, ?)",
            (report_type, note, datetime.now(timezone.utc).isoformat())
        )
    return jsonify({"ok": True, "message": "Report saved for demo review."})

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5000)
