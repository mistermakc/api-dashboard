from flask import Flask, render_template, request, session, redirect
from sqlalchemy import create_engine

app = Flask(__name__)
engine = create_engine("sqlite:///paymepal.db")
app.config["SECRET_KEY"] = "Max"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    query = f"""
    SELECT *
    FROM transactions t
    INNER JOIN shops s
    ON t.shop_id = s.id
    WHERE user_id='{session["user_id"]}'
    """

    with engine.connect() as connection:
        results = connection.execute(query).fetchall()

    return render_template("private.html", transactions=results)

@app.route("/unauthorized")
def unauthorized():
    return render_template("unauthorized.html"), 403

@app.route("/login", methods=["POST"])
def login():
    username = request.form["user"]
    password = request.form["password"]

    query = f"""
        SELECT * 
        FROM users 
        WHERE username='{username}' AND password='{password}';
        """

    with engine.connect() as connection:
        row = connection.execute(query).fetchone()

        if row:
            session["username"] = username
            session["user_id"] = row[0]

            return redirect("/admin")

        else:
            return redirect("/unauthorized")

app.run(debug=True, port=8080)