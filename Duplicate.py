equation_filename = 'Equations.rkm'
equation_file = open(equation_filename, 'w')
equation_file.write('')
equation_file = open(equation_filename, 'a')

N = 100000
for i in range(N):
    if i == 0:
        equation_file.write(f'x{i}=10\n')
    elif i == N-1:
        equation_file.write(f'x{i}=x{i-1}')
    else:
        equation_file.write(f'2*x{i}=x{i-1}+x{i+1}\n')
equation_file.close()
