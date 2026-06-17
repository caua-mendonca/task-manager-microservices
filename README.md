# Task Manager — API de Microsserviços

![Node.js](https://img.shields.io/badge/Node.js-24.x-339933?logo=node.js&logoColor=white)
![Express](https://img.shields.io/badge/Express-4.18-000000?logo=express&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-47A248?logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)

API de gerenciamento de tarefas construída com arquitetura de microsserviços. Resolve o problema de escalabilidade e separação de responsabilidades em sistemas de gestão de produtividade, permitindo que cada serviço seja desenvolvido, implantado e escalado de forma independente.

---

## Stack Tecnológica

| Tecnologia | Versão | Uso |
|---|---|---|
| Node.js | 24.x | Runtime dos microsserviços |
| Express.js | 4.18.2 | Framework HTTP |
| MongoDB | 7.0 | Banco de dados NoSQL |
| Mongoose | 8.0.3 | ODM para MongoDB |
| JWT | 9.0.2 | Autenticação stateless |
| bcryptjs | 2.4.3 | Hash de senhas |
| Docker | Latest | Containerização |
| Docker Compose | Latest | Orquestração local |
| Prometheus | Latest | Coleta de métricas |
| Grafana | Latest | Visualização de métricas |
| k6 | Latest | Load testing |
| Swagger/OpenAPI | 3.0 | Documentação da API |

---

## Arquitetura

```
┌─────────────────────────────────────────────────┐
│                   Cliente / Browser              │
└──────────────────────┬──────────────────────────┘
                       │ :3000
         ┌─────────────▼─────────────┐
         │        API Gateway        │
         │  (rate-limit, cors,        │
         │   helmet, proxy)          │
         └────┬──────────┬───────────┘
              │          │           │
           :3001       :3002       :3003
    ┌──────▼─────┐ ┌───▼──────┐ ┌──▼────────┐
    │Auth Service│ │Task Svc  │ │User Svc   │
    │ JWT + bcrypt│ │CRUD tasks│ │Profiles   │
    └──────┬─────┘ └───┬──────┘ └──┬────────┘
           └───────────┴───────────┘
                       │ :27017
              ┌────────▼────────┐
              │    MongoDB 7.0  │
              └─────────────────┘

Monitoramento:
  Prometheus :9090 ← métricas de todos os serviços
  Grafana    :3004 ← dashboards e alertas
```

---

## Estrutura de Diretórios

```
task-manager/
├── api-gateway/          # Proxy reverso e ponto de entrada
│   └── src/
│       ├── middleware/   # rateLimiter, logger
│       └── routes/       # proxy.js
├── auth-service/         # Autenticação e emissão de JWT
│   └── src/
│       ├── config/       # Conexão MongoDB
│       ├── controllers/  # authController
│       ├── middleware/   # authMiddleware
│       ├── models/       # User
│       └── routes/       # authRoutes
├── task-service/         # CRUD de tarefas
│   └── src/
│       ├── config/
│       ├── controllers/  # taskController
│       ├── models/       # Task
│       └── routes/       # taskRoutes
├── user-service/         # Gerenciamento de perfis
│   └── src/
│       ├── config/
│       ├── controllers/  # userController
│       ├── models/       # UserProfile
│       └── routes/       # userRoutes
├── monitoring/
│   ├── prometheus/       # prometheus.yml
│   └── grafana/          # datasources e dashboards
├── load-testing/
│   └── k6/               # Scripts de teste de carga
├── docker-compose.yml    # Orquestração completa
├── render.yaml           # Deploy no Render.com
├── .env.example          # Template de variáveis de ambiente
└── README.md
```

---

## Branches e Ambientes

| Branch | Ambiente | Finalidade |
|---|---|---|
| `master` | Produção | Código estável — requer 2 aprovações para merge |
| `staging` | Homologação | Validação QA antes de produção |
| `develop` | Desenvolvimento | Integração de features |

---

## Pré-requisitos

- [Node.js](https://nodejs.org) >= 18.x
- [Docker](https://www.docker.com) >= 24.x
- [Docker Compose](https://docs.docker.com/compose) >= 2.x
- [Git](https://git-scm.com) >= 2.x

---

## Instalação e Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/task-manager-microservices.git
cd task-manager-microservices
git checkout develop
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite .env com suas credenciais reais
```

Variáveis obrigatórias no `.env`:

| Variável | Descrição |
|---|---|
| `JWT_SECRET` | Chave secreta para assinar tokens JWT |
| `JWT_EXPIRES_IN` | Tempo de expiração do token (ex: `7d`) |
| `MONGO_URI` | URI de conexão com MongoDB |
| `GRAFANA_PASSWORD` | Senha do painel Grafana |

### 3. Suba o ambiente com Docker

```bash
docker compose up -d
```

---

## Executando por Ambiente

### Desenvolvimento local com Docker

```bash
# Subir todos os serviços
docker compose up -d

# Ver logs em tempo real
docker compose logs -f

# Derrubar tudo
docker compose down
```

### Desenvolvimento individual (sem Docker)

```bash
# Em terminais separados:
cd api-gateway && npm install && npm run dev   # :3000
cd auth-service && npm install && npm run dev  # :3001
cd task-service && npm install && npm run dev  # :3002
cd user-service && npm start                   # :3003
```

### Load Testing

```bash
docker compose --profile testing run k6 run /scripts/test.js
```

---

## Endpoints e Documentação

Após subir com Docker:

| Serviço | URL | Descrição |
|---|---|---|
| API Gateway | http://localhost:3000 | Ponto de entrada |
| Auth Swagger | http://localhost:3001/api/auth/docs | Docs de autenticação |
| Task Swagger | http://localhost:3002/api/tasks/docs | Docs de tarefas |
| User Swagger | http://localhost:3003/api/users/docs | Docs de usuários |
| Prometheus | http://localhost:9090 | Métricas |
| Grafana | http://localhost:3004 | Dashboards (admin / GRAFANA_PASSWORD) |

### Health Checks

```bash
curl http://localhost:3000/health  # API Gateway
curl http://localhost:3001/health  # Auth Service
curl http://localhost:3002/health  # Task Service
curl http://localhost:3003/health  # User Service
```

---

## Fluxo de Desenvolvimento

### Criando uma feature

```bash
git checkout develop
git pull origin develop
git checkout -b feature/nome-da-feature

# desenvolver...
git add .
git commit -m "feat: descrição da funcionalidade"

# abrir PR: feature/* → develop
```

### Promovendo para staging / produção

```
feature/* → develop  (1 aprovação)
develop   → staging  (1 aprovação + QA)
staging   → master   (2 aprovações)
```

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para o guia completo.

---

## Licença

MIT © 2026
