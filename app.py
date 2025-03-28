from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import supabase
import os
from datetime import datetime

from gotrue.errors import AuthError, AuthApiError

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

sb = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)


# Helper function to check if user is logged in
def is_logged_in():
    return "user" in session


# Helper function to fetch a movie
def fetch_movie(movie_id):
    movie = sb.table("movies").select("*").eq("id", movie_id).execute().data
    return movie[0] if movie else None


# Fetch all movies
def get_movies():
    response = sb.table("movies").select("*").execute()
    return response.data or []


@app.route("/")
def index():
    return render_template("index.html", movies=get_movies())


@app.route("/login", methods=["GET", "POST"])
def login():
    response = None
    if request.method == "POST":
        email, password = request.form["email"], request.form["password"]
        try:
            response = sb.auth.sign_in_with_password({"email": email, "password": password})
        except AuthApiError as auth_exception:
            print(auth_exception)
            return render_template("login.html", error="Nieprawidłowe dane logowania")
        finally:
            if response and hasattr(response, "user"):
                session["user"] = response.user.email
                return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not is_logged_in():
        return redirect(url_for("login"))

    today_date = datetime.today().strftime('%Y-%m-%d')
    if request.method == "POST":
        release_year = request.form.get("release_year")
        release_year = f"{release_year}-01-01" if release_year else None
        data = {
            "polish_title": request.form["polish_title"],
            "original_title": request.form["original_title"],
            "watched_date": request.form["watched_date"],
            "rating": request.form["rating"],
            "release_year": release_year,
            "who_submitted": session["user"].split("@")[0]
        }
        sb.table("movies").insert(data).execute()
        return redirect(url_for("index"))
    return render_template("admin.html", today_date=today_date)


@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    if not is_logged_in():
        return redirect(url_for("login"))

    movie = fetch_movie(movie_id)
    if not movie:
        return "Film nie został znaleziony", 404

    if request.method == "POST":
        release_year = request.form.get("release_year")
        release_year = f"{release_year}-01-01" if release_year else None
        updated_data = {
            "polish_title": request.form["polish_title"],
            "original_title": request.form["original_title"],
            "watched_date": request.form["watched_date"],
            "rating": request.form["rating"],
            "release_year": release_year,
            "who_submitted": session["user"].split("@")[0]
        }
        sb.table("movies").update(updated_data).eq("id", movie_id).execute()
        return redirect(url_for("index"))

    return render_template("edit.html", movie=movie)


@app.route('/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    if not is_logged_in():
        return redirect(url_for('login'))

    sb.table('movies').delete().eq('id', movie_id).execute()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=False)

