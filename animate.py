from manim import *
from manim import config
from types import SimpleNamespace


class CreateScene(Scene):
    def __init__(self, t, xA, xB, len_bloco_a = .11, len_bloco_b = .11, len_pista = .5, **kwargs):
        
        self.len_bloco_a = len_bloco_a * 10
        self.len_bloco_b = len_bloco_b * 10
        self.len_pista = len_pista * 10

        self.t = t
        self.xA = xA*10 + self.len_bloco_a/2
        self.xB = xB*10 - self.len_bloco_b/2

        super().__init__(**kwargs)

    def construct(self):

        parede_esquerda = Rectangle(width=0.02, height=2, color=GRAY, fill_opacity=1).move_to([0 + self.len_bloco_a/2 - 0.02, 0, 0])
        parede_direita = Rectangle(width=0.02, height=2, color=GRAY, fill_opacity=1).move_to([self.len_pista - self.len_bloco_b/2 + 0.02, 0, 0])

        blocoA = Rectangle(width=self.len_bloco_a, height=0.5, color=BLUE, fill_opacity=1).move_to([self.xA[0], 0, 0])
        #centroA  = Circle(radius=0.02, color=GRAY, fill_opacity=1).move_to[self.xA[0], 0, 0]
        blocoB = Rectangle(width=self.len_bloco_b, height=0.5, color=RED, fill_opacity=1).move_to([self.xB[0], 0, 0])
        #centroB  = Circle(radius=0.02, color=GRAY, fill_opacity=1).move_to[self.xB[0], 0, 0]

        #self.add(parede_esquerda, parede_direita, blocoA, blocoB, centroA, centroB)
        self.add(parede_esquerda, parede_direita, blocoA, blocoB)

        dt = (self.t[1] - self.t[0])*2.5
        for i in range(1, len(self.t)):
            self.play(
                blocoA.animate.move_to([self.xA[i], 0, 0]),
                blocoB.animate.move_to([self.xB[i], 0, 0]),
                
                #centroA.animate.move_to([self.xA[i], 0, 0]),
                #centroB.animate.move_to([self.xB[i], 0, 0]),

                run_time=dt,
                rate_func=linear
            )
        self.wait()
    