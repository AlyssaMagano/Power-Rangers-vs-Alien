import pyxel
import random

def colide(x1, y1, w1, h1, x2, y2, w2, h2):
    return (x1 < x2 + w2 and x1 + w1 > x2 and
            y1 < y2 + h2 and y1 + h1 > y2)

# Classe dos tiros do inimigo
class Tiro:
    def __init__(self, inimigo):
        self.tiros = []

        self.timer_spawn = 0
        self.spawn_interval = 20
        self.inimigo = inimigo


    def update(self):
        self.timer_spawn += 1
        if self.timer_spawn > self.spawn_interval:
            y_rand = self.inimigo.y + random.randint(0, self.inimigo.altura - 8)
            self.tiros.append([self.inimigo.x, y_rand])
            self.timer_spawn = 0
        # atualiza e remove tiros fora da tela
        self.tiros = [[t[0] - 4, t[1]] for t in self.tiros if t[0] - 4 > 0]

    def draw(self):
        for t in self.tiros:
            pyxel.blt(t[0], t[1], 0, 0, 120, 16, 8, 14)

# Classe do inimigo
class Inimigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 60
        self.altura = 80
        self.cor = 13
        self.health = 500

    def draw(self):
        # desenha sprite do inimigo
        pyxel.blt(self.x, self.y + 9, 0, 0, 48, 55, 72, 14)

# Power Azul
class PowerAzul:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cor = 5
        self.health = 100
        self.anim_frame = 0
        self.anim_timer = 0
        self.flip = False
        self.vy = 0
        self.no_chao = True
        self.projeteis = []  # lista de projéteis
        self.tiro_cooldown = 0  # intervalo entre tiros
        self.tiro_anim = 0  # controla animação de tiro
        self.vivo = True
        self.abaixado = False

    def update(self):
        if not self.vivo or self.health <= 0:
            self.vivo = False
            return
        for p in self.projeteis:
            if p[2]:  # direita
                p[0] += 5
            else:     # esquerda
                p[0] -= 5
        # remove projéteis fora da tela
        self.projeteis = [p for p in self.projeteis if 0 <= p[0] < 256]
        if self.tiro_cooldown > 0:
            self.tiro_cooldown -= 1
        if self.tiro_anim > 0:
            self.tiro_anim -= 1
        # limite do mapa
        limite_esquerda = 10
        limite_direita = 170  # antes do inimigo
        dx = (pyxel.btn(pyxel.KEY_RIGHT) and self.x < limite_direita) * 3 - (pyxel.btn(pyxel.KEY_LEFT) and self.x > limite_esquerda) * 3
        if dx > 0: self.flip = False
        if dx < 0: self.flip = True
        self.x += dx
        if self.x < limite_esquerda:
            self.x = limite_esquerda
        if self.x > limite_direita:
            self.x = limite_direita

        # pulo
        if pyxel.btnp(pyxel.KEY_UP) and self.no_chao:
            self.vy = -6
            self.no_chao = False

        # gravidade
        self.vy += 0.35
        self.y += self.vy
        if self.y >= 100:
            self.y = 100
            self.vy = 0
            self.no_chao = True

        # animação
        if dx or not self.no_chao:
            self.anim_timer += 1
            if self.anim_timer > 5:
                self.anim_frame = 1 + ((self.anim_frame - 1 + 1) % 3)
                self.anim_timer = 0
        else:
            self.anim_frame = 0

        # dispara projétil ao apertar shift direito
        if pyxel.btn(pyxel.KEY_RSHIFT) and self.tiro_cooldown == 0:
            if not self.flip:
                self.projeteis.append([self.x+12, self.y-5, True])
            else:
                self.projeteis.append([self.x-12, self.y-5, False])
            self.tiro_cooldown = 15
            self.tiro_anim = 8
            pyxel.play(0, 0)

        # Abaixar
        if pyxel.btn(pyxel.KEY_DOWN):
            self.abaixado = True
        else:
            self.abaixado = False

    def draw(self):
        if not self.vivo or self.health <= 0:
            return
        largura = -24 if self.flip else 24
        if self.abaixado:
            # Desenha sprite abaixado (ajuste Y e frame se necessário)
            pyxel.blt(self.x-12, self.y, 0, 72, 0, largura, 16, 14)
        elif self.tiro_anim > 0:
            pyxel.blt(self.x-12, self.y-12, 0, 96, 0, largura, 24, 14)
        else:
            pyxel.blt(self.x-12, self.y-12, 0, self.anim_frame*24, 0, largura, 24, 14)
        # desenha os projéteis
        for p in self.projeteis:
            if p[2]:
                pyxel.blt(p[0], p[1], 0, 24, 120, 8, 8, 14)
            else:
                pyxel.blt(p[0], p[1], 0, 24, 120, -8, 8, 14)

    def soco(self, inimigo):
        if pyxel.btn(pyxel.KEY_RETURN):
            if (self.x+10 > inimigo.x and self.x-10 < inimigo.x+inimigo.largura and
                self.y+10 > inimigo.y and self.y-10 < inimigo.y+inimigo.altura):
                inimigo.health -= 2

