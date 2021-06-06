import numpy as np


class SRp:
    def __init__(self, deg, start_s, mode, fi_file, psi_file):
        self.p = 2
        self.deg = deg
        self.s = start_s
        self.mode = mode

        if mode == 'table':
            self.fi = self.import_function(fi_file)
            self.psi = self.import_function(psi_file)
        elif mode == 'analytical':
            pass

        self.irreducible = {2: np.poly1d([1, 1, 1]),  # Неприводимые многочлены
                            4: np.poly1d([1, 0, 0, 1, 1]),
                            8: np.poly1d([1, 0, 0, 0, 1, 1, 0, 1, 1]),
                            16: np.poly1d([1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1])}

    def step(self, x):
        y = self.f(x)
        self.h(x)
        self.mod2()
        return self.mod2_p(y)

    def h(self, x):
        if self.mode == 'table':
            self.shift(self.fi_table(x))
            self.mod_p()
        elif self.mode == 'analytical':
            self.shift(self.fi_anal(x))

    def f(self, x):
        if self.mode == 'table':
            return self.psi_table(self.fi_table(x))
        elif self.mode == 'analytical':
            return self.psi_anal(self.fi_anal(x))

    def shift(self, x):
        output = self.s[0]

        for i in range(0, len(self.s) - 1):
            self.s[i] = self.s[i + 1]
        self.s[len(self.s) - 1] = x

        return output

    def mod2(self):  # Приводит коэффициенты полиномов регистра по модулю 2
        for i in range(len(self.s)):
            self.s[i] = self.mod2_p(self.s[i])

    def mod2_p(self, p):  # Приводит коэффициенты полинома по модулю 2
        for i in range(len(p)):
            p[i] %= self.p
        return p

    def fi_table(self, x):
        line = self.rs_to_number()
        column = self.polynom_to_number(x)
        # print('fi line', line)
        # print('fi column', column)
        return self.fi[line][column]

    def psi_table(self, fi_x):
        line = self.rs_to_number()
        column = self.polynom_to_number(fi_x)
        # print('psi line', line)
        # print('psi column', column)
        return self.psi[line][column]

    def fi_anal(self, x):  # Функция фи, возвращает число
        return self.s[2] + self.s[3] + x

    def psi_anal(self, fi_x):  # Функция пси, возвращает число
        return self.s[0] + self.s[2] + 1 + fi_x

    def polynom_to_number(self, a):
        result = 0
        for i in range(len(a)):
            result += a[i] * (2 ** (len(a) - i - 1))
        return result

    def rs_to_number(self):
        result = 0
        for i in range(len(self.s)):
            # print(self.polynom_to_number(self.s[i]), '*', 2 ** self.deg, '**', (len(self.s) - i - 1))
            result += self.polynom_to_number(self.s[i]) * (2 ** (self.deg + 1)) ** (len(self.s) - i - 1)
        return result

    def mod_p(self):  # Приводит все полиномы регистра по модулю неприводимого многочлена
        for i in range(len(self.s)):
            p = np.poly1d(self.s[i])  # Преобразуем ячеку регистра из массива в poly1d
            p = (p / self.irreducible[self.deg])[1]  # Приводим по модулю неприводимого многочлена
            p = np.array(p)  # Преобразуем обратно в array
            p = np.int8(p)  # Преобразуем коэффициенты из numpy.float64 в int8
            self.s[i] = p

    def import_function(self, file_name):
        file = open(file_name, "r")
        a = []
        counter = 0
        for line in file:
            a.append([])
            for s in line:
                if s != ' ' and s != '\n':
                    a[counter].append(int(s))
            counter += 1

        b = []
        column = 2 ** (self.deg + 1)
        for i in range(len(a)):
            b.append([])
            b[i] = np.array_split(a[i], column)
        return b


fi_file = 'simple field test/fi.txt'
psi_file = 'simple field test/psi.txt'
sr = SRp(2, [np.array([1, 0, 1]), np.array([0, 1, 1])], 'table', fi_file, psi_file)
print('psi: ', sr.psi)
print('fi: ', sr.fi)
print('Start S: ', sr.s)
print('------------------------------------------')
print('X:', np.array([1, 0, 1]))
print('Y: ', sr.step(np.array([1, 0, 1])))
print('New S: ', sr.s)
print('------------------------------------------')
print('X:', np.array([1, 1, 1]))
print('Y: ', sr.step(np.array([1, 1, 1])))
print('New S: ', sr.s)
print('------------------------------------------')
print('X:', np.array([0, 0, 1]))
print('Y: ', sr.step(np.array([0, 0, 1])))
print('New S: ', sr.s)
print('------------------------------------------')
print('X:', np.array([1, 0, 0]))
print('Y: ', sr.step(np.array([1, 0, 0])))
print('New S: ', sr.s)
print('------------------------------------------')
print('X:', np.array([0, 0, 1]))
print('Y: ', sr.step(np.array([0, 0, 1])))
print('New S: ', sr.s)
print('------------------------------------------')
print('X:', np.array([1, 1, 1]))
print('Y: ', sr.step(np.array([1, 1, 1])))
print('New S: ', sr.s)
print('------------------------------------------')
print('X:', np.array([0, 0, 0]))
print('Y: ', sr.step(np.array([0, 0, 0])))
print('New S: ', sr.s)
print('------------------------------------------')
print('X:', np.array([1, 0, 1]))
print('Y: ', sr.step(np.array([1, 0, 1])))
print('New S: ', sr.s)
print('------------------------------------------')
print('X:', np.array([1, 1, 1]))
print('Y: ', sr.step(np.array([1, 1, 1])))
print('New S: ', sr.s)
