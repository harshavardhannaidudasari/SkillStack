"""SkillStack — a personal skill/learning tracker.

Tracks skills across any technology, programming language, tool, or soft
skill: what you're learning, how far along you are, and notes/resources for
each. Single-file Flask app backed by SQLite — no external services needed.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, g, redirect, render_template, request, url_for

DB_PATH = Path(__file__).resolve().parent / "data" / "skillstack.db"

STATUSES = ["Want to Learn", "Learning", "Proficient", "Expert"]
# Free-text category (not an enum) is what actually makes this cover "every
# technology and programming language" rather than a fixed list this app
# would need updating every time a new one shows up — these are just
# starting suggestions shown in the add-skill form's datalist.
CATEGORY_SUGGESTIONS = [
    "Programming Language", "Frontend", "Backend", "Database", "DevOps",
    "Cloud", "Mobile", "Machine Learning", "Data Science", "Testing",
    "Security", "Design", "Soft Skill", "Tool",
]

app = Flask(__name__)


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc: BaseException | None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'Want to Learn',
            progress INTEGER NOT NULL DEFAULT 0,
            notes TEXT NOT NULL DEFAULT '',
            resources TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    db.commit()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def clamp_progress(value: str | int) -> int:
    try:
        n = int(value)
    except (TypeError, ValueError):
        return 0
    return max(0, min(100, n))


@app.route("/")
def index():
    db = get_db()
    category = request.args.get("category", "").strip()
    status = request.args.get("status", "").strip()

    query = "SELECT * FROM skills WHERE 1=1"
    params: list[str] = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if status:
        query += " AND status = ?"
        params.append(status)
    query += " ORDER BY updated_at DESC"

    skills = db.execute(query, params).fetchall()
    categories = [
        r["category"]
        for r in db.execute(
            "SELECT DISTINCT category FROM skills WHERE category != '' ORDER BY category"
        ).fetchall()
    ]
    counts = {
        row["status"]: row["n"]
        for row in db.execute(
            "SELECT status, COUNT(*) AS n FROM skills GROUP BY status"
        ).fetchall()
    }

    return render_template(
        "index.html",
        skills=skills,
        statuses=STATUSES,
        category_suggestions=CATEGORY_SUGGESTIONS,
        categories=categories,
        counts=counts,
        selected_category=category,
        selected_status=status,
        total=sum(counts.values()),
    )


@app.route("/skills", methods=["POST"])
def add_skill():
    name = request.form.get("name", "").strip()
    if not name:
        return redirect(url_for("index"))

    db = get_db()
    ts = now_iso()
    db.execute(
        """
        INSERT INTO skills (name, category, status, progress, notes, resources, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            request.form.get("category", "").strip(),
            request.form.get("status", STATUSES[0]),
            clamp_progress(request.form.get("progress", 0)),
            request.form.get("notes", "").strip(),
            request.form.get("resources", "").strip(),
            ts,
            ts,
        ),
    )
    db.commit()
    return redirect(url_for("index"))


@app.route("/skills/<int:skill_id>/update", methods=["POST"])
def update_skill(skill_id: int):
    db = get_db()
    db.execute(
        """
        UPDATE skills
        SET name = ?, category = ?, status = ?, progress = ?, notes = ?, resources = ?, updated_at = ?
        WHERE id = ?
        """,
        (
            request.form.get("name", "").strip(),
            request.form.get("category", "").strip(),
            request.form.get("status", STATUSES[0]),
            clamp_progress(request.form.get("progress", 0)),
            request.form.get("notes", "").strip(),
            request.form.get("resources", "").strip(),
            now_iso(),
            skill_id,
        ),
    )
    db.commit()
    return redirect(url_for("index"))


@app.route("/skills/<int:skill_id>/delete", methods=["POST"])
def delete_skill(skill_id: int):
    db = get_db()
    db.execute("DELETE FROM skills WHERE id = ?", (skill_id,))
    db.commit()
    return redirect(url_for("index"))


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True, port=5050)
