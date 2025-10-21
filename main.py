from src.animate import CreateScene
from src.animate import CreateScene_2
from manim import tempconfig
from src.simulate import *
from src.my_models import *
import numpy as np
from scipy.interpolate import interp1d



def criar_animacao(sol: SimpleNamespace):
    scene = CreateScene(sol.t, sol.y[0], sol.y[1],
                        len_bloco_a=len_bloco_a(),
                        len_bloco_b=len_bloco_b(),                        
                        len_pista=x_dir(),
                        l1_natural=len_mola_a(),
                        l2_natural=len_mola_b())
    
    with tempconfig({"quality": "medium_quality"}):
        scene.render()

def criar_animacao_2(sim: SimpleNamespace, exp_t, exp_x_a, exp_x_b):

    # Eixo original e novo eixo
    # Cria função de interpolação para os dados experimentais
    interp_exp_a = interp1d(exp_t,exp_x_a, kind='cubic', fill_value='extrapolate')
    interp_exp_b = interp1d(exp_t, exp_x_b, kind='cubic', fill_value='extrapolate')
# Reamostra o vetor experimental no mesmo eixo do vetor simulado
    exp_x_a_int = interp_exp_a(sim.t)
    exp_x_b_int = interp_exp_b(sim.t)

    scene = CreateScene_2(sim.t, sim.y[0], sim.y[1], exp_x_a_int, exp_x_b_int,
                        len_bloco_a=len_bloco_a(),
                        len_bloco_b=len_bloco_b(),                        
                        len_pista=x_dir(),
                        l1_natural=len_mola_a(),
                        l2_natural=len_mola_b())
    
    with tempconfig({"quality": "medium_quality"}):
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
    va = 0
    vb = 0
    data1 = [xa, xb, va, vb]

    t_final = t_mola[-1]

    print(data1)

    model1 = get_model_1()
    silumacao1 = Simulate(model=model1, inicial_data=data1, t_final=t_final, simulation_len=550, description = "simulacao1")
    silumacao1.solveRK45()

    data_sim1 = get_sol("./simulation_files/simulacao1.dat")
    

    #----------------------Cria a animação -----------------------------------
    criar_animacao_2(data_sim1, t_mola, yA_mola, yB_mola)
    #criar_animacao(data_mola)

   

if __name__ == "__main__":
    main()