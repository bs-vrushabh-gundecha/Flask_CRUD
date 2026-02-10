from flask import Flask, render_template, request, redirect, session, flash, url_for
# import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, migrate
from config import Config
from functools import wraps

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@127.0.0.1:3307/test_flask_db"
app.config.from_object(Config)


# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
db.init_app(app)
migrate.init_app(app, db)

from models import User, AdminMaster

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_id" not in session:
            flash("Please Login First", "warning")
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def superadmin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'superadmin':
            return "You dont have permission for this feature"
        return f(*args, **kwargs)
    return decorated


@app.route("/")
@login_required
def home():
    if "admin_id" not in session: 
        return redirect('/login')

    users = User.query.all()   # SELECT * FROM users
    return render_template("index.html", users=users)
    # return "App running successfully"

@app.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
    if "admin_id" not in session: 
        return redirect('/login')

    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.email = request.form['email']
        user.name = request.form['username']
        user.contact = request.form['mobile']

        db.session.commit()
        return redirect("/")

    return render_template("update_form.html", user=user)

@app.route("/delete/<int:id>")
@login_required
@superadmin_required
def delete(id):

    if session.get('role') != "superadmin":
        return "Access Denied: SuperAdmin only"

    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/")

@app.route('/add',methods=['GET', 'POST'])
@login_required
def add():
    if "admin_id" not in session:
        return redirect('/login')

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        mobile = request.form['mobile']
        user = User(
            name=username,
            email=email,
            contact=mobile
        )

        db.session.add(user)
        db.session.commit()
        

        return redirect('/')
        
    return render_template('add_form.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # print(request.form)
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('pwd')
        role = request.form.get('role')

        if not username or not email or not password:
            return "All fields are required"

        hashed_password = generate_password_hash(password)

        admin = AdminMaster(
            username = username,
            email = email,
            password = hashed_password,
            role = role
        )

        db.session.add(admin)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

    
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form)
        username = request.form.get('username')
        password = request.form.get('pwd')

        admin = AdminMaster.query.filter_by(username=username).first()

        # check_password_hash(stored_password, entered_password)
        if admin and check_password_hash(admin.password, password) :
            # session['admin_id'] = admin.id
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            session['role'] = admin.role
            flash("Login successful", "success")
            return redirect('/')
        else :
            flash("Invalid username or password", "danger")
            return redirect('/login')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect('/login')




# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=True)
#     email = db.Column(db.String(200), nullable=True)
#     contact = db.Column(db.String(13), nullable=True)
#     full_name = db.Column(db.String(300), nullable=True)

if __name__ == "__main__":
    app.run(debug=True)
