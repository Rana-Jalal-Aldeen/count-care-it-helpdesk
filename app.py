from flask import Flask, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "countcare_secret"

style = """
<style>
body {
    font-family: Arial, sans-serif;
    background: #eef2f7;
    margin: 0;
    color: #172b4d;
}

.navbar {
    background: linear-gradient(90deg, #0f1f38, #173b70);
    padding: 22px 35px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.2);
}

.navbar h2,
.logo {
    margin: 0;
    font-size: 26px;
    color: white !important;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 15px;
}

.user {
    color: white;
    font-weight: bold;
}

.logout-btn {
    background: #ff4d4d;
    color: white;
    padding: 8px 14px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: bold;
}

.logout-btn:hover {
    background: #cc0000;
}


.container {
    padding: 35px;
    max-width: 1100px;
    margin: auto;
}

h1, h2 {
    color: #172b4d;
}

.card {
    background: white;
    padding: 25px;
    margin-bottom: 20px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(9,30,66,0.15);
    border-left: 6px solid #0052cc;
}

.card:hover {
    transform: translateY(-2px);
    transition: 0.2s;
}

button {
    background: #0052cc;
    color: white;
    border: none;
    padding: 12px 18px;
    border-radius: 8px;
    cursor: pointer;
    margin-right: 10px;
    font-weight: bold;
}

button:hover {
    background: #0065ff;
}

input, textarea, select {
    width: 100%;
    padding: 12px;
    margin: 8px 0 18px 0;
    border-radius: 8px;
    border: 1px solid #c1c7d0;
    box-sizing: border-box;
}

form {
    background: white;
    padding: 28px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(9,30,66,0.15);
}

.status {
    padding: 7px 12px;
    border-radius: 20px;
    color: white;
    font-size: 13px;
    font-weight: bold;
    display: inline-block;
}

.open { background: #6b778c; }
.progress { background: #ff991f; }
.done { background: #36b37e; }

a {
    color: #0052cc;
    font-weight: bold;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

.high-priority {
    background: #ffdddd;
    color: #b00020;
    padding: 5px 10px;
    border-radius: 12px;
    font-weight: bold;
}

.medium-priority {
    background: #fff3cd;
    color: #856404;
    padding: 5px 10px;
    border-radius: 12px;
    font-weight: bold;
}

.low-priority {
    background: #ddffdd;
    color: #1b5e20;
    padding: 5px 10px;
    border-radius: 12px;
    font-weight: bold;
}

</style>
"""

def navbar():

    username = session.get("username", "Gast")

    return f"""
    <div class="navbar">

        <h2 class="logo">COUNT+CARE IT Help Desk</h2>

        <div class="nav-right">

            <span class="user">
                Eingeloggt als: {username}
            </span>

            <a href="/logout" class="logout-btn">
                Logout
            </a>

        </div>

    </div>
    """


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("tickets.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = username
            session["role"] = user[3]
            return redirect(url_for("home"))
        else:
            return style + """
            <div class="container">
                <form method="POST">
                    <h2>Login</h2>
                    <p style="color:red;">Falscher Benutzername oder Passwort</p>

                    <label>Benutzername:</label>
                    <input name="username" required>

                    <label>Passwort:</label>
                    <input name="password" type="password" required>

                    <button>Einloggen</button>
                </form>
            </div>
            """

    return style + """
    <div class="container">
        <form method="POST">
            <h2>Login</h2>

            <label>Benutzername:</label>
            <input name="username" required>

            <label>Passwort:</label>
            <input name="password" type="password" required>

            <button>Einloggen</button>
        </form>
    </div>
    """

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
def home():
    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tickets")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status='Offen'")
    offen = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status='In Bearbeitung'")
    in_bearbeitung = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status='Gelöst'")
    geloest = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE priority='Hoch'")
    high_priority = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE priority='Mittel'")
    medium_priority = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE priority='Niedrig'")
    low_priority = cursor.fetchone()[0]

    conn.close()

    return style + navbar() + f"""
    <div class="container">
        <h1>Dashboard</h1>

        <p>Eingeloggt als: {session["username"]}</p>
        <a href="/logout"><button>Logout</button></a>
        <br><br>

        <div class="card" onclick="window.location='/tickets'" style="cursor:pointer;">
            <h3>Alle Tickets</h3>
            <h2>{total}</h2>
        </div>

           <div class="card" onclick="window.location='/tickets?status=Offen'" style="cursor:pointer;">
                    <h3>Offen</h3>
                    <h2>{offen}</h2>
                </div>

                <div class="card" onclick="window.location='/tickets?status=In Bearbeitung'" style="cursor:pointer;">
                    <h3>In Bearbeitung</h3>
                    <h2>{in_bearbeitung}</h2>
                </div>

                <div class="card" onclick="window.location='/tickets?status=Gelöst'" style="cursor:pointer;">
                    <h3>Gelöst</h3>
                    <h2>{geloest}</h2>
                </div>  

        <div class="card" onclick="window.location='/tickets?priority=Hoch'" style="cursor:pointer;">
                    <h3>Hohe Priorität</h3>
                    <h2>{high_priority}</h2>
                </div>  

        <div class="card" onclick="window.location='/tickets?priority=Mittel'" style="cursor:pointer;">
                    <h3>Mittlere Priorität</h3>
                    <h2>{medium_priority}</h2>
                </div>

        <div class="card" onclick="window.location='/tickets?priority=Niedrig'" style="cursor:pointer;">
                    <h3>Niedrige Priorität</h3>
                    <h2>{low_priority}</h2>
                </div>

        <a href="/create"><button>Ticket erstellen</button></a>
        <a href="/tickets"><button>Alle Tickets anzeigen</button></a>
    </div>
    """

