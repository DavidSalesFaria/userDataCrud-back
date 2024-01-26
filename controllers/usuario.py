from flask import Blueprint, Response, request, abort
from models.usuario import db, Usuario
import json
import re
from jsonschema import validate, ValidationError

def validate_email(email):
  """Valida um endereço de email.

  Args:
    email: O endereço de email a ser validado.

  Returns:
    True se o endereço de email for válido, False se for inválido.
  """

  regex = re.compile(r'^[a-zA-Z0-9_\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,63}$')
  return regex.match(email) is not None

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
            "dataDeAniversario": {
                "type": "string",
            },
            "genero": {
                "type": "string",
            },
        },
        "required": ["nome", "sobrenome", "email", "senha", "dataDeAniversario", "genero"],
        "maxProperties": 6
    }

app = Blueprint("usuario", __name__)

@app.route("/")
@app.route("/<int:id>")
def index(id=None):
    # Check if id was provided
    if not id:
        # Is returned an iterator with all users
        query = Usuario.query.all()
        # Cast every object into dict
        resp = [u.to_dict() for u in query]
    else:
        # Get a specific user by id
        query = Usuario.query.where(Usuario.id == id).first()
        resp = query.to_dict() if query else {}
    
    return Response(response=json.dumps({"status": "success", "data": resp}), status=200, content_type="application/json")


@app.route("/add", methods=["POST"])
def add():
    data: dict = request.get_json(force=True)

    try:
        validate(data, user_data_schema)

        # usuario = Usuario(
        #     data["nome"], 
        #     data["sobrenome"],
        #     data["email"],
        #     data["senha"],
        #     data["dataDeAniversario"],
        #     data["genero"]
        #     )

        # usuario.birthday_to_datetime()
        # # # Converte a data de aniversário do usuário para datetime
        # db.session.add(usuario)
        # db.session.commit()
        # Retorna a resposta em json
        return Response(response=json.dumps({"status": "success", "data": data}), status=200, content_type="application/json")
    except ValidationError as e:

        return Response(response=json.dumps({"status": "bad request", "message": e.message}), status=400, content_type="application/json")


@app.route("/edit/<id>", methods=["PUT", "POST"])
def edit(useremail):
    # Get a specific user by id
    usuario = Usuario.query.where(Usuario.email == id).first()
    data = request.get_json(force=True)  
    usuario.nome = data["nome"]
    usuario.sobrenome = data["sobrenome"]
    usuario.email = data["email"]
    usuario.senha = data["senha"]
    usuario.dataDeAniversario = data["dataDeAniversario"]
    usuario.genero = data["genero"]
    usuario.birthday_to_datetime()
    db.session.commit()
    return Response(response=json.dumps({"status": "success", "data": usuario.to_dict()}), status=200, content_type="application/json")


@app.route("/delete/<id>", methods=["DELETE", "GET"])
def delete(id):
    usuario = Usuario.query.where(Usuario.email == id).first()
    db.session.delete(usuario)
    db.session.commit()
    return Response(response=json.dumps({"status": "success", "data": usuario.to_dict()}), status=200, content_type="application/json")

