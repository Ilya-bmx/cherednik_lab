def to_bin(a, r):
    result = []
    for i in range(r):
        result.append(a % 2)
        a = a // 2
    result.reverse()
    return result


for i in range(32):
    i_bin = to_bin(i)
