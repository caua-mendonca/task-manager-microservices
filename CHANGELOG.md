# Changelog

Todas as mudanças notáveis neste projeto serão documentadas aqui.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [Unreleased]

### Added
- Estrutura base de microsserviços (api-gateway, auth-service, task-service, user-service)
- Autenticação JWT com bcrypt
- API Gateway com rate limiting, CORS e helmet
- Monitoramento com Prometheus e Grafana
- Load testing com k6
- Docker Compose para orquestração local
- Configuração de deploy no Render.com
- Documentação Swagger em todos os serviços
- Health check endpoint em todos os serviços

---

## [1.0.0] — 2026-06-17

### Added
- Versão inicial do projeto
