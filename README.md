# API Usuario

Esta API fornece endpoints para gerenciar dados de usuário, incluindo nome, sobrenome, e-mail, senha, data de aniversário e gênero.

## Requisitos
* Python 3.8+

## Dados Armazenados:
- nome
- sobrenome
- email
- senha
- data de nascimento
- genero


## Info:
**Language:** Python

**Database:** PostgreSql

**Framework:** Flask

**Deploy Website:** Render


## `/users/` - Methotd [GET]

Retorna uma lista de todos os usuários.

**Exemplos:**

```
GET /users/
```

## `/users/<id>` - Methotd [GET]

Retorna os dados de um usuário específico.

**Parâmetro:**

* `id`: id do usuário

**Exemplos:**

```
GET /users/2
```

## `/users/`  - Methotd [POST]


Cria um novo usuário.

**Método:** POST

**Corpo da requisição:**

```
{
  "nome": "Fulano de Tal",
  "sobrenome": "Silva",
  "email": "fulano@example.com",
  "senha": "123456",
  "data_nascimento": "1990-01-01",
  "genero": "masculino"
}
```

**Exemplo:**

```
POST /users/add
```

## `/users/<id>`  - Methotd [PUT]

Atualiza um usuário específico.

**Parâmetro:**

* `id`: id do usuário

**Corpo da requisição:**

```
{
  "nome": "Beltrano de Tal",
  "sobrenome": "Santos",
  "email": "beltrano@example.com",
  "senha": "654321",
  "data_nascimento": "1992-02-02",
  "genero": "feminino"
}
```

**Exemplo:**

```
PUT /users/2
```

## `/users/<id>`  - Methotd [DELETE]

Exclui um usuário específico.

**Parâmetro:**

* `id`: id do usuário

**Exemplo:**

```
DELETE /users/2
```

## Autor

[David Shelton]
