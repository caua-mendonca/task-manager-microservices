# ROTEIRO DE APRESENTACAO — Task Manager API
# Data: 15/06/2026 | Disciplina: Desenvolvimento de Software para Web

---

## ANTES DE SAIR DE CASA

```bash
cd TrabMarcio/task-manager
docker compose up -d
docker compose ps
```

Todos os containers devem aparecer como **Up** ou **healthy**.

### Abrir essas 5 abas no browser e deixar prontas:

| Aba | URL | Quem usa |
|-----|-----|----------|
| 1 | http://localhost:3001/api/auth/docs   | Renan |
| 2 | http://localhost:3002/api/tasks/docs  | Renan |
| 3 | http://localhost:3003/api/users/docs  | Renan |
| 4 | http://localhost:9090/targets         | Caua  |
| 5 | http://localhost:3004/d/task-manager-overview | Caua |

---

## PARTE 1 — JULIO (Slides 1 e 2)
Apenas fala, sem demo tecnica. Apresenta o grupo e a visao geral.

---

## PARTE 2 — ARTHUR (Slides 3 e 13)
Apenas fala, explica o diagrama de arquitetura. Sem demo tecnica.

---

## PARTE 3 — GUILHERME (Slides 4 e 5)

### Mostrar containers rodando (Slide 4 — Docker)

Abrir terminal e rodar:
```bash
docker compose ps
```

Saida esperada — todos devem estar **Up**:
```
NAME           STATUS          PORTS
api-gateway    Up              0.0.0.0:3000->3000/tcp
auth-service   Up              0.0.0.0:3001->3001/tcp
grafana        Up              0.0.0.0:3004->3000/tcp
mongo          Up (healthy)    0.0.0.0:27017->27017/tcp
prometheus     Up              0.0.0.0:9090->9090/tcp
task-service   Up              0.0.0.0:3002->3002/tcp
user-service   Up              0.0.0.0:3003->3003/tcp
```

Fala:
> "Sete containers rodando com um unico comando: docker compose up -d"

---

## PARTE 4 — RENAN (Slides 6 e 7) — DEMO AO VIVO DA API

### PASSO 1 — Registrar usuario
Abrir aba 1: http://localhost:3001/api/auth/docs

Clicar em: **POST /api/auth/register** > **Try it out**

Colar no campo body:
```json
{
  "name": "Apresentacao Turma",
  "email": "demo@apresentacao.com",
  "password": "senha123",
  "role": "admin"
}
```

Clicar **Execute**.

Resposta esperada (201):
```json
{
  "message": "Usuario criado com sucesso",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "665abc123...",
    "name": "Apresentacao Turma",
    "email": "demo@apresentacao.com",
    "role": "admin"
  }
}
```

**COPIAR O TOKEN** — vai precisar dele em todos os proximos passos.

---

### PASSO 2 — Autorizar no Swagger (Auth Service)
Clicar no botao **Authorize** (canto superior direito do Swagger)
Colar o token no campo **Value**
Clicar **Authorize** > **Close**

Fala:
> "Agora todas as requisicoes vao enviar o token JWT automaticamente."

---

### PASSO 3 — Ver dados do usuario logado
Clicar em: **GET /api/auth/me** > **Try it out** > **Execute**

Resposta esperada (200):
```json
{
  "user": {
    "id": "665abc123...",
    "name": "Apresentacao Turma",
    "email": "demo@apresentacao.com",
    "role": "admin"
  }
}
```

---

### PASSO 4 — Ir para o Task Service
Abrir aba 2: http://localhost:3002/api/tasks/docs

Clicar em **Authorize** > colar o mesmo token > **Authorize** > **Close**

---

### PASSO 5 — Criar Tarefa 1
Clicar em: **POST /api/tasks** > **Try it out**

Colar:
```json
{
  "title": "Preparar slides da apresentacao",
  "description": "Finalizar os 13 slides para a disciplina",
  "priority": "high",
  "status": "pending",
  "category": "faculdade",
  "tags": ["apresentacao", "web"]
}
```

Clicar **Execute**.

Resposta esperada (201):
```json
{
  "message": "Tarefa criada com sucesso",
  "data": {
    "_id": "665def456...",
    "title": "Preparar slides da apresentacao",
    "priority": "high",
    "status": "pending",
    "createdBy": "665abc123...",
    "deletedAt": null
  }
}
```

