from flask import Flask, request, Response
import json
from models.usuario import db, Users
from controllers import blue as usuario_controller
from dotenv import load_dotenv
import os
import jwt # lib for create tokens
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Load the enviroment variables
load_dotenv(".env")

app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI1")
app.config["SECRET_KEY"] = os.getenv("APP_SECRET_KEY")

# Inicia e configura o banco de dados
db.init_app(app=app)
with app.test_request_context():
        db.create_all()

# Register the usuario's blueprint
app.register_blueprint(usuario_controller, url_prefix="/users/")


@app.route("/login")
def login():

    auth = request.authorization

    # Check if there is authorization
    if not auth or not auth.get("username") or not auth.get("password"):
        return Response(response=json.dumps({"status": "Unautorized", "messsage": "Login is required!}"}), status=401, content_type="application/json")

    user = Users.query.filter_by(email=auth.get("username")).first()

    # Check if user exists
    if not user:
        return Response(response=json.dumps({"status": "Unautorized", "messsage": "User not found!"}), status=401, content_type="application/json")

    # Check user's password
    if check_password_hash(user.senha, auth.get("password")):
        # create a token
        token = jwt.encode({
            "username": auth.get("username"), 
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            }, key=app.config["SECRET_KEY"])

        return Response(response=json.dumps({"status": "success", "token": token}), status=200, content_type="application/json")
    
    return Response(response=json.dumps({"status": "Unautorized", "messsage": "Invalid password!"}), status=401, content_type="application/json")

if __name__ == "__main__":
    app.run(debug=True)