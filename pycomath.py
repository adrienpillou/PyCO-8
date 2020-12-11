# Pico math library
import math
import random

def atan2(dx, dy):
    # To fix : wrong return value
    ans = math.atan2(dx, dy)
    value = f"{ans:.3f}"
    return float(value)

def band():
    pass

def bnot():
    pass

def bor():
    pass

def bxor():
    pass

def ceil(x):
    return round(x)

def cos(angle):
    # (0 ; 1) => (-1 ; 1)
    angle = (angle*2*math.pi)/1
    ans = math.cos(angle)
    value = f"{ans:.4f}"
    return float(value)

def flr(x):
    return int(x)

def max(x, y):
    if x < y:
        return y
    else:
        return x

def mid(a, b, c):
    if(b<a):
        return a
    elif (b>c):
        return c
    else:
        return b

def min(x, y):
    if x > y:
        return y
    else:
        return x

def rnd(b=1):
    return random.uniform(0,b)

def sgn(number):
    if number >= 0:
        return 1
    else:
        return -1

def shl():
    pass

def shr():
    pass

def sin(angle):
    # (0 ; 1) => (-1 ; 1)
    angle = (angle*2*math.pi)/1
    ans = -math.sin(angle)
    value = f"{ans:.4f}"
    return float(value)

def sqrt(num):
    return math.sqrt(num)

def srand(val):
    random.seed(val)
