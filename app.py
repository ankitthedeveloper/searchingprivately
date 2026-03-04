from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "database.db"

def query_db(search_term):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT * FROM records
    WHERE name LIKE ?
       OR father_name LIKE ?
       OR address LIKE ?
       OR mobile LIKE ?
    LIMIT 100
    """

    value = f"%{search_term}%"
    cursor.execute(query, (value, value, value, value))
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
    app.run(debug=True)