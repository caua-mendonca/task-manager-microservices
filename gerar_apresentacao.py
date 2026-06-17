"""
Gerador de apresentação PowerPoint — Task Manager Microservices API
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import os

# ── Paleta de cores ─────────────────────────────────────────────────
C_BG_DARK    = RGBColor(0x0D, 0x1B, 0x2A)   # Azul petróleo escuro
C_BG_MID     = RGBColor(0x11, 0x26, 0x3E)   # Azul médio
C_ACCENT     = RGBColor(0x00, 0xB4, 0xD8)   # Ciano brilhante
C_ACCENT2    = RGBColor(0x48, 0xCA, 0xE4)   # Ciano claro
C_GREEN      = RGBColor(0x06, 0xD6, 0xA0)   # Verde esmeralda
C_YELLOW     = RGBColor(0xFF, 0xD1, 0x66)   # Âmbar
C_WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
C_GRAY       = RGBColor(0x8E, 0xCF, 0xE8)   # Azul acinzentado
C_CARD       = RGBColor(0x16, 0x32, 0x4F)   # Azul card
C_LINE       = RGBColor(0x00, 0xB4, 0xD8)   # Linha decorativa

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H

blank_layout = prs.slide_layouts[6]  # completamente em branco


# ── helpers ─────────────────────────────────────────────────────────

def add_bg(slide, color=C_BG_DARK):
    """Preenche o fundo do slide com a cor especificada."""
    bg = slide.shapes.add_shape(1, 0, 0, SLIDE_W, SLIDE_H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg


def add_rect(slide, x, y, w, h, color, radius=False):
    shape = slide.shapes.add_shape(1, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_text(slide, text, x, y, w, h, size, bold=False, color=C_WHITE,
             align=PP_ALIGN.LEFT, italic=False, font="Calibri"):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font
    return tb


def add_multiline(slide, lines, x, y, w, h, size, color=C_WHITE,
                  bold_first=False, bullet=True, font="Calibri"):
    """Adiciona uma caixa de texto com múltiplas linhas."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        prefix = "  •  " if bullet else ""
        run.text = prefix + line
        run.font.size = Pt(size)
        run.font.bold = (i == 0 and bold_first)
        run.font.color.rgb = color
        run.font.name = font
    return tb


def accent_bar(slide, y_pos=Inches(0.12), w=Inches(2.5)):
    """Barra colorida de topo."""
    bar = slide.shapes.add_shape(1, 0, y_pos, SLIDE_W, Inches(0.07))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_ACCENT
    bar.line.fill.background()


def slide_number(slide, n, total=13):
    add_text(slide, f"{n}/{total}", Inches(12.5), Inches(7.1),
             Inches(0.8), Inches(0.3), 9, color=C_GRAY, align=PP_ALIGN.RIGHT)


def section_badge(slide, label, color=C_ACCENT):
    """Pílula com o nome da seção no canto superior direito."""
    badge = slide.shapes.add_shape(1, Inches(11.2), Inches(0.22),
                                   Inches(1.9), Inches(0.4))
    badge.fill.solid()
    badge.fill.fore_color.rgb = color
    badge.line.fill.background()
    tf = badge.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = label
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = C_BG_DARK
    run.font.name = "Calibri"


