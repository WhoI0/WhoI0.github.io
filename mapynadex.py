# server.py
import time
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os

DB_FILE = os.getenv("SMOKERS_DB", "smokers.db")
EXPIRE_SECONDS = 10 * 60  # 10 минут

app = FastAPI(title="Smokers backend")

class Report(BaseModel):
    user_id: int
    first_name: str | None = None
    lat: float
    lon: float
    ttl: int | None = None  # optional: custom TTL seconds

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS smokers (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT,
        lat REAL,
        lon REAL,
        ts INTEGER
    )
    """)
    conn.commit()
    conn.close()

def upsert_position(user_id: int, first_name: str, lat: float, lon: float):
    ts = int(time.time())
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO smokers(user_id, first_name, lat, lon, ts) VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET first_name=excluded.first_name, lat=excluded.lat, lon=excluded.lon, ts=excluded.ts
    """, (user_id, first_name, lat, lon, ts))
    conn.commit()
    conn.close()

def get_active_smokers() -> List[dict]:
    cutoff = int(time.time()) - EXPIRE_SECONDS
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT user_id, first_name, lat, lon, ts FROM smokers WHERE ts >= ?", (cutoff,))
    rows = cur.fetchall()
    conn.close()
    return [{"user_id": r[0], "first_name": r[1], "lat": r[2], "lon": r[3], "ts": r[4]} for r in rows]

def cleanup_old():
    cutoff = int(time.time()) - EXPIRE_SECONDS
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM smokers WHERE ts < ?", (cutoff,))
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup():
    init_db()

@app.post("/report")
async def report_pos(r: Report):
    # basic validation
    if not (-90 <= r.lat <= 90 and -180 <= r.lon <= 180):
        raise HTTPException(400, "Invalid coordinates")
    upsert_position(r.user_id, r.first_name or "", r.lat, r.lon)
    cleanup_old()
    return {"status": "ok"}

@app.get("/smokers")
async def smokers_list():
    cleanup_old()
    return get_active_smokers()
