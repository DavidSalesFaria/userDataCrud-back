from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column("nome", db.String(150))
    sobrenome = db.Column("sobrenome", db.String(150))
    email = db.Column("email", db.String(150), unique=True)
    senha = db.Column("senha", db.String(200))
    data_nascimento = db.Column("data_nascimento", db.Date)
    genero = db.Column("genero", db.String(30))
    admin = db.Column("admin", db.Boolean)


    def __init__(self, nome, sobrenome, email, senha, data_nascimento, genero, admin):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha
        self.data_nascimento = data_nascimento
        self.genero = genero
        self.admin = admin
        
    def copy(self):
        copy = Users(
            self.nome,
            self.sobrenome,
            self.email,
            self.senha,
            self.data_nascimento,
            self.genero,
            self.admin
        )
        copy.id = self.id
        return copy

    def birthday_to_str(self):
        """ attribute data_nascimento datetime -> str
        """
        if isinstance(self.data_nascimento, date):
            self.data_nascimento = datetime.strftime(self.data_nascimento, "%Y-%m-%d")
        

    def birthday_to_datetime(self):
        """ attribute data_nascimento str -> datetime
        """
        if isinstance(self.data_nascimento, str):
            self.data_nascimento = datetime.strptime(self.data_nascimento, "%Y-%m-%d")
          

    def to_dict(self, columns=[]):

        copy = self.copy()
        copy.birthday_to_str()

        # Verifica se foram informadas colunas para filtrar o retorno
        if not columns:
            return {
                "id": copy.id,
                "nome": copy.nome,
                "sobrenome": self.sobrenome,
                "email": copy.email,
                "senha": copy.senha,
                "data_nascimento": copy.data_nascimento,
                "genero": copy.genero,
                "admin": self.admin
            }
        else:
            return {col: getattr(copy, col) for col in columns}

