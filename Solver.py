import numpy as np
from numpy.linalg import norm
from scipy import sparse
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve as solve
from time import time_ns as tic, time_ns as toc
from Equations import n, rows, cols, residuals, derivatives


def update(k, r):
    print(f'Iter, Res: {k}, {norm(r)}')


def run_solver_algorithm():
    t0 = tic()
    x = np.ones(n)
    print(f'Solving {n} Equations...')
    k = 0
    tol = 1e-10
    r = residuals(x)
    r_norm = norm(r)
    while r_norm > tol:
        update(k, r)
        v = derivatives(x, r)
        A = sparse.csc_matrix((v, (rows, cols)))
        dx = solve(A, -r)
        xn = x + dx
        rn = residuals(xn)
        rn_norm = norm(rn)
        while rn_norm > r_norm:
            print('Residual Increased! Damping Increased.')
            dx = dx / 2
            xn = x + dx
            rn = residuals(xn)
            if norm(dx / x) < tol:
                print('\n*****Even a tiny step size failed to reduce residual****\n')
                return x, r
        k = k + 1
        x = xn
        r = rn
        r_norm = rn_norm
        if r_norm < tol:
            update(k, r)
            break
    print(f'Solving {n} equations took {(toc()-t0) / 1e6} ms')
    return x, r
