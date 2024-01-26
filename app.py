from flask import Flask
from models.usuario import db
from controllers.usuario import app as usuario_controller
from dotenv import load_dotenv
import os

# Load the enviroment variables
load_dotenv(".env")

app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI1")

# Inicia e configura o banco de dados
db.init_app(app=app)
with app.test_request_context():
        db.create_all()

# Register the usuario's blueprint
app.register_blueprint(usuario_controller, url_prefix="/usuario/")


if __name__ == "__main__":
    app.run(debug=True)