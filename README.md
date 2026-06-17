# Financas API

API REST para gerenciamento de finanças pessoais desenvolvida em Django REST Framework com autenticação JWT.

## Tecnologias

- **Django** 6.0.5
- **Django REST Framework** 3.14.0
- **djangorestframework-simplejwt** 5.5.1 (JWT Authentication)
- **PostgreSQL**
- **Python** 3.13.5

## Instalação

### Pré-requisitos
- Python 3.13+
- PostgreSQL instalado e rodando
- pip e virtualenv

### Passos

1. **Clone o repositório**
```bash
git clone <seu-repositorio>
cd financas_api
```

2. **Crie e ative o ambiente virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados**

Certifique-se de que o PostgreSQL está rodando e crie um banco de dados:
```sql
CREATE DATABASE financas_db;
```

5. **Crie e execute as migrações**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crie um superusuário (opcional)**
```bash
python manage.py createsuperuser
```

7. **Inicie o servidor**
```bash
python manage.py runserver
```

O servidor rodará em `http://127.0.0.1:8000/`

## Estrutura do Projeto

```
financas_api/
├── core/                  # Configurações principais do projeto
│   ├── settings.py       # Configurações Django
│   ├── urls.py          # URLs principais
│   └── wsgi.py
├── usuarios/            # App de gerenciamento de usuários
│   ├── models.py        # Modelo de usuário
│   ├── serializers.py   # Serializers
│   ├── views.py         # Views/ViewSets
│   ├── urls.py          # URLs do app
│   └── admin.py
├── categorias/          # App de categorias (implementado)
│   ├── models.py        # Modelo de categoria
│   ├── serializers.py   # Serializers
│   ├── views.py         # Views/ViewSets
│   ├── urls.py          # URLs do app
│   ├── permissions.py   # Permissões customizadas
│   └── admin.py
├── transacoes/          # App de transações (em desenvolvimento)
├── manage.py
└── requirements.txt
```

---

## API - Endpoints de Usuários

### Base URL
```
http://localhost:8000/api/usuarios/
```

---

### 1. **Cadastro de Usuário**

**POST** `/api/usuarios/cadastro/`

Registra um novo usuário no sistema e retorna tokens JWT.

**Body (JSON)**
```json
{
  "username": "joao_silva",
  "email": "joao@example.com",
  "password": "SenhaForte123!",
  "password_confirm": "SenhaForte123!",
  "first_name": "João",
  "last_name": "Silva"
}
```

**Response (201 Created)**
```json
{
  "message": "Usuário cadastrado com sucesso",
  "usuario": {
    "id": 1,
    "username": "joao_silva",
    "email": "joao@example.com",
    "first_name": "João",
    "last_name": "Silva",
    "criado_em": "2026-05-25T10:30:00Z",
    "atualizado_em": "2026-05-25T10:30:00Z"
  },
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Teste com cURL**
```bash
curl -X POST http://localhost:8000/api/usuarios/cadastro/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao_silva",
    "email": "joao@example.com",
    "password": "SenhaForte123!",
    "password_confirm": "SenhaForte123!",
    "first_name": "João",
    "last_name": "Silva"
  }'
```

---

### 2. **Login (Obter Token JWT)**

**POST** `/api/usuarios/login/`

Autentica o usuário e retorna tokens de acesso e refresh.

**Body (JSON)**
```json
{
  "username": "joao_silva",
  "password": "SenhaForte123!"
}
```

**Response (200 OK)**
```json
{
  "message": "Login realizado com sucesso",
  "usuario": {
    "id": 1,
    "username": "joao_silva",
    "email": "joao@example.com",
    "first_name": "João",
    "last_name": "Silva",
    "criado_em": "2026-05-25T10:30:00Z",
    "atualizado_em": "2026-05-25T10:30:00Z"
  },
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Teste com cURL**
```bash
curl -X POST http://localhost:8000/api/usuarios/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao_silva",
    "password": "SenhaForte123!"
  }'
```

---

### 3. **Refresh Token**

**POST** `/api/token/refresh/`

Renova o token de acesso usando o refresh token.

**Body (JSON)**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK)**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Teste com cURL**
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "seu_refresh_token_aqui"
  }'
