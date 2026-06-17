# AGENTS.md — Task Manager Microservices API

Documento de referência técnica para agentes de IA e desenvolvedores que precisam entender, manter ou evoluir este projeto sem contexto prévio. Última atualização: 2026-06-08.

---

## Visão Geral

API REST de gerenciamento de tarefas construída com arquitetura de **microserviços Node.js**. Trabalho acadêmico para a disciplina de Desenvolvimento de Software para Web — apresentação: **15/06/2026**.

**Status: 100% completo e funcional.** Todos os serviços sobem, passam em testes funcionais e de carga.

---

## Estrutura de Diretórios

```
task-manager/
├── api-gateway/          # Porta 3000 — proxy reverso + rate limiting + métricas
│   ├── src/
│   │   ├── index.js
│   │   ├── middleware/
│   │   │   ├── logger.js
│   │   │   └── rateLimiter.js
│   │   └── routes/
│   │       └── proxy.js
│   ├── Dockerfile
│   ├── package.json
│   └── .dockerignore
├── auth-service/         # Porta 3001 — JWT, registro, login
│   ├── src/
│   │   ├── index.js
│   │   ├── config/db.js
│   │   ├── controllers/authController.js
│   │   ├── middleware/authMiddleware.js
│   │   ├── models/User.js
│   │   └── routes/authRoutes.js
│   ├── Dockerfile
│   ├── package.json
│   └── .dockerignore
├── task-service/         # Porta 3002 — CRUD de tarefas
│   ├── src/
│   │   ├── index.js
│   │   ├── config/db.js
│   │   ├── controllers/taskController.js
│   │   ├── middleware/authMiddleware.js
│   │   ├── models/Task.js
│   │   └── routes/taskRoutes.js
│   ├── Dockerfile
│   ├── package.json
│   └── .dockerignore
├── user-service/         # Porta 3003 — perfis de usuário (lê coleção do auth-service)
│   ├── src/
│   │   ├── index.js
│   │   ├── config/db.js
│   │   ├── controllers/userController.js
│   │   ├── middleware/authMiddleware.js
│   │   ├── models/UserProfile.js
│   │   └── routes/userRoutes.js
│   ├── Dockerfile
│   ├── package.json
│   └── .dockerignore
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml          # Scrape dos 4 serviços a cada 15s
│   └── grafana/
│       └── provisioning/
│           ├── datasources/
│           │   └── datasource.yml  # Prometheus como datasource padrão
│           └── dashboards/
│               ├── dashboards.yml  # Auto-provisioning config
│               └── task-manager-dashboard.json  # 7 painéis
├── load-testing/
│   └── k6/
│       └── test.js                 # Staged load test (até 100 VUs, 2m30s)
├── docker-compose.yml
├── .env
├── apresentacao.html               # Apresentação 13 slides (abre no browser)
└── AGENTS.md                       # Este arquivo
```

---

## Como Subir o Projeto

```bash
cd TrabMarcio/task-manager

# Subir todos os serviços (exceto k6)
docker compose up -d

# Verificar se todos estão saudáveis
docker compose ps

# Ver logs em tempo real
docker compose logs -f

# Parar tudo
docker compose down
```

**Ordem de inicialização garantida pelo Docker Compose:**
1. `mongo` (healthcheck: `mongosh --eval "db.adminCommand('ping').ok"`)
2. `auth-service`, `task-service`, `user-service` (aguardam `mongo: condition: service_healthy`)
3. `api-gateway` (aguarda os 3 serviços acima iniciarem)
4. `prometheus`, `grafana`

---

## Variáveis de Ambiente (`.env`)

```env
JWT_SECRET=supersecretjwtkey2024taskmanager
JWT_EXPIRES_IN=7d
MONGO_URI=mongodb://mongo:27017/taskmanager
API_GATEWAY_PORT=3000
AUTH_SERVICE_PORT=3001
TASK_SERVICE_PORT=3002
USER_SERVICE_PORT=3003
AUTH_SERVICE_URL=http://auth-service:3001
TASK_SERVICE_URL=http://task-service:3002
USER_SERVICE_URL=http://user-service:3003
GRAFANA_PASSWORD=admin123
```

---

## Endpoints da API

Todos os endpoints passam pelo API Gateway na porta **3000**. JWT no header `Authorization: Bearer <token>`.

