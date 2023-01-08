def levenstein(first_array, second_array):
    editing_distance = [[i + j if i * j == 0 else 0
                         for j in range(len(second_array) + 1)]
                        for i in range(len(first_array) + 1)]
    for i in range(1, len(first_array) + 1):
        for j in range(1, len(second_array) + 1):
            if first_array[i - 1] == second_array[j - 1]:
                editing_distance[i][j] = editing_distance[i - 1][j - 1]
            else:
                editing_distance[i][j] = 1 + \
                            min(editing_distance[i - 1][j], editing_distance[i][j - 1], editing_distance[i - 1][j - 1])
    return editing_distance[len(first_array)][len(second_array)]


write = open('scores.txt', 'w')
mas = open('input.txt').read().split('\n')
for i in range(len(mas)):
    a, b = mas[i].split()
    first = open(a, 'r').read().split()
    second = open(b, 'r').read().split()
    lev = levenstein(first, second)
    if max(len(first), len(second)) != 0:
        open('scores.txt', 'a').write(str(1 - lev / max(len(first), len(second))) + '\n')
    else:
        open('scores.txt', 'a').write('0.0\n')
