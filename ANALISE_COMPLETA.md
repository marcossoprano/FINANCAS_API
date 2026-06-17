# 🔍 Auditoria Completa — Finanças API

**Data da análise:** 16/06/2026
**Projeto:** Finanças Pessoais API
**Tech Lead responsável pela auditoria:** Cline

---

## 📊 Sumário Executivo

O projeto encontra-se em **estágio inicial de desenvolvimento (estimado ~15% concluído)**. O único módulo funcional é o de **Usuários e Autenticação**, que está **completo e operacional**. Os módulos de **Categorias** e **Transações** existem apenas como esqueletos (apps Django criados mas sem implementação). Dashboard, Relatórios e demais funcionalidades **não foram iniciados**.

---

## 1️⃣ Status Atual

### ✅ Concluído
| Funcionalidade | Status | Observações |
|---|---|---|
| Configuração do projeto Django | ✅ Completo | Django 6.0.5, DRF 3.17.1 |
| Modelo de usuário customizado | ✅ Completo | `Usuario(AbstractUser)` com campos extras |
| Cadastro de usuário | ✅ Completo | `POST /api/usuarios/cadastro/` |
| Login | ✅ Completo | `POST /api/usuarios/login/` |
| Perfil (GET/PATCH/DELETE) | ✅ Completo | `GET/PATCH/DELETE /api/usuarios/perfil/` |
| Alteração de senha | ✅ Completo | `PATCH /api/usuarios/trocar-senha/` |
| JWT (Access + Refresh) | ✅ Completo | Tokens nas views + endpoints `/api/token/` e `/api/token/refresh/` |
| Admin do Django | ✅ Completo | `UsuarioAdmin` configurado |
| CORS configurado | ✅ Completo | Origem localhost:3000 liberada |

### 🟡 Parcialmente Implementado
| Funcionalidade | Status | Observações |
|---|---|---|
| App `categorias` criado | 🟡 Estrutura vazia | Models, views, urls, admin — todos vazios |
| App `transacoes` criado | 🟡 Estrutura vazia | Models, views, urls, admin — todos vazios |
| Rotas registradas no `core/urls.py` | 🟡 Sem implementação | Rotas existem mas levam a apps vazios |
| PostgreSQL configurado | 🟡 Comentado | Configuração nos settings mas usando SQLite |

### ⬜ Não Iniciado
| Funcionalidade | Status |
|---|---|
| CRUD de Categorias | ⬜ Não iniciado |
| CRUD de Transações | ⬜ Não iniciado |
| Dashboard Financeiro | ⬜ Não iniciado |
| Relatórios Mensais/Anuais | ⬜ Não iniciado |
| Recuperação de Senha | ⬜ Não iniciado |
| Logout (blacklist de tokens) | ⬜ Não iniciado |
| Filtros de transações | ⬜ Não iniciado |
| Metas financeiras | ⬜ Não iniciado |
| Orçamentos | ⬜ Não iniciado |
| Exportação PDF/Excel | ⬜ Não iniciado |
| Testes automatizados | ⬜ Não iniciado |

---

## 2️⃣ Estrutura do Projeto

### Organização dos Apps Django

```
financas_api/
├── core/                     # Configuração principal do projeto
│   ├── settings.py           # Settings com DRF, JWT, CORS
│   ├── urls.py               # Rotas principais (admin, api/*, token/*)
│   ├── asgi.py
│   └── wsgi.py
├── usuarios/                 # ✅ FUNCIONAL
│   ├── models.py             # Usuario(AbstractUser)
│   ├── serializers.py        # 5 serializers implementados
│   ├── views.py              # ViewSet com 4 actions
│   ├── urls.py               # Router configurado
│   ├── admin.py              # Admin configurado
│   └── migrations/           # 0001_initial.py (migração aplicada)
├── categorias/               # ❌ ESQUELETO
│   ├── models.py             # Vazio (template)
│   ├── views.py              # Vazio (template)
│   ├── urls.py               # Vazio (comentário placeholder)
│   └── admin.py              # Vazio (template)
├── transacoes/               # ❌ ESQUELETO
│   ├── models.py             # Vazio (template)
│   ├── views.py              # Vazio (template)
│   ├── urls.py               # Vazio (comentário placeholder)
│   └── admin.py              # Vazio (template)
├── manage.py
├── requirements.txt
├── db.sqlite3
└── README.md
```

### Models Existentes

