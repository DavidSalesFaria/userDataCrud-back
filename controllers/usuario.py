from flask import Blueprint, Response, request, abort
from models.usuario import db, Users
import json
import re
from jsonschema import validate, ValidationError
import jwt # lib for create tokens
from functools import wraps
import os
from werkzeug.security import generate_password_hash, check_password_hash


def validate_email(email):
  """Valida um endereço de email.

  Args:
    email: O endereço de email a ser validado.

  Returns:
    True se o endereço de email for válido, False se for inválido.
  """

  regex = re.compile(r'^[a-zA-Z0-9_\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,63}$')
  return regex.match(email) is not None

# Decorator that require token to access route
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        app_secret_key = os.getenv("APP_SECRET_KEY")

        token = None

        if "token" in request.headers:
            token = request.headers["token"]

        # Check if there is not a token
        if not token:
            return Response(response=json.dumps({"status": "Unauthorized", "message": "Token is required"}), status=401, content_type="application/json")
        
        # Try decode token
        try:
            data = jwt.decode(token, app_secret_key, algorithms=["HS256"])
            current_user = Users.query.filter_by(email=data["username"]).first()
        except:
            return Response(response=json.dumps({"status": "Forbidden", "message": "Token is invalid", "data": jwt.decode(token, app_secret_key, algorithms=["HS256"])}), status=403, content_type="application/json")

        return f(current_user, *args, **kwargs)
    return decorated


user_data_schema = {
        "type": "object",
        "properties": {
            "nome": {
                "type": "string",
            },
            "sobrenome": {
                "type": "string",
            },
            "email": {
                "type": "string",
            },
             "senha": {
                "type": "string",
            },
            "data_nascimento": {
                "type": "string",
            },
            "genero": {
                "type": "string",
            },
        },
        "required": ["nome", "sobrenome", "email", "senha", "data_nascimento", "genero"],
        "maxProperties": 6
    }

blue = Blueprint("users", __name__)


@blue.route("/")
@blue.route("/<int:id>")
@token_required
def index(current_user, id=None):

    if not current_user.admin:
        return Response(response=json.dumps({"status": "Unsautorized", "message": "Cannot perform that function"}), status=401, content_type="application/json")

    # Check if id was provided
    if not id:
        # Is returned an iterator with all users
        query = Users.query.all()
        # Cast every object into dict
        resp = [u.to_dict() for u in query]
    else:
        # Get a specific user by id
        query = Users.query.where(Users.id == id).first()
        resp = query.to_dict() if query else {}
    
    return Response(response=json.dumps({"status": "success", "data": resp}), status=200, content_type="application/json")


@blue.route("/add", methods=["POST"])
# @token_required
def add():
    data: dict = request.get_json(force=True)

    # Try add user
    try:
        # Validate json
        validate(data, user_data_schema)

        usuario = Users(
            data["nome"], 
            data["sobrenome"],
            data["email"],
            generate_password_hash(data["senha"]),
            data["data_nascimento"],
            data["genero"],
            admin=False
            )

        # user's birthday str -> datetime
        usuario.birthday_to_datetime()
        db.session.add(usuario)
        db.session.commit()

        return Response(response=json.dumps({"status": "success", "data": data}), status=200, content_type="application/json")

    except ValidationError as e:
        return Response(response=json.dumps({"status": "bad request", "message": e.message}), status=400, content_type="application/json")


@blue.route("/edit/<id>", methods=["PUT", "POST"])
@token_required
def edit(id):
    # Get a specific user by id
    usuario = Users.query.where(Users.id == id).first()
    data = request.get_json(force=True)

    # Try edit user
    try:
        # Validate json
        validate(data, user_data_schema)

        usuario.nome = data["nome"]
        usuario.sobrenome = data["sobrenome"]
        usuario.email = data["email"]
        usuario.senha = generate_password_hash(data["senha"])
        usuario.data_nascimento = data["data_nascimento"]
        usuario.genero = data["genero"]

        # user's birthday str -> datetime
        usuario.birthday_to_datetime()

        db.session.commit()

        return Response(response=json.dumps({"status": "success", "data": usuario.to_dict()}), status=200, content_type="application/json")

    except ValidationError as e:
        return Response(response=json.dumps({"status": "bad request", "message": e.message}), status=400, content_type="application/json")

    

# @blue.route("/delete/<id>", methods=["DELETE", "GET"])
# @token_required
# def delete(id):
#     query = Users.query.where(Users.id == id)
#     usuario = query.first()

#     # Check if there is a user found
#     if usuario:
#         db.session.delete(usuario)
#         db.session.commit()
#         return Response(response=json.dumps({"status": "success", "data": usuario.to_dict()}), status=200, content_type="application/json")
        
#     else:
#         return Response(response=json.dumps({"status": "success", "data": {}}), status=200, content_type="application/json")


@blue.route("/promote_user/<id>", methods=["POST"])
def promote_user(id):
    user = Users.query.filter_by(id=id).first()
    if not user:
        return Response(response=json.dumps({"status": "bad request", "message": "User not found!"}), status=400, content_type="application/json")

    user.admin = True
    db.session.commit()
    return Response(response=json.dumps({"status": "sucess", "message": f"User {user.nome} promoted!"}), status=200, content_type="application/json")