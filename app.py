from flask import Flask, render_template, request, redirect
# import mysql.connector
from extensions import db, migrate
from config import Config

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@127.0.0.1:3307/test_flask_db"
app.config.from_object(Config)

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
db.init_app(app)
migrate.init_app(app, db)

from models import User

@app.route("/")
def home():
    users = User.query.all()   # SELECT * FROM users
    return render_template("index.html", users=users)
    # return "App running successfully"

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.email = request.form['email']
        user.name = request.form['username']
        user.contact = request.form['mobile']

        db.session.commit()
        return redirect("/")

    return render_template("update_form.html", user=user)

@app.route("/delete/<int:id>")
def delete(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/")

@app.route('/add',methods=['GET', 'POST'])
def add():
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


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=True)
#     email = db.Column(db.String(200), nullable=True)
#     contact = db.Column(db.String(13), nullable=True)
#     full_name = db.Column(db.String(300), nullable=True)

if __name__ == "__main__":
    app.run(debug=True)
