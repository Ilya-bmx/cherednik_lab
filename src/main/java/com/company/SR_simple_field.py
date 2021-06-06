import copy
import time
import random


class SR:
    def __init__(self, p, start_s, mode, fi_file, psi_file):
        self.p = p
        self.s = start_s
        self.mode = mode
        if mode == 'table':
            self.fi = self.import_function(fi_file)
            self.psi = self.import_function(psi_file)
        elif mode == 'analytical':
            pass

    def step(self, x):
        y = self.f(x)
        self.h(x)
        self.mod()
        return y % self.p

    def several_steps(self, several_x):
        several_y = []
        for x in several_x:
            several_y.append(self.step(x))
        return several_y

    # фи
    def h(self, x):
        if self.mode == 'table':
            self.shift(self.fi_table(x))
        elif self.mode == 'analytical':
            self.shift(self.fi_anal(x))

    # пси
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

    def mod(self):
        for i in range(len(self.s)):
            self.s[i] %= self.p

    def fi_anal(self, x):
        return self.s[2] + self.s[3] + x

    def psi_anal(self, fi_x):
        return self.s[0] + self.s[2] + 1 + fi_x

    def fi_table(self, x):
        line = self.rs_to_number()
        column = x
        return self.fi[line][column]

    def psi_table(self, fi_x):
        line = self.rs_to_number()
        column = fi_x
        return self.psi[line][column]

    def rs_to_number(self):
        result = 0
        for i in range(len(self.s)):
            result += self.s[i] * self.p ** (len(self.s) - i - 1)
        return result

    def import_function(self, file_name):
        file = open(file_name, "r")
        a = []
        n = 0
        flag = 0
        number = 0
        for line in file:
            if line != "\n":
                a.append([])
                for i in range(len(line)):
                    if line[i] != "\n" and line[i] != " ":
                        number = number * 10 + int(line[i])
                        flag = 1
                    elif flag == 1:
                        a[n].append(number)
                        number = 0
                n += 1
        return a


def to_bin(a, r):
    result = []
    for i in range(r):
        result.append(a % 2)
        a = a // 2
    result.reverse()
    return result


#  Получает на вход число в двоичной системе счисления, в виде списка
#  Возвращает число в десятичной системе счисления
def from_bin(a):
    result = 0
    for i in range(len(a)):
        result += a[i] * 2 ** (len(a) - i - 1)
    return result

ln = 5  # Длина входной последовательности
rn = 4  # Размер регистра
