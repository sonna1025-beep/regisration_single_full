from flask import Flask, request, redirect, url_for, flash, send_file, render_template_string
import sqlite3
import re
import pandas as pd

app = Flask(__name__)
app.secret_key = "secret123"

DB_NAME = "register.db"
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ovog TEXT,
        ner TEXT,
        utas TEXT,
        email TEXT UNIQUE
    )''')
    conn.commit()
    conn.close()

HTML = """<!DOCTYPE html>
<html><body>
<h2>Бүртгэл</h2>

{% with messages = get_flashed_messages(with_categories=true) %}
{% for category, msg in messages %}
<p>{{msg}}</p>
{% endfor %}
{% endwith %}

<form method="POST" action="/register">
<input name="ovog" placeholder="Овог" required><br>
<input name="ner" placeholder="Нэр" required><br>
<input name="utas" placeholder="Утас" required><br>
<input name="email" placeholder="Имэйл (example@gmail.com)" required><br>
<button>Register</button>
</form>

<a href="/admin">Admin</a>
</body></html>"""

ADMIN_HTML = """<html><body>
<h2>Admin</h2>
<table border=1>
<tr><th>Овог</th><th>Нэр</th><th>Утас</th><th>Имэйл</th></tr>
{% for row in data %}
<tr>
<td>{{ row[1] }}</td>
<td>{{ row[2] }}</td>
<td>{{ row[3] }}</td>
<td>{{ row[4] }}</td>
</tr>
{% endfor %}
</table>
<br>
<a href="/export">Excel татах</a>
</body></html>"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/register', methods=['POST'])
def register():
    ovog = request.form['ovog']
    ner = request.form['ner']
    utas = request.form['utas']
    email = request.form['email']

    if not re.match(EMAIL_REGEX, email):
        flash("Имэйл буруу! Жишээ: example@gmail.com", "error")
        return redirect(url_for('index'))

    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO users (ovog, ner, utas, email) VALUES (?, ?, ?, ?)",
                  (ovog, ner, utas, email))
        conn.commit()
        conn.close()
        flash("Бүртгэл амжилттай!", "success")
    except:
        flash("Имэйл давхардсан!", "error")

    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    data = c.fetchall()
    conn.close()
    return render_template_string(ADMIN_HTML, data=data)

@app.route('/export')
def export():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT ovog, ner, utas, email FROM users", conn)
    conn.close()
    file = "Register.xlsx"
    df.to_excel(file, index=False)
    return send_file(file, as_attachment=True)

if __name__ == "__main__":
    from waitress import serve
    init_db()
    serve(app, host="0.0.0.0", port=5000)
