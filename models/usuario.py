from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column("nome", db.String(150))
    sobrenome = db.Column("sobrenome", db.String(150))
    email = db.Column("email", db.String(150))
    senha = db.Column("senha", db.String(150))
    dataDeAniversario = db.Column("data_de_aniversario", db.Date)
    genero = db.Column("genero", db.String(30))

    def __init__(self, nome, sobrenome, email, senha, dataDeAniversario, genero):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha
        self.dataDeAniversario = dataDeAniversario
        self.genero = genero
        
    def copy(self):
        copy = Usuario(
            self.nome,
            self.sobrenome,
            self.email,
            self.senha,
            self.dataDeAniversario,
            self.genero
        )
        copy.id = self.id
        return copy

    def birthday_to_str(self):
        """ attribute data_nascimento datetime -> str
        """
        if isinstance(self.dataDeAniversario, date):
            self.dataDeAniversario = datetime.strftime(self.dataDeAniversario, "%Y-%m-%d")
        

    def birthday_to_datetime(self):
        """ attribute data_nascimento str -> datetime
        """
        if isinstance(self.dataDeAniversario, str):
            self.dataDeAniversario = datetime.strptime(self.dataDeAniversario, "%Y-%m-%d")
          

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
                "dataDeAniversario": copy.dataDeAniversario,
                "genero": copy.genero
            }
        else:
            return {col: getattr(copy, col) for col in columns}


# usu = Usuario(
#             "David",
#             "Shelton",
#             "david@bugmail.com",
#             "123",
#             "2002-02-26",
#             "masculino"
#         )
# usu.id = 4


# usu_date = usu.birthday_to_datetime()
# print(usu.to_dict())
# print(usu_date.to_dict())