import matplotlib as plt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


from simulate import *


file_path = "./simulation_files/simulacao1.dat"

f = open(file_path, "rt")

data_sim = get_sol(file_path=file_path)


t = data_sim.t
yA = data_sim.y[0]
yB = data_sim.y[1]

# Criação dos subplots: 2 linhas, 1 coluna
fig, axs = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

# --- Bloco A ---
axs[0].plot(t, yA, label="Bloco A", color="tab:blue")
axs[0].set_ylabel("Posição (m)")
axs[0].legend()
axs[0].grid(True)

# --- Bloco B ---
axs[1].plot(t, yB, label="Bloco B", color="tab:orange")
axs[1].set_xlabel("Tempo (s)")
axs[1].set_ylabel("Posição (m)")
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.show()

f.close()