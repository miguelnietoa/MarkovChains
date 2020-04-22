import numpy as np


def file2string(path):
    return open(path, 'r').read().replace('\n', '')


def calc_frec(str, k):
    markov = dict()
    n = len(str) - k + 1
    for i in range(n):
        sub = str[i:i + k]
        if i + k != len(str):
            char = str[i + k:i + k + 1]
        else:
            break
        if sub not in markov:
            markov[sub] = dict()
        if char not in markov[sub]:
            markov[sub][char] = 0
        markov[sub][char] += 1
    return markov


def calc_probabilidades(markov):
    for x in markov:
        sum = 0
        for y in markov[x]:
            sum += markov[x][y]
        for y in markov[x]:
            markov[x][y] /= sum
    return markov


def max_char(markov, sub):
    if sub in markov:
        list = []
        for x in markov[sub]:
            list.append((markov[sub][x], x))
        list.sort()
        rnd = np.random.uniform()
        ant = 0
        for num in list:
            if ant <= rnd <= ant + num[0]:
                return num[1]
            else:
                ant += num[0]
    return None


str = file2string('file.txt').lower()
k = 3  # int(input('Digite longitud de subcadena (k):'))
n = 1000  # int(input('Digite número de caracteres a generar (n):'))
markov = calc_frec(str, k)
markov = calc_probabilidades(markov)
print(markov)
text = str[:k]
while len(text) < n:
    x = max_char(markov, text[-k:])
    if x is None:
        print('No se puede generar más texto')
        break
    else:
        text += x
print('********TEXTO:***********')
print(text)