# Power Rosa
class PowerRosa:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cor = 14
        self.health = 100
        self.anim_frame = 0
        self.anim_timer = 0
        self.flip = False
        self.vy = 0
        self.no_chao = True
        self.projeteis = []  # lista dos projéteis
        self.tiro_cooldown = 0  # intervalo entre tiros
        self.tiro_anim = 0  # controla animação do tiro
        self.vivo = True
        self.abaixado = False

    def update(self):
        if not self.vivo or self.health <= 0:
            self.vivo = False
            return
        # atualiza projéteis
        for p in self.projeteis:
            if p[2]:
                p[0] += 5
            else:
                p[0] -= 5
        # remove projéteis fora da tela
        self.projeteis = [p for p in self.projeteis if 0 <= p[0] < 256]
        if self.tiro_cooldown > 0:
            self.tiro_cooldown -= 1
        if self.tiro_anim > 0:
            self.tiro_anim -= 1
        # limite do mapa
        limite_esquerda = 10
        limite_direita = 170  # antes do inimigo
        dx = (pyxel.btn(pyxel.KEY_D) and self.x < limite_direita) * 3 - (pyxel.btn(pyxel.KEY_A) and self.x > limite_esquerda) * 3
        if dx > 0: self.flip = False
        if dx < 0: self.flip = True
        self.x += dx
        if self.x < limite_esquerda:
            self.x = limite_esquerda
        if self.x > limite_direita:
            self.x = limite_direita

        # pulo
        if pyxel.btnp(pyxel.KEY_W) and self.no_chao:
            self.vy = -6
            self.no_chao = False

        # gravidade
        self.vy += 0.35
        self.y += self.vy
        if self.y >= 100:
            self.y = 100
            self.vy = 0
            self.no_chao = True

        # animação
        if dx or not self.no_chao:
            self.anim_timer += 1
            if self.anim_timer > 5:
                self.anim_frame = 1 + ((self.anim_frame - 1 + 1) % 3)
                self.anim_timer = 0
        else:
            self.anim_frame = 0

        # dispara projétil ao apertar F
        if pyxel.btn(pyxel.KEY_F) and self.tiro_cooldown == 0:
            if not self.flip:
                self.projeteis.append([self.x+12, self.y-5, True])
            else:
                self.projeteis.append([self.x-12, self.y-5, False])
            self.tiro_cooldown = 15
            self.tiro_anim = 8
            pyxel.play(0, 0)

        # Abaixar
        if pyxel.btn(pyxel.KEY_S):
            self.abaixado = True
        else:
            self.abaixado = False

    def draw(self):
        if not self.vivo or self.health <= 0:
            return
        largura = -24 if self.flip else 24
        if self.abaixado:
            # Desenha sprite abaixado (ajuste Y e frame se necessário)
            pyxel.blt(self.x-12, self.y, 0, 72, 24, largura, 16, 14)
        elif self.tiro_anim > 0:
            pyxel.blt(self.x-12, self.y-12, 0, 96, 24, largura, 24, 14)
        else:
            pyxel.blt(self.x-12, self.y-12, 0, self.anim_frame*24, 24, largura, 24, 14)
        # desenha os projéteis
        for p in self.projeteis:
            if p[2]:
                pyxel.blt(p[0], p[1], 0, 16, 120, 8, 8, 14)
            else:
                pyxel.blt(p[0], p[1], 0, 16, 120, -8, 8, 14)

    def soco(self, inimigo):
        if pyxel.btn(pyxel.KEY_F):
            if (self.x+10 > inimigo.x and self.x-10 < inimigo.x+inimigo.largura and
                self.y+10 > inimigo.y and self.y-10 < inimigo.y+inimigo.altura):
                inimigo.health -= 2

# Barras de vida
def draw_health_bar(x, y, pct, color):
    pct = max(0, pct)
    if color == 14:
        pyxel.blt(x, y, 0, 0, 128, 32, 8, 14)
        bar_x, bar_y, bar_w, bar_h = x+5, y+3, 22, 3
        pyxel.rect(bar_x, bar_y, bar_w, bar_h, 7)
        fill_w = int(bar_w * (pct / 100))
        if fill_w > 0:
            pyxel.rect(bar_x, bar_y, fill_w, bar_h, 8)
    elif color == 5:
        pyxel.blt(x, y, 0, 0, 136, 32, 8, 14)
        bar_x, bar_y, bar_w, bar_h = x+5, y+3, 22, 3
        pyxel.rect(bar_x, bar_y, bar_w, bar_h, 7)
        fill_w = int(bar_w * (pct / 100))
        if fill_w > 0:
            pyxel.rect(bar_x, bar_y, fill_w, bar_h, 5)
    elif color == 13:
        # barra de vida do vilão
        pyxel.blt(x, y, 0, 0, 144, 79, 16, 14)
        bar_x, bar_y, bar_w, bar_h = x+6, y+5, 68, 6
        pyxel.rect(bar_x, bar_y, bar_w, bar_h, 7)
        fill_w = int(bar_w * (pct / 500))
        if fill_w > 0:
            pyxel.rect(bar_x, bar_y, fill_w, bar_h, 11)
    else:
        width = pct * 0.5
        pyxel.rect(x, y, 50, 5, 7)
        pyxel.rect(x, y, width, 5, 7, color)