| Model | App | Campos | Status |
|---|---|---|---|
| `Usuario` | usuarios | `username`, `email` (unique), `password`, `first_name`, `last_name`, `criado_em`, `atualizado_em`, mais campos herdados de `AbstractUser` | ✅ Completo |

### Serializers Existentes

| Serializer | App | Uso | Status |
|---|---|---|---|
| `UsuarioRegisterSerializer` | usuarios | Cadastro (valida senha, cria usuário) | ✅ Completo |
| `UsuarioPerfillSerializer` | usuarios | GET perfil (somente leitura em campos de data) | ✅ Completo |
| `UsuarioUpdateSerializer` | usuarios | PATCH perfil (valida email único) | ✅ Completo |
| `UsuarioChangePasswordSerializer` | usuarios | Troca de senha (valida senha antiga, confirma nova) | ✅ Completo |
| `UsuarioLoginSerializer` | usuarios | Login (valida username + password) | ✅ Completo |

### Views Existentes

| View | App | Actions | Status |
|---|---|---|---|
| `UsuarioViewSet` | usuarios | `cadastro`, `login`, `perfil` (GET/PATCH/DELETE), `trocar_senha` | ✅ Completo |

### URLs Configuradas

| Rota | Métodos | Autenticação | Status |
|---|---|---|---|
| `/admin/` | All | Staff | ✅ |
| `/api/usuarios/cadastro/` | POST | AllowAny | ✅ |
| `/api/usuarios/login/` | POST | AllowAny | ✅ |
| `/api/usuarios/perfil/` | GET/PATCH/DELETE | IsAuthenticated | ✅ |
| `/api/usuarios/trocar-senha/` | PATCH | IsAuthenticated | ✅ |
| `/api/token/` | POST | AllowAny | ✅ (JWT padrão) |
| `/api/token/refresh/` | POST | AllowAny | ✅ (JWT padrão) |
| `/api/categorias/` | — | — | ⬜ Vazio |
| `/api/transacoes/` | — | — | ⬜ Vazio |

---

## 3️⃣ Banco de Dados

### Entidades Existentes
Apenas **1 entidade** implementada: `Usuario`

### Relacionamentos
- Nenhum relacionamento entre models foi definido ainda (categorias e transações não existem)

### Possíveis Melhorias

1. **Modelo `Categoria`** deve ter:
   - `usuario` (FK para Usuario) — categoria pertence a um usuário
   - `nome` (CharField)
   - `tipo` (ChoiceField: receita/despesa)
   - `cor` (CharField, opcional — para exibição em gráficos)
   - `icone` (CharField, opcional)
   - `criado_em`, `atualizado_em`

2. **Modelo `Transacao`** deve ter:
   - `usuario` (FK para Usuario)
   - `categoria` (FK para Categoria)
   - `tipo` (ChoiceField: receita/despesa)
   - `valor` (DecimalField)
   - `descricao` (TextField, opcional)
   - `data` (DateField)
   - `criado_em`, `atualizado_em`

3. **Modelo `MetaFinanceira`** (futuro):
   - `usuario` (FK)
   - `nome`
   - `valor_meta`
   - `valor_atual`
   - `data_limite`
   - `categoria` (FK opcional)

### Problemas de Modelagem Atuais
- ⚠️ Senha do PostgreSQL exposta no `settings.py` (linhas 97-103, comentada)
- ⚠️ SECRET_KEY em texto plano no código (django-insecure-...)
- ⚠️ DEBUG = True em produção potencial

---

## 4️⃣ Qualidade da Arquitetura

### ✅ Pontos Fortes

| Aspecto | Avaliação |
|---|---|
| **Separação de responsabilidades** | ✅ Apps bem divididos (usuarios, categorias, transacoes) |
| **Modelo de usuário customizado** | ✅ `AUTH_USER_MODEL = 'usuarios.Usuario'` — boa prática |
| **Uso de ViewSets** | ✅ Ações agrupadas por endpoint `@action` |
| **Serializers dedicados** | ✅ Serializers específicos por operação (Register, Perfil, Update, ChangePassword, Login) |
| **JWT configurado** | ✅ SimpleJWT integrado e configurado |
| **CORS configurado** | ✅ Frontend localhost:3000 liberado |
| **Fatiamento de serializers** | ✅ Validações separadas por contexto (email único no update, senha antiga no change) |

### ⚠️ Pontos de Atenção

