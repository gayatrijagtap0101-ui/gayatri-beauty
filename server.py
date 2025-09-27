from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
from pathlib import Path

app = Flask(__name__)

# Database file
DB_FILE = Path("bookings.db")

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            service TEXT NOT NULL,
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Serve the frontend
@app.route("/")
def home():
    return send_from_directory(".", "Gayatri.html")

# API endpoint for bookings
@app.route("/api/book", methods=["POST"])
def book():
    data = request.json
    name = data.get("name")
    address = data.get("address")
    service = data.get("service")
    date = data.get("date")

    if not all([name, address, service, date]):
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bookings (name, address, service, date) VALUES (?, ?, ?, ?)",
        (name, address, service, date)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Booking submitted successfully!"})

# Admin page to view bookings
@app.route("/admin")
def admin():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, address, service, date, created_at FROM bookings ORDER BY created_at DESC")
    bookings = cursor.fetchall()
    conn.close()
    return render_template("admin.html", bookings=bookings)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
