from animate import CreateScene
from manim import tempconfig
from simulate import *
import numpy as np

def main():                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    

    #Começar pegando os dados iniciais
    #definição de constantes
    constantes = {
        "massa": .2,
        "k1": 50,
        "k2": 50,
        "La": .11,
        "Lb": .11,
        "l1": .1,
        "l2": .1,
        "kmag": 2e-4, 
        "mi": 0.1,
        "x_esq": 0, 
        "x_dir": .6,
        "k_aux": .001}
    
    #MODELO 1:
    xa = .05
    xb = .4
    va = 0
    vb = 0
    data1 = [xa, xb, va, vb]

    def model1(t, data):

        xa, xb, va, vb = data

        def f_mola(x, l, x_lim, k) -> float:
            if x > l - x_lim:
                return 0
            return -k*(x + x_lim - l) + constantes.get("k_aux")/(x + x_lim)                                                                
        
        def f_atrito(v) -> float:
            return -v*constantes.get("mi")
       
        def f_magnetica(xa, xb) -> float:
            dist = (xb - constantes.get("Lb")) - (xa + constantes.get("La"))
            return -constantes.get("kmag") / (dist**2)
        

        acel_a = f_mola(xa, constantes.get("l1"), constantes.get("x_esq"), constantes.get("k1"))
        acel_a += f_atrito(va)
        acel_a += f_magnetica(xa, xb)
        acel_a /= constantes.get("massa")

        acel_b = -f_mola(-xb, constantes.get("l2"), constantes.get("x_dir"), constantes.get("k2"))
        acel_b += f_atrito(vb)
        acel_b += -f_magnetica(xa, xb)
        acel_b /= constantes.get("massa")

        return [va, vb, acel_a, acel_b]

    silumacao1 = Simulate(model=model1, inicial_data=data1, t_final=5, simulation_len=300, description = "simulacao1")
    silumacao1.solveRK45()

    # Cria e renderiza a cena
    sol = get_sol("./simulation_files/simulacao1.dat")

    scene = CreateScene(sol.t, sol.y[0], sol.y[1],
                        len_bloco_a=constantes.get("La"),
                        len_bloco_b=constantes.get("Lb"),
                        len_pista=constantes.get("x_dir"))
    
    with tempconfig({"quality": "low_quality"}):
        scene.render()

if __name__ == "__main__":
    main()