| Aspecto | Problema | Recomendação |
|---|---|---|
| **Segurança** | `SECRET_KEY` e senha do banco no código | Usar variáveis de ambiente (`python-decouple` ou `django-environ`) |
| **DEBUG** | `DEBUG = True` fixo | Controlar via variável de ambiente |
| **Paginação** | Não configurada | Adicionar `DEFAULT_PAGINATION_CLASS` no DRF settings |
| **Permissões globais** | Não definidas | Adicionar `DEFAULT_PERMISSION_CLASSES = ['rest_framework.permissions.IsAuthenticated']` |
| **Throttling** | Não configurado | Importante para endpoints de login/cadastro evitar brute force |
| **Versionamento de API** | Não implementado | Considerar `/api/v1/` no futuro |
| **Testes** | Nenhum teste implementado | Prioridade para próximo sprint |
| **Logout** | Sem blacklist de tokens JWT | Configurar `BLACKLIST_AFTER_ROTATION = True` e app `blacklist` |
| **Refresh Token** | `ROTATE_REFRESH_TOKENS = False` | Considerar ativar para melhor segurança |
| **JTI Claim duplicado** | `JTI_CLAIM` definido 3x (linhas 171, 173, 184) | Remover duplicações |

### Escalabilidade
- ⚠️ A estrutura atual escala bem para o porte proposto
- ⚠️ O uso de SQLite é limitante para produção (já planejada migração para PostgreSQL)
- ⚠️ Falta configuração de índices nos models futuros

### Manutenibilidade
- ✅ Código limpo e organizado
- ✅ Docstrings presentes
- ✅ Validações separadas em serializers
- ⚠️ Faltam testes

### Padrões REST
- ✅ Nomes em português consistentes (boa prática para o contexto)
- ✅ Uso correto de HTTP methods (GET, POST, PATCH, DELETE)
- ✅ Status codes apropriados (201, 200, 204, 400, 401)
- ⚠️ DELETE retorna 204 mas sem corpo (pode retornar 200 com mensagem)

---

## 5️⃣ Problemas Encontrados

### 🔴 Críticos

| # | Problema | Arquivo | Linha | Impacto |
|---|---|---|---|---|
| 1 | `SECRET_KEY` exposta no código | `core/settings.py` | 23 | **ALTO** — vulnerabilidade de segurança |
| 2 | Senha do PostgreSQL em texto plano | `core/settings.py` | 99 | **ALTO** — vazamento de credenciais |
| 3 | `JTI_CLAIM` definido 3x | `core/settings.py` | 171, 173, 184 | **MÉDIO** — sobrescrita desnecessária (último valor vence) |
| 4 | Nenhuma permissão global definida | `core/settings.py` | 141-145 | **MÉDIO** — sem `DEFAULT_PERMISSION_CLASSES` |
| 5 | `categorias` e `transacoes` completamente vazios | Ambos apps | — | **ALTO** — funcionalidades principais não existem |

### 🟡 Médios

| # | Problema | Descrição |
|---|---|---|
| 6 | Sem testes automatizados | Risco de regressão ao implementar novas features |
| 7 | `LANGUAGE_CODE = 'en-us'` | Inconsistente com nomes de endpoints em português |
| 8 | `TIME_ZONE = 'UTC'` | Deveria ser 'America/Sao_Paulo' para contexto brasileiro |
| 9 | Sem paginação no DRF | Listagens podem ficar lentas com muitos registros |
| 10 | `UsuarioUpdateSerializer` usa `fields` sem `read_only_fields` | `email` pode ser alterado, o que é ok, mas não há validação de username |
| 11 | DELETE perfil retorna 204 sem corpo | Padrão inconsistente (outros endpoints retornam mensagem) |

### 🟢 Leves / Cosméticos

| # | Problema | Descrição |
|---|---|---|
| 12 | `perfil` escrito com um 'f' no serializer (`UsuarioPerfillSerializer`) | Erro de digitação: deveria ser `UsuarioPerfilSerializer` |
| 13 | Docstring "Metadados" no admin | Erro de português: "Metadados" → "Metadados" |
| 14 | `categorias/admin.py` importa mas não registra nada | Código boilerplate não utilizado |
| 15 | `transacoes/admin.py` importa mas não registra nada | Código boilerplate não utilizado |

---

## 6️⃣ Próximos Passos — Priorizados