**COPIAR O _id DA TAREFA** — ex: 665def456...

---

### PASSO 6 — Criar Tarefa 2
Mesmo endpoint **POST /api/tasks** > **Try it out**

Colar:
```json
{
  "title": "Subir containers Docker",
  "description": "Garantir que todos os 7 containers estao rodando",
  "priority": "critical",
  "status": "done",
  "category": "infraestrutura",
  "tags": ["docker", "devops"]
}
```

Clicar **Execute** — salvar o _id tambem.

---

### PASSO 7 — Criar Tarefa 3
```json
{
  "title": "Configurar Prometheus e Grafana",
  "description": "Dashboard com 7 paineis de monitoramento",
  "priority": "medium",
  "status": "in_progress",
  "category": "monitoramento"
}
```

---

### PASSO 8 — Listar todas as tarefas
Clicar em: **GET /api/tasks** > **Try it out**

Preencher:
- page: **1**
- limit: **10**

Clicar **Execute**.

Resposta esperada (200):
```json
{
  "data": [
    { "title": "Configurar Prometheus e Grafana", "status": "in_progress" },
    { "title": "Subir containers Docker", "status": "done" },
    { "title": "Preparar slides da apresentacao", "status": "pending" }
  ],
  "pagination": {
    "total": 3,
    "page": 1,
    "limit": 10,
    "totalPages": 1
  }
}
```

Fala:
> "Tres tarefas criadas, paginacao funcionando, total 3."

---

### PASSO 9 — Filtrar por prioridade alta
Mesmo **GET /api/tasks** > **Try it out**

Preencher:
- priority: **high**
- page: **1**
- limit: **10**

Clicar **Execute** — deve retornar so "Preparar slides".

Fala:
> "Filtro por prioridade — retornou apenas as tarefas de prioridade high."

---

### PASSO 10 — Buscar por nome
Clicar em: **GET /api/tasks/name/{title}** > **Try it out**

No campo title digitar: **Docker**

Clicar **Execute** — deve retornar "Subir containers Docker".

Fala:
> "Busca por nome usando regex — nao precisa digitar o titulo completo."

---

### PASSO 11 — Buscar por ID
Clicar em: **GET /api/tasks/{id}** > **Try it out**

Colar o _id da Tarefa 1 copiado no Passo 5.

Clicar **Execute** — retorna os detalhes completos da tarefa.

---

### PASSO 12 — Atualizar status
Clicar em: **PATCH /api/tasks/{id}/status** > **Try it out**

- id: colar o _id da Tarefa 1
- Body:
```json
{
  "status": "in_progress"
}
```

Clicar **Execute**.

Resposta esperada (200):
```json
{
  "message": "Status atualizado",
  "data": {
    "title": "Preparar slides da apresentacao",
    "status": "in_progress"
  }
}
```

Fala:
> "Atualizou so o status sem precisar mandar o objeto inteiro."

---

### PASSO 13 — Atualizar tarefa completa
Clicar em: **PUT /api/tasks/{id}** > **Try it out**

- id: colar o _id da Tarefa 1
- Body:
```json
{
  "title": "Preparar slides da apresentacao",
  "description": "CONCLUIDO — 13 slides prontos e revisados",
  "priority": "high",
  "status": "done",
  "dueDate": "2026-06-15T10:00:00.000Z"
}
```

Clicar **Execute** — retorna a tarefa atualizada.

---

### PASSO 14 — Soft Delete (deletar tarefa)
Clicar em: **DELETE /api/tasks/{id}** > **Try it out**

- id: colar o _id da Tarefa 3 (Prometheus/Grafana)

Clicar **Execute**.

Resposta esperada (200):
```json
{
  "message": "Tarefa deletada com sucesso (soft delete)"
}
```

Agora fazer **GET /api/tasks** novamente — so 2 tarefas aparecem.

Fala:
> "A tarefa sumiu da listagem mas nao foi apagada do banco — o campo deletedAt foi preenchido."

---

### PASSO 15 — Restaurar tarefa deletada (admin)
Clicar em: **POST /api/tasks/{id}/restore** > **Try it out**

- id: o mesmo _id da tarefa deletada

Clicar **Execute**.

Resposta esperada (200):
```json
{
  "message": "Tarefa restaurada",
  "data": { "title": "Configurar Prometheus e Grafana", "deletedAt": null }
}
```

Fazer **GET /api/tasks** novamente — as 3 tarefas voltam.

