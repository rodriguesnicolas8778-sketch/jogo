"""
Interface gráfica animada para A Jornada de Hércules.

Usa tkinter (já vem com o Python) e reaproveita as classes
Personagem, Heroi e Vilao sem mudar nada nelas.
Os personagens são desenhados com formas no Canvas.

Como rodar:  python interface.py   (ou python main.py)
Atalhos:     1 = atacar | 2 = usar poção | N = novo jogo
"""
import io
import math
import random
import tkinter as tk
from contextlib import redirect_stdout

from personagem import Personagem
from heroi import Heroi
from vilao import Vilao

LARGURA, ALTURA = 820, 390
CHAO = 338  # linha onde os pés dos personagens tocam o chão

CORES = {
    "fundo": "#120d1f",
    "painel": "#1d1630",
    "borda": "#3a2f55",
    "texto": "#efe7d2",
    "apagado": "#958cab",
    "heroi": "#e0a83e",      # bronze dourado
    "vilao": "#6fd38a",      # fogo verde do submundo
    "barra_fundo": "#2c2342",
    "perigo": "#e0574f",
    "cura": "#9cf0a0",
    "botao": "#2d2450",
    "botao_ativo": "#41346f",
}
PELE_HERCULES = "#c68a5b"
PELE_HADES = "#cdbba0"


