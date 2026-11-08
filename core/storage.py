import json
import os
import sqlite3

DB = os.getenv("VULNX_DB", "storage/vulnx.db")


def init():
    os.makedirs(os.path.dirname(DB) or ".", exist_ok=True)
    with sqlite3.connect(DB) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS scans(id TEXT PRIMARY KEY,target TEXT,created TEXT,payload TEXT)"
        )


def save(scan):
    init()
    with sqlite3.connect(DB) as connection:
        connection.execute(
            "INSERT OR REPLACE INTO scans VALUES(?,?,?,?)",
            (scan["scan_id"], scan["target"], scan["started_at"], json.dumps(scan)),
        )


def recent(limit=25):
    init()
    with sqlite3.connect(DB) as connection:
        rows = connection.execute(
            "SELECT payload FROM scans ORDER BY created DESC LIMIT ?", (limit,)
        ).fetchall()
    return [json.loads(row[0]) for row in rows]
