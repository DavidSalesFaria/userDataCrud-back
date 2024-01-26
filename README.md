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


## Blueprint
### `/users`

## Endpoints

### `/`

Retorna uma lista de todos os usuários.

**Método:** GET

**Parâmetro:**
* `id` (opcional): id do usuário

**Exemplos:**

Retorna uma lista de todos os usuários.

```
GET /users/
```

### `/<id>`

Retorna um usuário específico.

**Método:** GET

**Parâmetro:**
* `id`: id do usuário

**Exemplo:**

```
GET /users/jose@bugmail.com
```

### `/users/add`

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

Cria um usuário com os dados especificados no corpo da requisição.

```
POST /users/add
```

### `/users/edit/<id>`

Atualiza um usuário específico.

**Método:** PUT

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

Atualiza um usuário específico com os dados especificados no corpo da requisição.

```
PUT /users/edit/jose@bugmail.com
```

### `/users/delete/<id>`

Exclui um usuário específico.

**Método:** DELETE

**Parâmetro:**

* `id`: id do usuário

**Exemplo:**
Exclui o usuário com o id especificado.

```
DELETE /users/delete/jose@bugmail.com
```


## Autor

[David Shelton]

