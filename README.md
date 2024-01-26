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
* `useremail` (opcional): Email do usuário

**Exemplos:**

Retorna uma lista de todos os usuários.

```
GET /users/
```

### `/<useremail>`

Retorna um usuário específico.

**Método:** GET

**Parâmetro:**
* `useremail`: Email do usuário

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

### `/users/edit/<useremail>`

Atualiza um usuário específico.

**Método:** PUT

**Parâmetro:**

* `useremail`: Email do usuário

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

Atualiza o usuário com o email especificado com os dados especificados no corpo da requisição.

```
PUT /users/edit/jose@bugmail.com
```

### `/users/delete/<useremail>`

Exclui um usuário específico.

**Método:** DELETE

**Parâmetro:**

* `useremail`: Email do usuário

**Exemplo:**
Exclui o usuário com o email especificado.

```
DELETE /users/delete/jose@bugmail.com
```


## Autor

[David Shelton]

