from GeneticAlgorithm.knapsack import TruckProblem
from GeneticAlgorithm.ga import GeneticAlgorithm
import copy

#        50 produtos com 3 medidas diferentes (750cm³, 900cm³, 500cm³)
#        para serem alocados em duas carretas com capacidade máxima de 12000cm³ e 10000 cm³ respectivamente.
n_Produtos = 50
Qant_Carretas = 2
m = [750, 900, 500]
c = [12000, 10000]
n_ind = 100
n_generations = 500
p_mut = 0.15
p_sel = 0.1

TP = TruckProblem(n_Produtos, Qant_Carretas, m, c)
ga = GeneticAlgorithm(TP, n_ind)
print("TRUCK SAFE PROJECT: ")
for i in range(10):
    ga.genetic_algorithm(copy.deepcopy(ga.get_population()),n_generations,p_mut,p_sel, m)