Fala:
> "Restaurada — isso e o soft delete. Dado nunca se perde."

---

### PASSO 16 — Ver usuarios (User Service — admin)
Abrir aba 3: http://localhost:3003/api/users/docs

Clicar **Authorize** > colar token > **Authorize** > **Close**

Clicar em: **GET /api/users** > **Try it out**

Preencher:
- page: **1**
- limit: **10**

Clicar **Execute**.

Resposta esperada (200):
```json
{
  "data": [
    { "name": "Apresentacao Turma", "email": "demo@apresentacao.com", "role": "admin" }
  ],
  "pagination": { "total": 1, "page": 1 }
}
```

Fala:
> "User Service lendo da mesma colecao do Auth Service — sem duplicacao de dados."

---

## PARTE 5 — CAUA — Prometheus ao vivo (Slide 10)

### PASSO 1 — Abrir aba 4 (Prometheus Targets)
URL: http://localhost:9090/targets

Mostrar para a sala — 4 targets com **State: UP** em verde.

Fala:
> "Quatro targets UP — o Prometheus esta coletando metricas de todos os servicos agora."

---

### PASSO 2 — Consultar metrica customizada
Clicar em **Graph** no menu do Prometheus

Na barra de busca digitar:
```
http_requests_total
```

Clicar **Execute** > clicar na aba **Graph**

Fala:
> "Essa e a metrica que criamos — conta cada requisicao com metodo, rota e status."

---

### PASSO 3 — Consultar taxa de requisicoes
Apagar e digitar:
```
rate(http_requests_total[1m])
```

Clicar **Execute** > aba **Graph**

Fala:
> "Requisicoes por segundo no ultimo minuto — deu pra ver o pico quando fizemos os testes."

---

### PASSO 4 — Consultar memoria
Digitar:
```
nodejs_heap_size_used_bytes
```

Clicar **Execute** > aba **Graph**

Fala:
> "Memoria heap de cada servico — api-gateway usa muito menos porque so faz proxy."

---

### PASSO 5 — Consultar status dos servicos
Digitar:
```
up
```

Clicar **Execute** > aba **Table**

Deve aparecer 4 linhas com valor **1** (= UP).

---

## PARTE 6 — CAUA — Grafana ao vivo (Slide 10)

### PASSO 1 — Abrir aba 5 (Grafana Dashboard)
URL: http://localhost:3004/d/task-manager-overview

Login se pedir: admin / admin123

---

### PASSO 2 — Explicar cada painel (ver abaixo)

**Painel 1 — Status dos Servicos (barras verdes)**
> "Quatro barras verdes — todos os servicos UP. Se um cair, vira vermelho na hora."

**Painel 2 — Taxa de Requisicoes HTTP**
> "Requisicoes por segundo em tempo real. Os picos sao os testes que fizemos."

**Painel 3 — Total de Requisicoes (numero grande)**
> "Total acumulado desde que o sistema subiu."

Fazer uma requisicao no Swagger agora — mostrar o numero subindo.

**Painel 4 — Memoria Heap Node.js**
> "Gateway usa 10 MiB, os outros servicos usam 25-30 MiB por causa do Mongoose carregado."

**Painel 5 — Uso de CPU**
> "Menos de 1% de CPU em operacao normal — sistema muito leve."

**Painel 6 — Event Loop Lag**
> "Abaixo de 5ms de media — Node.js nao esta travando em nenhuma operacao pesada."

**Painel 7 — Handles Ativos**
> "Conexoes abertas por servico — valores estaveis, sem vazamento de memoria."

---

### PASSO 3 — Gerar dados ao vivo nos graficos
Voltar no Swagger e executar rapidamente 3 GETs:
- GET /api/tasks
- GET /api/tasks
- GET /api/tasks

Voltar no Grafana — mostrar os graficos subindo em tempo real.

Fala:
> "Olha o grafico de requisicoes subindo agora — sao os GETs que acabei de fazer."

---

## PARTE 7 — CAUA — Swagger ao vivo (Slide 12)

Mostrar as 3 abas ja abertas:

**Aba 1:** http://localhost:3001/api/auth/docs
> "Auth Service — todos os endpoints de autenticacao documentados."

**Aba 2:** http://localhost:3002/api/tasks/docs
> "Task Service — CRUD completo com schemas detalhados."

Expandir um endpoint qualquer > mostrar o **Schema** do request body e dos responses.

