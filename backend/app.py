from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash
)
from werkzeug.security import check_password_hash
from functools import wraps
import os
from dotenv import load_dotenv
from db import get_db_connection

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "frontend", "templates"),
    static_folder=os.path.join(BASE_DIR, "frontend", "static")
)

app.secret_key = os.getenv("FLASK_SECRET_KEY")


# Check whether the user is logged in
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("home"))
        return func(*args, **kwargs)
    return wrapper


# Check whether the user has the required role
def role_required(*roles):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            if session.get("role") not in roles:
                flash("You are not authorized to access this page.")
                return redirect(url_for("dashboard"))
            return func(*args, **kwargs)
        return wrapper
    return decorator


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


# Login
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    selected_role = request.form.get("role", "").strip().lower()

    if not username or not password or selected_role not in (
        "admin", "faculty", "student"
    ):
        flash("Please enter valid login details.")
        return redirect(url_for("home"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT user_id, username, password_hash, role,
                   student_id, faculty_id
            FROM users
            WHERE username = %s
            """,
            (username,)
        )

        user = cursor.fetchone()



        print("\n--- LOGIN DEBUG ---")
        print("Username entered:", username)
        print("Selected role:", selected_role)
        print("User found:", user is not None)

        if user:
            print("Database role:", user["role"])
            print(
                "Password matches:",
                check_password_hash(user["password_hash"], password)
            )

        print("--- END DEBUG ---\n")        

        if (
            user is None
            or user["role"].lower() != selected_role
            or not check_password_hash(user["password_hash"], password)
        ):
            flash("Invalid username, password, or role.")
            return redirect(url_for("home"))

        session.clear()
        session["user_id"] = user["user_id"]
        session["username"] = user["username"]
        session["role"] = user["role"].lower()
        session["student_id"] = user["student_id"]
        session["faculty_id"] = user["faculty_id"]

        return redirect(url_for("dashboard"))

    except Exception:
        app.logger.exception("Login error")
        flash("Unable to log in right now. Please try again.")
        return redirect(url_for("home"))

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# Redirect according to role
@app.route("/dashboard")
@login_required
def dashboard():
    role = session.get("role")

    if role == "admin":
        return redirect(url_for("admin"))
    elif role == "faculty":
        return redirect(url_for("faculty"))
    elif role == "student":
        return redirect(url_for("student"))

    session.clear()
    return redirect(url_for("home"))


@app.route("/admin")
@role_required("admin")
def admin():
    return render_template("admin_dashboard.html")


@app.route("/student")
@role_required("student")
def student():
    return render_template("student_dashboard.html")


@app.route("/faculty")
@role_required("faculty")
def faculty():
    return render_template("faculty_dashboard.html")


@app.route("/subjects")
@role_required("admin")
def subjects():
    return render_template("manage_subjects.html")


@app.route("/mark-attendance")
@role_required("faculty")
def mark_attendance():
    return render_template("mark_attendance.html")


@app.route("/attendance-records")
@role_required("admin", "faculty")
def attendance_records():
    return render_template("attendance_records.html")


@app.route("/attendance-history")
@role_required("student")
def attendance_history():
    return render_template("attendance_history.html")


# Logout
@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    if not app.secret_key:
        raise RuntimeError("FLASK_SECRET_KEY is missing from .env")

    app.run(debug=True)