import scipy.stats as stats
from scipy.integrate import solve_ivp
from scipy import interpolate
import numpy as np
from types import SimpleNamespace



class Simulate:
    def __init__(self, model, inicial_data, t_final, simulation_len, description="teste"):
        self.model = model
        self.inicial_data = inicial_data
        self.t_final = t_final
        self.simulation_len = simulation_len
        self.file_name = f'./simulation_files/{description}.dat'

        with open(self.file_name, 'w') as f:
            f.write(f"Model: {description}\n")        
            f.write(f"t        x_a        x_b        v_a        v_b\n")

    
    def get_file_name(self):
        return self.file_name
    
    def solveRK45(self): 
        t_eval = np.linspace(0, self.t_final, self.simulation_len)
        sol = solve_ivp(
            self.model,
            [0, self.t_final],
            self.inicial_data,
            t_eval=t_eval,
            method="RK45",
            rtol=1e-5,
            atol=1e-8
        )      
        
        print("Resolvi")
        print(sol)

        with open(self.file_name, "a") as f:
            for i in range(len(sol.t)):
                f.write(f"{sol.t[i]}  {sol.y[0][i]}  {sol.y[1][i]}  {sol.y[2][i]}  {sol.y[3][i]}\n")



def get_sol(file_path: str) -> SimpleNamespace:
    
    """
    Lê um arquivo de dados com cabeçalho de 2 linhas no formato:
    t  x  y  vx  vy ...
    e retorna um objeto sol com atributos sol.t e sol.x (igual ao solve_ivp).
    """
    dados = np.loadtxt(file_path, skiprows=2)
    sol = SimpleNamespace()
    sol.t = dados[:, 0]      # primeira coluna -> tempo
    sol.x = dados[:, 1:].T
    sol.y = sol.x

    return sol