def capturar(funcao, *args):
    """Executa um método das classes e devolve o que ele daria de print."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        funcao(*args)
    return [linha for linha in buffer.getvalue().splitlines() if linha.strip()]


def suave(t):
    """Curva de animação: começa rápido e desacelera no final."""
    return 1 - (1 - t) ** 2


def girar(pontos, cx, cy, angulo):
    """Gira uma lista de pontos (x, y) em volta de (cx, cy)."""
    a = math.radians(angulo)
    cos, sen = math.cos(a), math.sin(a)
    saida = []
    for x, y in pontos:
        saida += [cx + x * cos - y * sen, cy + x * sen + y * cos]
    return saida


def octogono(cx, cy, r):
    return [(cx + r * math.cos(i * math.pi / 4), cy + r * math.sin(i * math.pi / 4))
            for i in range(8)]


# ================= Desenho dos personagens =================

class Figura:
    """Base para um personagem desenhado no Canvas."""

    def __init__(self, canvas, x, y, tag):
        self.c = canvas
        self.x, self.y = x, y
        self.tag = tag

    def pts(self, pontos):
        """Converte pontos relativos aos pés em coordenadas da tela."""
        saida = []
        for dx, dy in pontos:
            saida += [self.x + dx, self.y + dy]
        return saida

    def poligono(self, pontos, cor, contorno="", **extra):
        return self.c.create_polygon(self.pts(pontos), fill=cor, outline=contorno,
                                     tags=(self.tag,), **extra)

    def oval(self, x0, y0, x1, y1, cor, contorno="", tags=()):
        return self.c.create_oval(self.x + x0, self.y + y0, self.x + x1, self.y + y1,
                                  fill=cor, outline=contorno, tags=(self.tag,) + tags)

    def linha(self, pontos, cor, largura=2):
        return self.c.create_line(self.pts(pontos), fill=cor, width=largura,
                                  capstyle="round", tags=(self.tag,))

    def sombra(self):
        self.oval(-48, -6, 48, 8, "#08050f", tags=("sombra",))

    def mover(self, dx, dy=0):
        self.c.move(self.tag, dx, dy)
        self.x += dx
        self.y += dy

    def mover_para(self, x):
        self.mover(x - self.x)


class FiguraHercules(Figura):
    """Hércules da mitologia: pele do Leão de Nemeia e clava de madeira."""

    PIVO = (18, -142)  # ombro do braço que segura a clava
    BRACO = [(-7, 0), (7, 0), (6, 38), (-6, 38)]
    CLAVA = [(-4, 40), (4, 40), (12, 98), (9, 112), (0, 117), (-9, 112), (-12, 98)]

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, "hercules")
        pele, contorno = PELE_HERCULES, "#8a5a35"
        leao, leao_escuro = "#c08a42", "#7a4f1e"

        self.sombra()
        # Pele de leão caindo pelas costas
        self.poligono([(-12, -175), (-38, -150), (-48, -100), (-42, -56), (-30, -74),
                       (-22, -110), (-16, -150)], "#b07a35", leao_escuro)
        # Braço de trás
        self.poligono([(-27, -142), (-16, -140), (-22, -104), (-33, -106)], pele, contorno)
        self.poligono(octogono(-27, -100, 7), pele, contorno)
        # Pernas e sandálias
        self.poligono([(-18, -70), (-6, -70), (-9, -10), (-21, -10)], pele, contorno)
        self.poligono([(4, -70), (16, -70), (21, -10), (9, -10)], pele, contorno)
        self.poligono([(-25, -10), (-5, -10), (-3, 0), (-25, 0)], "#5a3a1e")
        self.poligono([(5, -10), (25, -10), (29, 0), (5, 0)], "#5a3a1e")
        self.linha([(-21, -30), (-9, -24)], "#5a3a1e", 2)
        self.linha([(9, -30), (21, -24)], "#5a3a1e", 2)
        # Túnica com barra dourada
        self.poligono([(-25, -98), (25, -98), (33, -62), (0, -57), (-33, -62)],
                      "#ece2c6", "#bfae86")
        self.linha([(-33, -64), (0, -59), (33, -64)], CORES["heroi"], 3)
        # Tronco
        self.poligono([(-24, -96), (24, -96), (30, -138), (15, -150), (-15, -150),
                       (-30, -138)], pele, contorno)
        self.linha([(0, -136), (0, -104)], "#a8704a", 2)
        self.linha([(-17, -128), (-4, -123)], "#a8704a", 2)
        self.linha([(4, -123), (17, -128)], "#a8704a", 2)
        for y in (-114, -106):
            self.linha([(-8, y), (-3, y)], "#a8704a", 1)
            self.linha([(3, y), (8, y)], "#a8704a", 1)
        # Cinto
        self.c.create_rectangle(self.x - 25, self.y - 100, self.x + 25, self.y - 92,
                                fill="#6b4423", outline="", tags=(self.tag,))
        self.c.create_rectangle(self.x - 5, self.y - 101, self.x + 5, self.y - 91,
                                fill=CORES["heroi"], outline="", tags=(self.tag,))
        # Patas do leão amarradas no peito
        self.poligono([(-17, -150), (-9, -150), (6, -129), (0, -124)], leao, leao_escuro)
        self.poligono([(17, -150), (9, -150), (-5, -129), (2, -124)], leao, leao_escuro)
        self.oval(-3, -131, 5, -123, leao_escuro)
        # Pescoço, juba e cabeça
        self.poligono([(-6, -158), (8, -158), (8, -148), (-6, -148)], pele)
        self.oval(-23, -198, 20, -155, "#8a5a24")
        self.oval(-12, -184, 16, -152, pele, contorno)
        self.poligono([(-10, -166), (16, -166), (15, -155), (6, -147), (-4, -147),
                       (-11, -156)], "#5a3a22")
        self.oval(1, -173, 5, -168, "#2a1a10")
        self.oval(9, -173, 13, -168, "#2a1a10")
        self.linha([(0, -176), (14, -176)], "#5a3a22", 2)
        # Cabeça do leão usada como capuz
        self.oval(-19, -207, -8, -196, leao, leao_escuro)
        self.oval(10, -207, 21, -196, leao, leao_escuro)
        self.poligono([(-20, -176), (-18, -194), (-6, -203), (10, -203), (21, -192),
                       (19, -178), (4, -182), (-8, -182)], leao, leao_escuro)
        self.oval(-2, -195, 2, -191, "#2a1a10")
        self.oval(9, -195, 13, -191, "#2a1a10")
        self.poligono([(-3, -182), (0, -176), (3, -182)], "#f5efe0")
        self.poligono([(9, -182), (12, -176), (15, -182)], "#f5efe0")

        # Braço da frente e clava (giram juntos em volta do ombro)
        self.clava = self.c.create_polygon(0, 0, 0, 0, fill="#6b4423", outline="#3e2614",
                                           width=2, tags=(self.tag,))
        self.braco = self.c.create_polygon(0, 0, 0, 0, fill=pele, outline=contorno,
                                           tags=(self.tag,))
        self.punho = self.c.create_polygon(0, 0, 0, 0, fill=pele, outline=contorno,
                                           tags=(self.tag,))
        self.angulo = 205
        self.posicionar_clava(205)

    def posicionar_clava(self, angulo):
        """0 = braço para baixo, 180 = clava para cima, 290 = golpe à frente."""
        self.angulo = angulo
        cx, cy = self.x + self.PIVO[0], self.y + self.PIVO[1]
        self.c.coords(self.clava, girar(self.CLAVA, cx, cy, angulo))
        self.c.coords(self.braco, girar(self.BRACO, cx, cy, angulo))
        self.c.coords(self.punho, girar(octogono(0, 44, 8), cx, cy, angulo))

    def peito(self):
        return self.x + 4, self.y - 120


class FiguraHades(Figura):
    """Hades da mitologia: rei do submundo, de coroa e bidente."""

    PIVO = (-20, -140)
    MANGA = [(-9, 0), (9, 0), (8, 40), (-8, 40)]

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, "hades")
        manto, manto_escuro = "#2e1a40", "#1a0f26"

        self.sombra()
        # Cabelo longo e capa com a barra rasgada
        self.poligono([(-16, -190), (16, -190), (24, -136), (-4, -150)], "#120a14")
        self.poligono([(-30, -150), (30, -150), (50, 0), (36, -12), (24, 2), (10, -12),
                       (-4, 2), (-18, -12), (-32, 2), (-50, 0)], "#1a1024", "#0c0612")
        # Túnica
        self.poligono([(-22, -150), (22, -150), (30, 0), (-30, 0)], manto, manto_escuro)
        self.linha([(0, -140), (0, -4)], "#4b2d63", 3)
        # Cinto com fivela de caveira
        self.c.create_rectangle(self.x - 24, self.y - 100, self.x + 24, self.y - 92,
                                fill="#0f0a16", outline="", tags=(self.tag,))
        self.oval(-6, -105, 6, -89, "#d8d2c0")
        self.oval(-4, -100, -1, -96, "#0f0a16")
        self.oval(1, -100, 4, -96, "#0f0a16")
        # Ombreiras com pontas
        self.poligono([(-36, -138), (-30, -156), (-20, -150), (-10, -140), (-20, -126)],
                      "#3c3550", "#1f1b2c")
        self.poligono([(36, -138), (30, -156), (20, -150), (10, -140), (20, -126)],
                      "#3c3550", "#1f1b2c")
        # Pescoço e cabeça
        self.poligono([(-6, -160), (6, -160), (6, -148), (-6, -148)], PELE_HADES)
        self.oval(-14, -190, 12, -156, PELE_HADES, "#8f7e66")
        self.poligono([(-14, -170), (10, -170), (8, -158), (-2, -126), (-8, -128),
                       (-14, -158)], "#120a14")
        self.linha([(-8, -164), (2, -163)], "#5b2a3a", 2)
        self.oval(-11, -179, -6, -174, "#ffb03b")
        self.oval(-3, -179, 2, -174, "#ffb03b")
        self.linha([(-13, -183), (-5, -179)], "#120a14", 2)
        self.linha([(-2, -179), (4, -183)], "#120a14", 2)
        # Coroa de ferro
        self.poligono([(-15, -186), (-14, -202), (-9, -192), (-4, -209), (1, -193),
                       (6, -205), (10, -191), (13, -200), (13, -186)], "#4a445e", "#2a2638")
        # Braço de trás segurando o bidente
        self.poligono([(16, -144), (28, -138), (27, -118), (16, -118)], manto, manto_escuro)
        self.linha([(24, -218), (24, 0)], "#5d586e", 4)
        self.linha([(15, -218), (33, -218)], "#5d586e", 3)
        for px in (17, 31):
            self.linha([(px, -218), (px, -236)], "#5d586e", 3)
            self.poligono([(px - 4, -234), (px, -245), (px + 4, -234)], "#7c7690")
        self.poligono(octogono(24, -116, 7), PELE_HADES, "#8f7e66")

        # Braço da frente (gira para lançar o fogo)
        self.manga = self.c.create_polygon(0, 0, 0, 0, fill=manto, outline=manto_escuro,
                                           tags=(self.tag,))
        self.mao = self.c.create_polygon(0, 0, 0, 0, fill=PELE_HADES, outline="#8f7e66",
                                         tags=(self.tag,))
        self.brilho = []
        self.angulo = 15
        self.posicionar_braco(15)

    def posicionar_braco(self, angulo):
        """15 = braço relaxado, 85 = apontando para Hércules."""
        self.angulo = angulo
        cx, cy = self.x + self.PIVO[0], self.y + self.PIVO[1]
        self.c.coords(self.manga, girar(self.MANGA, cx, cy, angulo))
        self.c.coords(self.mao, girar(octogono(0, 46, 7), cx, cy, angulo))
        if self.brilho:
            self.acender_mao(self.raio_brilho)

    def posicao_mao(self):
        cx, cy = self.x + self.PIVO[0], self.y + self.PIVO[1]
        x, y = girar([(0, 50)], cx, cy, self.angulo)
        return x, y

    def acender_mao(self, raio):
        """Fogo verde crescendo na mão de Hades."""
        self.raio_brilho = raio
        if not self.brilho:
            self.brilho = [self.c.create_oval(0, 0, 0, 0, fill=cor, outline="", tags=(self.tag,))
                           for cor in ("#2f9e4f", "#7be38a", "#f0fff0")]
        x, y = self.posicao_mao()
        for item, fator in zip(self.brilho, (1, 0.65, 0.3)):
            r = raio * fator
            self.c.coords(item, x - r, y - r, x + r, y + r)

    def apagar_mao(self):
        for item in self.brilho:
            self.c.delete(item)
        self.brilho = []

    def peito(self):
        return self.x - 6, self.y - 120


# ================= Janela do jogo =================

class JogoHercules(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("A Jornada de Hércules")
        self.configure(bg=CORES["fundo"], padx=20, pady=16)
        self.resizable(False, False)
        self.ocupado = False

        self._montar_tela()
        self.bind("1", lambda e: self.jogar("atacar"))
        self.bind("2", lambda e: self.jogar("pocao"))
        self.bind("n", lambda e: self.novo_jogo())
        self.bind("N", lambda e: self.novo_jogo())
        self.novo_jogo()

    # ---------- Montagem da tela ----------

    def _montar_tela(self):
        self.tela = tk.Canvas(self, width=LARGURA, height=ALTURA, bg=CORES["fundo"],
                              highlightthickness=2, highlightbackground=CORES["borda"])
        self.tela.pack()

        moldura = tk.Frame(self, bg=CORES["borda"], padx=1, pady=1)
        moldura.pack(fill="both", expand=True, pady=12)
        self.registro = tk.Text(moldura, height=7, wrap="word", bd=0,
                                font=("Helvetica", 11), bg=CORES["painel"],
                                fg=CORES["texto"], padx=14, pady=8,
                                state="disabled", cursor="arrow")
        rolagem = tk.Scrollbar(moldura, command=self.registro.yview)
        self.registro.config(yscrollcommand=rolagem.set)
        rolagem.pack(side="right", fill="y")
        self.registro.pack(side="left", fill="both", expand=True)
        self.registro.tag_config("heroi", foreground=CORES["heroi"])
        self.registro.tag_config("vilao", foreground=CORES["vilao"])
        self.registro.tag_config("sistema", foreground=CORES["apagado"])
        self.registro.tag_config("rodada", font=("Georgia", 11, "bold"), spacing1=6)
        self.registro.tag_config("resultado", font=("Georgia", 13, "bold"), spacing1=8)

        barra = tk.Frame(self, bg=CORES["fundo"])
        barra.pack(fill="x")
        self.botao_atacar = self._botao(barra, "Atacar  (1)", lambda: self.jogar("atacar"))
        self.botao_pocao = self._botao(barra, "Usar poção  (2)", lambda: self.jogar("pocao"))
        self.botao_novo = self._botao(barra, "Novo jogo  (N)", self.novo_jogo)
        self.botao_atacar.pack(side="left")
        self.botao_pocao.pack(side="left", padx=10)
        self.botao_novo.pack(side="right")

    def _botao(self, pai, texto, comando):
        return tk.Button(pai, text=texto, command=comando, font=("Helvetica", 12, "bold"),
                         fg=CORES["texto"], bg=CORES["botao"],
                         activeforeground=CORES["texto"], activebackground=CORES["botao_ativo"],
                         disabledforeground=CORES["apagado"], relief="flat",
                         bd=0, padx=18, pady=10, cursor="hand2")

    def desenhar_cenario(self):
        c = self.tela
        # Céu da caverna em faixas de cor
        topo, base = (12, 8, 22), (52, 30, 66)
        faixas = 22
        for i in range(faixas):
            t = i / (faixas - 1)
            cor = "#%02x%02x%02x" % tuple(int(a + (b - a) * t) for a, b in zip(topo, base))
            y0 = i * 300 / faixas
            c.create_rectangle(0, y0, LARGURA, y0 + 300 / faixas + 1, fill=cor, outline="")
        # Montanhas de pedra ao fundo
        c.create_polygon(0, 150, 60, 110, 130, 150, 210, 95, 290, 140, 370, 88, 450, 135,
                         530, 100, 610, 145, 700, 92, 780, 128, LARGURA, 110,
                         LARGURA, 280, 0, 280, fill="#160f24", outline="")
        # Estalactites
        for x, comp in [(40, 50), (120, 28), (230, 60), (300, 34), (420, 46), (500, 26),
                        (640, 58), (700, 30), (780, 44)]:
            c.create_polygon(x, 0, x + 18, 0, x + 9, comp, fill="#0b0714", outline="")
        # Colunas gregas (uma delas quebrada)
        for x, altura, quebrada in [(70, 150, False), (330, 95, True), (760, 160, False)]:
            topo_col = 270 - altura
            c.create_rectangle(x - 17, topo_col, x + 17, 270, fill="#3b3552", outline="")
            for dx in (-8, 0, 8):
                c.create_line(x + dx, topo_col + 4, x + dx, 262, fill="#2c2742", width=2)
            c.create_rectangle(x - 23, 260, x + 23, 270, fill="#463f60", outline="")
            if quebrada:
                c.create_polygon(x - 17, topo_col, x - 9, topo_col - 12, x - 2, topo_col - 4,
                                 x + 6, topo_col - 16, x + 17, topo_col - 6, x + 17, topo_col,
                                 fill="#3b3552", outline="")
            else:
                c.create_rectangle(x - 25, topo_col - 10, x + 25, topo_col,
                                   fill="#463f60", outline="")
        # Rio Estige
        c.create_rectangle(0, 270, LARGURA, 300, fill="#12302f", outline="")
        for y, deslocamento in [(280, 0), (291, 40)]:
            pontos = []
            for x in range(-40, LARGURA + 40, 40):
                pontos += [x + deslocamento, y, x + deslocamento + 20, y - 3]
            c.create_line(pontos, fill="#1f5248", width=2, smooth=True)
        for x in (150, 460, 690):
            c.create_oval(x - 18, 278, x + 18, 286, fill="#245c45", outline="")
        # Chão de pedra
        c.create_rectangle(0, 300, LARGURA, ALTURA, fill="#2a2036", outline="")
        for y in (318, CHAO + 18, CHAO + 40):
            c.create_line(0, y, LARGURA, y, fill="#1f1829")
        # Parte da frente do chão: cobre quem afunda no final
        c.create_rectangle(0, CHAO + 1, LARGURA, ALTURA, fill="#2a2036", outline="",
                           tags=("chao_frente",))
        for i, y in enumerate((CHAO + 18, CHAO + 40)):
            c.create_line(0, y, LARGURA, y, fill="#1f1829", tags=("chao_frente",))
            for x in range(30 + i * 45, LARGURA, 90):
                c.create_line(x, y - 18 if i == 0 else y - 22, x, y, fill="#1f1829",
                              tags=("chao_frente",))

    def desenhar_hud(self):
        c = self.tela
        c.create_text(24, 18, anchor="nw", text=self.heroi.nome, fill=CORES["heroi"],
                      font=("Georgia", 20, "bold"), tags=("hud",))
        c.create_text(LARGURA - 24, 18, anchor="ne", text=self.vilao.nome, fill=CORES["vilao"],
                      font=("Georgia", 20, "bold"), tags=("hud",))
        c.create_rectangle(24, 54, 284, 68, fill=CORES["barra_fundo"], outline="", tags=("hud",))
        c.create_rectangle(LARGURA - 284, 54, LARGURA - 24, 68, fill=CORES["barra_fundo"],
                           outline="", tags=("hud",))
        self.barra_heroi = c.create_rectangle(24, 54, 284, 68, outline="", tags=("hud",))
        self.barra_vilao = c.create_rectangle(LARGURA - 284, 54, LARGURA - 24, 68,
                                              outline="", tags=("hud",))
        self.texto_heroi = c.create_text(24, 76, anchor="nw", fill=CORES["texto"],
                                         font=("Helvetica", 11, "bold"), tags=("hud",))
        self.texto_vilao = c.create_text(LARGURA - 24, 76, anchor="ne", fill=CORES["texto"],
                                         font=("Helvetica", 11, "bold"), tags=("hud",))
        self.texto_rodada = c.create_text(LARGURA / 2, 30, fill=CORES["apagado"],
                                          font=("Georgia", 13, "italic"), tags=("hud",))

    def atualizar_hud(self):
        self.max_heroi = max(self.max_heroi, self.heroi.vida)
        self.max_vilao = max(self.max_vilao, self.vilao.vida)

        p = self.heroi.vida / self.max_heroi
        self.tela.coords(self.barra_heroi, 24, 54, 24 + 260 * p, 68)
        self.tela.itemconfig(self.barra_heroi,
                             fill=CORES["perigo"] if p < 0.3 else CORES["heroi"])
        p = self.vilao.vida / self.max_vilao
        self.tela.coords(self.barra_vilao, LARGURA - 24 - 260 * p, 54, LARGURA - 24, 68)
        self.tela.itemconfig(self.barra_vilao,
                             fill=CORES["perigo"] if p < 0.3 else CORES["vilao"])

        self.tela.itemconfig(self.texto_heroi, text=f"Vida {self.heroi.vida}/{self.max_heroi}"
                             f"     Poções {self.heroi.itens['Poção']}")
        self.tela.itemconfig(self.texto_vilao, text=f"Maldade {self.vilao.maldade}"
                             f"     Vida {self.vilao.vida}/{self.max_vilao}")
        self.tela.itemconfig(self.texto_rodada,
                             text="" if self.terminou else f"Rodada {self.rodada}")
        self.tela.tag_raise("hud")
        self.atualizar_botoes()

    def atualizar_botoes(self):
        pode = not self.terminou and not self.ocupado
        self.botao_atacar.config(state="normal" if pode else "disabled")
        self.botao_pocao.config(
            state="normal" if pode and self.heroi.itens['Poção'] > 0 else "disabled")
        self.botao_novo.config(state="disabled" if self.ocupado else "normal")

    # ---------- Registro ----------

    def escrever(self, linha, tag=None):
        if tag is None:
            if linha.startswith(self.heroi.nome):
                tag = "heroi"
            elif linha.startswith(self.vilao.nome):
                tag = "vilao"
        self.registro.config(state="normal")
        self.registro.insert("end", linha + "\n", tag or ())
        self.registro.config(state="disabled")
        self.registro.see("end")

    def escrever_varias(self, linhas, tag=None):
        for linha in linhas:
            self.escrever(linha, tag)

    # ---------- Ferramentas de animação ----------

    def animar(self, quadros, passo, fim=None, intervalo=16):
        """Chama passo(i, quadros) várias vezes, um quadro a cada 16 ms."""
        def rodar(i=0):
            if i < quadros:
                passo(i, quadros)
                self.after(intervalo, rodar, i + 1)
            elif fim:
                fim()
        rodar()

    def sequencia(self, etapas, fim=None):
        """Executa etapas em ordem: (quadros, função) anima, número espera ms,
        e uma função comum é chamada uma vez."""
        if not etapas:
            if fim:
                fim()
            return
        etapa, resto = etapas[0], etapas[1:]
        seguir = lambda: self.sequencia(resto, fim)
        if isinstance(etapa, int):
            self.after(etapa, seguir)
        elif isinstance(etapa, tuple):
            self.animar(etapa[0], etapa[1], seguir)
        else:
            etapa()
            seguir()

    def particulas(self, x, y, cores, qtd=16, forca=6, gravidade=0.3, subir=False, quadros=24):
        c = self.tela
        lista = []
        for _ in range(qtd):
            angulo = random.uniform(0, 2 * math.pi)
            v = random.uniform(forca * 0.4, forca)
            vx, vy = math.cos(angulo) * v, math.sin(angulo) * v
            if subir:
                vx, vy = vx * 0.3, -abs(vy) * 0.5 - 1
            r = random.uniform(2, 4.5)
            item = c.create_oval(x - r, y - r, x + r, y + r, fill=random.choice(cores), outline="")
            lista.append([item, vx, vy])

        def passo(i, n):
            for p in lista:
                c.move(p[0], p[1], p[2])
                p[2] += gravidade

        self.animar(quadros, passo, lambda: [c.delete(p[0]) for p in lista])

    def numero(self, x, y, texto, cor):
        """Número de dano ou cura subindo na tela."""
        c = self.tela
        sombra = c.create_text(x + 2, y + 2, text=texto, fill="#000000",
                               font=("Georgia", 24, "bold"))
        frente = c.create_text(x, y, text=texto, fill=cor, font=("Georgia", 24, "bold"))
        self.animar(36, lambda i, n: (c.move(sombra, 0, -1.4), c.move(frente, 0, -1.4)),
                    lambda: (c.delete(sombra), c.delete(frente)))

    def piscar(self, figura):
        c = self.tela
        originais = []
        for item in c.find_withtag(figura.tag):
            if "sombra" in c.gettags(item):
                continue
            cor = c.itemcget(item, "fill")
            if cor:
                originais.append((item, cor))
                c.itemconfig(item, fill="#ffffff")
        self.after(90, lambda: [c.itemconfig(item, fill=cor) for item, cor in originais])

    def tremer(self, figura):
        deslocamentos = [9, -16, 12, -8, 3]

        def passo(i, n):
            figura.mover(deslocamentos[i])
        self.animar(len(deslocamentos), passo, intervalo=40)

    def impacto(self, figura, dano, cores):
        x, y = figura.peito()
        self.piscar(figura)
        self.tremer(figura)
        self.particulas(x, y, cores, qtd=20, forca=7)
        self.numero(x, y - 70, f"-{dano}", CORES["perigo"])

    # ---------- Animações de cada ação ----------

    def animar_ataque_heroi(self, ao_acertar, fim):
        h = self.fig_heroi
        inicio, alvo = h.x, h.x + 225

        def preparar(i, n):
            h.posicionar_clava(205 - 40 * suave((i + 1) / n))

        def avancar(i, n):
            h.mover_para(inicio + (alvo - inicio) * suave((i + 1) / n))
            h.posicionar_clava(h.angulo)

        def golpear(i, n):
            h.posicionar_clava(165 + 125 * ((i + 1) / n) ** 2)

        def voltar(i, n):
            t = suave((i + 1) / n)
            h.mover_para(alvo + (inicio - alvo) * t)
            h.posicionar_clava(290 - 85 * t)

        self.sequencia([(7, preparar), (13, avancar), (5, golpear), ao_acertar,
                        240, (16, voltar)], fim)

    def animar_ataque_vilao(self, ao_acertar, fim):
        h = self.fig_vilao
        c = self.tela
        bola, rastro = [], []

        def erguer(i, n):
            t = suave((i + 1) / n)
            h.posicionar_braco(15 + 70 * t)
            h.acender_mao(4 + 10 * t)

        def criar_bola():
            h.apagar_mao()
            for cor in ("#2f9e4f", "#7be38a", "#f0fff0"):
                bola.append(c.create_oval(0, 0, 0, 0, fill=cor, outline=""))

        origem = {}

        def voar(i, n):
            if not origem:
                origem["x"], origem["y"] = h.posicao_mao()
            t = (i + 1) / n
            alvo_x, alvo_y = self.fig_heroi.peito()
            x = origem["x"] + (alvo_x - origem["x"]) * t
            y = origem["y"] + (alvo_y - origem["y"]) * t - 50 * math.sin(math.pi * t)
            for item, r in zip(bola, (15, 10, 5)):
                c.coords(item, x - r, y - r, x + r, y + r)
            r = random.uniform(2, 5)
            rastro.append(c.create_oval(x - r, y - r + random.uniform(-4, 4), x + r, y + r,
                                        fill=random.choice(("#2f9e4f", "#7be38a")), outline=""))

        def explodir():
            for item in bola + rastro:
                c.delete(item)
            ao_acertar()

        def baixar(i, n):
            h.posicionar_braco(85 - 70 * suave((i + 1) / n))

        self.sequencia([(10, erguer), 120, criar_bola, (18, voar), explodir,
                        (10, baixar), 200], fim)

    def animar_pocao(self, fim):
        x, y = self.fig_heroi.peito()
        self.particulas(x, y + 30, ["#9cf0a0", "#f7e08a", "#ffffff"], qtd=26, forca=4,
                        gravidade=-0.05, subir=True, quadros=40)
        self.numero(x, y - 70, "+30", CORES["cura"])
        self.after(800, fim)

    def animar_derrota(self, figura, fim):
        c = self.tela
        c.tag_raise("chao_frente")
        c.tag_raise("hud")

        def afundar(i, n):
            figura.mover(0, 3.2)
            if i % 4 == 0:
                self.particulas(figura.x + random.uniform(-40, 40), CHAO - 4,
                                ["#4b3f63", "#6d5f88", "#2f9e4f"], qtd=4, forca=2,
                                gravidade=-0.08, subir=True, quadros=30)

        self.sequencia([300, (85, afundar), 300], fim)

    # ---------- Lógica do jogo (mesma do main.py) ----------

    def novo_jogo(self):
        if self.ocupado:
            return
        self.heroi = Heroi('Hercules', 30, 100, 20, 5)
        self.npc = Personagem('Andarilho Misterioso', 28, 80, 5, 2)
        self.npc2 = Personagem('Namorada de Hercules', 28, 80, 5, 2)
        self.vilao = Vilao('Hades', 45, 120, 18, 4, 'Alta')
        self.refens = [self.npc, self.npc2]
        self.historico = []
        self.rodada = 1
        self.terminou = False
        self.max_heroi = self.heroi.vida
        self.max_vilao = self.vilao.vida

        self.tela.delete("all")
        self.desenhar_cenario()
        self.fig_heroi = FiguraHercules(self.tela, 200, CHAO)
        self.fig_vilao = FiguraHades(self.tela, 585, CHAO)
        self.desenhar_hud()

        self.registro.config(state="normal")
        self.registro.delete("1.0", "end")
        self.registro.config(state="disabled")
        for personagem in [self.heroi, self.vilao] + self.refens:
            self.escrever(str(personagem), "sistema")
        self.escrever_varias(capturar(self.vilao.dialogar, self.heroi,
                                      'Seus amigos estão presos no submundo!'))
        self.escrever_varias(capturar(self.heroi.dialogar, self.vilao,
                                      'Vou libertá-los, Hades!'))
        self.historico.append('Hades desafiou Hercules')
        self.atualizar_hud()

    def jogar(self, escolha):
        if self.ocupado or self.terminou:
            return
        if escolha == "pocao" and self.heroi.itens['Poção'] == 0:
            return

        self.ocupado = True
        self.atualizar_botoes()
        self.escrever(f"Rodada {self.rodada}", "rodada")

        if escolha == "atacar":
            def acertar():
                antes = self.vilao.vida
                self.escrever_varias(capturar(self.heroi.atacar, self.vilao))
                self.impacto(self.fig_vilao, antes - self.vilao.vida,
                             ["#fff3c4", CORES["heroi"], "#ffffff"])
                self.atualizar_hud()
            self.historico.append(f'Rodada {self.rodada}: Hercules atacou')
            self.animar_ataque_heroi(acertar, self.depois_do_heroi)
        else:
            self.escrever_varias(capturar(self.heroi.usar_pocao), "heroi")
            self.historico.append(f'Rodada {self.rodada}: Hercules usou poção')
            self.atualizar_hud()
            self.animar_pocao(self.depois_do_heroi)

    def depois_do_heroi(self):
        if self.vilao.esta_vivo():
            self.after(250, self.turno_do_vilao)
        else:
            self.finalizar()

    def turno_do_vilao(self):
        def acertar():
            antes = self.heroi.vida
            self.escrever_varias(capturar(self.vilao.atacar, self.heroi))
            self.impacto(self.fig_heroi, antes - self.heroi.vida,
                         ["#7be38a", "#2f9e4f", "#f0fff0"])
            self.atualizar_hud()
        self.historico.append(f'Rodada {self.rodada}: Hades atacou')
        self.animar_ataque_vilao(acertar, self.depois_do_vilao)

    def depois_do_vilao(self):
        self.rodada += 1
        if self.heroi.esta_vivo():
            self.ocupado = False
            self.atualizar_hud()
        else:
            self.finalizar()

    def finalizar(self):
        self.terminou = True
        venceu = self.heroi.esta_vivo()
        perdedor = self.fig_vilao if venceu else self.fig_heroi

        def mostrar_resultado():
            self.tela.delete(perdedor.tag)  # some de vez depois de afundar
            self.tela.delete("sombra")
            if venceu:
                self.fig_heroi.posicionar_clava(180)
                titulo, cor = "Hércules venceu!", CORES["heroi"]
                self.escrever("Hercules venceu Hades!", "resultado")
                for refem in self.refens:
                    self.escrever_varias(capturar(self.heroi.salvar_refem, refem), "heroi")
                self.escrever_varias(capturar(self.npc2.dialogar, self.heroi,
                                              'Você me salvou, Hercules!'), "sistema")
                self.historico.append('Hercules venceu e salvou os reféns')
            else:
                self.fig_vilao.posicionar_braco(85)
                self.fig_vilao.acender_mao(14)
                titulo, cor = "Hades venceu...", CORES["vilao"]
                self.escrever("Hades venceu... Os reféns continuam presos.", "resultado")
                self.historico.append('Hades venceu')

            self.tela.create_text(LARGURA / 2 + 63, 203, text=titulo, fill="#000000",
                                  font=("Georgia", 32, "bold"))
            self.tela.create_text(LARGURA / 2 + 60, 200, text=titulo, fill=cor,
                                  font=("Georgia", 32, "bold"))
            self.escrever("Histórico", "rodada")
            self.escrever_varias(self.historico, "sistema")
            self.ocupado = False
            self.atualizar_hud()

        self.ocupado = True
        self.atualizar_hud()
        self.animar_derrota(perdedor, mostrar_resultado)


if __name__ == "__main__":
    JogoHercules().mainloop()