### Auth Service (`/api/auth`)

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| POST | `/api/auth/register` | — | Registra usuário (retorna JWT) |
| POST | `/api/auth/login` | — | Login (retorna JWT) |
| GET | `/api/auth/me` | JWT | Dados do usuário autenticado |
| POST | `/api/auth/refresh` | JWT | Renova token JWT |

### Task Service (`/api/tasks`)

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| GET | `/api/tasks` | JWT | Lista tarefas com filtros e paginação |
| GET | `/api/tasks/:id` | JWT | Busca tarefa por ID |
| GET | `/api/tasks/name/:title` | JWT | Busca tarefas por título (regex) |
| POST | `/api/tasks` | JWT | Cria tarefa |
| PUT | `/api/tasks/:id` | JWT | Atualiza tarefa |
| PATCH | `/api/tasks/:id/status` | JWT | Atualiza apenas o status |
| DELETE | `/api/tasks/:id` | JWT | Soft delete |
| DELETE | `/api/tasks/:id/hard` | JWT + admin | Hard delete permanente |
| POST | `/api/tasks/:id/restore` | JWT + admin | Restaura soft-deleted task |

**Query params de GET `/api/tasks`:** `page`, `limit`, `status`, `priority`, `category`, `search`, `sortBy`, `order`, `assignedTo`

**Status válidos:** `pending`, `in_progress`, `done`, `cancelled`
**Prioridades válidas:** `low`, `medium`, `high`, `critical`

### User Service (`/api/users`)

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| GET | `/api/users` | JWT + admin | Lista todos os usuários com paginação |
| GET | `/api/users/:id` | JWT | Busca por ID (user só acessa próprio perfil) |
| PUT | `/api/users/:id` | JWT | Atualiza perfil (bio, avatar, name; role só por admin) |
| DELETE | `/api/users/:id` | JWT + admin | Soft delete do usuário |

---

## Swagger / OpenAPI

Disponível em cada serviço (acessar via porta direta ou após subir):

- Auth Service: `http://localhost:3001/api/auth/docs`
- Task Service: `http://localhost:3002/api/tasks/docs`
- User Service: `http://localhost:3003/api/users/docs`

Via API Gateway (após proxy): `http://localhost:3000/api/auth/docs` etc.

---

## Monitoramento

### Prometheus — `http://localhost:9090`

Coleta métricas dos 4 serviços a cada 15s. Targets:

```
api-gateway:3000/metrics
auth-service:3001/metrics
task-service:3002/metrics
user-service:3003/metrics
```

Métrica customizada no API Gateway: `http_requests_total{method, route, status}` (Counter).
Métricas padrão via `prom-client.collectDefaultMetrics()` em todos os serviços.

### Grafana — `http://localhost:3004`

- Login: `admin` / `admin123`
- Dashboard auto-provisionado: **Task Manager Overview** (uid: `task-manager-overview`)
- 7 painéis: Service Status, HTTP Request Rate, Total Requests, Node.js Heap Memory, CPU Usage, Event Loop Lag, Active Handles
- Refresh automático: 10s

---

## Load Testing (k6)

```bash
# Rodar o teste de carga (serviços devem estar rodando)
# No Git Bash / WSL — prefixo MSYS_NO_PATHCONV=1 evita conversão de paths no Windows
MSYS_NO_PATHCONV=1 docker compose --profile testing run --rm k6 run /scripts/test.js

# No PowerShell
$env:MSYS_NO_PATHCONV=1; docker compose --profile testing run --rm k6 run /scripts/test.js
```

**Cenário de carga:**
- 0→10 VUs em 30s
- 10→50 VUs em 1min
- 50→100 VUs em 30s
- 100→0 VUs em 30s

**Resultado verificado em produção:**
- 1838 iterações completas
- 11.029 requisições totais
- **0% de erros**
- Duração média: 10.66ms | p95: 31.02ms

**Thresholds:** `http_req_duration p(95) < 500ms`, `errors rate < 10%`

---

## Modelos de Dados (MongoDB — database: `taskmanager`)

### Coleção `users` (auth-service + user-service)

```javascript
{
  name: String (required, min 2),
  email: String (required, unique, lowercase),
  password: String (required, min 6, select: false — nunca retorna em queries),
  role: 'admin' | 'user' (default: 'user'),
  isActive: Boolean (default: true),
  deletedAt: Date (default: null — soft delete),
  createdAt, updatedAt // timestamps
}
```

**Índices:** `email` (unique, implícito), `deletedAt`

**Compartilhamento:** `user-service` usa `mongoose.model('UserProfile', schema, 'users')` — o terceiro argumento força a usar a mesma coleção do `auth-service`.

