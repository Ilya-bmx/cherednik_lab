import random

fi_file = open('functions/fi.txt', 'w+')
# матрица 2 на 2^8
for i in range(2 ** 8):
    fi_file.write(str(random.randint(0, 100) % 2))
    fi_file.write(' ')
    fi_file.write(str(random.randint(0, 100) % 2))
    fi_file.write('\n')

psi_file = open('functions/psi.txt', 'w+')
# матрица 2 на 2^8
for i in range(2 ** 8):
    psi_file.write(str(random.randint(0, 100) % 2))
    psi_file.write(' ')
    psi_file.write(str(random.randint(0, 100) % 2))
    psi_file.write('\n')
