def levenstein(first_arr, second_arr):
    F = [[i + j if i * j == 0 else 0 for j in range(len(second_arr) + 1)] for i in range(len(first_arr) + 1)]
    for i in range(1, len(first_arr) + 1):
        for j in range(1, len(second_arr) + 1):
            if first_arr[i - 1] == second_arr[j - 1]:
                F[i][j] = F[i - 1][j - 1]
            else:
                F[i][j] = 1 + min(F[i - 1][j], F[i][j - 1], F[i - 1][j - 1])
    return F[len(first_arr)][len(second_arr)]


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
