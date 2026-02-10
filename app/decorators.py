from functools import wraps
from flask import session, redirect, flash, url_for
from app.models import AdminMaster

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_id" not in session:
            flash("Please login first", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_id" not in session:
            flash("Please login first", "error")
            return redirect(url_for("auth.login"))

        admin = AdminMaster.query.get(session["admin_id"])

        if admin.role != "superadmin":
            flash("Access denied: You dont have access", "error")
            return redirect(url_for("users.home"))

        return f(*args, **kwargs)
    return decorated_function
