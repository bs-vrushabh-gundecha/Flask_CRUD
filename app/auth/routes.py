from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models import AdminMaster

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['pwd']

        hashed_password = generate_password_hash(password)

        admin = AdminMaster(
            username=username,
            email=email,
            password=hashed_password,
            role="admin"   # default role
        )

        db.session.add(admin)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect("/login")

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        admin = AdminMaster.query.filter_by(
            username=request.form['username']
        ).first()

        if admin and check_password_hash(admin.password, request.form['pwd']):
            session["admin_id"] = admin.id
            session["role"] = admin.role   # store role
            flash("Login successful", "success")
            return redirect("/")
        else:
            flash("Invalid username or password", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect("/login")
