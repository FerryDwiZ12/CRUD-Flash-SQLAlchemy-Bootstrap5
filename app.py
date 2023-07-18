
import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

app = Flask(__name__)

# Load variabel lingkungan dari .env
load_dotenv()

app.config["DEBUG"] = os.getenv("DEBUG")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Nama = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    Password = db.Column(db.String(100))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['Nama']
        email = request.form['Email']
        password = request.form['Password']
        new_user = Users(Nama=name, Email=email, Password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        users = get_all_users()
        return render_template('index.html', users=users)


@app.route('/delete/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('home'))


def get_all_users():
    return Users.query.all()

def get_user_by_id(id):
    return Users.query.get(id)

@app.route('/edit/<int:user_id>', methods=['GET'])
def edit_user(user_id):
    user = get_user_by_id(user_id)
    return render_template('editData.html', user=user)

def update_user(user_id, new_name, new_email, new_password):
    user = Users.query.get(user_id)
    if user:
        user.Nama = new_name
        user.Email = new_email
        user.Password = new_password
        db.session.commit()
    else :
        flash("User with ID {} not found.".format(user_id), "error")    


@app.route('/update', methods=['POST'])
def update_data():
    user_id = request.form['user_id']
    new_name = request.form['Nama']
    new_email = request.form['Email']
    new_password = request.form['Password']
    update_user(user_id, new_name, new_email, new_password)  # Pastikan semua argumen disertakan
    return redirect(url_for('home'))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
