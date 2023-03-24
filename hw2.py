from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'myKey!'
db = SQLAlchemy(app)


class Users(db.Model):
    m_id = db.Column(db.Integer, primary_key=True)
    m_name = db.Column(db.String(200), nullable=False)
    m_points = db.Column(db.Integer)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route("/add/", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('fname')
        id = request.form.get('fid')
        points = request.form.get('fscore')
        my_user = Users(m_name=name, m_id = id, m_points = points)
        check_user = Users.query.filter_by(m_id = id).first()
        if check_user:
            flash("Cannot create Users with duplicate IDs")
        else:
            db.session.add(my_user)
            db.session.commit()
    return render_template("add.html")

@app.route("/remove/", methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        id = request.form.get('fid')
        user = Users.query.filter_by(m_id = id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            flash("User with ID " + id + " deleted")
        else:
            flash("User with ID " + id + " does not exist in database")
    return render_template("remove.html")

@app.route("/get/", methods=['GET', 'POST'])
def get():
    if request.method == 'POST':
        id = request.form.get('fid')
        user = Users.query.filter_by(m_id = id).first()
        if user:
            flash("Name: " + user.m_name + "  ID: " + str(user.m_id) + " Score: " + str(user.m_points))
        else:
            flash("User with ID " + id + " does not exist in database")
    return render_template("find.html")

with app.app_context():
    db.create_all()
if __name__ == "__main__":
    app.run()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
