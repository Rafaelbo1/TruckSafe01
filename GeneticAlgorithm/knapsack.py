from random import choice
from random import randint


class TruckProblem:
    nC = 0
    nP = 0
    MedProduto = []  # fixo
    Capacidades = []  # fixo

    # CONSTRUTOR DA CLASSE
    def __init__(self, nProdutos, nCarretas, w, c):

        # Preenche numero de itens e Carretas
        self.nC= nCarretas
        self.nP = nProdutos

        # Monta a lista de pesos
        for i in range(nProdutos):
            self.MedProduto.append(choice(w))

        # Monta a lista de capacidades
        aux = c
        for i in range(nCarretas):
            # aux é uma copia da lista de capacidades disponíveis
            # Escolhe um MedProduto de capacidade aleatório
            r = choice(aux)
            # inclui em Capacidades
            self.Capacidades.append(r)
            # Remove r de aux para evitar repetição em Capacidades
            aux.remove(r)

    # MÉTODOS AUXILIARES
    # Aloca randomicamente outra configuração de itens
    def allocate(self):
        Produtos = []
        for i in range(self.nP):
            Produtos.append(-1)

        for i in range(self.nP):
            Produtos[i] = choice(range(self.nC))

        self.r_desallocate(Produtos)
        return Produtos

    # Desaloca randomicamente até 30% dos itens das Carretas
    def r_desallocate(self, Produtos):
        a = randint(1, round(len(Produtos) * 0.3))
        for i in range(a):
            Produtos[randint(0, len(Produtos) - 1)] = -1

    # Retorna o peso atual de uma configuração de itens
    def get_Carretas_w(self, Produtos):
        Carretas = []

        for i in range(self.nC):
            Carretas.append(0)
            for j in range(self.nP):
                p = Produtos[j]
                if (p == i):
                    Carretas[i] += self.MedProduto[j]
        return Carretas

    # Retorna o espaço vazio em cada uma das Carretas
    # MedProdutoes negativos indicam que a Carreta ultrapassou sua capacidade
    def left_space(self, Produtos):
        Carretas = self.get_Carretas_w(Produtos)
        ls = []
        for i in range(self.nC):
            ls.append(Carretas[i])
            delta = (self.Capacidades[i]) - (Carretas[i])
            ls[i] = delta
        return ls

    # Verifica se a alocação feita é valida, com base no espaço livre na Carreta
    def is_valid(self, Produtos):
        ls = self.left_space(Produtos)
        for i in ls:
            if i < 0:
                return False
        return True

    # Corrije a sobrecarga nas Carretas
    def correct(self, Produtos):
        ls = self.left_space(Produtos)
        for i in range(len(ls)):
            if ls[i] < 0:
                self.unload(Produtos, i)
        return Produtos

    # Descarrega a Carreta que excedem o limite da capacidade
    # Descarrega retirando os itens mais leves, pois queremos maximizar o peso dos itens
    def unload(self, Produtos, id_Carreta):
        ls = self.left_space(Produtos)
        while ls[id_Carreta] < 0:
            # aux: lista auxiliar que guarda o id dos itens(em [Produtos]) que estão na Carreta sobrecarregada
            # f: lista do MedProduto dos pesos dos itens que pertencem a lista aux
            aux = []
            f = []
            # inicia aux com os id em [Produtos]
            for i in range(len(Produtos)):
                if Produtos[i] == id_Carreta:
                    aux.append(i)
            # inicia f com os pesos dos itens que estão na Carreta passada(id_Carreta)
            for i in aux:
                f.append(self.MedProduto[i])

            # RETIRADA DOS ITENS:
            # (1) enumera-se a lista de pesos f[], de forma que teremos:
            #       f[] = [(id_em_aux , peso_do_Produto), (), ..., ()]
            # (2) Ordena-se f[] de acordo com os pesos, mas mantendo o id_em_aux
            # (3) retira-se o Produto atribuindo -1 na lista [Produtos]
            #       f[0][0] retorna o id_em_aux do Produto, neste caso do Produto de menor peso pois está ordenado
            #       aux[f[0][0]] retorna o id_em_Produtos do Produto de menor peso no momento
            #       recalcule ls, já que 1 Produto foi retirado
            f = list(enumerate(f))
            f = sorted(f, key=lambda tup: tup[1])
            Produtos[aux[f[0][0]]] = -1
            ls = self.left_space(Produtos)

    # Dado a lista de itens retorna a quantidade de itens deixados fora da alocação
    def left_Produtos(self, Produtos):
        li = []
        for i in range(len(Produtos)):
            if Produtos[i] == -1:
                li.append(i)
        return li

    # Printa a alocação nas Carretas
    def printCarretas(self, Produtos, m):
        Carretas = self.CarretasList(self.get_num_Carretas())
        outCarreta = []

        for i in range(len(Produtos)):
            Carreta_index = Produtos[i]
            if Carreta_index != -1:
                Produto = self.getMedProduto()[i]
                Carretas[Carreta_index].append(Produto)
                continue
            outCarreta.append(self.getMedProduto()[i])
        MedI1 = 0
        MedI2 = 0
        MedI3 = 0
        for i in range(len(Carretas)):
            Carreta = Carretas[i]
            for j in Carreta:
                if j == m[0]:
                    MedI1 += 1
                if j == m[1]:
                    MedI2 += 1
                if j == m[2]:
                    MedI3 += 1
        MedOutP1 = 0
        MedOutP2 = 0
        MedOutP3 = 0
        for c in outCarreta:
            if c == m[0]:
                MedOutP1 += 1
            if c == m[1]:
                MedOutP2 += 1
            if c == m[2]:
                MedOutP3 += 1

        for i in range(len(Carretas)):
            Carreta = Carretas[i]
            MedInP1 = 0
            MedInP2 = 0
            MedInP3 = 0
            for j in Carreta:
                if j == m[0]:
                    MedInP1 += 1
                if j == m[1]:
                    MedInP2 += 1
                if j == m[2]:
                    MedInP3 += 1

            print('Carreta {} = Alocou ({}Produtos de {}cm³ -  {}Produtos de {}cm³ - {}Produtos de {}cm³) | Max Vol. = {}cm³ , Vol. Utilizado no Truck= {}cm³'
                  .format(i + 1, MedInP1, m[0], MedInP2,m[1], MedInP3, m[2], self.getCapacidades()[i],sum(Carretas[i])))
        print('---------------------------------------------------------------------------------------------')
        print ('TOTAL DE PRODUTOS ALOCADOS:')
        print('DE {}cm³ = {}'.format(m[0], MedI1))
        print('DE {}cm³ = {}'.format(m[1],MedI2))
        print('DE {}cm³ = {}'.format(m[2],MedI3))

        print('---------------------------------------------------------------------------------------------')
        print('TOTAL DE PRODUTOS NÃO ALOCADOS:')
        print('DE {}cm³ = {}'.format(m[0], MedOutP1))
        print('DE {}cm³ = {}'.format(m[1], MedOutP2))
        print('DE {}cm³ = {}'.format(m[2], MedOutP3))


    def CarretasList(self, size):
        Carretas = list()
        for i in range(0, size):
            Carretas.append(list())
        return Carretas

    # GETS
    def getMedProduto(self):
        return self.MedProduto

    def getCapacidades(self):
        return self.Capacidades

    def get_num_Produtos(self):
        return self.nP

    def get_num_Carretas(self):
        return self.nC