### Coleção `tasks` (task-service)

```javascript
{
  title: String (required, 3-100 chars),
  description: String (max 1000),
  status: 'pending' | 'in_progress' | 'done' | 'cancelled' (default: 'pending'),
  priority: 'low' | 'medium' | 'high' | 'critical' (default: 'medium'),
  category: String (default: 'general'),
  assignedTo: String,
  createdBy: String (required — ID do usuário),
  dueDate: Date,
  tags: [String],
  isActive: Boolean,
  deletedAt: Date (soft delete),
  createdAt, updatedAt
}
```

**Índices:** `status`, `priority`, `createdBy`, `deletedAt`, `title + description` (text search)

---

## Decisões de Arquitetura

### RBAC (Role-Based Access Control)

JWT carrega `{ id, email, role, name }`. O middleware `authMiddleware.js` em cada serviço valida o token e popula `req.user`. Rotas admin usam `authorize('admin')` (task-service) ou `adminOnly` (user-service).

```
admin → acessa todos os recursos de todos os usuários
user  → acessa apenas seus próprios recursos (filtro por createdBy)
```

### Soft Delete

`deletedAt: null` = ativo. `deletedAt: Date` = deletado. Todas as queries filtram `{ deletedAt: null }`. Hard delete só disponível para admin.

### Retry de Conexão MongoDB

Todos os `db.js` tentam conectar até 5 vezes com intervalo de 3s antes de chamar `process.exit(1)`. Isso complementa o healthcheck do Docker (que garante que o MongoDB está aceitando pings antes de iniciar os serviços).

### Proxy no API Gateway

`http-proxy-middleware` com `restreamBody` para repassar o body JSON nas requisições POST/PUT (necessário porque `express.json()` consome o stream antes do proxy).

---

## Problemas Conhecidos e Soluções

| Problema | Causa | Solução |
|----------|-------|---------|
| Race condition no startup | `depends_on` sem healthcheck não espera o MongoDB estar pronto | Healthcheck no `mongo` + `condition: service_healthy` |
| user-service retorna `total: 0` | Model usava coleção `userprofiles` diferente da `users` do auth | Terceiro argumento em `mongoose.model(..., ..., 'users')` |
| k6 path conversion no Windows | Git Bash converte `/scripts/test.js` para path do Windows | Prefixar com `MSYS_NO_PATHCONV=1` |
| Duplicate Mongoose index warning | `userSchema.index({ email: 1 })` duplicava o índice criado por `unique: true` | Removida a linha explícita |
| Container name conflict ao reiniciar | Container anterior ainda registrado | `docker rm -f $(docker ps -aq)` antes de subir |

---

## Apresentação

Arquivo `apresentacao.html` na raiz do projeto. Abrir diretamente no browser (não precisa de servidor).

**Navegação:** ← → para slides, Space para avançar, F para fullscreen, Home/End para início/fim.

**AÇÃO PENDENTE:** Substituir os placeholders no Slide 1:
- `[Aluno 1 — Nome]` → nome real
- `[Aluno 2 — Nome]` → nome real
- `[Aluno 3 — Nome]` → nome real (se houver)

---

## Checklist de Verificação Rápida

Antes de apresentar, executar:

```bash
# 1. Subir serviços
docker compose up -d

# 2. Verificar containers
docker compose ps

# 3. Testar health de cada serviço
curl http://localhost:3000/health  # api-gateway
curl http://localhost:3001/health  # auth-service
curl http://localhost:3002/health  # task-service
curl http://localhost:3003/health  # user-service

# 4. Testar fluxo completo
curl -s -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Teste","email":"teste@test.com","password":"senha123"}' | grep token

# 5. Prometheus targets (todos devem ser "up")
curl -s http://localhost:9090/api/v1/targets | grep health

# 6. Grafana acessível
# http://localhost:3004 — login: admin / admin123

# 7. Load test
MSYS_NO_PATHCONV=1 docker compose --profile testing run --rm k6 run /scripts/test.js
```

---

## Dependências por Serviço

### api-gateway
`express`, `http-proxy-middleware`, `cors`, `helmet`, `express-rate-limit`, `morgan`, `prom-client`, `dotenv`

### auth-service / task-service / user-service
`express`, `mongoose`, `bcryptjs`, `jsonwebtoken`, `express-validator`, `prom-client`, `swagger-jsdoc`, `swagger-ui-express`, `dotenv`
