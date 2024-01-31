from flask import Blueprint, Response, request
from models.usuario import db, Users
import json
import re
from jsonschema import validate, ValidationError
import jwt # lib for create tokens
from functools import wraps
import os
# Generate and check hash password
from werkzeug.security import generate_password_hash


def validate_email(email):
  """Validate a email address

  Args:
    email: User email address

  Returns:
    True if email is valid, False else.
  """

  regex = re.compile(r'^[a-zA-Z0-9_\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,63}$')
  return regex.match(email) is not None


def admin_required(f):
    """Add admin=True kwarg in @token_required decorator, then
    admin token is required to that decorator
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        return f(*args, **kwargs, admin=True)
    return decorated


# Decorator that require token to access route
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get secret key from enviroment
        app_secret_key= os.getenv("APP_SECRET_KEY")

        token = None
        admin = False
        current_user = None  

        # Check if token is in headers
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
            return Response(response=json.dumps({"status": "Forbidden", "message": "Token is invalid"}), status=403, content_type="application/json")

        # Check if there is a kwarg with name "admin"
        if "admin" in kwargs:
            admin = kwargs.pop("admin") 

        # If admin token is required
        if admin:
            if  not current_user.admin:
                return Response(response=json.dumps({"status": "Unauthorized", "message": "Admin is required"}), status=401, content_type="application/json")

        return f(*args, **kwargs)

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
@admin_required
@token_required
def get_all_users():
    # Is returned an iterator with all users
    query = Users.query.all()
    # Cast every object into dict
    resp = [u.to_dict() for u in query]
    
    return Response(response=json.dumps({"status": "success", "data": resp}), status=200, content_type="application/json")


@blue.route("/<int:id>")
@token_required
def get_one_ser(id):

    # Get a specific user by id
    query = Users.query.where(Users.id == id).first()
    resp = query.to_dict() if query else {}
    
    return Response(response=json.dumps({"status": "success", "data": resp}), status=200, content_type="application/json")


@blue.route("/", methods=["POST"])
# @token_required
def add():
    data: dict = request.get_json(force=True)

    # Try add user
    try:
        # Validate json
        validate(data, user_data_schema)


        usuario = Users(
            data["nome"], 
            data["sobrenome"] if data["sobrenome"] else None,
            data["email"],
            generate_password_hash(data["senha"]),
            data["data_nascimento"] if data["data_nascimento"] else None,
            data["genero"] if data["genero"] else None,
            admin=False
            )
        
        if usuario.exists():
            return Response(response=json.dumps({"status": "conflict", "message": "The user already exists in the database"}), status=409, content_type="application/json")

        if usuario.data_nascimento:
            # user's birthday str -> datetime
            usuario.birthday_to_datetime()

        db.session.add(usuario)
        db.session.commit()

        return Response(response=json.dumps({"status": "success", "data": data}), status=200, content_type="application/json")

    except ValidationError as e:
        return Response(response=json.dumps({"status": "bad request", "message": e.message}), status=400, content_type="application/json")


@blue.route("/<id>", methods=["PUT", "POST"])
@admin_required
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

    

@blue.route("/<id>", methods=["DELETE"])
@admin_required
@token_required
def delete(current_user, id):

    # Check if current user is not admin
    if not current_user.admin:
        return Response(response=json.dumps({"status": "Unsautorized", "message": "Cannot perform that function"}), status=401, content_type="application/json")

    query = Users.query.where(Users.id == id)
    usuario = query.first()

    # Check if there is a user found
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return Response(response=json.dumps({"status": "success", "data": usuario.to_dict()}), status=200, content_type="application/json")
        
    else:
        return Response(response=json.dumps({"status": "success", "data": {}}), status=200, content_type="application/json")


@blue.route("/promote_user/<id>", methods=["POST"])
def promote_user(id):
    user = Users.query.filter_by(id=id).first()
    if not user:
        return Response(response=json.dumps({"status": "bad request", "message": "User not found!"}), status=400, content_type="application/json")

    user.admin = True
    db.session.commit()
    return Response(response=json.dumps({"status": "sucess", "message": f"User {user.nome} promoted!"}), status=200, content_type="application/json")