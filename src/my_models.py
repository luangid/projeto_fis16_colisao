
"""

Método de seleção natural -> Método genético

k_aux = 0.00019929656014001004
mi_a = 0.2436596466289415
mi_b = 0.25119718072186403
kmag = 0.0009974787386021545
k1 = 64.65310283725339
k2 = 170.11300389846951

Qui-quadrado: 0.41024110591162394
Grau de liberdade: 1036
p-valor: 1.0
chi/dof: 0.00039197610253796845
"""

"""
k_aux = 0.0019463894572041957
mi_a = 0.40715605386515
mi_b = 0.16090075032935466
kmag = 0.0011568595400724367
k1 = 74.48475415893962
k2 = 210.37593337174815

Qui-quadrado: 0.29204997517556297
Grau de liberdade: 1036
p-valor: 1.0
chi/dof: 0.0002819015204397326
"""


__constantes__ = {
   "massa": .6328,
    "k1": 74.48475415893962,
    "k2":  210.37593337174815,
    "La": .16,
    "Lb": .16,
    "l1": .10,
    "l2": .04,
    "kmag": 0.0011568595400724367, 
    "mi_a": 0.40715605386515,
    "mi_b":  0.16090075032935466,
    "x_esq": 0, 
    "x_dir": 0.88,
    "k_aux": 0.0019463894572041957
    }

__constantes__bkup = {
   "massa": .6328,
    "k1": 68.21074904300337,
    "k2":  157.42099589097114,
    "La": .16,
    "Lb": .16,
    "l1": .10,
    "l2": .04,
    "kmag": 2.7752704293985674e-5, 
    "mi": 0.2325477382032417,
    "x_esq": 0, 
    "x_dir": 0.82,
    "k_aux": 0.0007926794669811548
    }


def massa():
    return __constantes__.get("massa")

def k_mola_a():
    return __constantes__.get("k1")
def k_mola_b():
    return __constantes__.get("k2") 
def len_bloco_a():
    return __constantes__.get("La")
def len_bloco_b():
    return __constantes__.get("Lb")
def len_mola_a():
    return __constantes__.get("l1")
def len_mola_b():
    return __constantes__.get("l2")
def k_magnetico():
    return __constantes__.get("kmag")
def mi_a():
    return __constantes__.get("mi_a")
def mi_b():
    return __constantes__.get("mi_b")
def x_esq():
    return __constantes__.get("x_esq")
def x_dir():
    return __constantes__.get("x_dir")
def k_aux():
    return __constantes__.get("k_aux")


def __model1__(t, data):

        xa, xb, va, vb = data

        def f_mola(x, l, x_lim, k) -> float:
            if x >= l - x_lim:
                return 0
            return -k*(x + x_lim - l) + __constantes__.get("k_aux")/(x + x_lim)                                                                
        
        def f_atrito(v, mi) -> float:
            return -v*mi
       
        def f_magnetica(xa, xb) -> float:
            dist = (xb - __constantes__.get("Lb")) - (xa + __constantes__.get("La"))
            return -__constantes__.get("kmag") / (dist**2)
        

        acel_a = f_mola(xa, __constantes__.get("l1"), __constantes__.get("x_esq"), __constantes__.get("k1"))
        acel_a += f_atrito(va, __constantes__.get("mi_a"))
        acel_a += f_magnetica(xa, xb)
        acel_a /= __constantes__.get("massa")

        acel_b = -f_mola(-xb, __constantes__.get("l2"), __constantes__.get("x_dir"), __constantes__.get("k2"))
        acel_b += f_atrito(vb, __constantes__.get("mi_b"))
        acel_b += -f_magnetica(xa, xb)
        acel_b /= __constantes__.get("massa")

        return [va, vb, acel_a, acel_b]

def get_model_1():
    return __model1__
