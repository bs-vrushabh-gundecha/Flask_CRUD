from flask import Blueprint, render_template, request, redirect
from app.extensions import db
from app.models import User
from app.decorators import login_required, superadmin_required

users_bp = Blueprint('users', __name__)

@users_bp.route("/")
@login_required
# def home():
#     users = User.query.all()

#     print(type(users))   # 👈 paste it here

#     return render_template("index.html", users=users)
def home():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")
    sort = request.args.get("sort", "id")      # id, name, email
    order = request.args.get("order", "desc") # asc or desc

    query = User.query

    # 🔍 Search
    if search:
        query = query.filter(
            User.name.ilike(f"%{search}%") |
            User.email.ilike(f"%{search}%") |
            User.contact.ilike(f"%{search}%")
        )

    # 📌 Sorting
    if sort == "name":
        column = User.name
    elif sort == "email":
        column = User.email
    else:
        column = User.id

    # ⬆⬇ Order
    if order == "asc":
        query = query.order_by(column.asc())
    else:
        query = query.order_by(column.desc())

    users = query.paginate(page=page, per_page=5)

    return render_template(
        "index.html",
        users=users,
        search=search,
        sort=sort,
        order=order
    )


@users_bp.route("/add", methods=["GET","POST"])
@login_required
def add():
    if request.method == "POST":
        user = User(
            name=request.form['username'],
            email=request.form['email'],
            contact=request.form['mobile']
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    return render_template("add_form.html")


@users_bp.route("/update/<int:id>", methods=["GET","POST"])
@login_required
def update(id):
    user = User.query.get_or_404(id)

    if request.method == "POST":
        user.name = request.form['username']
        user.email = request.form['email']
        user.contact = request.form['mobile']
        db.session.commit()
        return redirect("/")

    return render_template("update_form.html", user=user)


@users_bp.route("/delete/<int:id>")
@superadmin_required   # only superadmin can delete
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")
