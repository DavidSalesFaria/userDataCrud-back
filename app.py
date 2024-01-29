from flask import Flask, request, Response
import json
from models.usuario import db
from controllers import blue as usuario_controller
from dotenv import load_dotenv
import os
import jwt # lib for create tokens
import datetime

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
    
    # check authorization
    if auth and auth.get("username") == "DavidShelton":
        # create a token
        token = jwt.encode({
            "user": auth.get("username"), 
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
            }, key=app.config["SECRET_KEY"])

        return Response(response=json.dumps({"status": "success", "token": token, "token_dec": jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])}), status=200, content_type="application/json")
    else:
        return Response(response=json.dumps({"status": "bad request", "message": "Login Required"}), status=401, content_type="application/json")

if __name__ == "__main__":
    app.run(debug=True)