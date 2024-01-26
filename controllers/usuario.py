from flask import Blueprint, Response, request
from models.usuario import db, Usuario
import json
import re

def validate_email(email):
  """Valida um endereço de email.

  Args:
    email: O endereço de email a ser validado.

  Returns:
    True se o endereço de email for válido, False se for inválido.
  """

  regex = re.compile(r'^[a-zA-Z0-9_\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,63}$')
  return regex.match(email) is not None

app = Blueprint("usuario", __name__)

@app.route("/")
@app.route("/<id>")
def index(id=None):
    # Check if id was provided
    if not id:
        # Is returned an iterator with all users
        query = Usuario.query.all()
        # Cast every object into dict
        result = [u.to_dict() for u in query]
    else:
        # Get a specific user by id
        query = Usuario.query.where(Usuario.id == id)
        result = query.first().to_dict()
    
    return Response(response=json.dumps({"status": "success", "data": result}), status=200, content_type="application/json")


@app.route("/add", methods=["POST"])
def add():
    data = request.get_json(force=True)
    usuario = Usuario(
        data["nome"], 
        data["sobrenome"],
        data["email"],
        data["senha"],
        data["dataDeAniversario"],
        data["genero"]
        )
    # Converte a data de aniversário do usuário para datetime
    usuario.birthday_to_datetime()
    db.session.add(usuario)
    db.session.commit()
    # Retorna a resposta em json
    return Response(response=json.dumps({"status": "success", "data": usuario.to_dict()}), status=200, content_type="application/json")


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