```

---

### 4. **Consultar Perfil**

**GET** `/api/usuarios/perfil/`

Retorna os dados do usuário autenticado.

**Headers (Obrigatório)**
```
Authorization: Bearer <seu_access_token>
```

**Response (200 OK)**
```json
{
  "id": 1,
  "username": "joao_silva",
  "email": "joao@example.com",
  "first_name": "João",
  "last_name": "Silva",
  "criado_em": "2026-05-25T10:30:00Z",
  "atualizado_em": "2026-05-25T10:30:00Z"
}
```

**Teste com cURL**
```bash
curl -X GET http://localhost:8000/api/usuarios/perfil/ \
  -H "Authorization: Bearer seu_access_token_aqui"
```

---

### 5. **Editar Perfil**

**PATCH** `/api/usuarios/perfil/`

Atualiza os dados do perfil do usuário autenticado.

**Headers (Obrigatório)**
```
Authorization: Bearer <seu_access_token>
```

**Body (JSON)** - Todos os campos são opcionais
```json
{
  "first_name": "João Paulo",
  "last_name": "Silva Santos",
  "email": "joao_novo@example.com"
}
```

**Response (200 OK)**
```json
{
  "message": "Perfil atualizado com sucesso",
  "usuario": {
    "id": 1,
    "username": "joao_silva",
    "email": "joao_novo@example.com",
    "first_name": "João Paulo",
    "last_name": "Silva Santos",
    "criado_em": "2026-05-25T10:30:00Z",
    "atualizado_em": "2026-05-25T11:45:00Z"
  }
}
```

**Teste com cURL**
```bash
curl -X PATCH http://localhost:8000/api/usuarios/perfil/ \
  -H "Authorization: Bearer seu_access_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "João Paulo",
    "email": "joao_novo@example.com"
  }'
```

---

### 6. **Trocar Senha**

**PATCH** `/api/usuarios/trocar-senha/`

Altera a senha do usuário autenticado.

**Headers (Obrigatório)**
```
Authorization: Bearer <seu_access_token>
```

**Body (JSON)**
```json
{
  "old_password": "SenhaForte123!",
  "new_password": "NovaSenha456!",
  "new_password_confirm": "NovaSenha456!"
}
```

**Response (200 OK)**
```json
{
  "message": "Senha alterada com sucesso"
}
```

**Teste com cURL**
```bash
curl -X PATCH http://localhost:8000/api/usuarios/trocar-senha/ \
  -H "Authorization: Bearer seu_access_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "SenhaForte123!",
    "new_password": "NovaSenha456!",
    "new_password_confirm": "NovaSenha456!"
  }'
```

---

### 7. **Excluir Conta**

**DELETE** `/api/usuarios/perfil/`

Deleta permanentemente a conta do usuário autenticado.

**Headers (Obrigatório)**
```
Authorization: Bearer <seu_access_token>
```

**Response (204 No Content)**
Sem conteúdo na resposta (sucesso)

**Teste com cURL**
```bash
curl -X DELETE http://localhost:8000/api/usuarios/perfil/ \
  -H "Authorization: Bearer seu_access_token_aqui"
```

---

## API - Endpoints de Categorias

### Base URL
```
http://localhost:8000/api/categorias/
```

> **Nota:** Todos os endpoints de categorias exigem autenticação JWT.
> Envie o header: `Authorization: Bearer <seu_access_token>`

---

### 1. **Listar Categorias**

**GET** `/api/categorias/`

Retorna todas as categorias do usuário autenticado.

**Headers (Obrigatório)**
```
Authorization: Bearer <seu_access_token>
```

**Response (200 OK)**
```json
[
  {
    "id": 1,
    "nome": "Alimentação",
    "tipo": "despesa",
    "usuario": 1,
    "usuario_nome": "joao_silva",
    "criada_em": "2026-05-25T10:30:00Z"
  },
  {
    "id": 2,
    "nome": "Salário",
    "tipo": "receita",
    "usuario": 1,
    "usuario_nome": "joao_silva",
    "criada_em": "2026-05-25T11:00:00Z"
  }
]
```

**Teste com cURL**
```bash
curl -X GET http://localhost:8000/api/categorias/ \
  -H "Authorization: Bearer seu_access_token_aqui"
