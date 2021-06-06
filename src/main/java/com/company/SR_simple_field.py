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


def split(a, k,
          sr):  # Принимает на вход массив и возвращает двумерный массив-разбиение исходного на классы k-эквивалентности
    b = [[a[0]]]

    for i in range(1, len(a)):  # Проходим по всем элементав в "а", начиная с первого
        flag = True
        for j in range(len(b)):  # Проходим по всем классам в "b"
            if equal(a[i], b[j][0], k,
                     sr):  # Если текущий элемент из "a" k-эквивалентен нулевому элементу текущего подкласса "b"
                b[j].append(a[i])  # Добавляем элемент из "a" в этот класс
                flag = False
        if flag:  # Если мы не добавили текущий элемент из "a" ни в один класс из "b", то добавляем его как новый класс
            b.append([a[i]])

    return copy.deepcopy(b)


def equal(a, b, k, sr):  # Проверяет, являются ли состояния a и b k-эквивалентными для регистра sr
    sr_a = SR(2, to_bin(a, len(sr.s)), sr.mode, 'functions/fi.txt', 'functions/psi.txt')  # Регистр сдвига в состоянии a
    sr_b = SR(2, to_bin(b, len(sr.s)), sr.mode, 'functions/fi.txt', 'functions/psi.txt')  # Регистр сдвига в состоянии b
    flag = True
    for i in range(2 ** k):  # Например, если мы проверяем 3-эквивалентность, то проверок будет 2 ** 3 = 8
        sr_a = SR(2, to_bin(a, len(sr.s)), sr.mode, 'functions/fi.txt',
                  'functions/psi.txt')  # Регистр сдвига в состоянии a
        sr_b = SR(2, to_bin(b, len(sr.s)), sr.mode, 'functions/fi.txt',
                  'functions/psi.txt')  # Регистр сдвига в состоянии b
        if sr_a.several_steps(to_bin(i, k)) != sr_b.several_steps(to_bin(i, k)):
            flag = False
    return flag


def to_bin(a, r):
    result = []
    for i in range(r):
        result.append(a % 2)
        a = a // 2
    result.reverse()
    return result


# Разбивает регистр на классы эквивалентности
def eq_classes(sr):
    states = [i for i in range(2 ** len(sr.s))]
    # print('All states:', states)

    ec = [[states]]  # Массив 0-эквивалентных состояний
    # print('0-эквивалентные:', ec[0])
    for i in range(1, 2 ** len(sr.s)):
        ec.append([])  # Добавляем класс эквивалентности (1-эквиваелнтности, 2-эквивалентности и т.д.)
        for j in range(len(ec[i - 1])):  # Цикл проходит по подклассам в предыдущем классе эквивалентности
            if len(ec[i - 1][j]) > 1:
                for k in split(ec[i - 1][j], i, sr):
                    ec[i].append(k)
            else:
                ec[i].append(ec[i - 1][j])
        # print(i, '-эквивалентные: ', ec[i], sep='')
        if ec[i] == ec[i - 1]:
            # print(i - 1, '-эквивалентные совпали с ', i, '-эквивалентными. Конец.', sep='')
            return ec[i]


# Получает на вход массив
# Возвращает массив, в котором удалены все повторения
def delete_equal(a):
    n = []
    for i in a:
        if i not in n:
            n.append(i)
    return n


# Получаем на вход массив
# Возвращает максимум и его индекс
def max_and_index(a):
    m = 0  # Максимум
    p = 0  # Позиция максимума
    for i in range(len(a)):
        if a[i] > m:
            m = a[i]
            p = i
    return m, p


#  Получает на вход число в двоичной системе счисления, в виде списка
#  Возвращает число в десятичной системе счисления
def from_bin(a):
    result = 0
    for i in range(len(a)):
        result += a[i] * 2 ** (len(a) - i - 1)
    return result


'''
sr = SR(2, [0, 1, 1, 0], 'table', 'functions/fi.txt', 'functions/psi.txt')
print(sr.s)
print(sr.step(0))

print(sr.several_steps([0, 0, 0, 0, 0, 0]))

print(sr.s)
'''
'''
print(sr.several_steps([1, 1, 1, 1, 1, 1]))
print(sr.s)
eq_classes(sr)
'''

