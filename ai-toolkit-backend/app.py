# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sqlite3 # Using SQLite for simplicity, but you'd use PostgreSQL for Render production

app = Flask(__name__)
CORS(app) # Enable CORS to allow requests from your frontend domain

DATABASE = 'users.db' # For SQLite, this will be a file. For PostgreSQL, it's a connection string.

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # This function creates the database table if it doesn't exist
    with app.app_context():
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                toolkit_name TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def home():
    return "AI Toolkit Backend is running!"

@app.route('/api/capture-user-data', methods=['POST'])
def capture_user_data():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    toolkit_name = data.get('toolkit') # Optional: if you send this from frontend

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, toolkit_name) VALUES (?, ?, ?)",
                       (name, email, toolkit_name))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return jsonify({"message": "User data captured successfully", "id": user_id}), 201
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Failed to store data", "details": str(e)}), 500

if __name__ == '__main__':
    init_db() # Initialize the database when the app starts (for SQLite)
    app.run(debug=True) # debug=True is for local development only