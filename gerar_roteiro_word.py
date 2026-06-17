"""
Gerador do Roteiro de Apresentacao em Word
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

doc = Document()

# ── Configurar pagina ──────────────────────────────────────────────
section = doc.sections[0]
section.page_width  = Inches(8.27)   # A4
section.page_height = Inches(11.69)
section.left_margin   = Cm(2)
section.right_margin  = Cm(2)
section.top_margin    = Cm(2)
section.bottom_margin = Cm(2)

# ── Paleta ─────────────────────────────────────────────────────────
AZUL_ESCURO  = RGBColor(0x0D, 0x1B, 0x2A)
AZUL_MEDIO   = RGBColor(0x00, 0x72, 0xBC)
CIANO        = RGBColor(0x00, 0xB4, 0xD8)
VERDE        = RGBColor(0x06, 0xD6, 0xA0)
AMARELO      = RGBColor(0xE6, 0xA8, 0x00)
VERMELHO     = RGBColor(0xCC, 0x33, 0x33)
CINZA        = RGBColor(0x44, 0x44, 0x44)
PRETO        = RGBColor(0x00, 0x00, 0x00)
BRANCO       = RGBColor(0xFF, 0xFF, 0xFF)

# ── Helpers ────────────────────────────────────────────────────────

def set_cell_bg(cell, hex_color):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  hex_color)
    tcPr.append(shd)


def heading1(text, color=AZUL_MEDIO):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after  = Pt(4)
    run = p.add_run(text)
    run.bold      = True
    run.font.size = Pt(16)
    run.font.color.rgb = color
    return p


def heading2(text, color=CIANO):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text)
    run.bold      = True
    run.font.size = Pt(13)
    run.font.color.rgb = color
    return p


def heading3(text, color=VERDE):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(1)
    run = p.add_run(text)
    run.bold      = True
    run.font.size = Pt(11)
    run.font.color.rgb = color
    return p


def body(text, bold_part=None, color=PRETO, size=10.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.font.size      = Pt(size)
    run.font.color.rgb = color
    return p


def bullet(text, level=0, color=PRETO):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent  = Cm(0.5 + level * 0.5)
    p.paragraph_format.space_after  = Pt(1)
    run = p.add_run(text)
    run.font.size      = Pt(10)
    run.font.color.rgb = color
    return p


def code_block(lines):
    """Caixa estilo codigo com fundo cinza claro."""
    for line in lines:
        p = doc.add_paragraph()
        p.paragraph_format.space_after  = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.left_indent  = Cm(0.5)
        # fundo via shading no paragrafo
        pPr = p._p.get_or_add_pPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'),   'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'),  'EBEBEB')
        pPr.append(shd)
        run = p.add_run(line if line else " ")
        run.font.name      = 'Courier New'
        run.font.size      = Pt(8.5)
        run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x6E)


def fala(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = Cm(0.8)
    p.paragraph_format.space_after  = Pt(4)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  'E8F4FD')
    pPr.append(shd)
    run = p.add_run('"' + text + '"')
    run.font.size      = Pt(10)
    run.font.italic    = True
    run.font.color.rgb = RGBColor(0x00, 0x45, 0x88)


def divider():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    run = p.add_run('_' * 90)
    run.font.size      = Pt(6)
    run.font.color.rgb = RGBColor(0xBB, 0xBB, 0xBB)


def table_2col(rows, header=None, col_w=(8, 6)):
    t = doc.add_table(rows=len(rows) + (1 if header else 0), cols=2)
    t.style = 'Table Grid'
    if header:
        r = t.rows[0]
        for i, h in enumerate(header):
            cell = r.cells[i]
            set_cell_bg(cell, '0D1B2A')
            run = cell.paragraphs[0].add_run(h)
            run.bold           = True
            run.font.size      = Pt(10)
            run.font.color.rgb = BRANCO
    for ri, (c1, c2) in enumerate(rows):
        row = t.rows[ri + (1 if header else 0)]
        p1  = row.cells[0].paragraphs[0]
        r1  = p1.add_run(c1)
        r1.font.size      = Pt(9.5)
        r1.font.color.rgb = RGBColor(0x00, 0x55, 0x88)
        r1.font.bold      = True
        p2  = row.cells[1].paragraphs[0]
        r2  = p2.add_run(c2)
        r2.font.size      = Pt(9.5)
        r2.font.color.rgb = CINZA
    t.columns[0].width = Cm(col_w[0])
    t.columns[1].width = Cm(col_w[1])
    doc.add_paragraph()


def json_block(json_str):
    lines = json_str.strip().split('\n')
    code_block(lines)
    doc.add_paragraph()


# ══════════════════════════════════════════════════════════════════
# CAPA
# ══════════════════════════════════════════════════════════════════
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(40)
run = p_title.add_run('ROTEIRO DE APRESENTACAO')
run.bold           = True
run.font.size      = Pt(22)
run.font.color.rgb = AZUL_MEDIO

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run2 = p_sub.add_run('Task Manager Microservices API')
run2.bold           = True
run2.font.size      = Pt(16)
run2.font.color.rgb = CIANO

doc.add_paragraph()
p_info = doc.add_paragraph()
p_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
run3 = p_info.add_run('Desenvolvimento de Software para Web  |  15/06/2026')
run3.font.size      = Pt(11)
run3.font.color.rgb = CINZA

doc.add_paragraph()
divider()
doc.add_paragraph()

# Equipe
heading2('Equipe')
membros = [
    ('Julio Pimentel',    'Slides 1 e 2  —  Capa + Visao Geral'),
    ('Arthur Carvalhais', 'Slides 3 e 13 —  Arquitetura + Conclusao'),
    ('Guilherme Souza',   'Slides 4 e 5  —  Docker + Banco de Dados'),
    ('Renan Prado',       'Slides 6 e 7  —  Funcionalidades + Demo ao vivo'),
    ('Luis Barbosa',      'Slides 8 e 9  —  Seguranca + Testes k6'),
    ('Caua Mendonca',     'Slides 10, 11 e 12  —  Observabilidade + Deploy + Swagger'),
]
table_2col(membros, header=['Nome', 'Responsabilidade'])

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════
# SECAO 1 — ANTES DE SAIR DE CASA
# ══════════════════════════════════════════════════════════════════
heading1('1. ANTES DE SAIR DE CASA')

heading2('Subir todos os containers')
code_block([
    'cd TrabMarcio/task-manager',
    'docker compose up -d',
    'docker compose ps',
])
doc.add_paragraph()
body('Todos os containers devem aparecer como Up ou healthy.', color=CINZA)

heading2('Abrir as 5 abas no browser e deixar prontas')
abas = [
    ('Aba 1 — Auth Swagger',    'http://localhost:3001/api/auth/docs',              'Renan'),
    ('Aba 2 — Task Swagger',    'http://localhost:3002/api/tasks/docs',             'Renan'),
    ('Aba 3 — User Swagger',    'http://localhost:3003/api/users/docs',             'Renan'),
    ('Aba 4 — Prometheus',      'http://localhost:9090/targets',                    'Caua'),
    ('Aba 5 — Grafana',         'http://localhost:3004/d/task-manager-overview',    'Caua'),
]
t = doc.add_table(rows=len(abas)+1, cols=3)
t.style = 'Table Grid'
for i, h in enumerate(['Aba', 'URL', 'Quem usa']):
    cell = t.rows[0].cells[i]
    set_cell_bg(cell, '0D1B2A')
    run = cell.paragraphs[0].add_run(h)
    run.bold = True; run.font.size = Pt(10); run.font.color.rgb = BRANCO
for ri, (aba, url, quem) in enumerate(abas):
    row = t.rows[ri+1]
    for ci, val in enumerate([aba, url, quem]):
        run = row.cells[ci].paragraphs[0].add_run(val)
        run.font.size = Pt(9)
        run.font.color.rgb = CIANO if ci == 1 else CINZA
        run.bold = (ci == 0)
doc.add_paragraph()
divider()

# ══════════════════════════════════════════════════════════════════
# SECAO 2 — JULIO (Slides 1 e 2)
# ══════════════════════════════════════════════════════════════════
heading1('2. JULIO PIMENTEL — Slides 1 e 2  (Sem demo tecnica)')
body('Apenas fala. Apresenta o grupo, o projeto e a visao geral.')
fala('Boa tarde. Apresentamos o Task Manager, uma API REST de gerenciamento de tarefas com arquitetura de microservicos, desenvolvida para a disciplina de Desenvolvimento de Software para Web.')
body('Apresentar cada integrante e o que cada um vai apresentar. Em seguida passa para o Arthur.')
divider()

# ══════════════════════════════════════════════════════════════════
# SECAO 3 — ARTHUR (Slides 3 e 13)
# ══════════════════════════════════════════════════════════════════
heading1('3. ARTHUR CARVALHAIS — Slides 3 e 13  (Sem demo tecnica)')
body('Explica o diagrama de arquitetura apontando para o slide.')
fala('O sistema e dividido em microservicos. Tudo comeca pelo cliente que manda uma requisicao para o API Gateway na porta 3000. O Gateway e a porta de entrada unica: aplica seguranca, rate limiting, CORS, e encaminha para o servico correto.')
fala('Temos tres servicos — Auth cuida de login e JWT, Task faz o CRUD de tarefas, e User gerencia perfis. Eles se comunicam via HTTP interno numa rede privada Docker chamada task_network.')
fala('Os tres servicos salvam dados no MongoDB, que tem duas colecoes: users e tasks.')
fala('Na parte de monitoramento, o Prometheus coleta metricas de todos os servicos a cada 15 segundos, e o Grafana exibe tudo em dashboard em tempo real.')
divider()

# ══════════════════════════════════════════════════════════════════
# SECAO 4 — GUILHERME (Slides 4 e 5)
# ══════════════════════════════════════════════════════════════════
heading1('4. GUILHERME SOUZA — Slides 4 e 5')

heading2('Slide 4 — Docker: mostrar containers rodando')
body('Abrir terminal e executar:')
code_block(['docker compose ps'])
doc.add_paragraph()
body('Saida esperada — todos devem estar Up:')
code_block([
    'NAME           STATUS          PORTS',
    'api-gateway    Up              0.0.0.0:3000->3000/tcp',
    'auth-service   Up              0.0.0.0:3001->3001/tcp',
    'grafana        Up              0.0.0.0:3004->3000/tcp',
    'mongo          Up (healthy)    0.0.0.0:27017->27017/tcp',
    'prometheus     Up              0.0.0.0:9090->9090/tcp',
    'task-service   Up              0.0.0.0:3002->3002/tcp',
    'user-service   Up              0.0.0.0:3003->3003/tcp',
])
doc.add_paragraph()
fala('Sete containers rodando com um unico comando: docker compose up -d')

heading2('Slide 5 — Banco de Dados: apenas fala')
fala('Usamos MongoDB com duas colecoes: users e tasks. O soft delete funciona com o campo deletedAt — o dado nunca e apagado, apenas marcado. Toda consulta filtra deletedAt null.')
divider()

# ══════════════════════════════════════════════════════════════════
# SECAO 5 — RENAN — DEMO AO VIVO
# ══════════════════════════════════════════════════════════════════
heading1('5. RENAN PRADO — Slides 6 e 7  (DEMO AO VIVO)')
body('Abrir Aba 1: http://localhost:3001/api/auth/docs', color=AZUL_MEDIO)

heading2('PASSO 1 — Registrar usuario')
body('Clicar em: POST /api/auth/register > Try it out')
body('Colar no campo body:')
json_block('''{
  "name": "Apresentacao Turma",
  "email": "demo@apresentacao.com",
  "password": "senha123",
  "role": "admin"
}''')
body('Clicar Execute. Resposta esperada (201):')
json_block('''{
  "message": "Usuario criado com sucesso",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "665abc123...",
    "name": "Apresentacao Turma",
    "role": "admin"
  }
}''')
p = doc.add_paragraph()
run = p.add_run('COPIAR O TOKEN — vai ser usado em todos os proximos passos!')
run.bold = True; run.font.color.rgb = VERMELHO; run.font.size = Pt(10)

heading2('PASSO 2 — Autorizar no Swagger')
bullet('Clicar no botao Authorize (canto superior direito)')
bullet('Colar o token no campo Value')
bullet('Clicar Authorize > Close')
fala('Agora todas as requisicoes vao enviar o token JWT automaticamente.')

heading2('PASSO 3 — Ver dados do usuario logado')
body('Clicar em: GET /api/auth/me > Try it out > Execute')
body('Resposta esperada (200):')
json_block('''{
  "user": {
    "id": "665abc123...",
    "name": "Apresentacao Turma",
    "email": "demo@apresentacao.com",
    "role": "admin"
  }
}''')

heading2('PASSO 4 — Ir para Task Service')
body('Abrir Aba 2: http://localhost:3002/api/tasks/docs', color=AZUL_MEDIO)
body('Clicar Authorize > colar o mesmo token > Authorize > Close')

heading2('PASSO 5 — Criar Tarefa 1')
body('Clicar em: POST /api/tasks > Try it out')
json_block('''{
  "title": "Preparar slides da apresentacao",
  "description": "Finalizar os 13 slides para a disciplina",
  "priority": "high",
  "status": "pending",
  "category": "faculdade",
  "tags": ["apresentacao", "web"]
}''')
p = doc.add_paragraph()
run = p.add_run('COPIAR O _id RETORNADO — ex: 665def456...')
run.bold = True; run.font.color.rgb = VERMELHO; run.font.size = Pt(10)

heading2('PASSO 6 — Criar Tarefa 2')
json_block('''{
  "title": "Subir containers Docker",
  "description": "Garantir que todos os 7 containers estao rodando",
  "priority": "critical",
  "status": "done",
  "category": "infraestrutura",
  "tags": ["docker", "devops"]
}''')

heading2('PASSO 7 — Criar Tarefa 3')
json_block('''{
  "title": "Configurar Prometheus e Grafana",
  "description": "Dashboard com 7 paineis de monitoramento",
  "priority": "medium",
  "status": "in_progress",
  "category": "monitoramento"
}''')

heading2('PASSO 8 — Listar todas as tarefas')
body('Clicar em: GET /api/tasks > Try it out')
bullet('page: 1')
bullet('limit: 10')
body('Clicar Execute. Resposta esperada:')
json_block('''{
  "data": [
    { "title": "Configurar Prometheus e Grafana", "status": "in_progress" },
    { "title": "Subir containers Docker", "status": "done" },
    { "title": "Preparar slides da apresentacao", "status": "pending" }
  ],
  "pagination": { "total": 3, "page": 1, "totalPages": 1 }
}''')
fala('Tres tarefas criadas, paginacao funcionando, total 3.')

heading2('PASSO 9 — Filtrar por prioridade')
body('GET /api/tasks > Try it out > preencher:')
bullet('priority: high')
body('Clicar Execute — deve retornar somente "Preparar slides".')
fala('Filtro por prioridade — retornou apenas as tarefas de prioridade high.')

heading2('PASSO 10 — Buscar por nome')
body('GET /api/tasks/name/{title} > Try it out')
bullet('title: Docker')
body('Clicar Execute — retorna "Subir containers Docker".')
fala('Busca por nome usando regex — nao precisa digitar o titulo completo.')

heading2('PASSO 11 — Buscar por ID')
body('GET /api/tasks/{id} > Try it out')
bullet('id: colar o _id da Tarefa 1')
body('Clicar Execute — retorna os detalhes completos.')

heading2('PASSO 12 — Atualizar status')
body('PATCH /api/tasks/{id}/status > Try it out')
bullet('id: _id da Tarefa 1')
json_block('{ "status": "in_progress" }')
fala('Atualizou so o status sem precisar mandar o objeto inteiro.')

heading2('PASSO 13 — Atualizar tarefa completa')
body('PUT /api/tasks/{id} > Try it out')
bullet('id: _id da Tarefa 1')
json_block('''{
  "title": "Preparar slides da apresentacao",
  "description": "CONCLUIDO — 13 slides prontos e revisados",
  "priority": "high",
  "status": "done",
  "dueDate": "2026-06-15T10:00:00.000Z"
}''')

heading2('PASSO 14 — Soft Delete')
body('DELETE /api/tasks/{id} > Try it out')
bullet('id: _id da Tarefa 3 (Prometheus/Grafana)')
body('Resposta esperada:')
json_block('{ "message": "Tarefa deletada com sucesso (soft delete)" }')
body('Fazer GET /api/tasks novamente — so 2 tarefas aparecem.')
fala('A tarefa sumiu da listagem mas nao foi apagada do banco — o campo deletedAt foi preenchido.')

heading2('PASSO 15 — Restaurar tarefa (admin)')
body('POST /api/tasks/{id}/restore > Try it out')
bullet('id: mesmo _id da tarefa deletada')
body('Fazer GET /api/tasks novamente — as 3 tarefas voltam.')
fala('Restaurada — isso e o soft delete. Dado nunca se perde.')

heading2('PASSO 16 — Listar usuarios (User Service)')
body('Abrir Aba 3: http://localhost:3003/api/users/docs', color=AZUL_MEDIO)
body('Autorizar com o token. GET /api/users > Try it out > page:1, limit:10 > Execute')
fala('User Service lendo da mesma colecao do Auth Service — sem duplicacao de dados.')
divider()

# ══════════════════════════════════════════════════════════════════
# SECAO 6 — LUIS (Slides 8 e 9)
# ══════════════════════════════════════════════════════════════════
heading1('6. LUIS BARBOSA — Slides 8 e 9  (Sem demo tecnica)')
body('Slide 8 — Seguranca: explica JWT, RBAC, bcrypt, Helmet, CORS, Rate Limit, validacao.')
body('Slide 9 — Testes k6: explica cenario de carga e mostra os resultados.')
fala('Rodamos o k6 com 100 usuarios simultaneos durante 2 minutos e meio. Resultado: 1.838 iteracoes, 11.029 requisicoes, 0% de erros, p95 de 31ms — 14 vezes abaixo do limite de 500ms.')
body('Comando para rodar ao vivo se quiser mostrar:')
code_block(['MSYS_NO_PATHCONV=1 docker compose --profile testing run --rm k6 run /scripts/test.js'])
doc.add_paragraph()
divider()

# ══════════════════════════════════════════════════════════════════
# SECAO 7 — CAUA — PROMETHEUS (Slide 10)
# ══════════════════════════════════════════════════════════════════
heading1('7. CAUA MENDONCA — Slides 10, 11 e 12  (DEMO AO VIVO)')

heading2('Slide 10 — Prometheus ao vivo')
body('Abrir Aba 4: http://localhost:9090/targets', color=AZUL_MEDIO)
fala('Quatro targets UP — o Prometheus esta coletando metricas de todos os servicos agora.')

body('Clicar em Graph. Queries para executar:')
queries = [
    ('http_requests_total',              'Total de requisicoes por rota/metodo/status'),
    ('rate(http_requests_total[1m])',     'Taxa de requisicoes por segundo no ultimo minuto'),
    ('nodejs_heap_size_used_bytes',       'Memoria heap de cada servico em bytes'),
    ('rate(process_cpu_seconds_total[1m])', 'CPU por servico'),
    ('up',                               'Status de todos os targets (1=UP, 0=DOWN)'),
]
t2 = doc.add_table(rows=len(queries)+1, cols=2)
t2.style = 'Table Grid'
for i, h in enumerate(['Query PromQL', 'O que mostra']):
    cell = t2.rows[0].cells[i]
    set_cell_bg(cell, '0D1B2A')
    run = cell.paragraphs[0].add_run(h)
    run.bold = True; run.font.size = Pt(10); run.font.color.rgb = BRANCO
for ri, (q, d) in enumerate(queries):
    row = t2.rows[ri+1]
    r1 = row.cells[0].paragraphs[0].add_run(q)
    r1.font.name = 'Courier New'; r1.font.size = Pt(9); r1.font.color.rgb = CIANO
    r2 = row.cells[1].paragraphs[0].add_run(d)
    r2.font.size = Pt(9); r2.font.color.rgb = CINZA
doc.add_paragraph()

heading2('Slide 10 — Grafana ao vivo')
body('Abrir Aba 5: http://localhost:3004/d/task-manager-overview  |  Login: admin / admin123', color=AZUL_MEDIO)

paineis = [
    ('Status dos Servicos',           '4 barras verdes — todos os servicos UP. Se cair, vira vermelho.'),
    ('Taxa de Requisicoes HTTP',       'Requisicoes por segundo em tempo real. Picos sao os testes.'),
    ('Total de Requisicoes',           'Contador acumulado. Fazer uma req no Swagger e mostrar subindo.'),
    ('Memoria Heap Node.js',           'Gateway usa 10 MiB, outros servicos 25-30 MiB (Mongoose carregado).'),
    ('Uso de CPU por Servico',         'Menos de 1% em operacao normal — sistema muito leve.'),
    ('Event Loop Lag',                 'Abaixo de 5ms de media — Node.js nao esta travando.'),
    ('Handles Ativos',                 'Conexoes abertas estaveis — sem vazamento de memoria.'),
]
t3 = doc.add_table(rows=len(paineis)+1, cols=2)
t3.style = 'Table Grid'
for i, h in enumerate(['Painel', 'O que falar']):
    cell = t3.rows[0].cells[i]
    set_cell_bg(cell, '0D1B2A')
    run = cell.paragraphs[0].add_run(h)
    run.bold = True; run.font.size = Pt(10); run.font.color.rgb = BRANCO
for ri, (painel, desc) in enumerate(paineis):
    row = t3.rows[ri+1]
    r1 = row.cells[0].paragraphs[0].add_run(painel)
    r1.font.size = Pt(9); r1.font.color.rgb = CIANO; r1.bold = True
    r2 = row.cells[1].paragraphs[0].add_run(desc)
    r2.font.size = Pt(9); r2.font.color.rgb = CINZA
doc.add_paragraph()

body('Gerar dados ao vivo — voltar no Swagger e fazer 3 GETs rapidamente:')
code_block(['GET /api/tasks', 'GET /api/tasks', 'GET /api/tasks'])
doc.add_paragraph()
fala('Olha o grafico de requisicoes subindo agora — sao os GETs que acabei de fazer.')

heading2('Slide 11 — Deploy: apenas fala')
fala('O deploy e 100% local com Docker Desktop. Um unico comando sobe os 7 containers. O MongoDB usa volume persistente — os dados nao somem mesmo que o container reinicie.')
body('Mostrar Docker Desktop com os 7 containers rodando ou terminal com docker compose ps.')

heading2('Slide 12 — Swagger: mostrar as 3 URLs')
body('Mostrar as 3 abas ja abertas. Expandir um endpoint e mostrar o Schema.')
fala('Cada endpoint mostra quais campos aceita, quais sao obrigatorios, e todos os possiveis codigos de retorno. E o OpenAPI 3.0 gerado automaticamente a partir do codigo.')
divider()

# ══════════════════════════════════════════════════════════════════
# SECAO 8 — ARTHUR (Slide 13)
# ══════════════════════════════════════════════════════════════════
heading1('8. ARTHUR CARVALHAIS — Slide 13  (Conclusao)')
fala('Para fechar, o projeto atingiu 0% de erros sob 100 usuarios simultaneos. A arquitetura de microservicos nos ensinou como separar responsabilidades de verdade. Docker Compose sobe tudo com um comando. E o Prometheus mais Grafana deixaram o sistema completamente observavel em tempo real.')
body('Melhorias futuras:')
bullet('Kafka para comunicacao assincrona entre servicos')
bullet('CI/CD com GitHub Actions')
bullet('Deploy em Kubernetes')
bullet('Cache com Redis')
fala('O projeto esta rodando ao vivo agora. Qualquer duvida, podemos demonstrar qualquer parte na hora.')
divider()

# ══════════════════════════════════════════════════════════════════
# SECAO 9 — ORDEM E TEMPO
# ══════════════════════════════════════════════════════════════════
heading1('9. ORDEM COMPLETA E TEMPO ESTIMADO')
ordem = [
    ('1', 'Julio',     'Slides 1 e 2  —  Capa + Visao Geral',          '~3 min'),
    ('2', 'Arthur',    'Slide 3       —  Arquitetura',                  '~3 min'),
    ('3', 'Guilherme', 'Slides 4 e 5  —  Docker + Banco',               '~4 min'),
    ('4', 'Renan',     'Slides 6 e 7  —  Funcionalidades + Demo',       '~6 min'),
    ('5', 'Luis',      'Slides 8 e 9  —  Seguranca + Testes k6',        '~4 min'),
    ('6', 'Caua',      'Slides 10, 11, 12  —  Prometheus + Grafana + Swagger', '~8 min'),
    ('7', 'Arthur',    'Slide 13      —  Conclusao',                    '~2 min'),
]
t4 = doc.add_table(rows=len(ordem)+1, cols=4)
t4.style = 'Table Grid'
for i, h in enumerate(['#', 'Quem', 'Conteudo', 'Tempo']):
    cell = t4.rows[0].cells[i]
    set_cell_bg(cell, '0D1B2A')
    run = cell.paragraphs[0].add_run(h)
    run.bold = True; run.font.size = Pt(10); run.font.color.rgb = BRANCO
for ri, (n, quem, cont, tempo) in enumerate(ordem):
    row = t4.rows[ri+1]
    for ci, val in enumerate([n, quem, cont, tempo]):
        run = row.cells[ci].paragraphs[0].add_run(val)
        run.font.size = Pt(9.5)
        if ci == 1: run.bold = True; run.font.color.rgb = CIANO
        elif ci == 3: run.font.color.rgb = VERDE; run.bold = True
        else: run.font.color.rgb = CINZA
doc.add_paragraph()
p_total = doc.add_paragraph()
run = p_total.add_run('TOTAL ESTIMADO: ~30 MINUTOS')
run.bold = True; run.font.size = Pt(11); run.font.color.rgb = VERDE
divider()

# ══════════════════════════════════════════════════════════════════
# SECAO 10 — SE ALGO DER ERRADO
# ══════════════════════════════════════════════════════════════════
heading1('10. SE ALGO DER ERRADO')
problemas = [
    ('Container caiu',                    'docker compose up -d'),
    ('Token expirado (erro 401)',          'Registrar novo usuario com email diferente'),
    ('Swagger nao autoriza',              'Clicar Authorize e colar o token sem "Bearer"'),
    ('Grafana sem dados (No data)',        'Mudar periodo para "Last 5 minutes" canto superior direito'),
    ('Targets DOWN no Prometheus',        'docker compose restart prometheus'),
    ('Erro 409 no register (email ja existe)', 'Usar outro email: demo2@teste.com'),
    ('Grafana nao abre',                  'docker compose restart grafana  (aguardar 15s)'),
    ('Tudo travado',                      'docker compose down && docker compose up -d'),
]
t5 = doc.add_table(rows=len(problemas)+1, cols=2)
t5.style = 'Table Grid'
for i, h in enumerate(['Problema', 'Solucao']):
    cell = t5.rows[0].cells[i]
    set_cell_bg(cell, '0D1B2A')
    run = cell.paragraphs[0].add_run(h)
    run.bold = True; run.font.size = Pt(10); run.font.color.rgb = BRANCO
for ri, (prob, sol) in enumerate(problemas):
    row = t5.rows[ri+1]
    r1 = row.cells[0].paragraphs[0].add_run(prob)
    r1.font.size = Pt(9.5); r1.font.color.rgb = VERMELHO; r1.bold = True
    r2 = row.cells[1].paragraphs[0].add_run(sol)
    r2.font.name = 'Courier New'; r2.font.size = Pt(9); r2.font.color.rgb = CINZA
doc.add_paragraph()
divider()

# ══════════════════════════════════════════════════════════════════
# SECAO 11 — URLS E COMANDOS RAPIDOS
# ══════════════════════════════════════════════════════════════════
heading1('11. URLS E COMANDOS RAPIDOS')

heading2('URLs de referencia')
urls = [
    ('API Gateway',         'http://localhost:3000'),
    ('Auth Swagger',        'http://localhost:3001/api/auth/docs'),
    ('Task Swagger',        'http://localhost:3002/api/tasks/docs'),
    ('User Swagger',        'http://localhost:3003/api/users/docs'),
    ('Prometheus',          'http://localhost:9090'),
    ('Prometheus Targets',  'http://localhost:9090/targets'),
    ('Grafana Dashboard',   'http://localhost:3004/d/task-manager-overview'),
    ('Grafana Login',       'admin  /  admin123'),
]
table_2col(urls, header=['Servico', 'URL / Acesso'], col_w=(5, 9))

heading2('Comandos essenciais')
code_block([
    '# Subir tudo',
    'docker compose up -d',
    '',
    '# Ver status',
    'docker compose ps',
    '',
    '# Logs de um servico',
    'docker compose logs auth-service --tail=20',
    '',
    '# Reiniciar um servico',
    'docker compose restart grafana',
    '',
    '# Reiniciar tudo',
    'docker compose down && docker compose up -d',
    '',
    '# Rodar teste de carga k6',
    'MSYS_NO_PATHCONV=1 docker compose --profile testing run --rm k6 run /scripts/test.js',
])
doc.add_paragraph()

# ══════════════════════════════════════════════════════════════════
# SECAO 12 — JSONS PRONTOS PARA COPIAR
# ══════════════════════════════════════════════════════════════════
heading1('12. JSONS PRONTOS PARA COPIAR E COLAR')

heading2('Usuario admin (POST /api/auth/register)')
json_block('''{
  "name": "Apresentacao Turma",
  "email": "demo@apresentacao.com",
  "password": "senha123",
  "role": "admin"
}''')

heading2('Tarefa 1 — prioridade high (POST /api/tasks)')
json_block('''{
  "title": "Preparar slides da apresentacao",
  "description": "Finalizar os 13 slides para a disciplina",
  "priority": "high",
  "status": "pending",
  "category": "faculdade",
  "tags": ["apresentacao", "web"]
}''')

heading2('Tarefa 2 — prioridade critical')
json_block('''{
  "title": "Subir containers Docker",
  "description": "Garantir que todos os 7 containers estao rodando",
  "priority": "critical",
  "status": "done",
  "category": "infraestrutura",
  "tags": ["docker", "devops"]
}''')

heading2('Tarefa 3 — prioridade medium')
json_block('''{
  "title": "Configurar Prometheus e Grafana",
  "description": "Dashboard com 7 paineis de monitoramento",
  "priority": "medium",
  "status": "in_progress",
  "category": "monitoramento"
}''')

heading2('Atualizar status (PATCH /api/tasks/{id}/status)')
json_block('{ "status": "in_progress" }')

heading2('Atualizar tarefa completa (PUT /api/tasks/{id})')
json_block('''{
  "title": "Preparar slides da apresentacao",
  "description": "CONCLUIDO — 13 slides prontos e revisados",
  "priority": "high",
  "status": "done",
  "dueDate": "2026-06-15T10:00:00.000Z"
}''')

# ── Salvar ─────────────────────────────────────────────────────────
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'ROTEIRO_APRESENTACAO.docx')
doc.save(output_path)
print('Salvo em:', output_path)
