from src.animate import CreateScene
from manim import tempconfig
from src.simulate import *
from src.my_models import *
import numpy as np



def criar_animacao(sol: SimpleNamespace):
    scene = CreateScene(sol.t, sol.y[0], sol.y[1],
                        len_bloco_a=len_bloco_a(),
                        len_bloco_b=len_mola_b(),                        
                        len_pista=x_esq(),
                        l1_natural=len_mola_a,
                        l2_natural=len_mola_b)
    
    with tempconfig({"quality": "low_quality"}):
        scene.render()

def main():                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    
    #Começar pegando os dados iniciais
    data_ima = get_sol("./experiment_files/data_ima.txt")
    data_mola = get_sol("./experiment_files/data_mola.txt")

    
    #MODELO 1:
    xa = .03
    xb = .4
    va = 0
    vb = 0
    data1 = [xa, xb, va, vb]

    model1 = get_model_1()

    silumacao1 = Simulate(model=model1, inicial_data=data1, t_final=5, simulation_len=500, description = "simulacao1")
    silumacao1.solveRK45()

    # Cria e renderiza a cena
    data_sim1 = get_sol("./simulation_files/simulacao1.dat")


    #----------------------Cria a animação -----------------------------------
    #criar_animacao(data_sim1)

   

if __name__ == "__main__":
    main()