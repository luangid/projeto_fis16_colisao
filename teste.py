import matplotlib as plt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from src.simulate import *
from src.my_models import *



file_mola = "./experiment_files/data_mola.txt"

data_mola = get_sol(file_path=file_mola)

t_mola = (data_mola.y[1] - data_mola.y[1][0]) / 120
yA_mola = (data_mola.y[0] - data_mola.y[0][0]) * (0.1/125.1)
yB_mola = (data_mola.y[2] - data_mola.y[0][0]) * (0.1/125.1)

vA_mola = np.gradient(yA_mola, t_mola)
vB_mola = np.gradient(yB_mola, t_mola)


#model1 = get_model_1()
#silumacao1 = Simulate(model=model1, inicial_data=data1, t_final=5, simulation_len=500, description = "simulacao1")


file_sim = "./simulation_files/simulacao1.dat"

f = open(file_sim, "rt")

data_sim = get_sol(file_path=file_sim)

t_sim = data_sim.t
y_sim_a = data_sim.y[0]
y_sim_b = data_sim.y[1]

"""
# Criação dos subplots:  linhas,  coluna
fig, axs = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

#axs[0].plot(t, yA, label="Bloco A", color="tab:blue")
axs[0].plot(t_mola, yA_mola, label="Experimento Mola - BLOCA A", color="tab:blue")
axs[0].plot(t_mola, yB_mola, label="Experimento Mola - BLOCO B", color="tab:red")
axs[0].set_xlabel("Tempo (s)")
axs[0].set_ylabel("Posição (m)")
axs[0].legend()
axs[0].grid(True)


#axs[0].plot(t, yA, label="Bloco A", color="tab:blue")
axs[1].plot(t_sim, y_sim_a, label="Simulalção Mola - BLOCA A", color="tab:blue")
axs[1].plot(t_sim, y_sim_b, label="Simulalção Mola - BLOCO B", color="tab:red")
axs[1].set_xlabel("Tempo (s)")
axs[1].set_ylabel("Posição (m)")
axs[1].legend()
axs[1].grid(True)
"""

plt.figure(figsize=(10, 6))
plt.plot(t_mola, yA_mola, label="Experimento Mola - BLOCA A", color="tab:blue")
plt.plot(t_mola, yB_mola, label="Experimento Mola - BLOCO B", color="tab:red")
plt.plot(t_sim, y_sim_a, label="Simulalção Mola - BLOCA A", color="tab:blue", linestyle='dashed')
plt.plot(t_sim, y_sim_b, label="Simulalção Mola - BLOCO B", color="tab:red", linestyle='dashed')
plt.xlabel("Tempo (s)")
plt.ylabel("Posição (m)")
plt.legend()
plt.grid(True)
# --- Bloco A ---


plt.tight_layout()
plt.show()

f.close()