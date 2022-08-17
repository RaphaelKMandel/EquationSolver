# Imports
from Initialize import init, tic, t0
import WriteEquations
from Solver import run_solver_algorithm
import numpy as np


# Main Code
x, r = run_solver_algorithm()
print(f'Total Runtime: {(tic()-t0)/1e6} ms')
