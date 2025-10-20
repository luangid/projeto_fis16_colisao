import matplotlib as plt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.optimize import curve_fit
from scipy.integrate import solve_ivp
from scipy.stats import chi2

import numpy as np


from src.simulate import *
from src.my_models import *

file_mola = "./experiment_files/data_mola.txt"
file_ima = "./experiment_files/data_ima.txt"

data_mola = get_sol(file_path=file_mola)

t_mola = np.array((data_mola.y[1] - data_mola.y[1][0]) / 120)
yA_mola = np.array((data_mola.y[0]) * (0.1/125.1))
yB_mola = np.array((data_mola.y[2]) * (0.1/125.1))

vA_mola = np.gradient(yA_mola, t_mola)
vB_mola = np.gradient(yB_mola, t_mola)



#MODELO 1:
xa = yA_mola[0]
xb = yB_mola[0]
va = vA_mola[0]
vb = vB_mola[0]
data1 = [xa, xb, va, vb]

print(f"xa_zero: {xa}")
print(f"xb_zero: {xb}")
print(f"va_zero: {va}")
print(f"vb_zero: {vb}")

"""
k_aux = 0.0031
mi = 0.3330
kmag = 0.0199
k1 = 30.1849
k2 = 74.4762
"""

__constantes__ = {
   "massa": .6328,
    "k1": 52.3246,
    "k2": 198.1295,
    "La": .16,
    "Lb": .16,
    "l1": .10,
    "l2": .04,
    "kmag": 0.0018, 
    "mi": 0.2621,
    "x_esq": 0, 
    "x_dir": 0.88,
    "k_aux": 0.0004
    }


p0 = [__constantes__.get("k_aux"), __constantes__.get("mi"),  __constantes__.get("kmag"),  __constantes__.get("k1"),  __constantes__.get("k2")]

def model1(t, data_inicio, k_aux, mi, kmag, k1, k2):

    xa, xb, va, vb = data_inicio


    def f_mola(x, l, x_lim, k) -> float:
            if x > l - x_lim:
                return 0
            return -k*(x + x_lim - l) + k_aux/(x + x_lim)                                                                
    
    def f_atrito(v) -> float:
        return -v*mi
    
    def f_magnetica(xa, xb) -> float:
        dist = (xb - __constantes__.get("Lb")) - (xa + __constantes__.get("La"))
        return -kmag / (dist**2)
        

    

    acel_a = f_mola(xa, __constantes__.get("l1"), __constantes__.get("x_esq"), k1)
    acel_a += f_atrito(va)
    acel_a += f_magnetica(xa, xb)
    acel_a /= __constantes__.get("massa")

    acel_b = -f_mola(-xb, __constantes__.get("l2"), __constantes__.get("x_dir"), k2)
    acel_b += f_atrito(vb)
    acel_b += -f_magnetica(xa, xb)
    acel_b /= __constantes__.get("massa")

    return [va, vb, acel_a, acel_b]

def model1_sim(t, k_aux, mi, kmag, k1, k2, data_inicio):
    def sistema(t, y):
        xa, xb, va, vb = y
        return model1(t, (xa, xb, va, vb), k_aux, mi, kmag, k1, k2)
    
    sol = solve_ivp(
        sistema,
        [t[0], t[-1]],
        data_inicio,
        t_eval=t,
        method='RK45',
        rtol=1e-6,
        atol=1e-9
    )
    # Verificação extra
    if not sol.success or np.isnan(sol.y).any():
        # evita contaminar o fit
        return np.full((4, len(t)), np.nan)
    
    if not sol.success or sol.y.shape[0] != 4:
        # devolve arrays de NaN para evitar quebrar o curve_fit
        return np.full((4, len(t)), np.nan)
    return sol.y

def modelo_fit(t, k_aux, mi, kmag, k1, k2):
    sol = model1_sim(t, k_aux, mi, kmag, k1, k2, data1)
    # concatena posições dos dois blocos para comparar com dados experimentais
    xa_sim, xb_sim = sol[0], sol[1]
    return np.concatenate([xa_sim, xb_sim])
 

#Sistema de feedback
#-------------------------------------------------------------------------------------------------------
y_total_exp = np.concatenate([yA_mola, yB_mola])

tries = 10

"""
k_aux = 0.0487
mi = 0.1510
kmag = 0.0498
k1 = 57.7754
k2 = 169.505
"""

boundaries = (
    [0, 0, 0, 0, 0],  # limites inferiores
    [1.0, 1.0, 1.0, 300.0, 300.0]   # limites superiores
)

params, covariance = curve_fit(
        modelo_fit,
        t_mola,
        y_total_exp,
        p0=p0, 
        bounds=boundaries,
        maxfev=5000)

max_ite = 50
tolerencia = 1e-4

y_sim_fit = modelo_fit(t_mola, *params)

sigma = np.ones_like(y_sim_fit)
chi2_val = np.sum(((y_total_exp - y_sim_fit) / sigma)**2)
dof = len(y_total_exp) - len(params)  # 6 parâmetros: k_aux, mi, kmag, k1, k2, x_dir

chi2_best = chi2_val
params_best = params.copy()

# p-valor
p_val = chi2.sf(chi2_val, dof)
cont = 0

for i in range(max_ite):
    if chi2_val/dof < tolerencia:
        print("Convergência atingida.")
        break
    
    params, covariance = curve_fit(
            modelo_fit,
            t_mola,
            y_total_exp,
            p0=p0, 
            bounds=boundaries,
            maxfev=5000)

    y_sim_fit = modelo_fit(t_mola, *params)

    sigma = np.ones_like(y_sim_fit)
    chi2_val = np.sum(((y_total_exp - y_sim_fit) / sigma)**2)

    if chi2_val < chi2_best:
        chi2_best = chi2_val
        params_best = params.copy()
        p0 = params_best
        cont = 0
    else:
        cont += 1
        scale = 0.005*cont

        perturbation = np.random.normal(scale=scale*np.abs(params_best))
        p0 = params_best + perturbation

    if i == max_ite - 1:
        print("Número máximo de iterações atingido.")




k_aux, mi, kmag, k1, k2 = params_best
print(f"k_aux = {k_aux:.4f}")
print(f"mi = {mi:.4f}")
print(f"kmag = {kmag:.4f}")
print(f"k1 = {k1:.4f}")
print(f"k2 = {k2:.4f}")
print(f"\nQui-quadrado: {chi2_val:.4f}")
print(f"Grau de liberdade: {dof}")
print(f"p-valor: {p_val:.4f}")
print(f"p-valor: {chi2_best/dof:.4f}")

#print(f"Melhor chi2: {chi2_best:.4f} | chi2/dof: {chi2_best/dof:.4f}")

