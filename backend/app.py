from flask import Flask, jsonify
import os
import mysql.connector

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Backend is running"
    })

@app.route("/api/users")
def users():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "appuser"),
            password=os.getenv("DB_PASSWORD", "apppassword"),
            database=os.getenv("DB_NAME", "appdb")
        )

        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM users")
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify([
            {"id": row[0], "name": row[1]}
            for row in rows
        ])

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
