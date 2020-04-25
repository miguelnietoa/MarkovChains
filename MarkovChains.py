import numpy as np
import copy
from matplotlib import pyplot as plt


class MarkovChain:
    def __init__(self, filename, k):
        self.markovFrec = dict()
        self.markovProb = dict()
        self.str = self.file2string(filename).lower()
        self.k = k
        self.calc_frec()
        self.markovProb = copy.deepcopy(self.markovFrec)
        self.calc_probabilidades()

    def file2string(self, filename):
        return open(filename, 'r', encoding='utf-8').read().replace('\n', '')

    def calc_frec(self):
        n = len(self.str) - self.k
        for i in range(n):
            sub = self.str[i:i + self.k]
            char = self.str[i + self.k:i + self.k + 1]
            if sub not in self.markovFrec:
                self.markovFrec[sub] = dict()
            if char not in self.markovFrec[sub]:
                self.markovFrec[sub][char] = 0
            self.markovFrec[sub][char] += 1

    def calc_probabilidades(self):
        for x in self.markovProb:
            sum = 0
            for y in self.markovProb[x]:
                sum += self.markovProb[x][y]
            for y in self.markovProb[x]:
                self.markovProb[x][y] /= sum

    def max_char(self, markov, substr):
        if substr in markov:
            chars = []
            prob = []
            for char in markov[substr]:
                prob.append(markov[substr][char])
                chars.append(char)
            # numpy.random.choice devuelve una lista, así que
            # como se escoge un solo elemento, devolvemos la posición 0
            return np.random.choice(chars, 1, p=prob)[0]
        return None

    def generar_texto(self, n):
        text = self.str[:self.k]
        while len(text) < n:
            x = self.max_char(self.markovProb, text[-self.k:])
            if x is None:
                print('No se puede generar más texto')
                break
            else:
                text += x
        return text

    def graficar(self):
        list = []
        cont = 0
        for substr in self.markovFrec:
            for char in self.markovFrec[substr]:
                list.extend(['\'%s\'' % char] * self.markovFrec[substr][char])
                cont += 1
            plt.style.use('fivethirtyeight')
            plt.hist(list, bins=cont, align='mid', histtype='bar')
            plt.xlabel('Caracteres siguientes')
            plt.ylabel('Frecuencia')
            plt.title('Apariciones de la subcadena "%s"' % substr)
            plt.tight_layout()
            plt.show()
            list.clear()
            cont = 0


if __name__ == '__main__':
    filename = 'file.txt'  # input('Digite el nombre del archivo: ')
    k = 4  # int(input('Digite K: '))
    n = 100  # int(input('Digite número de caracteres para generar texto: '))
    modelo = MarkovChain(filename, k)
    print(modelo.generar_texto(n))