> "Cada endpoint mostra quais campos aceita, quais sao obrigatorios, e todos os possiveis codigos de retorno — 200, 201, 400, 401, 403, 404."

**Aba 3:** http://localhost:3003/api/users/docs
> "User Service — gerenciamento de perfis."

---

## ORDEM COMPLETA DA APRESENTACAO

```
1. Julio       Slide 1 (Capa) + Slide 2 (Visao Geral)        ~3 min
2. Arthur      Slide 3 (Arquitetura)                          ~3 min
3. Guilherme   Slide 4 (Docker) + Slide 5 (Banco de Dados)   ~4 min
4. Renan       Slide 6 (Funcionalidades) + Slide 7 (Demo)    ~6 min
5. Luis        Slide 8 (Seguranca) + Slide 9 (Testes k6)     ~4 min
6. Caua        Slide 10 (Prometheus+Grafana)                  ~4 min
               Slide 11 (Deploy)                              ~2 min
               Slide 12 (Swagger)                             ~2 min
7. Arthur      Slide 13 (Conclusao)                           ~2 min
```

**Total estimado: ~30 minutos**

---

## SE ALGO DER ERRADO

| Problema | Solucao |
|----------|---------|
| Container caiu | `docker compose up -d` |
| Token expirado (erro 401) | Registrar novo usuario com email diferente |
| Swagger nao autoriza | Clicar Authorize e colar o token sem "Bearer" na frente |
| Grafana sem dados | Mudar periodo para "Last 5 minutes" no canto superior direito |
| Targets DOWN no Prometheus | `docker compose restart prometheus` |
| Erro 409 no register (email ja existe) | Usar email diferente: demo2@teste.com |
| Grafana nao abre | `docker compose restart grafana` e aguardar 15s |
| Tudo travado | `docker compose down && docker compose up -d` |

---

## COMANDOS RAPIDOS PARA COPIAR

```bash
# Subir tudo
docker compose up -d

# Ver status
docker compose ps

# Ver logs de um servico
docker compose logs auth-service --tail=20

# Reiniciar um servico
docker compose restart grafana

# Reiniciar tudo
docker compose down && docker compose up -d

# Rodar teste de carga k6
MSYS_NO_PATHCONV=1 docker compose --profile testing run --rm k6 run /scripts/test.js
```

---

## DADOS PARA CRIAR NA DEMO (copie e cole direto)

### Usuario admin (registro)
```json
{
  "name": "Apresentacao Turma",
  "email": "demo@apresentacao.com",
  "password": "senha123",
  "role": "admin"
}
```

### Tarefa 1 — prioridade high
```json
{
  "title": "Preparar slides da apresentacao",
  "description": "Finalizar os 13 slides para a disciplina",
  "priority": "high",
  "status": "pending",
  "category": "faculdade",
  "tags": ["apresentacao", "web"]
}
```

### Tarefa 2 — prioridade critical
```json
{
  "title": "Subir containers Docker",
  "description": "Garantir que todos os 7 containers estao rodando",
  "priority": "critical",
  "status": "done",
  "category": "infraestrutura",
  "tags": ["docker", "devops"]
}
```

### Tarefa 3 — prioridade medium
```json
{
  "title": "Configurar Prometheus e Grafana",
  "description": "Dashboard com 7 paineis de monitoramento",
  "priority": "medium",
  "status": "in_progress",
  "category": "monitoramento"
}
```

### Atualizar status
```json
{ "status": "in_progress" }
```

### Atualizar tarefa completa
```json
{
  "title": "Preparar slides da apresentacao",
  "description": "CONCLUIDO — 13 slides prontos e revisados",
  "priority": "high",
  "status": "done",
  "dueDate": "2026-06-15T10:00:00.000Z"
}
```

---

## URLS COMPLETAS DE REFERENCIA

```
API Gateway:        http://localhost:3000
Auth Swagger:       http://localhost:3001/api/auth/docs
Task Swagger:       http://localhost:3002/api/tasks/docs
User Swagger:       http://localhost:3003/api/users/docs
Prometheus:         http://localhost:9090
Prometheus Targets: http://localhost:9090/targets
Grafana:            http://localhost:3004
Grafana Dashboard:  http://localhost:3004/d/task-manager-overview
Grafana Login:      admin / admin123
MongoDB:            localhost:27017 (interno — acesso via Compass se precisar)
```