@app.route("/create", methods=["GET", "POST"])
def create_ticket():

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        category = request.form.get("category")
        priority = request.form.get("priority")
        assigned_to = request.form.get("assigned_to")
        created_at = datetime.now().strftime("%d.%m.%Y %H:%M")
        conn = sqlite3.connect("tickets.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tickets (title, description, category, status, priority, assigned_to, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (title, description, category, "Offen", priority, assigned_to, created_at)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("show"))

    return style + navbar() + """
    <div class="container">
        <form method="POST">
            <h2>Neues Ticket</h2>

            <label>Titel:</label>
            <input name="title" required>

            <label>Beschreibung:</label>
            <textarea name="description" required></textarea>

            <label>Kategorie:</label>
            <select name="category">
                <option>Netzwerk</option>
                <option>Hardware</option>
                <option>Software</option>
                <option>Zugang</option>
            </select>

            <label>Priorität:</label>

            <select name="priority">
                <option>Niedrig</option>
                <option selected>Mittel</option>
                <option>Hoch</option>
            </select>

            <label>Zuständig</label>

            <select name="assigned_to">
                <option>Ahmad</option>
                <option>IT Support</option>
                <option>Admin</option>
            </select>

            <button>Speichern</button>
        </form>
    </div>
    """

@app.route("/tickets")
def show():

    if "username" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search")
    status_filter = request.args.get("status")

    priority_filter = request.args.get("priority")

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    query = "SELECT * FROM tickets WHERE 1=1"
    params = []

    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")

    if status_filter and status_filter != "Alle":
        query += " AND status = ?"
        params.append(status_filter)

    if priority_filter and priority_filter != "Alle":
        query += " AND priority = ?"
        params.append(priority_filter)

    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()

    html = style + navbar() + """
    <div class="container">
    <h2>Tickets</h2>

    <br>
    <a href="/"><button>🏠 Startseite</button></a>
    <br><br>

    <form method="GET">
        Suche:
        <input name="search" placeholder="Titel suchen">

        Status:
        <select name="status">
            <option>Alle</option>
            <option>Offen</option>
            <option>In Bearbeitung</option>
            <option>Gelöst</option>
        </select>

        <button>Suchen</button>
    </form>
    <br>
    """

    for t in data:

        status_class = "open"

        priority_class = "low-priority"

        if t[5] == "Mittel":
            priority_class = "medium-priority"

        if t[5] == "Hoch":
            priority_class = "high-priority"

        if t[4] == "In Bearbeitung":
            status_class = "progress"

        if t[4] == "Gelöst":
            status_class = "done"

        html += f"""
        <div class="card" onclick="window.location='/edit/{t[0]}'" style="cursor:pointer;">
            <b>{t[1]}</b><br>
            {t[2]}<br>
            <i>{t[3]}</i><br><br>

            <b>Priorität:</b> <span class="{priority_class}">{t[5]}</span><br><br>

            <b>Zuständig:</b> {t[6]}<br><br>
            <b>Erstellt am:</b> {t[7]}<br><br>

            <span class="status {status_class}">{t[4]}</span><br><br>

            <a href="/edit/{t[0]}" onclick="event.stopPropagation()">Bearbeiten</a> |
            <a href="/delete/{t[0]}"
                onclick="event.stopPropagation(); return confirm('Möchten Sie dieses Ticket wirklich löschen?')">
                Löschen
            </a>
         </div>
        """

    html += "</div>"

    return html

@app.route("/add_comment/<int:ticket_id>", methods=["POST"])
def add_comment(ticket_id):

    if "username" not in session:
        return redirect(url_for("login"))

    comment = request.form.get("comment")
    created_at = datetime.now().strftime("%d.%m.%Y %H:%M")
    username = session["username"]

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO comments (ticket_id, username, comment, created_at)
    VALUES (?, ?, ?, ?)
    """, (ticket_id, username, comment, created_at))

    conn.commit()
    conn.close()

    return redirect(url_for("edit", id=ticket_id))

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):

    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        category = request.form.get("category")
        status = request.form.get("status")

        priority = request.form.get("priority")
        assigned_to = request.form.get("assigned_to")

        cursor.execute(
            "UPDATE tickets SET title=?, description=?, category=?, status=?, priority=?, assigned_to=? WHERE id=?",
            (title, description, category, status, priority, assigned_to, id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("show"))

    cursor.execute("SELECT * FROM tickets WHERE id=?", (id,))
    t = cursor.fetchone()

    cursor.execute(
        "SELECT username, comment, created_at FROM comments WHERE ticket_id=? ORDER BY id DESC",
        (id,)
    )
    comments = cursor.fetchall()

    conn.close()

    comments_html = ""

    for c in comments:
        comments_html += f"""
        <div class="card">
            <b>{c[0]}</b> - <small>{c[2]}</small><br>
            {c[1]}
        </div>
        """

    return style + navbar() + f"""
    <div class="container">
    <form method="POST">
        <h2>Ticket bearbeiten</h2>

        Titel:
        <input name="title" value="{t[1]}">

        Beschreibung:
        <textarea name="description">{t[2]}</textarea>

        Kategorie:
        <select name="category">
            <option {"selected" if t[3]=="Netzwerk" else ""}>Netzwerk</option>
            <option {"selected" if t[3]=="Hardware" else ""}>Hardware</option>
            <option {"selected" if t[3]=="Software" else ""}>Software</option>
            <option {"selected" if t[3]=="Zugang" else ""}>Zugang</option>
        </select>

        Status:
        <select name="status">
            <option {"selected" if t[4]=="Offen" else ""}>Offen</option>
            <option {"selected" if t[4]=="In Bearbeitung" else ""}>In Bearbeitung</option>
            <option {"selected" if t[4]=="Gelöst" else ""}>Gelöst</option>
        </select>

        <br><br>

        Priority:
        <select name="priority">
            <option {"selected" if t[5]=="Niedrig" else ""}>Niedrig</option>
            <option {"selected" if t[5]=="Mittel" else ""}>Mittel</option>
            <option {"selected" if t[5]=="Hoch" else ""}>Hoch</option>
        </select>

        <br><br>

        Assigned To:
        <select name="assigned_to">
            <option {"selected" if t[6]=="Ahmad" else ""}>Ahmad</option>
            <option {"selected" if t[6]=="IT Support" else ""}>IT Support</option>
            <option {"selected" if t[6]=="Admin" else ""}>Admin</option>
        </select>


        <button>Speichern</button>
    </form>

    <hr>
    <h3>Kommentare</h3>

    <form method="POST" action="/add_comment/{id}">
        <textarea name="comment" placeholder="Kommentar schreiben..." required></textarea>
        <button>Kommentar hinzufügen</button>
    </form>

    <br>

    {comments_html}

    </div>
    """

@app.route("/delete/<int:id>")
def delete(id):

    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("show"))


if __name__ == "__main__":
    app.run(debug=True)