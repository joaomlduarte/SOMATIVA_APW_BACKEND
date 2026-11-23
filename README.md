# MangeFlix: Backend (API REST)

API REST da plataforma **MangeFlix**, desenvolvida com **Django REST Framework** para a Situação de Aprendizagem de Aplicações Web (SENAI "Roberto Mange").
Ela cuida de cadastro, login com JWT, catálogo de filmes e favoritos de cada usuário.

> Frontend (Vue.js): https://github.com/joaomlduarte/SOMATIVA_APW_FRONTEND
>
> **No ar (Railway):** app em https://frontend-production-dc1ee1f6.up.railway.app, API em https://backend-production-a2814271.up.railway.app/api/

## Tecnologias

- Python 3.13, Django 5.2 e Django REST Framework
- Simple JWT (autenticação por token)
- django-cors-headers (liberação do frontend)
- python-dotenv (variáveis de ambiente)
- SQLite (banco de dados, acessado pelo ORM do Django)
- Gunicorn e WhiteNoise (servidor e arquivos estáticos em produção)

## Estrutura

```
mangeflix/            configurações do projeto (settings, urls)
usuarios/             cadastro e login
  serializers.py      validação do cadastro e do login
  services.py         autenticação por nome de usuário OU e-mail
  views.py / urls.py  rotas /api/cadastro/ e /api/login/
  tests.py            testes unitários
filmes/               catálogo e favoritos
  models.py           Filme e Favorito (favorito único por usuário + filme)
  serializers.py      FilmeSerializer e FavoritoSerializer
  views.py / urls.py  rotas /api/filmes/ e /api/favoritos/
  migrations/0002_*   cadastra os 12 filmes iniciais no banco
  tests.py            testes unitários
media/posters/        pôsteres dos filmes
```

Os usuários usam o modelo nativo do Django (`User`), que guarda a senha com hash.

## Endpoints

| Método | Endpoint | Função | Login? |
|---|---|---|---|
| POST | `/api/cadastro/` | Cadastrar usuário (`username`, `email`, `senha`, `confirmacao_senha`) | Não |
| POST | `/api/login/` | Login com usuário **ou** e-mail (`usuario`, `senha`); devolve o token JWT | Não |
| GET | `/api/filmes/` | Listar filmes | Sim |
| GET | `/api/filmes/{id}/` | Consultar um filme | Sim |
| GET | `/api/favoritos/` | Listar os favoritos do usuário logado | Sim |
| POST | `/api/favoritos/` | Adicionar filme aos favoritos (`filme_id`) | Sim |
| DELETE | `/api/favoritos/{id}/` | Remover favorito | Sim |

As rotas protegidas exigem o cabeçalho `Authorization: Bearer <token>`.
O usuário é identificado pelo token, nunca por um id enviado pelo frontend. Cada usuário só vê e só remove os próprios favoritos, e o mesmo filme não pode ser favoritado duas vezes.

## Como executar (Windows / PowerShell)

```powershell
# 1. Ambiente virtual e dependências
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Variáveis de ambiente: copie o modelo e troque a SECRET_KEY
copy .env.example .env

# 3. Banco de dados (cria as tabelas e cadastra os 12 filmes)
python manage.py migrate

# 4. (Opcional) usuário para o Django Admin
python manage.py createsuperuser

# 5. Subir a API em http://127.0.0.1:8000
python manage.py runserver
```

Para gerar uma `SECRET_KEY` nova:

```powershell
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

Novos filmes podem ser cadastrados pelo Django Admin em http://127.0.0.1:8000/admin/.

### Variáveis de ambiente (`.env`)

| Variável | Exemplo | Para quê |
|---|---|---|
| `SECRET_KEY` | (chave aleatória) | Chave secreta do Django (obrigatória) |
| `DEBUG` | `True` | Modo de desenvolvimento (também serve os pôsteres) |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Hosts aceitos |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173` | Endereço do frontend |

O `.env` não vai para o Git; só o `.env.example`.

## Testes

```powershell
python manage.py test
```

São 20 testes unitários: cadastro, validações, login por usuário e por e-mail, credenciais inválidas, proteção das rotas, favorito duplicado, isolamento dos favoritos entre usuários e remoção.

## Publicação no Railway

O projeto `SOMATIVA_APW` no Railway tem dois serviços, `backend` e `frontend`, e roda no plano gratuito.
O backend foi publicado a partir desta pasta com o Railway CLI:

```powershell
railway up --service backend
```

O Railpack detecta o Django, roda `python manage.py migrate` e sobe o `gunicorn`.
O banco SQLite fica em um volume montado em `/data`, então usuários e favoritos continuam salvos entre deploys.

Variáveis do serviço `backend` no Railway:

| Variável | Valor |
|---|---|
| `SECRET_KEY` | chave aleatória (só no Railway) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `backend-production-a2814271.up.railway.app` |
| `CSRF_TRUSTED_ORIGINS` | `https://backend-production-a2814271.up.railway.app` |
| `CORS_ALLOWED_ORIGINS` | `https://frontend-production-dc1ee1f6.up.railway.app` |
| `DATABASE_PATH` | `/data/db.sqlite3` |

No plano gratuito o serviço "dorme" depois de alguns minutos sem acesso. A primeira requisição seguinte demora alguns segundos para acordar.

## CI/CD e branches

- `master`: produção; `dev`: desenvolvimento.
- O GitHub Actions (`.github/workflows/ci.yml`) roda `check` e os testes a cada push e pull request.
