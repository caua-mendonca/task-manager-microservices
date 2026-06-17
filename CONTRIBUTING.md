# Guia de Contribuição

## Nomenclatura de Branches

| Prefixo | Uso | Exemplo |
|---|---|---|
| `feature/` | Nova funcionalidade | `feature/adicionar-tags-tarefa` |
| `fix/` | Correção de bug | `fix/token-jwt-expirado` |
| `hotfix/` | Correção crítica em produção | `hotfix/vulnerabilidade-auth` |
| `chore/` | Tarefa técnica (deps, config) | `chore/atualizar-mongoose` |
| `docs/` | Documentação | `docs/swagger-task-service` |
| `refactor/` | Refatoração sem mudança funcional | `refactor/extrair-middleware` |
| `test/` | Adição ou ajuste de testes | `test/auth-controller-unit` |

Sempre crie branches a partir de `develop`:

```bash
git checkout develop && git pull origin develop
git checkout -b feature/nome-da-feature
```

---

## Padrão de Commits (Conventional Commits)

```
<tipo>(<escopo opcional>): <descrição curta em imperativo>

[corpo opcional — o que e por quê, não como]

[rodapé opcional — breaking changes, issues fechadas]
```

### Tipos

| Tipo | Quando usar |
|---|---|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Somente documentação |
| `style` | Formatação (espaços, ponto-e-vírgula) sem mudança de lógica |
| `refactor` | Refatoração sem nova feature nem correção |
| `test` | Adição ou correção de testes |
| `chore` | Build, dependências, CI, scripts |
| `perf` | Melhoria de performance |
| `ci` | Mudanças em pipelines CI/CD |

### Exemplos

```bash
feat(auth): adicionar refresh token endpoint
fix(task-service): corrigir query de tarefas por status
docs(readme): atualizar instruções de setup local
chore: atualizar express para 4.19.0
refactor(api-gateway): extrair lógica de proxy para módulo separado
```

**Regras:**
- Descrição em minúsculas, sem ponto final
- Máximo 72 caracteres na primeira linha
- Use imperativo: "adicionar", "corrigir", "atualizar" (não "adicionado", "corrigido")

---

## Fluxo de Pull Requests

### Antes de abrir o PR

- [ ] Branch criada a partir de `develop` (ou `master` para hotfix)
- [ ] Commits seguem o padrão Conventional Commits
- [ ] Código testado localmente com `docker compose up`
- [ ] Health checks passando em todos os serviços afetados
- [ ] Nenhuma credencial ou `.env` commitado

### Destinos corretos

| De | Para | Aprovações |
|---|---|---|
| `feature/*`, `fix/*`, `chore/*`, `docs/*` | `develop` | 1 |
| `develop` | `staging` | 1 |
| `staging` | `master` | 2 |
| `hotfix/*` | `master` + `develop` | 2 |

### Tamanho do PR

Prefira PRs pequenos e focados. Um PR deve fazer uma coisa só. Se crescer demais, divida em PRs menores encadeados.

---

## Configuração do Ambiente Local

```bash
git clone https://github.com/SEU_USUARIO/task-manager-microservices.git
cd task-manager-microservices
cp .env.example .env
# preencha .env com valores locais
docker compose up -d
```

---

## Reportando Bugs

Use o template em `.github/ISSUE_TEMPLATE/bug_report.md` ao abrir uma issue.

## Solicitando Features

Use o template em `.github/ISSUE_TEMPLATE/feature_request.md`.