# Classe principal do jogo
class Jogo:

    def __init__(self):
        pyxel.init(256, 120, title="Power Rangers vs Jindrax")
        pyxel.images[0].load(0, 0, "sprites.png")
        pyxel.images[1].load(0, 0, "fundo.png")
        self.state = "menu"
        self.pr = PowerRosa(30, 100)
        self.pa = PowerAzul(50, 100)
        self.jd = Inimigo(180, 30)
        self.tiros = Tiro(self.jd)
        self.sparks = [[random.randint(0, 255), random.randint(0, 99), random.choice([8,10,11,12,14])] for _ in range(30)]
        # Define som de explosão (efeito curto)
        pyxel.sound(0).set("c3c2c1", "nns", "7", "f", 10)
        # Efeito sonoro de início de jogo (menu) com volume reduzido
        pyxel.sound(1).set("c3e3g3c4g3e3c3c2", "t", "3", "n", 25)
        pyxel.play(1, 1, loop=True)
        pyxel.run(self.update, self.draw)

    def update_menu(self):
        for spark in self.sparks:
            spark[1] += 1
            if spark[1] > 99:
                spark[0] = random.randint(0, 255)
                spark[1] = 0
                spark[2] = random.choice([8,10,11,12,14])
        if pyxel.btnp(pyxel.KEY_RETURN):
            pyxel.stop(1)
            self.state = "jogo"
            

    def draw_menu(self):
        pyxel.cls(3)
        pyxel.rect(0, 100, 256, 20, 1)
        titulo = "Power Rangers vs Alien"
        cores = [8,11,12,14,10]
        for i, letra in enumerate(titulo):
            offset = (pyxel.frame_count // 5) % 5
            cor = cores[(i+offset) % len(cores)]
            pyxel.text(30 + i*8, 40, letra, cor)
        cor_instrucao = 7 if (pyxel.frame_count // 20) % 2 == 0 else 8
        pyxel.text(70, 70, "PRESSIONE ENTER PARA INICIAR", cor_instrucao)
        for spark in self.sparks:
            pyxel.pset(spark[0], spark[1], spark[2])

    def update(self):
        if self.state == "menu":
            self.update_menu()
        elif self.state == "jogo":
            self.pr.update()
            self.pa.update()
            self.tiros.update()

            for t in self.tiros.tiros:
                # hitbox dos personagens: 24x24 
                # hitbox do tiro: 16x8
                pr_x = self.pr.x - 12
                pr_y = self.pr.y - 12
                pa_x = self.pa.x - 12
                pa_y = self.pa.y - 12
                tiro_x = t[0]
                tiro_y = t[1]
                if colide(pr_x, pr_y, 24, 24, tiro_x, tiro_y, 16, 8):
                    self.pr.health -= 10
                    self.tiros.tiros.remove(t)
                elif colide(pa_x, pa_y, 24, 24, tiro_x, tiro_y, 16, 8):
                    self.pa.health -= 10
                    self.tiros.tiros.remove(t)

            self.pr.soco(self.jd)
            self.pa.soco(self.jd)
            for p in self.pr.projeteis:
                if colide(p[0], p[1], 8, 8, self.jd.x, self.jd.y+9, self.jd.largura, self.jd.altura):
                    self.jd.health -= 10
                    self.pr.projeteis.remove(p)
            for p in self.pa.projeteis:
                if colide(p[0], p[1], 8, 8, self.jd.x, self.jd.y+9, self.jd.largura, self.jd.altura):
                    self.jd.health -= 10
                    self.pa.projeteis.remove(p)

            if self.jd.health <= 0:
                self.state = "victory"
            if self.pr.health <=0 and self.pa.health <=0:
                self.state = "GAME OVER"
        elif self.state in ["GAME OVER", "victory"]:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.pr = PowerRosa(30, 100)
                self.pa = PowerAzul(50, 100)
                self.jd = Inimigo(180, 30)
                self.tiros = Tiro(self.jd)
                self.state = "menu"

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "jogo":
            pyxel.cls(0)
            self.jd.draw()
            self.pr.draw()
            self.pa.draw()
            self.tiros.draw()
            draw_health_bar(10, 10, self.pr.health, 14)
            draw_health_bar(10, 20, self.pa.health, 5)
            barra_x = self.jd.x + (self.jd.largura // 2) - (79 // 2) - 4
            barra_y = self.jd.y - 20
            draw_health_bar(barra_x, barra_y, self.jd.health, 13)
        elif self.state == "GAME OVER":
            pyxel.cls(0)
            pyxel.text(100, 50, "GAME OVER", 8)
            pyxel.text(70, 70, "PRESSIONE ENTER PARA VOLTAR AO MENU", 7)
        elif self.state == "victory":
            pyxel.cls(0)
            pyxel.text(95, 50, "MATAMOS O INIMIGO!", 11)
            pyxel.text(70, 70, "PRESSIONE ENTER PARA VOLTAR AO MENU", 7)

# Inicia o jogo
Jogo()


