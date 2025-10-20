
"""
k_aux = 0.0026
mi = 0.2726
kmag = 0.0011
k1 = 62.4839
k2 = 181.1594

Qui-quadrado: 0.4240
Grau de liberdade: 1055
p-valor: 1.0000
p-valor: 0.0004

"""


__constantes__ = {
   "massa": .6328,
    "k1": 62.4839,
    "k2":  181.1594,
    "La": .16,
    "Lb": .16,
    "l1": .10,
    "l2": .04,
    "kmag": 0.0001, 
    "mi": 0.2726,
    "x_esq": 0, 
    "x_dir": 0.88,
    "k_aux": 0.0026
    }

__constantes__bkup = {
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
def mi():
    return __constantes__.get("mi")
def x_esq():
    return __constantes__.get("x_esq")
def x_dir():
    return __constantes__.get("x_dir")
def k_aux():
    return __constantes__.get("k_aux")


def __model1__(t, data):

        xa, xb, va, vb = data

        def f_mola(x, l, x_lim, k) -> float:
            if x > l - x_lim:
                return 0
            return -k*(x + x_lim - l) + __constantes__.get("k_aux")/(x + x_lim)                                                                
        
        def f_atrito(v) -> float:
            return -v*__constantes__.get("mi")
       
        def f_magnetica(xa, xb) -> float:
            dist = (xb - __constantes__.get("Lb")) - (xa + __constantes__.get("La"))
            return -__constantes__.get("kmag") / (dist**2)
        

        acel_a = f_mola(xa, __constantes__.get("l1"), __constantes__.get("x_esq"), __constantes__.get("k1"))
        acel_a += f_atrito(va)
        acel_a += f_magnetica(xa, xb)
        acel_a /= __constantes__.get("massa")

        acel_b = -f_mola(-xb, __constantes__.get("l2"), __constantes__.get("x_dir"), __constantes__.get("k2"))
        acel_b += f_atrito(vb)
        acel_b += -f_magnetica(xa, xb)
        acel_b /= __constantes__.get("massa")

        return [va, vb, acel_a, acel_b]

def get_model_1():
    return __model1__
