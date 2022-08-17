import re
import numpy as np
from time import time_ns as tic, time_ns as toc


def functions():
    return ['sqrt', 'cos', 'sin', 'tan', 'arcsin', 'arccos', 'arctan', 'exp', 'log', 'log10']


def functions_string():
    string = ''
    for func in functions():
        string = f'{string}{func}, '
    string = string[0:-2]
    return string


def read_lines():
    file_name = 'Equations.rkm'
    file_object = open(file_name, 'r')
    lines = file_object.read()
    lines = lines.lower()
    lines = lines.split('\n')
    return lines


def duplicate_lines(lines, var=None, start=None, stop=None):
    n_lines = None
    n_start = None
    insert_lines = []
    for k, line in enumerate(lines):
        if line[0:9] == 'duplicate':
            line = line.replace('duplicate ', '')
            line = line.split('=')
            var = line[0]
            start, stop = line[1].split(',')
            insert_lines, n_lines = duplicate_lines(lines[k+1:-1], var, start, stop)
            for m in range(k, k+n_lines):
                lines[m] = '~'
            n_start = k
        if line[0:3] == 'end':
            dup_lines = []
            n_lines = len(lines) + 1
            for m in range(int(start), int(stop) + 1):
                for dup_line in lines[:-1]:
                    dup_line = dup_line.replace(var, str(m))
                    dup_lines.append(dup_line)
            lines = dup_lines
            break
    for k in reversed(range(len(lines))):
        if lines[k] == '~':
            lines.pop(k)
    if n_start:
        lines_before = lines[0:n_start]
        lines_after = lines[n_start:]
        lines_before.extend(insert_lines)
        lines_before.extend(lines_after)
        lines = lines_before
    #lines.extend(insert_lines)
    for k, line in enumerate(lines):
        start_indexes = []
        end_indexes = []
        new_line = line
        for m, letter in enumerate(line):
            if letter == '[':
                start_indexes.append(m)
            if letter == ']':
                end_indexes.append(m)
        for m, start_index in enumerate(start_indexes):
            text = line[slice(start_index, end_indexes[m]+1)]
            new_line = new_line.replace(text, '[' + str(eval(text[1:-1])) + ']')
        lines[k] = new_line
    return lines, n_lines


def remove_blank_lines(lines):
    blank_lines = []
    for lin, line in enumerate(lines):
        line = line.replace(' ', '')
        if line == '' or line[0] == '#' or line[0] == '%':
            blank_lines.append(lin)
        else:
            lines[lin] = line
    for blank_line in reversed(blank_lines):
        lines.pop(blank_line)
    return lines


def parse_lines(lines):
    # Process Lines
    n = 0
    var_indexes = []
    unique_values = []
    unique_dict = dict()
    operators = ['+', '-', '*', '/', '^', '**']
    numbers = str([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    operators.reverse()
    for lin, line in enumerate(lines):
        line = line.replace(' ', '')
        new_line = line
        line = line.replace('(', '')
        line = line.replace(')', '')
        for func in functions():
            line = line.replace(func, '')
        for operator in operators:
            line = line.replace(operator, '=')
        line = line.split('=')
        var_index = []
        for k, var in enumerate(line):
            if var[0] in numbers:
                continue
            elif var not in unique_dict:
                index = len(unique_values)
                unique_values.append(var)
                unique_dict[f'{var}'] = n
                n += 1
            else:
                index = unique_dict[f'{var}']
            var_index.append(index)
            new_line = new_line.replace(var, f'~[{index}]')
        new_line = new_line.replace('~', 'x')
        new_line = new_line.replace('^', '**')
        new_line = new_line.split('=')
        new_line = new_line[0] + ' - (' + new_line[1] + ')'
        lines[lin] = new_line
        var_indexes.append(var_index)
    return lines, var_indexes


def get_gradient(lines, var_indexes, tolerance):
    rows = []
    cols = []
    gradient_lines = []
    for row, var_index in enumerate(var_indexes):
        line = lines[row]
        for col, index in enumerate(var_index):
            var = f'x[{index}]'
            #gradient_line = '(' + line.replace(f'{var}', f'({1+tolerance} * {var})') + f' - (r[{row}])) / {tol}'
            gradient_line = line.replace(f'{var}', f'({1 + tolerance} * {var})')
            gradient_lines.append(gradient_line)
            rows.append(row)
            cols.append(index)
    return gradient_lines, rows, cols


def write_module(rows, cols, residuals, derivatives):
    equation_filename = 'Equations.py'
    equation_file = open(equation_filename, 'w')
    equation_file.write('')
    equation_file = open(equation_filename, 'a')
    #equation_file.write('from numba import jit\n')
    equation_file.write('import numpy as np\n')
    equation_file.write(f'from numpy import {functions_string()}\n\n\n')
    equation_file.write(f'n = {len(residuals)}\n\n')
    equation_file.write(f'tol = {tol}\n\n')
#    equation_file.write(f'indexes = {nonzero_indexes}\n\n')
    equation_file.write(f'rows = {rows}\n')
    equation_file.write(f'cols = {cols}\n\n\n')
    #equation_file.write('residuals = [0]\n')
    #equation_file.write('@jit(nopython=True)\n')
    equation_file.write(f'def residuals(x):\n')
    #equation_file.write(f'    r = {len(residuals)} * [0]\n')
    equation_file.write(f'    r = np.zeros({len(residuals)})\n')
    for k, residual in enumerate(residuals):
        #equation_file.write(f'residuals.append(lambda x: {residual})\n')
        equation_file.write(f'    r[{k}] = {residual}\n')
    equation_file.write('    return r\n\n\n')
    #equation_file.write('derivatives = []\n')
    #equation_file.write('@jit(nopython=True)\n')
    equation_file.write('def derivatives(x, r):\n')
    #equation_file.write(f'    drdx = {len(derivatives)} * [0]\n')
    equation_file.write(f'    drdx = np.zeros({len(derivatives)})\n')
    for k, derivative in enumerate(derivatives):
        #equation_file.write(f'derivatives.append(lambda x, residuals: {derivative})\n')
        equation_file.write(f'    drdx[{k}] = {derivative}\n')
    equation_file.write(f'    drdx = (drdx - r[rows])/(tol * x[{rows}])\n')
    equation_file.write('    return drdx\n')
    equation_file.close()


# Code to Execute on Import
t0 = tic()
tol = 1e-3
equations = read_lines()
#equations, _ = duplicate_lines(equations)
equations = remove_blank_lines(equations)
[equations, indexes] = parse_lines(equations)
gradients, rows, cols = get_gradient(equations, indexes, tol)
write_module(rows, cols, equations, gradients)
print(f'Processing {len(equations)} Equations took {(toc()-t0)/1e6} ms')