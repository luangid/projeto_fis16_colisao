from manim import *

class CreateScene(Scene):
    def __init__(self, t, xA, xB, len_bloco_a=0.11, len_bloco_b=0.11, len_pista=0.5, l1_natural=0.08, l2_natural=0.08,  **kwargs):
        zoom = 10
        
        centralize = len_pista*zoom/2

        
        self.len_bloco_a = len_bloco_a * zoom 
        self.len_bloco_b = len_bloco_b * zoom
        self.inicio = -centralize
        self.len_pista = len_pista * zoom - centralize

        self.t = t
        self.xA = xA * zoom + self.len_bloco_a / 2 - centralize
        self.xB = xB * zoom - self.len_bloco_b / 2 - centralize

        # Comprimentos naturais (ajusta conforme teu modelo físico)
        self.l1_natural = l1_natural * zoom
        self.l2_natural = l2_natural * zoom

        super().__init__(**kwargs)

    def construct(self):
        # Paredes
        parede_esquerda = Rectangle(width=0.02, height=2, color=GRAY, fill_opacity=1).move_to([-0.02 +self.inicio, 0, 0])
        parede_direita = Rectangle(width=0.02, height=2, color=GRAY, fill_opacity=1).move_to([self.len_pista + 0.02, 0, 0])

        # Blocos
        blocoA = Rectangle(width=self.len_bloco_a, height=0.5, color=BLUE, fill_opacity=1).move_to([self.xA[0], 0, 0])
        centroA = Circle(radius=0.02, color=GRAY, fill_opacity=1).move_to([self.xA[0], 0, 0])
        blocoB = Rectangle(width=self.len_bloco_b, height=0.5, color=RED, fill_opacity=1).move_to([self.xB[0], 0, 0])
        centroB = Circle(radius=0.02, color=GRAY, fill_opacity=1).move_to([self.xB[0], 0, 0])

        # Função pra desenhar mola em zigue-zague
        def criar_mola(x1, x2, n_espiras=6, amp=0.15):
            dx = (x2 - x1) / (n_espiras * 2)
            pontos = []
            for i in range(n_espiras * 2 + 1):
                x = x1 + i * dx
                y = amp * ((-1) ** i) if 0 < i < n_espiras * 2 else 0
                pontos.append([x, y, 0])
            return VMobject().set_points_smoothly(pontos).set_stroke(color=GRAY, width=2)

        # Função que decide onde desenhar a mola da esquerda
        def mola_esquerda_dinamica():
            x_bloco = blocoA.get_left()[0]
            # Se a distância até a parede for menor que o comprimento natural, a mola encosta na parede
            if x_bloco - (self.inicio-0.02) <= self.l1_natural:
                x_inicial = self.inicio - 0.02
                x_final = x_bloco
            else:
                # Se o bloco estiver longe, a mola “descola” da parede e fica colada no bloco
                x_final = x_bloco
                x_inicial = x_final - self.l1_natural
            return criar_mola(x_inicial, x_final)

        # Mesmo raciocínio para a mola direita
        def mola_direita_dinamica():
            x_bloco = blocoB.get_right()[0]
            if (self.len_pista + 0.02) - x_bloco <= self.l2_natural:
                x_inicial = x_bloco
                x_final = self.len_pista + 0.02
            else:
                x_inicial = x_bloco
                x_final = x_inicial + self.l2_natural
            return criar_mola(x_inicial, x_final)

        mola_esq = always_redraw(mola_esquerda_dinamica)
        mola_dir = always_redraw(mola_direita_dinamica)

        # Adiciona tudo
        # Agrupa todo o sistema
        """
        sistema = VGroup(
            parede_esquerda,
            parede_direita,
            blocoA,
            blocoB,
            centroA,
            centroB,
            mola_esq,
            mola_dir
        )
        """
        # Move todo o sistema 5 unidades para a esquerda
        #sistema.shift(LEFT * 5)

        # Adiciona o sistema à cena
        #self.add(sistema)
        self.add(parede_esquerda, parede_direita, mola_esq, mola_dir, blocoA, blocoB, centroA, centroB)

        # Anima conforme os dados simulados
        dt = self.t[1] - self.t[0]
        for i in range(1, len(self.t)):
            self.play(
                blocoA.animate.move_to([self.xA[i], 0, 0]),
                blocoB.animate.move_to([self.xB[i], 0, 0]),
                centroA.animate.move_to([self.xA[i], 0, 0]),
                centroB.animate.move_to([self.xB[i], 0, 0]),
                run_time=dt,
                rate_func=linear
            )

        self.wait()