def divider(slide, y):
    line = slide.shapes.add_shape(1, Inches(0.5), y, Inches(12.33), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = C_ACCENT
    line.line.fill.background()


def card(slide, x, y, w, h):
    c = slide.shapes.add_shape(1, x, y, w, h)
    c.fill.solid()
    c.fill.fore_color.rgb = C_CARD
    c.line.color.rgb = C_ACCENT
    c.line.width = Pt(0.75)
    return c


def icon_circle(slide, x, y, r, color, text=""):
    c = slide.shapes.add_shape(9, x, y, r, r)  # 9 = oval
    c.fill.solid()
    c.fill.fore_color.rgb = color
    c.line.fill.background()
    if text:
        tf = c.text_frame
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run()
        run.text = text
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = C_WHITE
        run.font.name = "Calibri"
    return c


# ════════════════════════════════════════════════════════════════════
# SLIDE 1 — CAPA
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
add_bg(s)

# Gradiente decorativo (retângulo lateral)
deco = s.shapes.add_shape(1, Inches(9.5), 0, Inches(3.83), SLIDE_H)
deco.fill.solid()
deco.fill.fore_color.rgb = C_BG_MID
deco.line.fill.background()

# Círculos decorativos
icon_circle(s, Inches(10.0), Inches(1.0), Inches(1.4), C_ACCENT)
icon_circle(s, Inches(11.2), Inches(2.8), Inches(0.9), C_GREEN)
icon_circle(s, Inches(10.5), Inches(4.5), Inches(1.1), RGBColor(0x03, 0x60, 0x7C))

add_text(s, "⚙", Inches(10.2), Inches(1.1), Inches(1.0), Inches(1.0),
         32, bold=True, color=C_BG_DARK, align=PP_ALIGN.CENTER)
add_text(s, "🐳", Inches(11.3), Inches(2.9), Inches(0.7), Inches(0.7),
         22, bold=True, color=C_BG_DARK, align=PP_ALIGN.CENTER)
add_text(s, "🗄", Inches(10.6), Inches(4.6), Inches(0.9), Inches(0.7),
         22, bold=True, color=C_BG_DARK, align=PP_ALIGN.CENTER)

# Barra lateral colorida
bar = s.shapes.add_shape(1, Inches(0.4), Inches(2.5), Inches(0.1), Inches(3.2))
bar.fill.solid()
bar.fill.fore_color.rgb = C_ACCENT
bar.line.fill.background()

# Tag disciplina
tag = s.shapes.add_shape(1, Inches(0.6), Inches(1.6), Inches(4.5), Inches(0.45))
tag.fill.solid()
tag.fill.fore_color.rgb = C_ACCENT
tag.line.fill.background()
add_text(s, "Desenvolvimento de Software para Web",
         Inches(0.65), Inches(1.62), Inches(4.4), Inches(0.4),
         11, bold=True, color=C_BG_DARK)

# Título principal
add_text(s, "Task Manager", Inches(0.6), Inches(2.2), Inches(8.5), Inches(1.1),
         52, bold=True, color=C_WHITE, font="Calibri")
add_text(s, "Microservices API", Inches(0.6), Inches(3.15), Inches(8.5), Inches(0.9),
         38, bold=False, color=C_ACCENT, font="Calibri")

divider(s, Inches(4.25))

# Integrantes
add_text(s, "Equipe", Inches(0.6), Inches(4.35), Inches(5.0), Inches(0.4),
         13, bold=True, color=C_GRAY)
add_multiline(s,
    ["Cauã Mendonça", "Arthur Carvalhais", "Guilherme Souza",
     "Julio Pimentel", "Luis Barbosa", "Renan Prado"],
    Inches(0.6), Inches(4.75), Inches(5.0), Inches(1.8),
    13, color=C_WHITE, bullet=False)

# Data
add_text(s, "15 de Junho de 2026", Inches(0.6), Inches(6.7), Inches(4.0), Inches(0.4),
         12, color=C_GRAY)

slide_number(s, 1)


# ════════════════════════════════════════════════════════════════════
# SLIDE 2 — VISÃO GERAL
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
add_bg(s)
accent_bar(s)
section_badge(s, "Julio — Visão Geral", C_ACCENT)

add_text(s, "Visão Geral do Projeto", Inches(0.6), Inches(0.3), Inches(9), Inches(0.65),
         32, bold=True, color=C_WHITE)
divider(s, Inches(1.05))

# Card: Objetivo
card(s, Inches(0.5), Inches(1.2), Inches(3.7), Inches(2.1))
add_text(s, "🎯  Objetivo", Inches(0.65), Inches(1.3), Inches(3.4), Inches(0.45),
         14, bold=True, color=C_ACCENT)
add_multiline(s,
    ["API REST para gerenciamento de tarefas", "Arquitetura de microserviços", "Escalável e orientada a boas práticas"],
    Inches(0.65), Inches(1.75), Inches(3.4), Inches(1.3), 12, bullet=True)

# Card: Problema
card(s, Inches(4.4), Inches(1.2), Inches(3.9), Inches(2.1))
add_text(s, "❓  Problema Resolvido", Inches(4.55), Inches(1.3), Inches(3.6), Inches(0.45),
         14, bold=True, color=C_ACCENT)
add_multiline(s,
    ["Sistemas monolíticos não escalam bem", "Sem separação de responsabilidades", "Difícil manutenção e deploy independente"],
    Inches(4.55), Inches(1.75), Inches(3.6), Inches(1.3), 12, bullet=True)

# Card: Solução
card(s, Inches(8.5), Inches(1.2), Inches(4.3), Inches(2.1))
add_text(s, "✅  Solução", Inches(8.65), Inches(1.3), Inches(4.0), Inches(0.45),
         14, bold=True, color=C_GREEN)
add_multiline(s,
    ["4 serviços independentes + gateway", "Cada serviço com sua responsabilidade", "Deploy via Docker Compose"],
    Inches(8.65), Inches(1.75), Inches(4.0), Inches(1.3), 12, bullet=True)

# Tecnologias
add_text(s, "Stack Tecnológica", Inches(0.6), Inches(3.55), Inches(4), Inches(0.4),
         16, bold=True, color=C_ACCENT)
divider(s, Inches(4.0))

techs = [
    ("Node.js", C_GREEN), ("Express", C_ACCENT), ("MongoDB", C_GREEN),
    ("Docker", C_ACCENT), ("JWT", C_YELLOW), ("Prometheus", C_YELLOW),
    ("Grafana", C_ACCENT2), ("k6", C_GREEN), ("Swagger", C_ACCENT),
]
x = Inches(0.5)
for name, color in techs:
    pill = s.shapes.add_shape(1, x, Inches(4.15), Inches(1.15), Inches(0.42))
    pill.fill.solid()
    pill.fill.fore_color.rgb = color
    pill.line.fill.background()
    add_text(s, name, x + Inches(0.05), Inches(4.18), Inches(1.05), Inches(0.36),
             11, bold=True, color=C_BG_DARK, align=PP_ALIGN.CENTER)
    x += Inches(1.28)

# Fluxo simplificado
add_text(s, "Fluxo de uma requisição", Inches(0.6), Inches(4.75), Inches(6), Inches(0.4),
         14, bold=True, color=C_GRAY)
for i, (label, col) in enumerate([
    ("Cliente", C_ACCENT), ("→", C_WHITE), ("API Gateway :3000", C_ACCENT),
    ("→", C_WHITE), ("Microserviço", C_GREEN), ("→", C_WHITE), ("MongoDB", C_YELLOW)
]):
    xp = Inches(0.5 + i * 1.68)
    if label in ("→",):
        add_text(s, label, xp, Inches(5.15), Inches(0.5), Inches(0.4),
                 18, bold=True, color=C_WHITE)
    else:
        pill = s.shapes.add_shape(1, xp, Inches(5.1), Inches(1.55), Inches(0.42))
        pill.fill.solid()
        pill.fill.fore_color.rgb = col
        pill.line.fill.background()
        add_text(s, label, xp + Inches(0.03), Inches(5.13), Inches(1.5), Inches(0.36),
                 10, bold=True, color=C_BG_DARK, align=PP_ALIGN.CENTER)

slide_number(s, 2)


# ════════════════════════════════════════════════════════════════════
# SLIDE 3 — ARQUITETURA (redesenhado)
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
add_bg(s)
accent_bar(s)
section_badge(s, "Arthur — Arquitetura", C_ACCENT)

add_text(s, "Arquitetura do Sistema", Inches(0.35), Inches(0.25), Inches(9), Inches(0.6),
         28, bold=True, color=C_WHITE)
divider(s, Inches(0.95))

# ── Zona Docker Network (fundo tracejado) ──────────────────────────
docker_zone = s.shapes.add_shape(1, Inches(1.55), Inches(1.05), Inches(11.5), Inches(4.9))
docker_zone.fill.solid()
docker_zone.fill.fore_color.rgb = RGBColor(0x0A, 0x20, 0x35)
docker_zone.line.color.rgb = C_ACCENT
docker_zone.line.width = Pt(1.2)

docker_label_bg = s.shapes.add_shape(1, Inches(1.6), Inches(1.05), Inches(2.1), Inches(0.32))
docker_label_bg.fill.solid()
docker_label_bg.fill.fore_color.rgb = C_ACCENT
docker_label_bg.line.fill.background()
add_text(s, "  Docker Network: task_network",
         Inches(1.62), Inches(1.06), Inches(2.05), Inches(0.28),
         8, bold=True, color=C_BG_DARK)

# ── COLUNA 1: CLIENTE (fora da rede) ──────────────────────────────
cli_bg = s.shapes.add_shape(1, Inches(0.1), Inches(1.05), Inches(1.35), Inches(4.9))
cli_bg.fill.solid()
cli_bg.fill.fore_color.rgb = RGBColor(0x0D, 0x22, 0x38)
cli_bg.line.color.rgb = RGBColor(0x33, 0x55, 0x77)
cli_bg.line.width = Pt(0.75)

add_text(s, "CLIENTE", Inches(0.12), Inches(1.08), Inches(1.28), Inches(0.28),
         7, bold=True, color=RGBColor(0x55,0x88,0xAA), align=PP_ALIGN.CENTER)

cli_box = s.shapes.add_shape(1, Inches(0.15), Inches(2.3), Inches(1.25), Inches(1.5))
cli_box.fill.solid()
cli_box.fill.fore_color.rgb = RGBColor(0x0D, 0x2E, 0x4A)
cli_box.line.color.rgb = RGBColor(0x44,0x77,0x99)
cli_box.line.width = Pt(1.0)
add_text(s, "Browser\n/ App\n/ Mobile", Inches(0.17), Inches(2.38), Inches(1.2), Inches(0.7),
         9, color=C_GRAY, align=PP_ALIGN.CENTER)
add_text(s, "HTTPS\n:3000", Inches(0.17), Inches(3.1), Inches(1.2), Inches(0.55),
         8, bold=True, color=RGBColor(0x77,0xBB,0xDD), align=PP_ALIGN.CENTER, italic=True)

# ── SETA 1: Cliente → Gateway ─────────────────────────────────────
arr1 = s.shapes.add_shape(1, Inches(1.42), Inches(2.94), Inches(0.22), Inches(0.08))
arr1.fill.solid(); arr1.fill.fore_color.rgb = C_ACCENT; arr1.line.fill.background()
add_text(s, "▶", Inches(1.45), Inches(2.78), Inches(0.25), Inches(0.35),
         14, bold=True, color=C_ACCENT, align=PP_ALIGN.CENTER)

# ── COLUNA 2: API GATEWAY ─────────────────────────────────────────
gw_zone_bg = s.shapes.add_shape(1, Inches(1.65), Inches(1.42), Inches(2.4), Inches(4.1))
gw_zone_bg.fill.solid()
gw_zone_bg.fill.fore_color.rgb = RGBColor(0x0C, 0x28, 0x42)
gw_zone_bg.line.color.rgb = C_ACCENT
gw_zone_bg.line.width = Pt(1.5)

add_text(s, "API GATEWAY", Inches(1.72), Inches(1.48), Inches(2.2), Inches(0.32),
         11, bold=True, color=C_ACCENT, align=PP_ALIGN.CENTER)
add_text(s, "porta  :3000", Inches(1.72), Inches(1.78), Inches(2.2), Inches(0.28),
         9, color=C_ACCENT2, align=PP_ALIGN.CENTER, italic=True)

# Separador
sep = s.shapes.add_shape(1, Inches(1.75), Inches(2.08), Inches(2.2), Inches(0.02))
sep.fill.solid(); sep.fill.fore_color.rgb = C_ACCENT; sep.line.fill.background()

gw_items = [
    ("Rate Limiting", "20.000 req / 15 min / IP"),
    ("CORS", "controla origens permitidas"),
    ("Helmet", "headers de segurança HTTP"),
    ("Proxy Reverso", "encaminha para o servico certo"),
    ("JWT pass-through", "nao valida, apenas repassa"),
    ("Prometheus", "expoe /metrics proprias"),
    ("Health Check", "GET /health sempre disponivel"),
]
for i, (title, desc) in enumerate(gw_items):
    y_item = Inches(2.15 + i * 0.47)
    dot = s.shapes.add_shape(9, Inches(1.8), y_item + Inches(0.08), Inches(0.14), Inches(0.14))
    dot.fill.solid(); dot.fill.fore_color.rgb = C_ACCENT; dot.line.fill.background()
    add_text(s, title, Inches(2.0), y_item, Inches(0.95), Inches(0.28),
             8.5, bold=True, color=C_WHITE)
    add_text(s, desc, Inches(2.0), y_item + Inches(0.22), Inches(1.9), Inches(0.22),
             7.5, color=C_GRAY, italic=True)

# ── SETA 2: Gateway → Serviços ────────────────────────────────────
for y_arr in [Inches(2.15), Inches(3.35), Inches(4.55)]:
    arr = s.shapes.add_shape(1, Inches(4.07), y_arr + Inches(0.3), Inches(0.55), Inches(0.07))
    arr.fill.solid(); arr.fill.fore_color.rgb = C_ACCENT2; arr.line.fill.background()
    add_text(s, "▶", Inches(4.45), y_arr + Inches(0.12), Inches(0.22), Inches(0.32),
             11, bold=True, color=C_ACCENT2, align=PP_ALIGN.CENTER)

add_text(s, "HTTP REST\nInterno", Inches(4.08), Inches(3.5), Inches(0.65), Inches(0.55),
         7, color=C_ACCENT2, italic=True, align=PP_ALIGN.CENTER)

# ── COLUNA 3: MICROSERVIÇOS ───────────────────────────────────────
services = [
    (
        "AUTH SERVICE",  ":3001",  C_ACCENT,
        [("POST /register", "cria usuario + hash bcrypt"),
         ("POST /login", "valida senha, gera JWT HS256"),
         ("GET /me", "dados do usuario autenticado"),
         ("POST /refresh", "renova token JWT (7 dias)"),
         ("Colecao MongoDB:", "users")],
    ),
    (
        "TASK SERVICE",  ":3002",  C_GREEN,
        [("GET /tasks", "lista c/ filtros + paginacao"),
         ("POST /tasks", "cria tarefa (createdBy = JWT id)"),
         ("PUT/PATCH /tasks/:id", "atualiza tarefa ou status"),
         ("DELETE /tasks/:id", "soft delete (deletedAt)"),
         ("Colecao MongoDB:", "tasks")],
    ),
    (
        "USER SERVICE",  ":3003",  C_YELLOW,
        [("GET /users", "lista usuarios (admin only)"),
         ("GET /users/:id", "busca perfil por ID"),
         ("PUT /users/:id", "atualiza nome, bio, avatar"),
         ("DELETE /users/:id", "soft delete (admin only)"),
         ("Colecao MongoDB:", "users  (SHARED c/ auth)")],
    ),
]

for idx, (svc_name, port, col, items) in enumerate(services):
    y_svc = Inches(1.42 + idx * 1.55)
    svc_bg = s.shapes.add_shape(1, Inches(4.7), y_svc, Inches(4.1), Inches(1.38))
    svc_bg.fill.solid()
    svc_bg.fill.fore_color.rgb = C_CARD
    svc_bg.line.color.rgb = col
    svc_bg.line.width = Pt(1.5)

    # Header colorido
    hdr = s.shapes.add_shape(1, Inches(4.7), y_svc, Inches(4.1), Inches(0.32))
    hdr.fill.solid(); hdr.fill.fore_color.rgb = col; hdr.line.fill.background()
    add_text(s, svc_name + "   " + port, Inches(4.75), y_svc + Inches(0.04),
             Inches(3.9), Inches(0.26), 9.5, bold=True, color=C_BG_DARK)

    # Itens de endpoint
    for j, (ep, desc) in enumerate(items):
        y_ep = y_svc + Inches(0.38 + j * 0.195)
        is_last = (j == len(items) - 1)
        ep_col = col if is_last else C_ACCENT2
        desc_col = col if is_last else C_GRAY
        add_text(s, ep, Inches(4.78), y_ep, Inches(1.85), Inches(0.19),
                 7.5, bold=True, color=ep_col, font="Courier New")
        add_text(s, desc, Inches(6.65), y_ep, Inches(2.1), Inches(0.19),
                 7.5, color=desc_col, italic=is_last)

# ── SETA 3: Serviços → MongoDB ───────────────────────────────────
for y_arr in [Inches(2.0), Inches(3.2), Inches(4.4)]:
    arr = s.shapes.add_shape(1, Inches(8.82), y_arr + Inches(0.35), Inches(0.4), Inches(0.06))
    arr.fill.solid(); arr.fill.fore_color.rgb = C_YELLOW; arr.line.fill.background()
    add_text(s, "▶", Inches(9.1), y_arr + Inches(0.18), Inches(0.2), Inches(0.3),
             10, bold=True, color=C_YELLOW, align=PP_ALIGN.CENTER)

add_text(s, "Mongoose\nODM", Inches(8.83), Inches(3.35), Inches(0.55), Inches(0.5),
         7, color=C_YELLOW, italic=True, align=PP_ALIGN.CENTER)

# ── COLUNA 4: MONGODB ─────────────────────────────────────────────
db_bg = s.shapes.add_shape(1, Inches(9.35), Inches(1.42), Inches(1.85), Inches(4.1))
db_bg.fill.solid()
db_bg.fill.fore_color.rgb = RGBColor(0x14, 0x2A, 0x1A)
db_bg.line.color.rgb = C_YELLOW
db_bg.line.width = Pt(1.5)

add_text(s, "MongoDB", Inches(9.37), Inches(1.5), Inches(1.8), Inches(0.3),
         11, bold=True, color=C_YELLOW, align=PP_ALIGN.CENTER)
add_text(s, ":27017", Inches(9.37), Inches(1.82), Inches(1.8), Inches(0.25),
         8.5, color=C_GRAY, align=PP_ALIGN.CENTER, italic=True)
add_text(s, "DB: taskmanager", Inches(9.4), Inches(2.1), Inches(1.75), Inches(0.25),
         8, color=C_GRAY, align=PP_ALIGN.CENTER)

sep2 = s.shapes.add_shape(1, Inches(9.45), Inches(2.38), Inches(1.6), Inches(0.02))
sep2.fill.solid(); sep2.fill.fore_color.rgb = C_YELLOW; sep2.line.fill.background()

# Coleções
cols_db = [
    ("users", ["name, email, password", "role, isActive, deletedAt", "auth + user service"], C_ACCENT),
    ("tasks", ["title, status, priority", "createdBy, deletedAt", "task service"], C_GREEN),
]
for i, (col_name, fields, color) in enumerate(cols_db):
    y_col = Inches(2.45 + i * 1.55)
    col_hdr = s.shapes.add_shape(1, Inches(9.4), y_col, Inches(1.7), Inches(0.28))
    col_hdr.fill.solid(); col_hdr.fill.fore_color.rgb = color; col_hdr.line.fill.background()
    add_text(s, "col: " + col_name, Inches(9.45), y_col + Inches(0.04),
             Inches(1.6), Inches(0.22), 8.5, bold=True, color=C_BG_DARK, font="Courier New")
    for j, field in enumerate(fields):
        add_text(s, field, Inches(9.43), y_col + Inches(0.32 + j * 0.3),
                 Inches(1.72), Inches(0.28), 7.5, color=C_GRAY if j < 2 else color,
                 italic=(j == 2))

# Volume persistente
vol = s.shapes.add_shape(1, Inches(9.4), Inches(5.55), Inches(1.7), Inches(0.68))
vol.fill.solid(); vol.fill.fore_color.rgb = RGBColor(0x10, 0x22, 0x10); vol.line.color.rgb = C_GREEN; vol.line.width = Pt(0.75)
add_text(s, "Volume", Inches(9.45), Inches(5.59), Inches(1.6), Inches(0.22),
         8, bold=True, color=C_GREEN, align=PP_ALIGN.CENTER)
add_text(s, "mongo_data\n(persistente)", Inches(9.45), Inches(5.8), Inches(1.6), Inches(0.38),
         7.5, color=C_GRAY, align=PP_ALIGN.CENTER, italic=True)

# ── ZONA MONITORAMENTO ─────────────────────────────────────────────
mon_zone = s.shapes.add_shape(1, Inches(0.1), Inches(6.1), Inches(13.1), Inches(1.12))
mon_zone.fill.solid()
mon_zone.fill.fore_color.rgb = RGBColor(0x10, 0x1E, 0x10)
mon_zone.line.color.rgb = C_GREEN
mon_zone.line.width = Pt(0.75)

add_text(s, "MONITORAMENTO", Inches(0.18), Inches(6.13), Inches(1.6), Inches(0.22),
         7.5, bold=True, color=C_GREEN)

mon_items = [
    ("Prometheus  :9090", "Scrape /metrics de todos os 4 servicos a cada 15s", C_YELLOW),
    ("Grafana  :3004", "Dashboard auto-provisionado — 7 paineis em tempo real", RGBColor(0xF7,0x93,0x1E)),
    ("k6  (container)", "Load test — 100 VUs, 0% erros, p95=31ms", C_GREEN),
]
for i, (name, desc, color) in enumerate(mon_items):
    xm = Inches(1.75 + i * 3.75)
    mb = s.shapes.add_shape(1, xm, Inches(6.12), Inches(3.55), Inches(1.0))
    mb.fill.solid(); mb.fill.fore_color.rgb = C_CARD; mb.line.color.rgb = color; mb.line.width = Pt(0.75)
    add_text(s, name, xm + Inches(0.12), Inches(6.2), Inches(3.3), Inches(0.3),
             10, bold=True, color=color)
    add_text(s, desc, xm + Inches(0.12), Inches(6.52), Inches(3.3), Inches(0.5),
             8.5, color=C_GRAY, italic=True)

# Seta Prometheus ← /metrics
add_text(s, "◄── scrape /metrics", Inches(1.77), Inches(5.72), Inches(2.5), Inches(0.3),
         8, color=C_YELLOW, italic=True)

slide_number(s, 3)


# ════════════════════════════════════════════════════════════════════
# SLIDE 4 — DOCKER
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
add_bg(s)
accent_bar(s)
section_badge(s, "Guilherme — Docker", RGBColor(0x00, 0x96, 0xC7))

add_text(s, "Containerização com Docker", Inches(0.6), Inches(0.3), Inches(9), Inches(0.65),
         32, bold=True, color=C_WHITE)
divider(s, Inches(1.05))

# Containers grid
containers = [
    ("mongo", ":27017", "Banco de dados\nMongoDB 7.0", C_GREEN),
    ("api-gateway", ":3000", "Proxy reverso\nRate Limit / CORS", C_ACCENT),
    ("auth-service", ":3001", "Autenticação\nJWT + Bcrypt", C_ACCENT2),
    ("task-service", ":3002", "CRUD de tarefas\nSoft Delete", C_YELLOW),
    ("user-service", ":3003", "Perfis de usuário\nAdmin / User", C_YELLOW),
    ("prometheus", ":9090", "Métricas\nScrape 15s", RGBColor(0xFF, 0x6B, 0x35)),
    ("grafana", ":3004", "Dashboards\n7 painéis", RGBColor(0xF7, 0x93, 0x1E)),
    ("k6", "testing", "Load Test\n100 VUs", C_GREEN),
]
cols = 4
for idx, (name, port, desc, color) in enumerate(containers):
    col = idx % cols
    row = idx // cols
    cx = Inches(0.4 + col * 3.2)
    cy = Inches(1.25 + row * 2.1)
    c = card(s, cx, cy, Inches(3.0), Inches(1.8))
    add_text(s, name, cx + Inches(0.15), cy + Inches(0.12), Inches(2.7), Inches(0.45),
             13, bold=True, color=color)
    add_text(s, port, cx + Inches(0.15), cy + Inches(0.55), Inches(2.7), Inches(0.3),
             10, color=C_GRAY)
    add_text(s, desc, cx + Inches(0.15), cy + Inches(0.88), Inches(2.7), Inches(0.7),
             10, color=C_WHITE)

# Comandos
add_text(s, "Comandos essenciais:", Inches(0.6), Inches(5.6), Inches(8), Inches(0.35),
         13, bold=True, color=C_ACCENT)
code_bg = card(s, Inches(0.5), Inches(6.0), Inches(12.3), Inches(1.2))
add_multiline(s,
    ["docker compose up -d   # sobe todos os serviços",
     "docker compose ps       # verifica status",
     "docker compose --profile testing run --rm k6 run /scripts/test.js"],
    Inches(0.65), Inches(6.05), Inches(12.0), Inches(1.1),
    10, color=C_ACCENT2, bullet=False, font="Courier New")

slide_number(s, 4)


# ════════════════════════════════════════════════════════════════════
# SLIDE 5 — BANCO DE DADOS
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
add_bg(s)
accent_bar(s)
section_badge(s, "Guilherme — Banco de Dados", C_GREEN)

add_text(s, "Banco de Dados — MongoDB", Inches(0.6), Inches(0.3), Inches(9), Inches(0.65),
         32, bold=True, color=C_WHITE)
divider(s, Inches(1.05))

# Coleção users
add_text(s, "Coleção  users", Inches(0.5), Inches(1.2), Inches(5.9), Inches(0.45),
         16, bold=True, color=C_ACCENT)
card(s, Inches(0.5), Inches(1.7), Inches(5.9), Inches(3.2))
fields_users = [
    ("name", "String", "required, min 2 chars"),
    ("email", "String", "unique, lowercase, regex"),
    ("password", "String", "bcrypt, select: false"),
    ("role", "String", "enum: admin | user"),
    ("isActive", "Boolean", "default: true"),
    ("deletedAt", "Date", "null = ativo  (soft delete)"),
    ("createdAt / updatedAt", "Date", "timestamps automáticos"),
]
for i, (field, tipo, desc) in enumerate(fields_users):
    y = Inches(1.8 + i * 0.39)
    add_text(s, field, Inches(0.65), y, Inches(2.2), Inches(0.36),
             10, bold=True, color=C_ACCENT2, font="Courier New")
    add_text(s, tipo, Inches(2.9), y, Inches(1.1), Inches(0.36),
             10, color=C_YELLOW)
    add_text(s, desc, Inches(4.05), y, Inches(2.2), Inches(0.36),
             9, color=C_GRAY, italic=True)

# Coleção tasks
add_text(s, "Coleção  tasks", Inches(6.6), Inches(1.2), Inches(6.0), Inches(0.45),
         16, bold=True, color=C_GREEN)
card(s, Inches(6.6), Inches(1.7), Inches(6.3), Inches(3.2))
fields_tasks = [
    ("title", "String", "required, 3-100 chars"),
    ("description", "String", "max 1000 chars"),
    ("status", "String", "pending|in_progress|done|cancelled"),
    ("priority", "String", "low|medium|high|critical"),
    ("category", "String", "default: general"),
    ("createdBy", "String", "ID do usuário dono"),
    ("dueDate / tags", "Date/[]", "prazo e etiquetas"),
    ("deletedAt", "Date", "soft delete (null = ativo)"),
]
for i, (field, tipo, desc) in enumerate(fields_tasks):
    y = Inches(1.8 + i * 0.39)
    add_text(s, field, Inches(6.75), y, Inches(1.9), Inches(0.36),
             10, bold=True, color=C_ACCENT2, font="Courier New")
    add_text(s, tipo, Inches(8.7), y, Inches(1.3), Inches(0.36),
             10, color=C_YELLOW)
    add_text(s, desc, Inches(10.05), y, Inches(2.7), Inches(0.36),
             9, color=C_GRAY, italic=True)

# Índices e estratégias
add_text(s, "Estratégias de Consulta", Inches(0.5), Inches(5.1), Inches(5), Inches(0.4),
         14, bold=True, color=C_ACCENT)
divider(s, Inches(5.55))
add_multiline(s,
    ["Paginação: page + limit (skip/limit no MongoDB)",
     "Filtros: status, priority, category, assignedTo, search",
     "Text Search: índice em title + description",
     "Soft Delete: todas as queries filtram  { deletedAt: null }",
     "Índices: status, priority, createdBy, deletedAt (performance)"],
    Inches(0.5), Inches(5.65), Inches(12.3), Inches(1.7), 11, bullet=True)

slide_number(s, 5)


# ════════════════════════════════════════════════════════════════════
# SLIDE 6 — FUNCIONALIDADES
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
add_bg(s)
accent_bar(s)
section_badge(s, "Renan — Funcionalidades", C_YELLOW)

add_text(s, "Funcionalidades da API", Inches(0.6), Inches(0.3), Inches(9), Inches(0.65),
         32, bold=True, color=C_WHITE)
divider(s, Inches(1.05))

# Tabela de endpoints
headers = ["Método", "Rota", "Auth", "Descrição"]
col_widths = [Inches(0.9), Inches(3.2), Inches(0.9), Inches(4.0)]
col_starts = [Inches(0.4), Inches(1.35), Inches(4.6), Inches(5.55)]

# Header row
header_bg = card(s, Inches(0.4), Inches(1.2), Inches(9.55), Inches(0.42))
header_bg.fill.fore_color.rgb = C_ACCENT
for i, (h, cx, cw) in enumerate(zip(headers, col_starts, col_widths)):
    add_text(s, h, cx, Inches(1.25), cw, Inches(0.35),
             11, bold=True, color=C_BG_DARK)

rows = [
    ("POST",   "/api/auth/register",      "—",     "Registrar usuário — retorna JWT"),
    ("POST",   "/api/auth/login",         "—",     "Login — retorna JWT"),
    ("GET",    "/api/tasks",              "JWT",   "Listar tarefas (filtros + paginação)"),
    ("POST",   "/api/tasks",              "JWT",   "Criar tarefa"),
    ("GET",    "/api/tasks/:id",          "JWT",   "Buscar por ID"),
    ("GET",    "/api/tasks/name/:title",  "JWT",   "Buscar por nome (regex)"),
    ("PUT",    "/api/tasks/:id",          "JWT",   "Atualizar tarefa completa"),
    ("PATCH",  "/api/tasks/:id/status",   "JWT",   "Atualizar apenas status"),
    ("DELETE", "/api/tasks/:id",          "JWT",   "Soft delete"),
    ("DELETE", "/api/tasks/:id/hard",     "Admin", "Hard delete permanente"),
    ("POST",   "/api/tasks/:id/restore",  "Admin", "Restaurar tarefa deletada"),
]
method_colors = {
    "GET": RGBColor(0x06, 0xD6, 0xA0),
    "POST": C_ACCENT,
    "PUT": C_YELLOW,
    "PATCH": RGBColor(0xFF, 0xA5, 0x00),
    "DELETE": RGBColor(0xFF, 0x5C, 0x5C),
}
for idx, (method, route, auth, desc) in enumerate(rows):
    y = Inches(1.7 + idx * 0.44)
    if idx % 2 == 0:
        row_bg = s.shapes.add_shape(1, Inches(0.4), y, Inches(9.55), Inches(0.42))
        row_bg.fill.solid()
        row_bg.fill.fore_color.rgb = C_CARD
        row_bg.line.fill.background()

    mc = method_colors.get(method, C_WHITE)
    add_text(s, method, col_starts[0], y + Inches(0.04), col_widths[0], Inches(0.35),
             9, bold=True, color=mc, font="Courier New")
    add_text(s, route, col_starts[1], y + Inches(0.04), col_widths[1], Inches(0.35),
             9, color=C_ACCENT2, font="Courier New")
    add_text(s, auth, col_starts[2], y + Inches(0.04), col_widths[2], Inches(0.35),
             9, color=C_GRAY)
    add_text(s, desc, col_starts[3], y + Inches(0.04), col_widths[3], Inches(0.35),
             9, color=C_WHITE)

# Features destaque (lado direito)
add_text(s, "Recursos Especiais", Inches(10.1), Inches(1.2), Inches(3.0), Inches(0.4),
         13, bold=True, color=C_ACCENT)
features = [
    ("🗑", "Soft Delete", "deletedAt field"),
    ("🔍", "Full-text Search", "índice MongoDB"),
    ("📄", "Paginação", "page + limit"),
    ("↕", "Ordenação", "sortBy + order"),
    ("🔖", "Filtros", "5 parâmetros"),
    ("♻", "Restore", "apenas admin"),
]
for i, (icon, title, sub) in enumerate(features):
    yf = Inches(1.75 + i * 0.85)
    fc = card(s, Inches(10.1), yf, Inches(3.0), Inches(0.72))
    add_text(s, icon + "  " + title, Inches(10.2), yf + Inches(0.06), Inches(2.8), Inches(0.35),
             11, bold=True, color=C_ACCENT)
    add_text(s, sub, Inches(10.2), yf + Inches(0.38), Inches(2.8), Inches(0.28),
             9, color=C_GRAY, italic=True)

slide_number(s, 6)


# ════════════════════════════════════════════════════════════════════
# SLIDE 7 — DEMONSTRAÇÃO DA API
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
add_bg(s)
accent_bar(s)
section_badge(s, "Renan — Demo", C_YELLOW)

add_text(s, "Demonstração da API", Inches(0.6), Inches(0.3), Inches(9), Inches(0.65),
         32, bold=True, color=C_WHITE)
divider(s, Inches(1.05))

# Passo 1 — Registro
add_text(s, "1  Registrar usuário", Inches(0.5), Inches(1.15), Inches(5.9), Inches(0.4),
         14, bold=True, color=C_ACCENT)
code1 = card(s, Inches(0.5), Inches(1.6), Inches(5.9), Inches(1.4))
add_multiline(s,
    ['POST /api/auth/register',
     '{ "name": "João", "email": "joao@test.com", "password": "senha123" }',
     '→ 201  { "token": "eyJhbGci..." }'],
    Inches(0.65), Inches(1.65), Inches(5.6), Inches(1.3),
    9.5, color=C_ACCENT2, bullet=False, font="Courier New")

# Passo 2 — Criar tarefa
add_text(s, "2  Criar tarefa", Inches(0.5), Inches(3.15), Inches(5.9), Inches(0.4),
         14, bold=True, color=C_GREEN)
code2 = card(s, Inches(0.5), Inches(3.6), Inches(5.9), Inches(1.5))
add_multiline(s,
    ['POST /api/tasks   Authorization: Bearer <token>',
     '{ "title": "Implementar API", "priority": "high",',
     '  "status": "pending", "dueDate": "2026-06-15" }',
     '→ 201  { "data": { "_id": "...", "title": "..." } }'],
    Inches(0.65), Inches(3.65), Inches(5.6), Inches(1.4),
    9.5, color=C_ACCENT2, bullet=False, font="Courier New")

# Passo 3 — Listar com filtros
add_text(s, "3  Listar tarefas com filtros", Inches(0.5), Inches(5.25), Inches(5.9), Inches(0.4),
         14, bold=True, color=C_YELLOW)
code3 = card(s, Inches(0.5), Inches(5.7), Inches(5.9), Inches(1.4))
add_multiline(s,
    ['GET /api/tasks?status=pending&priority=high&page=1&limit=10',
     '→ 200  { "data": [...], "pagination": { "total": 5, "page": 1 } }'],
    Inches(0.65), Inches(5.75), Inches(5.6), Inches(1.3),
    9.5, color=C_ACCENT2, bullet=False, font="Courier New")

# Lado direito — Fluxo visual
add_text(s, "Fluxo de Demonstração", Inches(6.6), Inches(1.15), Inches(6.3), Inches(0.4),
         14, bold=True, color=C_ACCENT)
steps = [
    ("1", "Registrar usuário via POST /register", C_ACCENT),
    ("2", "Fazer login via POST /login → obter JWT", C_ACCENT2),
    ("3", "Usar JWT no header Authorization: Bearer ...", C_YELLOW),
    ("4", "Criar tarefas com POST /tasks", C_GREEN),
    ("5", "Listar, filtrar e paginar com GET /tasks", C_GREEN),
    ("6", "Atualizar status: PATCH /tasks/:id/status", C_YELLOW),
    ("7", "Soft delete: DELETE /tasks/:id", RGBColor(0xFF,0x5C,0x5C)),
    ("8", "(admin) Restaurar: POST /tasks/:id/restore", C_GRAY),
]
for i, (num, text, col) in enumerate(steps):
    y_s = Inches(1.65 + i * 0.66)
    circle = s.shapes.add_shape(9, Inches(6.6), y_s, Inches(0.42), Inches(0.42))
    circle.fill.solid()
    circle.fill.fore_color.rgb = col
    circle.line.fill.background()
    add_text(s, num, Inches(6.6), y_s + Inches(0.02), Inches(0.42), Inches(0.38),
             11, bold=True, color=C_BG_DARK, align=PP_ALIGN.CENTER)
    add_text(s, text, Inches(7.15), y_s + Inches(0.04), Inches(5.7), Inches(0.36),
             10, color=C_WHITE)

slide_number(s, 7)


# ════════════════════════════════════════════════════════════════════
# SLIDE 8 — SEGURANÇA
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
add_bg(s)
accent_bar(s)
section_badge(s, "Luis — Segurança", RGBColor(0xFF,0x5C,0x5C))

add_text(s, "Segurança", Inches(0.6), Inches(0.3), Inches(9), Inches(0.65),
         32, bold=True, color=C_WHITE)
divider(s, Inches(1.05))

sec_items = [
    ("🔐", "Autenticação JWT",
     ["Token assinado com HS256", "Payload: { id, email, role, name }", "Expiração: 7 dias configurável"],
     C_ACCENT),
    ("👤", "Perfis RBAC",
     ["admin: acessa todos os recursos", "user: acessa apenas os próprios dados", "Verificação em cada middleware"],
     C_GREEN),
    ("✅", "Validação de Dados",
     ["express-validator em todos os inputs", "Erros retornados com status 400", "Campos obrigatórios e formatos"],
     C_YELLOW),
    ("🛡", "Proteções HTTP",
     ["Helmet: headers de segurança (XSS, CSP)", "CORS configurado por origin", "Rate Limit: 20k req/15min por IP"],
     RGBColor(0xFF,0x5C,0x5C)),
    ("🔒", "Senhas",
     ["bcrypt com salt 12 rounds", "Campo password: select: false", "Nunca retornado nas queries"],
     C_ACCENT2),
    ("🚫", "Soft Delete",
     ["Dados nunca apagados fisicamente", "deletedAt filtra registros inativos", "Hard delete restrito a admin"],
     C_GRAY),
]
cols = 3
for idx, (icon, title, pts, color) in enumerate(sec_items):
    col = idx % cols
    row = idx // cols
    cx = Inches(0.4 + col * 4.3)
    cy = Inches(1.25 + row * 2.65)
    c = card(s, cx, cy, Inches(4.1), Inches(2.4))
    add_text(s, icon + "  " + title, cx + Inches(0.15), cy + Inches(0.12),
             Inches(3.8), Inches(0.45), 13, bold=True, color=color)
    add_multiline(s, pts, cx + Inches(0.15), cy + Inches(0.6),
                  Inches(3.8), Inches(1.65), 10.5, bullet=True)

slide_number(s, 8)


# ════════════════════════════════════════════════════════════════════
# SLIDE 9 — TESTES
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
add_bg(s)
accent_bar(s)
section_badge(s, "Luis — Testes", C_GREEN)

add_text(s, "Testes de Carga com k6", Inches(0.6), Inches(0.3), Inches(9), Inches(0.65),
         32, bold=True, color=C_WHITE)
divider(s, Inches(1.05))

# Resultados destaque
results = [
    ("1.838", "Iterações\ncompletas", C_GREEN),
    ("11.029", "Requisições\ntotais", C_ACCENT),
    ("0%", "Taxa de\nerros", C_GREEN),
    ("10,66ms", "Duração\nmédia", C_ACCENT),
    ("31,02ms", "p95\nlatência", C_YELLOW),
    ("100", "VUs\nmáximos", C_ACCENT2),
]
for i, (val, label, color) in enumerate(results):
    cx = Inches(0.4 + i * 2.15)
    c = card(s, cx, Inches(1.2), Inches(2.0), Inches(1.5))
    add_text(s, val, cx, Inches(1.25), Inches(2.0), Inches(0.75),
             26, bold=True, color=color, align=PP_ALIGN.CENTER)
    add_text(s, label, cx, Inches(2.0), Inches(2.0), Inches(0.6),
             10, color=C_GRAY, align=PP_ALIGN.CENTER)

# Cenário de carga
add_text(s, "Cenário de Carga (Staged VUs)", Inches(0.5), Inches(2.95), Inches(7), Inches(0.4),
         14, bold=True, color=C_ACCENT)
stages = [
    ("0→10 VUs", "30s", "Ramp-up suave", C_GREEN),
    ("10→50 VUs", "1min", "Carga normal", C_ACCENT),
    ("50→100 VUs", "30s", "Pico máximo", C_YELLOW),
    ("100→0 VUs", "30s", "Ramp-down", C_GRAY),
]
for i, (vus, dur, desc, col) in enumerate(stages):
    cx = Inches(0.4 + i * 3.15)
    c = card(s, cx, Inches(3.45), Inches(3.0), Inches(1.1))
    add_text(s, vus, cx + Inches(0.1), Inches(3.52), Inches(2.8), Inches(0.42),
             14, bold=True, color=col)
    add_text(s, dur + "  —  " + desc, cx + Inches(0.1), Inches(3.95),
             Inches(2.8), Inches(0.35), 9.5, color=C_GRAY)

# Thresholds
add_text(s, "Thresholds definidos:", Inches(0.5), Inches(4.75), Inches(5), Inches(0.4),
         13, bold=True, color=C_ACCENT)
add_multiline(s,
    ["http_req_duration  p(95) < 500ms   ✅  p95 atingido: 31ms  (14× abaixo do limite)",
     "errors rate < 10%                  ✅  taxa de erros: 0%"],
    Inches(0.5), Inches(5.2), Inches(12.3), Inches(0.9),
    11, color=C_GREEN, bullet=True)

# Fluxo do teste
add_text(s, "Cada iteração k6 executa:", Inches(0.5), Inches(6.2), Inches(10), Inches(0.35),
         12, bold=True, color=C_GRAY)
add_multiline(s,
    ["GET /health  →  POST /tasks (criar)  →  GET /tasks (listar)  →  GET /tasks/:id  →  PATCH status  →  DELETE (soft)"],
    Inches(0.5), Inches(6.6), Inches(12.3), Inches(0.6), 10.5, color=C_ACCENT2, bullet=False)

# Comando
cmd_bg = card(s, Inches(0.5), Inches(7.1), Inches(12.3), Inches(0.3))
add_text(s, "MSYS_NO_PATHCONV=1  docker compose --profile testing run --rm k6 run /scripts/test.js",
         Inches(0.65), Inches(7.13), Inches(12.0), Inches(0.25),
         9, color=C_ACCENT2, font="Courier New")

slide_number(s, 9)


# ════════════════════════════════════════════════════════════════════
# SLIDE 10 — OBSERVABILIDADE
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
add_bg(s)
accent_bar(s)
section_badge(s, "Cauã — Observabilidade", C_YELLOW)

add_text(s, "Observabilidade", Inches(0.6), Inches(0.3), Inches(9), Inches(0.65),
         32, bold=True, color=C_WHITE)
divider(s, Inches(1.05))

# Prometheus
card(s, Inches(0.4), Inches(1.2), Inches(5.9), Inches(2.6))
add_text(s, "📊  Prometheus — :9090", Inches(0.55), Inches(1.3), Inches(5.6), Inches(0.45),
         15, bold=True, color=RGBColor(0xFF,0x6B,0x35))
add_multiline(s,
    ["Scrape dos 4 serviços a cada 15s",
     "4 targets ativos e saudáveis (health: up)",
     "Métrica customizada: http_requests_total{method,route,status}",
     "Métricas Node.js padrão via prom-client"],
    Inches(0.55), Inches(1.8), Inches(5.6), Inches(1.8), 11, bullet=True)

# Grafana
card(s, Inches(6.5), Inches(1.2), Inches(6.4), Inches(2.6))
add_text(s, "📈  Grafana — :3004", Inches(6.65), Inches(1.3), Inches(6.1), Inches(0.45),
         15, bold=True, color=RGBColor(0xF7,0x93,0x1E))
add_multiline(s,
    ["Login: admin / admin123",
     "Dashboard auto-provisionado (sem configuração manual)",
     "7 painéis: Status, Req Rate, Total Reqs, Heap, CPU, Event Loop, Handles",
     "Refresh automático a cada 10 segundos"],
    Inches(6.65), Inches(1.8), Inches(6.1), Inches(1.8), 11, bullet=True)

# 7 painéis Grafana
add_text(s, "Painéis do Dashboard  Task Manager Overview", Inches(0.5), Inches(4.0),
         Inches(9), Inches(0.4), 14, bold=True, color=C_ACCENT)
panels = [
    ("Service Status", "Stat — saúde"),
    ("HTTP Request Rate", "Time-series"),
    ("Total Requests", "Stat — contador"),
    ("Node.js Heap", "Time-series — memória"),
    ("CPU Usage", "Time-series"),
    ("Event Loop Lag", "Time-series"),
    ("Active Handles", "Time-series"),
]
for i, (title, sub) in enumerate(panels):
    cx = Inches(0.4 + (i % 4) * 3.2)
    cy = Inches(4.5 + (i // 4) * 1.35)
    c = card(s, cx, cy, Inches(3.05), Inches(1.1))
    add_text(s, title, cx + Inches(0.1), cy + Inches(0.1), Inches(2.85), Inches(0.42),
             11, bold=True, color=C_ACCENT)
    add_text(s, sub, cx + Inches(0.1), cy + Inches(0.52), Inches(2.85), Inches(0.35),
             9, color=C_GRAY, italic=True)

# Health + Logs
add_text(s, "Health Check:  GET /health  →  { status: 'ok', service: '...', timestamp: '...' }",
         Inches(0.5), Inches(7.1), Inches(12.3), Inches(0.3), 10, color=C_ACCENT2,
         font="Courier New")

slide_number(s, 10)


# ════════════════════════════════════════════════════════════════════
# SLIDE 11 — DEPLOY
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
add_bg(s)
accent_bar(s)
section_badge(s, "Cauã — Deploy", C_ACCENT)

add_text(s, "Deploy", Inches(0.6), Inches(0.3), Inches(9), Inches(0.65),
         32, bold=True, color=C_WHITE)
divider(s, Inches(1.05))

# Ambiente local
card(s, Inches(0.4), Inches(1.2), Inches(5.9), Inches(2.8))
add_text(s, "🖥  Ambiente Local (Docker Desktop)", Inches(0.55), Inches(1.3),
         Inches(5.6), Inches(0.45), 14, bold=True, color=C_ACCENT)
add_multiline(s,
    ["Windows 10 Pro com Docker Desktop",
     "7 containers orquestrados pelo Docker Compose",
     "MongoDB com volume persistente (mongo_data)",
     "Rede interna: task_network (bridge)",
     "Zero dependências externas após docker pull"],
    Inches(0.55), Inches(1.8), Inches(5.6), Inches(2.0), 11, bullet=True)

# Como fazer o deploy
card(s, Inches(6.5), Inches(1.2), Inches(6.4), Inches(2.8))
add_text(s, "🚀  Como Fazer o Deploy", Inches(6.65), Inches(1.3), Inches(6.1), Inches(0.45),
         14, bold=True, color=C_GREEN)
add_multiline(s,
    ["1. Instalar Docker Desktop",
     "2. Clonar o repositório",
     "3. cd TrabMarcio/task-manager",
     "4. docker compose up -d",
     "5. Aguardar MongoDB healthcheck (~20s)",
     "6. API disponível em localhost:3000"],
    Inches(6.65), Inches(1.8), Inches(6.1), Inches(2.0), 11, bullet=False)

# Portas expostas
add_text(s, "Portas Expostas", Inches(0.5), Inches(4.2), Inches(4), Inches(0.4),
         14, bold=True, color=C_ACCENT)
ports = [
    (":3000", "API Gateway (principal)", C_ACCENT),
    (":3001", "Auth Service", C_ACCENT2),
    (":3002", "Task Service", C_ACCENT2),
    (":3003", "User Service", C_ACCENT2),
    (":3004", "Grafana Dashboard", RGBColor(0xF7,0x93,0x1E)),
    (":9090", "Prometheus", RGBColor(0xFF,0x6B,0x35)),
    (":27017", "MongoDB", C_GREEN),
]
for i, (port, desc, col) in enumerate(ports):
    cx = Inches(0.4 + (i % 4) * 3.2)
    cy = Inches(4.7 + (i // 4) * 0.85)
    c = card(s, cx, cy, Inches(3.05), Inches(0.72))
    add_text(s, port, cx + Inches(0.1), cy + Inches(0.08), Inches(0.9), Inches(0.36),
             12, bold=True, color=col, font="Courier New")
    add_text(s, desc, cx + Inches(1.05), cy + Inches(0.1), Inches(1.9), Inches(0.36),
             10, color=C_WHITE)

# render.yaml
add_text(s, "render.yaml presente no repositório para deploy em nuvem (Render.com)",
         Inches(0.5), Inches(7.1), Inches(12.3), Inches(0.3),
         10, color=C_GRAY, italic=True)

slide_number(s, 11)


# ════════════════════════════════════════════════════════════════════
# SLIDE 12 — DOCUMENTAÇÃO
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
add_bg(s)
accent_bar(s)
section_badge(s, "Cauã — Documentação", C_ACCENT2)

add_text(s, "Documentação da API — Swagger", Inches(0.6), Inches(0.3), Inches(9), Inches(0.65),
         32, bold=True, color=C_WHITE)
divider(s, Inches(1.05))

# 3 endpoints Swagger
swagger_urls = [
    ("Auth Service", "/api/auth/docs", ":3001 ou via gateway :3000",
     ["POST /register  —  Registrar", "POST /login  —  Autenticar", "GET /me  —  Perfil", "POST /refresh  —  Renovar token"],
     C_ACCENT),
    ("Task Service", "/api/tasks/docs", ":3002 ou via gateway :3000",
     ["GET /tasks  —  Listar (filtros)", "POST /tasks  —  Criar", "PUT/PATCH/DELETE  —  CRUD", "Restore & Hard Delete (admin)"],
     C_GREEN),
    ("User Service", "/api/users/docs", ":3003 ou via gateway :3000",
     ["GET /users  —  Listar (admin)", "GET /users/:id  —  Buscar", "PUT /users/:id  —  Atualizar", "DELETE /users/:id  —  Desativar"],
     C_YELLOW),
]
for i, (name, path, host, eps, col) in enumerate(swagger_urls):
    cx = Inches(0.4 + i * 4.3)
    c = card(s, cx, Inches(1.2), Inches(4.1), Inches(3.2))
    add_text(s, name, cx + Inches(0.15), Inches(1.3), Inches(3.8), Inches(0.45),
             14, bold=True, color=col)
    add_text(s, path, cx + Inches(0.15), Inches(1.78), Inches(3.8), Inches(0.35),
             11, color=C_ACCENT2, font="Courier New")
    add_text(s, host, cx + Inches(0.15), Inches(2.1), Inches(3.8), Inches(0.3),
             9, color=C_GRAY, italic=True)
    add_multiline(s, eps, cx + Inches(0.15), Inches(2.45), Inches(3.8), Inches(1.7),
                  10, bullet=True, color=C_WHITE)

# Funcionalidades Swagger
add_text(s, "O que a documentação Swagger oferece:", Inches(0.5), Inches(4.6),
         Inches(7), Inches(0.4), 14, bold=True, color=C_ACCENT)
divider(s, Inches(5.05))
add_multiline(s,
    ["Interface visual para testar todos os endpoints diretamente no browser",
     "Autenticação JWT integrada: botão 'Authorize' com campo Bearer token",
     "Exemplos de request body com schemas detalhados (OpenAPI 3.0)",
     "Documentação de responses: 200, 201, 400, 401, 403, 404, 409, 500"],
    Inches(0.5), Inches(5.15), Inches(12.3), Inches(1.6), 11.5, bullet=True)

# Badge OpenAPI
badge_o = s.shapes.add_shape(1, Inches(0.5), Inches(6.9), Inches(2.8), Inches(0.42))
badge_o.fill.solid()
badge_o.fill.fore_color.rgb = C_GREEN
badge_o.line.fill.background()
add_text(s, "OpenAPI 3.0  /  Swagger UI", Inches(0.55), Inches(6.93), Inches(2.7), Inches(0.36),
         10, bold=True, color=C_BG_DARK, align=PP_ALIGN.CENTER)

badge_s = s.shapes.add_shape(1, Inches(3.5), Inches(6.9), Inches(2.2), Inches(0.42))
badge_s.fill.solid()
badge_s.fill.fore_color.rgb = C_ACCENT
badge_s.line.fill.background()
add_text(s, "swagger-jsdoc + swagger-ui-express", Inches(3.55), Inches(6.93),
         Inches(2.1), Inches(0.36), 9, bold=True, color=C_BG_DARK, align=PP_ALIGN.CENTER)

slide_number(s, 12)


# ════════════════════════════════════════════════════════════════════
# SLIDE 13 — CONCLUSÃO
# ════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
add_bg(s)
accent_bar(s)
section_badge(s, "Arthur — Conclusão", C_GREEN)

add_text(s, "Conclusão", Inches(0.6), Inches(0.3), Inches(9), Inches(0.65),
         32, bold=True, color=C_WHITE)
divider(s, Inches(1.05))

# 3 colunas
col_data = [
    ("💡", "Aprendizados", C_ACCENT, [
        "Microserviços exigem contratos\nbem definidos entre serviços",
        "Docker Compose simplifica muito\na orquestração local",
        "JWT stateless facilita escalar\nhorizontalmente",
        "Prometheus + Grafana tornam\no sistema observável em tempo real",
        "k6 revela gargalos antes de ir\npara produção",
    ]),
    ("💪", "Pontos Fortes", C_GREEN, [
        "Arquitetura desacoplada e escalável",
        "0% de erros sob 100 VUs simultâneos",
        "Documentação Swagger em todos\nos serviços",
        "Monitoramento completo com\nauto-provisionamento Grafana",
        "Segurança robusta (JWT, RBAC,\nHelmet, Rate Limit, bcrypt)",
    ]),
    ("🚀", "Melhorias Futuras", C_YELLOW, [
        "Message broker (RabbitMQ/Kafka)\npara comunicação assíncrona",
        "CI/CD pipeline (GitHub Actions)",
        "Deploy em Kubernetes (K8s)",
        "Cache Redis para hot data",
        "Autenticação OAuth2 / social login",
    ]),
]
for i, (icon, title, col, items) in enumerate(col_data):
    cx = Inches(0.4 + i * 4.3)
    c = card(s, cx, Inches(1.2), Inches(4.1), Inches(5.0))
    icon_circle(s, cx + Inches(0.15), Inches(1.3), Inches(0.55), col, icon)
    add_text(s, title, cx + Inches(0.85), Inches(1.35), Inches(3.1), Inches(0.45),
             14, bold=True, color=col)
    add_multiline(s, items, cx + Inches(0.15), Inches(1.9),
                  Inches(3.8), Inches(4.1), 10.5, bullet=True)

# Linha final
divider(s, Inches(6.4))
add_text(s, "Task Manager Microservices API  —  Desenvolvimento de Software para Web  —  Junho 2026",
         Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.35),
         11, color=C_GRAY, align=PP_ALIGN.CENTER)

slide_number(s, 13)


# ── Salvar ──────────────────────────────────────────────────────────
output_path = os.path.join(os.path.dirname(__file__), "Apresentacao_TaskManager_final3.pptx")
prs.save(output_path)
print(f"✅  Apresentação salva em:\n    {output_path}")