```

---

### 2. **Criar Categoria**

**POST** `/api/categorias/`

Cria uma nova categoria para o usuário autenticado.

**Headers (Obrigatório)**
```
Authorization: Bearer <seu_access_token>
```

**Body (JSON)**
```json
{
  "nome": "Alimentação",
  "tipo": "despesa"
}
```

> **Campos:**
> - `nome` (obrigatório): Nome da categoria (mínimo 2 caracteres)
> - `tipo` (opcional): "receita" ou "despesa". Se não informado, assume "despesa"

**Response (201 Created)**
```json
{
  "id": 1,
  "nome": "Alimentação",
  "tipo": "despesa",
  "usuario": 1,
  "usuario_nome": "joao_silva",
  "criada_em": "2026-05-25T12:00:00Z"
}
```

**Teste com cURL**
```bash
curl -X POST http://localhost:8000/api/categorias/ \
  -H "Authorization: Bearer seu_access_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Alimentação",
    "tipo": "despesa"
  }'
```

---

### 3. **Detalhes de uma Categoria**

**GET** `/api/categorias/{id}/`

Retorna os dados de uma categoria específica.

**Headers (Obrigatório)**
```
Authorization: Bearer <seu_access_token>
```

**Response (200 OK)**
```json
{
  "id": 1,
  "nome": "Alimentação",
  "tipo": "despesa",
  "usuario": 1,
  "usuario_nome": "joao_silva",
  "criada_em": "2026-05-25T12:00:00Z"
}
```

**Teste com cURL**
```bash
curl -X GET http://localhost:8000/api/categorias/1/ \
  -H "Authorization: Bearer seu_access_token_aqui"
```

---

### 4. **Atualizar Categoria (Parcial)**

**PATCH** `/api/categorias/{id}/`

Atualiza parcialmente uma categoria.

**Headers (Obrigatório)**
```
Authorization: Bearer <seu_access_token>
```

**Body (JSON)** - Todos os campos são opcionais
```json
{
  "nome": "Alimentação Saudável",
  "tipo": "receita"
}
```

**Response (200 OK)**
```json
{
  "id": 1,
  "nome": "Alimentação Saudável",
  "tipo": "receita",
  "usuario": 1,
  "usuario_nome": "joao_silva",
  "criada_em": "2026-05-25T12:00:00Z"
}
```

**Teste com cURL**
```bash
curl -X PATCH http://localhost:8000/api/categorias/1/ \
  -H "Authorization: Bearer seu_access_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Alimentação Saudável"
  }'
```

---

### 5. **Atualizar Categoria (Total)**

**PUT** `/api/categorias/{id}/`

Atualiza todos os campos de uma categoria.

**Headers (Obrigatório)**
```
Authorization: Bearer <seu_access_token>
```

**Body (JSON)**
```json
{
  "nome": "Transporte",
  "tipo": "despesa"
}
```

**Response (200 OK)**
```json
{
  "id": 1,
  "nome": "Transporte",
  "tipo": "despesa",
  "usuario": 1,
  "usuario_nome": "joao_silva",
  "criada_em": "2026-05-25T12:00:00Z"
}
```

**Teste com cURL**
```bash
curl -X PUT http://localhost:8000/api/categorias/1/ \
  -H "Authorization: Bearer seu_access_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Transporte",
    "tipo": "despesa"
  }'
```

---

### 6. **Excluir Categoria**

**DELETE** `/api/categorias/{id}/`

Exclui permanentemente uma categoria.

**Headers (Obrigatório)**
```
Authorization: Bearer <seu_access_token>
```

**Response (204 No Content)**
Sem conteúdo na resposta (sucesso)

**Teste com cURL**
```bash
curl -X DELETE http://localhost:8000/api/categorias/1/ \
  -H "Authorization: Bearer seu_access_token_aqui"
