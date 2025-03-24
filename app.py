from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import supabase
import os
from datetime import datetime

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


sb = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# Strona główna - wyświetlanie filmów
def get_movies():
    response = sb.table("movies").select("*").execute()
    return response.data if response.data else []

@app.route("/")
def index():
    movies = get_movies()
    return render_template("index.html", movies=movies)

# Logowanie użytkownika
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        response = sb.auth.sign_in_with_password({"email": email, "password": password})
        if response.user:
            session["user"] = response.user.email  # Zamiast response.user["email"]
            return redirect(url_for("index"))
    return render_template("login.html")


# Wylogowanie
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


# Podstrona admina - dodawanie filmów
@app.route("/admin", methods=["GET", "POST"])
def admin():
    today_date = datetime.today().strftime('%Y-%m-%d')  # Oblicza dzisiejszą datę w formacie YYYY-MM-DD

    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        year = request.form.get("release_year")
        release_year = f"{year}-01-01" if year else None

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
    if "user" not in session:
        return redirect(url_for("login"))

    # Pobranie danych z bazy
    movie = sb.table("movies").select("*").eq("id", movie_id).execute().data
    if not movie:
        return "Film nie został znaleziony", 404
    movie = movie[0]

    if request.method == "POST":
        # Pobranie danych z formularza
        polish_title = request.form["polish_title"]
        original_title = request.form["original_title"]
        watched_date = request.form["watched_date"]
        rating = request.form["rating"]
        release_year = request.form.get("release_year")

        release_year = f"{release_year}-01-01" if release_year else None

        # Zaktualizowanie danych w bazie
        updated_data = {
            "polish_title": polish_title,
            "original_title": original_title,
            "watched_date": watched_date,
            "rating": rating,
            "release_year": release_year,
            "who_submitted": session["user"].split("@")[0]
        }

        sb.table("movies").update(updated_data).eq("id", movie_id).execute()
        return redirect(url_for("index"))

    # Renderowanie formularza edycji
    return render_template("edit.html", movie=movie)

@app.route('/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    # Sprawdź, czy użytkownik jest zalogowany
    if not session.get('user'):
        return redirect(url_for('login'))  # Jeśli nie, przekieruj do logowania

    # Usuń film z bazy danych
    sb.table('movies').delete().eq('id', movie_id).execute()

    return redirect(url_for('index'))  # Po usunięciu, wróć do strony głównej


if __name__ == "__main__":
    app.run(debug=True)