### Sprint 1 — Fundamentos (Alta Prioridade)
| Ordem | Tarefa | Tempo Est. | Dependências |
|---|---|---|---|
| 1 | **🔧 Corrigir segurança**: mover SECRET_KEY e senha para `.env` | 1h | Nenhuma |
| 2 | **🔧 Corrigir JTI_CLAIM duplicado** | 15min | #1 |
| 3 | **🔧 Remover `BLACKLIST_AFTER_ROTATION = False`** para permitir logout | 15min | Nenhuma |
| 4 | **🔧 Adicionar `DEFAULT_PERMISSION_CLASSES = [IsAuthenticated]`** | 15min | Nenhuma |
| 5 | **🔧 Adicionar paginação global** | 15min | Nenhuma |
| 6 | **🔧 Mudar LANGUAGE_CODE e TIME_ZONE** | 5min | Nenhuma |
| 7 | **🔧 Corrigir typo `UsuarioPerfillSerializer`** | 5min | Nenhuma |

### Sprint 2 — Core Funcional (Alta Prioridade)
| Ordem | Tarefa | Tempo Est. | Dependências |
|---|---|---|---|
| 8 | **📦 Criar Modelo `Categoria`** com FK para Usuario | 1h | Nenhuma |
| 9 | **📦 Criar CRUD de Categorias** (ViewSet, Serializer, URLs) | 2h | #8 |
| 10 | **📦 Criar Modelo `Transacao`** com FK para Usuario e Categoria | 1h | #8 |
| 11 | **📦 Criar CRUD de Transações** com filtros (categoria, tipo, data, período) | 3h | #10 |

### Sprint 3 — Melhorias e Segurança (Média Prioridade)
| Ordem | Tarefa | Tempo Est. | Dependências |
|---|---|---|---|
| 12 | **🔒 Implementar Logout** com blacklist de tokens JWT | 1h | Nenhuma |
| 13 | **🔒 Adicionar Throttling** para endpoints de autenticação | 30min | Nenhuma |
| 14 | **🧪 Criar testes** para app usuarios (models, serializers, views) | 2h | Nenhuma |
| 15 | **🧪 Criar testes** para app categorias e transacoes | 3h | #9, #11 |

### Sprint 4 — Dashboard e Relatórios (Média Prioridade)
| Ordem | Tarefa | Tempo Est. | Dependências |
|---|---|---|---|
| 16 | **📊 Criar Dashboard** (saldo, receitas/despesas, fluxo de caixa) | 3h | #11 |
| 17 | **📊 Criar Relatórios** mensais/anuais com agrupamento por categoria | 3h | #11, #16 |

### Sprint 5 — Extras (Baixa Prioridade)
| Ordem | Tarefa | Tempo Est. | Dependências |
|---|---|---|---|
| 18 | **📧 Recuperação de senha** (email) | 2h | Nenhuma |
| 19 | **📄 Exportação PDF/Excel** | 3h | #17 |
| 20 | **🎯 Metas e Orçamentos** | 4h | #11 |

---

## 7️⃣ Roadmap Atualizado

```
Sprint 1 (Correções)     ████████░░░░░░░░░░░░  40%  ✅ Prioridade Máxima
Sprint 2 (Core)          ████████████████████  100% ⬜ PRÓXIMO
Sprint 3 (Testes/Seg)    ████████████████████  100% ⬜
Sprint 4 (Dashboard)     ████████████████████  100% ⬜
Sprint 5 (Extras)        ████████████████████  100% ⬜

Legenda:
✅ = Concluído
🟡 = Em andamento
⬜ = Não iniciado
```

---

## 🎯 Conclusão Geral

### O que está funcionando bem ✅
- Módulo de autenticação completo e robusto
- Código limpo e bem organizado
- Boas práticas Django (modelo customizado, ViewSets, serializers dedicados)
- JWT configurado corretamente

### O que precisa de atenção imediata 🔴
1. Exposição de credenciais no `settings.py`
2. Apps `categorias` e `transacoes` vazios (funcionalidade core do sistema)
3. Duplicação de `JTI_CLAIM` (não quebra, mas é código morto confuso)
4. Falta de testes automatizados

### Recomendação Estratégica 🎯
Recomendo **começar pela Sprint 1** (correções de segurança e configuração) e **imediatamente depois pela Sprint 2** (models e CRUDs de Categorias e Transações), pois sem essas funcionalidades o sistema não tem valor de negócio. Testes devem ser escritos em paralelo ao desenvolvimento (Sprint 3) para evitar dívida técnica.

**Estimativa total para MVP funcional:** ~10-12 horas de desenvolvimento
**Estimativa para funcionalidades completas:** ~25-30 horas