import random
import math

def uniform():
    return random.random()

def exp(l: float):
    U = random.random()
    return -1/l* math.log(U)

def normal(miu:float, var:float ):
    sd = math.sqrt(var)
    return std_normal()*sd + miu

def std_normal():
    Y1 = 1
    Y2 = 0
    while( Y2 - (Y1 - 1)**2/2  <=0):
        Y1 = exp(1)
        Y2 = exp(1)

    U = random.random()
    Z = Y1
    if(U > 1/2):
        Z*=-1
    return Z