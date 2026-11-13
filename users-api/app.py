"""Lab 8 - Activity 2, image 2: users API on port 3000 exposing GET get_users."""

import sqlite3
from contextlib import closing
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

DATABASE = Path(__file__).resolve().with_name("database.db")
FIELDS = ("name", "email", "phone", "address", "country")

# Inserted only when the users table is empty, so get_users has data to return.
SAMPLE_USERS = [
    ("John Doe", "john@example.com", "067765434567", "John Doe Street, Innsbruck", "Austria"),
    ("Jane Smith", "jane@example.com", "03123456", "Hamra Street, Beirut", "Lebanon"),
    ("Ali Hassan", "ali@example.com", "71987654", "Bliss Street, Beirut", "Lebanon"),
]


def connect_to_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_db_table():
    with closing(connect_to_db()) as conn, conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            )
        """)
        if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
                SAMPLE_USERS,
            )


def get_user_names():
    with closing(connect_to_db()) as conn:
        return [row["name"] for row in conn.execute("SELECT name FROM users ORDER BY user_id")]


def insert_user(user):
    with closing(connect_to_db()) as conn, conn:
        cur = conn.execute(
            "INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
            tuple(user[field] for field in FIELDS),
        )
        return {"user_id": cur.lastrowid, **{field: user[field] for field in FIELDS}}


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
create_db_table()


@app.route("/api/get_users", methods=["GET"])
def api_get_users():
    """Return a list of the names of all users in the database."""
    return jsonify(get_user_names())


@app.route("/api/users/add", methods=["POST"])
def api_add_user():
    user = request.get_json(silent=True)
    if not isinstance(user, dict):
        return jsonify(error="Request body must be a JSON object"), 400
    for field in FIELDS:
        if not isinstance(user.get(field), str) or not user[field].strip():
            return jsonify(error=f"{field} must be a nonempty string"), 400
    return jsonify(insert_user(user))


if __name__ == "__main__":
    # 0.0.0.0 so the app is reachable from outside the Docker container
    app.run(host="0.0.0.0", port=3000)
