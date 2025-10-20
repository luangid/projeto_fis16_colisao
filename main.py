from src.animate import CreateScene
from manim import tempconfig
from src.simulate import *
from src.my_models import *
import numpy as np



def criar_animacao(sol: SimpleNamespace):
    scene = CreateScene(sol.t, sol.y[0], sol.y[1],
                        len_bloco_a=len_bloco_a(),
                        len_bloco_b=len_bloco_b(),                        
                        len_pista=x_dir(),
                        l1_natural=len_mola_a(),
                        l2_natural=len_mola_b())
    
    with tempconfig({"quality": "low_quality"}):
        scene.render()

def main():                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    
    #Começar pegando os dados iniciais
    data_ima = get_sol("./experiment_files/data_ima.txt")
    data_mola = get_sol("./experiment_files/data_mola.txt")

    
    #MODELO 1:
    #Dados iniciais
    
    file_mola = "./experiment_files/data_mola.txt"

    data_mola = get_sol(file_path=file_mola)

    t_mola = (data_mola.y[1] - data_mola.y[1][0]) / 120
    yA_mola = (data_mola.y[0]) * (0.1/125.1)
    yB_mola = (data_mola.y[2]) * (0.1/125.1)

    vA_mola = np.gradient(yA_mola, t_mola)
    vB_mola = np.gradient(yB_mola, t_mola)
    
    xa = yA_mola[0]
    xb = yB_mola[0]
    va = vA_mola[0]
    vb = vB_mola[0]
    data1 = [xa, xb, va, vb]

    t_final = t_mola[-1]

    print(data1)

    model1 = get_model_1()
    silumacao1 = Simulate(model=model1, inicial_data=data1, t_final=t_final, simulation_len=550, description = "simulacao1")
    silumacao1.solveRK45()

    data_sim1 = get_sol("./simulation_files/simulacao1.dat")
    

    #----------------------Cria a animação -----------------------------------
    criar_animacao(data_sim1)

   

if __name__ == "__main__":
    main()