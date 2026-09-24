# =============================================================================
# SUMAN INFO — SQLITE DATA LAYER
# -----------------------------------------------------------------------------
# ALL site content (company info, contact details, theme colors, products,
# team) lives in this SQLite database (contact_submissions.db), not in
# config.py. config.py only supplies the ONE-TIME seed values used the very
# first time the app runs (when the tables are empty) and the admin
# username/password/secret key. After that first run, edit everything from
# the Admin Panel at /admin — changes are saved here and take effect
# immediately, with no code edits or restarts required.
# =============================================================================
import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "contact_submissions.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Ensures all tables exist even if the .db file was deleted/moved externally.
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            received_at TEXT NOT NULL,
            is_read INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tagline TEXT NOT NULL,
            description TEXT NOT NULL,
            price TEXT NOT NULL,
            icon TEXT NOT NULL,
            color TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS team (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            initials TEXT NOT NULL,
            color TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0
        );
        """
    )
    return conn


def init_db():
    """Create tables if they don't already exist."""
    get_connection().close()


def seed_defaults(defaults):
    """Populate settings/products/team ONLY if the tables are still empty.

    `defaults` is a dict with keys: company, contact, theme, nav_links,
    products (list), team (list) — see config.py for the shape. This never
    overwrites data an admin has already edited/saved.
    """
    with get_connection() as conn:
        settings_count = conn.execute("SELECT COUNT(*) AS c FROM settings").fetchone()["c"]
        products_count = conn.execute("SELECT COUNT(*) AS c FROM products").fetchone()["c"]
        team_count = conn.execute("SELECT COUNT(*) AS c FROM team").fetchone()["c"]

    if settings_count == 0:
        set_setting("company", defaults["company"])
        set_setting("contact", defaults["contact"])
        set_setting("theme", defaults["theme"])
        set_setting("nav_links", defaults["nav_links"])

    if products_count == 0:
        for i, p in enumerate(defaults["products"]):
            add_product({**p, "sort_order": i})

    if team_count == 0:
        for i, t in enumerate(defaults["team"]):
            add_team_member({**t, "sort_order": i})


# -----------------------------------------------------------------------------
# Settings (company / contact / theme / nav_links) — stored as JSON blobs
# -----------------------------------------------------------------------------
def get_setting(key, default=None):
    with get_connection() as conn:
        row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return json.loads(row["value"]) if row else default


def set_setting(key, value):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, json.dumps(value)),
        )
        conn.commit()


# -----------------------------------------------------------------------------
# Products (Services/Products section — fully admin-editable)
# -----------------------------------------------------------------------------
def get_products():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM products ORDER BY sort_order, id").fetchall()
        return [dict(row) for row in rows]


def get_product(product_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        return dict(row) if row else None


def add_product(data):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO products (name, tagline, description, price, icon, color, sort_order) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (data["name"], data["tagline"], data["description"], data["price"],
             data["icon"], data["color"], data.get("sort_order", 0)),
        )
        conn.commit()


def update_product(product_id, data):
    with get_connection() as conn:
        conn.execute(
            "UPDATE products SET name=?, tagline=?, description=?, price=?, icon=?, color=?, sort_order=? "
            "WHERE id=?",
            (data["name"], data["tagline"], data["description"], data["price"],
             data["icon"], data["color"], data.get("sort_order", 0), product_id),
        )
        conn.commit()


def delete_product(product_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()


# -----------------------------------------------------------------------------
# Team members — fully admin-editable
# -----------------------------------------------------------------------------
def get_team():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM team ORDER BY sort_order, id").fetchall()
        return [dict(row) for row in rows]


def get_team_member(member_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM team WHERE id = ?", (member_id,)).fetchone()
        return dict(row) if row else None


def add_team_member(data):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO team (name, role, initials, color, sort_order) VALUES (?, ?, ?, ?, ?)",
            (data["name"], data["role"], data["initials"], data["color"], data.get("sort_order", 0)),
        )
        conn.commit()


def update_team_member(member_id, data):
    with get_connection() as conn:
        conn.execute(
            "UPDATE team SET name=?, role=?, initials=?, color=?, sort_order=? WHERE id=?",
            (data["name"], data["role"], data["initials"], data["color"], data.get("sort_order", 0), member_id),
        )
        conn.commit()


def delete_team_member(member_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM team WHERE id = ?", (member_id,))
        conn.commit()


# -----------------------------------------------------------------------------
# Contact form submissions
# -----------------------------------------------------------------------------
def add_submission(name, email, message, received_at):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO submissions (name, email, message, received_at) VALUES (?, ?, ?, ?)",
            (name, email, message, received_at),
        )
        conn.commit()


def get_all_submissions():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM submissions ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def mark_as_read(submission_id):
    with get_connection() as conn:
        conn.execute("UPDATE submissions SET is_read = 1 WHERE id = ?", (submission_id,))
        conn.commit()


def delete_submission(submission_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM submissions WHERE id = ?", (submission_id,))
        conn.commit()


def count_unread():
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS c FROM submissions WHERE is_read = 0").fetchone()
        return row["c"] if row else 0
