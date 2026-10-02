from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key_change_this_later"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    display_name = db.Column(db.String(80), nullable=True, default="User")

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))
    
    user = User.query.filter_by(email=session["user"]).first()
    return render_template("dashboard.html", email=user.email, name=user.display_name or "User")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "All fields are required."})

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"success": False, "message": "Email already registered."})

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, display_name=email.split('@')[0])
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True, "message": "Account created successfully! You can now log in."})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session["user"] = user.email
        return jsonify({"success": True, "redirect": "/dashboard"})

    return jsonify({"success": False, "message": "Invalid email or password."})

@app.route("/update-profile", methods=["POST"])
def update_profile():
    if "user" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.get_json() or {}
    new_name = data.get("display_name")

    if not new_name:
        return jsonify({"success": False, "message": "Name cannot be empty."})

    user = User.query.filter_by(email=session["user"]).first()
    user.display_name = new_name
    db.session.commit()

    return jsonify({"success": True, "message": "Profile updated!"})

@app.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json() or {}
    email = data.get("email")
    new_password = data.get("password")

    if not email or not new_password:
        return jsonify({"success": False, "message": "Email and new password required."})

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "message": "Account not found."})

    user.password = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({"success": True, "message": "Password updated! Please log in."})

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)