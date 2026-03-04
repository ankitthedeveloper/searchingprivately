from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Works both locally and on Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

def query_db(search_term):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT * FROM records
    WHERE CAST(ID AS TEXT) LIKE ?
       OR name LIKE ?
       OR father_name LIKE ?
       OR address LIKE ?
       OR mobile LIKE ?
    LIMIT 100
    """

    value = f"%{search_term}%"
    cursor.execute(query, (value, value, value, value, value))
    results = cursor.fetchall()
    conn.close()

    return [dict(row) for row in results]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    term = request.args.get("q", "")
    if term == "":
        return jsonify([])
    results = query_db(term)
    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
