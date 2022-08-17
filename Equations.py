import numpy as np
from numpy import sqrt, cos, sin, tan, arcsin, arccos, arctan, exp, log, log10


n = 1

tol = 0.001

rows = [0, 0, 0]
cols = [0, 0, 0]


def residuals(x):
    r = np.zeros(1)
    r[0] = 4**x[0]+6**x[0] - (9**x[0])
    return r


def derivatives(x, r):
    drdx = np.zeros(3)
    drdx[0] = 4**(1.001 * x[0])+6**(1.001 * x[0]) - (9**(1.001 * x[0]))
    drdx[1] = 4**(1.001 * x[0])+6**(1.001 * x[0]) - (9**(1.001 * x[0]))
    drdx[2] = 4**(1.001 * x[0])+6**(1.001 * x[0]) - (9**(1.001 * x[0]))
    drdx = (drdx - r[rows])/(tol * x[[0, 0, 0]])
    return drdx
