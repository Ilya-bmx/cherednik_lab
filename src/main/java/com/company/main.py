from sys import setrecursionlimit
import SR_simple_field as register

# Функция phi_psi_fun ищет в таблицах Фи или Пси элемент,
# который нужно взять из таблицы и добавить в вектор состояния.
# Возвращает нужный элемент.
# Для поиска добавляет 0 или 1 в конец вектора состояния, переводит полученный вектор в 10-ое число,
# затем забирает из таблицы Фи или Пси элемент с таким индексом


# ориентированный граф
def make_reach_table():
    reach_table = []
    register_for_zeroes = register.SR(2, register.to_bin(0, register.rn), 'table', 'functions/fi.txt', 'functions/psi.txt')
    register_for_one = register.SR(2, register.to_bin(0, register.rn), 'table', 'functions/fi.txt', 'functions/psi.txt')
    for i in range(2 ** register.rn):
        table_line = [0] * 2 ** register.rn
        # print("register_for_zeroes: {}".format(register_for_zeroes.s))
        table_line[register_for_zeroes.step(0)] = 1
        # print("register_for_one: {}".format(register_for_one.s))
        table_line[register_for_one.step(1)] = 1
        reach_table.append(table_line)
    return reach_table


def depth_first_search(reach_table, mode):
    stack = []
    marked = []
    result = []

    for i in range(2 ** register.rn):
        flag = False
        for item in result:
            if i in item:
                flag = True
                break

        if flag:
            continue
        else:
            marked.append(i)
            stack.append(i)

            while len(stack) != 0:
                for j in range(len(reach_table[i])):
                    # условие на существование ребра в графе между вершинами i и j, для ориентированного при mod = normal
                    # и для неориентированного при mod = strong
                    if (((reach_table[i][j] == 1 or reach_table[j][i] == 1) and mode == "normal") or (
                            # тут учитываем напрваление для ребра из i --> j ( из A --> B )
                            reach_table[i][j] == 1 and mode == "strong")) and i != j: # i != j , чтобы не учитывать одно и то же ребро
                        flag = False
                        # проверяем, ходили ли мы по этой вершине уже или нет
                        for item in result:
                            if j in item:
                                flag = True
                                break
                        # если ходили, то поиск в глубину из неё не делаем, иначе делаем
                        if flag or j in marked:
                            continue
                        else:
                            # помещаем в стек и помечаем пройденной текущую вершину
                            marked.append(j)
                            stack.append(j)
                            dps_rec(reach_table, j, marked, stack, result, mode)
                            # убираем пройденную вершину из стэка, потому что мы её уже добавили в "пройденные"
                            stack.pop(-1)
                # убираем пройденную вершину из стэка, из которой мы поиск делали потому что мы её уже добавили в "пройденные"
                stack.pop(-1)
            if mode == "strong":
                marked_new = []
                stack_new = []
                result_new = []
                marked_copy = marked.copy()
                # для нахождения сильносвязных компонент необходимо выполнить поиск в глубину ещё раз из уже "пройденных" вершин
                for j in range(1, len(marked)):
                    dps_rec(reach_table, marked[j], marked_new, stack_new, result_new, "strong")
                    if marked[0] not in marked_new:
                        marked_copy.remove(marked[j])
                    marked_new = []
                    stack_new = []
                    result_new = []
                marked = marked_copy.copy()

            result.append(marked)
            marked = []
    return result


def dps_rec(reach_table, i, marked, stack, result, mode):
    for j in range(len(reach_table[i])):
        # условие на существование ребра в графе между вершинами i и j, для ориентированного при mod = normal
        # и для неориентированного при mod = strong
        if (((reach_table[i][j] == 1 or reach_table[j][i] == 1) and mode == "normal") or (reach_table[i][j] == 1 and mode == "strong")) and i != j:
            flag = False
            # проверяем, ходили ли мы по этой вершине уже или нет
            for item in result:
                if j in item:
                    flag = True
                    break
            # если ходили, то поиск в глубину из неё не делаем, иначе делаем
            if flag or j in marked:
                continue
            else:
                marked.append(j)
                stack.append(j)
                dps_rec(reach_table, j, marked, stack, result, mode)
                # так как у нас рекурсивный цикл , в котором мы все пройденные вершины помещаем в стэк,
                # после добавления в "пройденные вершины" вершину надо убрать из стэка
                stack.pop(-1)


def main():

    adjacency_matrix = make_reach_table()

    # Ищем компоненты связности в режиме normal - для не ориентированного графа
    links = depth_first_search(adjacency_matrix, "normal")
    print("Автомат связный") if len(links) == 1 \
        else print("Автомат несвязный, потому что делится на {} компонент связности".format(links))
    print("Компоненты связности: {}".format(links))
    # Ищем компоненты сильной связности в режиме strong - для ориентированного графа
    strong_links = depth_first_search(adjacency_matrix, "strong")
    print("Автомат сильно связный") if len(strong_links) == 1 \
        else print("Автомат не сильно связный, "
                   "потому что делится на {} компонент сильной связности".format(len(strong_links)))
    print("Компоненты сильной связности: {}".format(strong_links))


if __name__ == "__main__":
    main()
