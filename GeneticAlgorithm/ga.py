from random import random
import sys
# indivíduo = 1 cromossomo
# cromossomo = lista de itens
# gene = { cromossomo[i] = valor da Carreta no qual está o item,
#         i = id do item, weights[i] retorna o peso do item com id i}
import random


class GeneticAlgorithm:

    def __init__(self, problem, n_ind):
        self._p = problem
        self._population = self.init_population(n_ind)

    # Gera a população inicial
    def init_population(self, n_ind):
        population = []
        for i in range(n_ind):
            new_ind = self._p.allocate()
            population.append(new_ind)
        return population

    # Genetic algorithm:
    #   Realiza o algoritimo genético.
    #   Parâmetros:
    #         population: população
    #         ngen: número de gerações
    #         p_mut: probabilidade de mutação
    #         p_sel: porcentagem de elitismo
    #         f_thres: limiar de fitness(previne estagnação)
    def genetic_algorithm(self, population, ngen, p_mut, p_sel, m):
        n = 0
        a_fitness = self.fitness(population)
        while (n != ngen) and (max(a_fitness) != 1.0):

            new_pop = []
            mut = []

            selected = self.select(population, p_sel)
            # new_pop recebe todos os indivíduos pertencentes ao elitismo
            for i in range(len(selected)):
                new_pop.append(population[selected[i]])

            # Realiza uma diferença(conjuntos) entre duas listas
            #   neste caso, retorna uma lista de tamanho (1-p_sel)*population
            new_pop = self.Diff(population, new_pop)

            for i in range(int(len(population)*p_mut)):
                mut.append(new_pop.pop())

            #new_pop = self.Diff(new_pop, mut)

            # Realiza os operadores da seguinte forma:
            #   (1) Seleciona dois indivíduos de new_pop(i,i+1)
            #   (2) cross = o resultado da reprodução dos dois

            for i in range(0, len(new_pop), 2):
                try:
                    cross = self.op_crossover(new_pop[i], new_pop[i + 1])
                    new_pop[i] = cross[0]
                    new_pop[i + 1] = cross[1]
                except IndexError:
                    continue

            for i in mut:
                self.mutate(i)

            # Recoloca os indivíduos selecionados(elite) de volta ao new_pop
            for i in range(len(selected)):
                new_pop.append(population[selected[i]])
            for i in range(len(mut)):
                new_pop.append(mut[i])
            # Corrige os indivíduos inválidos
            new_pop = self.correct(new_pop)
            # A população recebe a nova geração
            population = new_pop
            # Recalcula-se o fitness
            a_fitness = self.fitness(population)
            n += 1

        a_fitness = sorted(list(enumerate(self.fitness(population))), key=lambda tup: tup[1], reverse=True)

     #   print('---------------------------------------------------------------------------------------------')
     #   print("Geração atual: ", n)
        self._p.printCarretas(population[a_fitness[0][0]], m)
        print("Fitness atual: ", a_fitness[0][1])
        print('---------------------------------------------------------------------------------------------')

    # Corrige a população caso exista indivíduos inviáveis
    def correct(self, population):
        c = []
        for i in range(len(population)):
            c.append(self._p.correct(population[i]))
        # c = (map(lambda x: self._p.correct(x), population))
        return c

    # Retorna uma lista contendo o fitness de cada indivíduo da população
    def fitness(self, population):
        # fit = 1 - [((T_ls)/(T_c))*((T_li)/(T_i))] | T_ls = soma dos espaços vazios|T_c = Capacidade total|T_li = Total de itens de fora| T_i = Total de itens.
        c = population
        b = lambda x: sum(self._p.left_space(x)) / sum((self._p.getCapacidades()))
        a = map(b, population)
        aux = (list(a))
        aux2 = (list(map(lambda x: len(self._p.left_Produtos(x)) / self._p.get_num_Produtos(), population)))
        fit = list(map(lambda x, y: 1 - (x * y), aux, aux2))
        return fit

    # Imprime os pesos e capacidades
    # imprime os indivíduos, seu peso atual e seu espaço livre
    def print_population(self):
        print("WEIGHTS: ", self._p.get_weights(), "CAPACITIES: ", self._p.get_capacities())
        for i in self._population:
            print()
            print("ITEMS: ", i)
            print(" ATUAL W: ", self._p.get_bags_w(i), " LEFT SPACE: ", self._p.left_space(i), " LEFT ITEMS: ",
                  list(map(lambda x: self._p._weights[x], self._p.left_items(i))))

    # Retorna a população
    def get_population(self):
        return self._population

    # Elitismo:
    #   aux é uma lista que ordena a população por fitness
    #   retorna os primeiros id's desta lista
    def select(self, population, p_sel=0.1):
        sel = []
        aux = sorted(list(enumerate(self.fitness(population))), key=lambda tup: tup[1], reverse=False)
        for i in range(int(p_sel * len(population))):
            sel.append((aux.pop())[0])
        return sel

    # One-point crossover:
    #   realiza um corte na metade do indivíduo
    def op_crossover(self, x, y):
        n = len(x)
        c = round(n / 2)
        son1 = x[:c] + y[c:]
        son2 = x[c:] + y[:c]
        return list((son1, son2))

    # Two-point crossover:
    #   realiza dois cortes
    def tp_crossover(self, x, y):
        n = len(x)
        c = round(n / 2) - 1
        son1 = x[:c] + y[c:len(y) - c] + x[len(x) - c:]
        son2 = y[:c] + x[c:len(x) - c] + y[len(y) - c:]

        return list((son1, son2))

    # Mutação:
    #   Aloca o maior peso que está fora das Carretas em uma das Carretas
    def mutate(self, x):
        # aux: recebe uma lista de indices dos itens que estão fora das Carretas
        aux = self._p.left_Produtos(x)
        max_w = [sys.maxsize, 0]  # max_w[0] -> indica o maior peso / max_w[1] -> indice do maior peso
        for i in aux:
            if self._p.getMedProduto()[i] < max_w[0]:
                max_w[0] = self._p.getMedProduto()[i]
                max_w[1] = i
        x[max_w[1]] = random.randint(0, self._p.get_num_Carretas() - 1)  # aloca o maior peso a alguma Carreta aleatória

    # Faz a diferença entre duas listas
    def Diff(self, li1, li2):
        li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
        return li_dif