```

---

### Regras de Negócio - Categorias

1. **Isolamento por usuário:** Cada usuário vê e gerencia apenas suas próprias categorias
2. **Categoria duplicada:** Não é permitido criar duas categorias com o mesmo **nome**, **tipo** e **mesmo usuário**
3. **Mesmo nome, tipo diferente:** É permitido ter "Alimentação" como despesa e "Alimentação" como receita
4. **Tipo padrão:** Se o campo `tipo` não for informado, a categoria será criada como "despesa"
5. **Normalização do nome:** O nome é automaticamente capitalizado (ex.: "alimentação" → "Alimentação")

---

## Fluxo Completo de Teste

### Cenário 1: Usuários

1. **Registre um novo usuário** (POST `/api/usuarios/cadastro/`)
2. **Faça login** (POST `/api/usuarios/login/`) — Copie o `access` token
3. **Consulte o perfil** (GET `/api/usuarios/perfil/`) — Use o `access` token no header
4. **Edite o perfil** (PATCH `/api/usuarios/perfil/`)
5. **Troque a senha** (PATCH `/api/usuarios/trocar-senha/`)
6. **Faça login novamente** com a nova senha para obter novo token
7. **Exclua a conta** (DELETE `/api/usuarios/perfil/`)

### Cenário 2: Categorias (após login)

1. **Faça login** (POST `/api/usuarios/login/`) — Copie o `access` token
2. **Crie categorias de despesa:**
   - POST `/api/categorias/` → `{ "nome": "Alimentação", "tipo": "despesa" }`
   - POST `/api/categorias/` → `{ "nome": "Transporte", "tipo": "despesa" }`
   - POST `/api/categorias/` → `{ "nome": "Moradia", "tipo": "despesa" }`
3. **Crie categorias de receita:**
   - POST `/api/categorias/` → `{ "nome": "Salário", "tipo": "receita" }`
   - POST `/api/categorias/` → `{ "nome": "Freelance", "tipo": "receita" }`
4. **Liste todas as suas categorias** (GET `/api/categorias/`)
5. **Consulte uma categoria específica** (GET `/api/categorias/1/`)
6. **Atualize o nome de uma categoria** (PATCH `/api/categorias/1/`)
7. **Tente criar uma categoria duplicada** (deve retornar erro 400)
8. **Exclua uma categoria** (DELETE `/api/categorias/1/`)

---

## Tratamento de Erros

### Erro 400 - Bad Request (Cadastro/Criação)
```json
{
  "nome": ["Categoria com este nome já existe para este usuário."]
}
```

### Erro 400 - Categoria Duplicada
```json
{
  "non_field_errors": [
    "Você já possui uma categoria \"Alimentação\" do tipo \"despesa\"."
  ]
}
```

### Erro 401 - Unauthorized
```json
{
  "detail": "As credenciais de autenticação não foram fornecidas."
}
```

### Erro 404 - Not Found
```json
{
  "detail": "Nenhum Categoria encontrado conforme o ID fornecido."
}
```

---

## Autenticação JWT

Todos os endpoints protegidos requerem um token JWT no header:

```
Authorization: Bearer <seu_access_token>
```

**Tempo de expiração do token de acesso:** 5 minutos
**Tempo de expiração do token de refresh:** 1 dia

Para renovar o token expirado, use o endpoint de refresh.

---

## Admin Panel

Acesse o painel administrativo em:
```
http://localhost:8000/admin/
```

Use as credenciais do superusuário criado. No admin é possível gerenciar usuários, categorias e visualizar logs.

---

## Troubleshooting

### "No module named 'rest_framework'"
```bash
pip install djangorestframework
```

### "No module named 'rest_framework_simplejwt'"
```bash
pip install djangorestframework-simplejwt
```

### "CORS error"
Certifique-se de que `corsheaders` está instalado e configurado em `MIDDLEWARE` no `settings.py`.

### Migration pendente
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Contribuição

Para contribuir com o projeto, por favor:

1. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
2. Commit suas mudanças (`git commit -m 'Add MinhaFeature'`)
3. Push para a branch (`git push origin feature/MinhaFeature`)
4. Abra um Pull Request

---

## Licença

Este projeto está sob licença MIT.