# Перебираем все возможные входные последовательности х длиной ln (всего 2^ln).
# Последовательность мы подаем на вход регистрам во всех разных начальных состояниях (всего 2^rn)
# и записываем соответствующие выходные последовательности y. Считаем сколько различных получилось среди них.
# Число различных = числу классов эквивалентности, на которые эта последовательность разбивает регистр сдвига.
# Затем мы отсортируем все последовательности в зависимости от того, насколько хорошо они разбивают регистр.
# После этого подадим регистру на вход конкатенацию лучших из них и ВЕРОЯТНО получим диагностическую последовательность.
ln = 5  # Длина входной последовательности
rn = 3  # Размер регистра
"""diagnostic_sequence_flag = False

sr = SR(2, to_bin(0, rn), 'table', 'functions/fi.txt', 'functions/psi.txt')
eq_cl = eq_classes(sr)
print('В регистре вот столько классов эквивалентности:', len(eq_cl))
print(' ')

while True:
    print('Подаем последовательности длины:', ln)
    flag = True
    equal_classes_split = []  # Сюда мы будем записывать количество классов, на которые последовательность разбила регистр
    for x in range(2 ** ln):  # Подаем на вход регистра сдвига все возможные входные последовательности х длиной 8
        time1 = time.perf_counter()  # Засекаем время
        y = []  # Массив, в который будут записаны выходные последовательности
        for start_s in range(2 ** rn):  # Перебираем начальные заполенния регистров сдвига
            sr = SR(2, to_bin(start_s, rn), 'table', 'functions/fi.txt', 'functions/psi.txt', )
            y.append(from_bin(sr.several_steps(to_bin(x, ln))))  # Записываем результат
        # print('y', y)
        # Теперь находим количество различных среди всего вывода
        y_reduced = delete_equal(y)
        k = len(y_reduced)
        equal_classes_split.append(k)

    # Количество классов, на которые последовательности разбили регистр (в порядке убывания)
    sorted_equal_classes_split = []
    # Массив прямо связан с sorted_equal_classes_split, каждый элемент в нем - позиция элемента до сортировки
    positions = []
    for i in range(len(equal_classes_split)):
        m, p = max_and_index(equal_classes_split)
        sorted_equal_classes_split.append(m)
        positions.append(p)
        equal_classes_split[p] = -1

    print('Элементы массива ниже — это количество классов, на которые разбили регистр последовательности длины ', ln, ':')
    print(sorted_equal_classes_split)

    #  r * t >= |S| = 2^rn, где t - количетво классов, на которое разбивается регистр последовательностями,
    #  а r - количетво последоваетльностей
    #  Будем суммировать количетво классов, на которое разбивается регистр последовательностями до тех пор пока
    #  не получим число >= |S| = 2^rn. Как только мы его получили - останавливаемся и запоминаем индекс элемента,
    #  на котором мы достигли нужной суммы. Далее нам потребуется всего лишь конкатенировать нужное количество
    #  входных последовательностей.
    s = 0  # Сумма количества классов, на которое разбивается регистр последовательностями
    index = -1  # Индекс элемента, на котором мы достигли нужной суммы
    for i in range(len(sorted_equal_classes_split)):
        if s < (len(eq_cl)):
            s += sorted_equal_classes_split[i]
        else:
            index = i
            break

    diagnostic_sequence = []
    if index == -1:
        print('Сумма всех классов, на которые последовательности разбивают регистр:', s, '< |S|. Следовательно из наших последовательностьей длины ',
              ln, 'не конкатенировать диагностическую последовательность')
    else:
        for i in range(index):
            diagnostic_sequence += to_bin(positions[i], ln)  # Складываем наиболее сильные разбиватели в супер-разбивателя
        # print('Супер-разбиватель:', diagnostic_sequence)

    y = []  # Массив, в который будут записаны выходные последовательности
    for start_s in range(2 ** rn):  # Перебираем начальные заполенния регистров сдвига
        sr = SR(2, to_bin(start_s, rn), 'table', 'functions/fi.txt', 'functions/psi.txt', )
        y.append(from_bin(sr.several_steps(diagnostic_sequence)))  # Записываем результат
    # print('y', y)
    # Теперь находим количество различных среди всего вывода
    y_reduced = delete_equal(y)
    # print('y_reduced', y_reduced)
    k = len(y_reduced)
    equal_classes_split.append(k)
    print('Предположительно диагностическая последовательность: ', diagnostic_sequence,
          ' разбила регистр на ', k, ' класса(ов).', sep='')

    if k >= len(eq_cl):
        diagnostic_sequence_flag = True
        print('Диагностическая последовательность нашлась!')
    else:
        print('Диагностическая последовательность не найдена. Перемешиваем.')

        counter = 0  # сколько раз будем перемешивать вектора в псевдодиагностической пос-ти
        while True:
            counter += 1
            # print('Попытка: ', counter)
            if counter == 500:
                # print('Больше пытаться не будем')
                break

            best_sequences_order = []
            for i in range(index):
                best_sequences_order.append(to_bin(positions[i], ln))

            best_sequences = []
            for i in range(len(best_sequences_order)):
                best_sequences.append(best_sequences_order[random.randint(0, len(best_sequences_order) - 1)])

            diagnostic_sequence = []
            for i in best_sequences:
                diagnostic_sequence += i

            y = []  # Массив, в который будут записаны выходные последовательности
            for start_s in range(2 ** rn):  # Перебираем начальные заполенния регистров сдвига
                sr = SR(2, to_bin(start_s, rn), 'table', 'functions/fi.txt', 'functions/psi.txt', )
                y.append(from_bin(sr.several_steps(diagnostic_sequence)))  # Записываем результат
            # print('y', y)
            # Теперь находим количество различных среди всего вывода
            y_reduced = delete_equal(y)
            # print('y_reduced', y_reduced)
            k = len(y_reduced)
            equal_classes_split.append(k)
            # print('Входная последовательность разбила регистр на ', k, ' класса.', sep='')

            if k < len(eq_cl):
                pass
                # print('Диагностическая последовательность не получилась.')
            else:
                print('Диагностическая последовательность:', diagnostic_sequence, 'разбивает на ', k, 'классов(ов).')
                break
        print('Перемешивание не помогло :(')
        print(' ')

    if diagnostic_sequence_flag:
        print(' ')
        print('———————————— ~0__0~ ————————————')
        print(' ')
        print('Диагностическая последовательность найдена. Конец алгоритма.')
        break
    else:
        # Увеличиваем длину входной последовательности
        ln += 1
        if ln == 12:
            print(' ')
            print('———————————— ~0__0~ ————————————')
            print(' ')
            print('Диагностическая последовательность не найдена.')
            break
"""