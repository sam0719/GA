import numpy as np
from math import sqrt,pi,sin,cos
import random

class QTS:
    def __init__(self):
        self.population_size = 10
        self.iteration = 1000
        self.weight = [382745,799601,909247,729069,467902,44328,34610,698150,823460,903959,853665,551830,610856,670702,488960,951111,323046,446298,931161,31385,496951,264724,224916,169684]
        self.value = [825594,1677009,1676628,1523970,943972,97426,69666,1296457,1679693,1902996,1844992,1049289,1252836,1319836,953277,2067538,675367,853655,1826027,65731,901489,577243,466257,369261]
        self.bag_capacity = 6404180
        self.qbit = np.zeros((len(self.weight), 2))
        self.qbit.fill(1/sqrt(2))
        self.mutation_rate = 0.1
    def measure(self,qbit):
        return np.vectorize(lambda x,y : 1 if (x > np.power(y,2)) else 0)\
                        (np.random.rand(len(self.weight)), np.array(qbit)[:, 1])    
    def cal_fitness(self,solution):
        x = np.array(solution)
        if x.ndim == 1:
            solution = [solution]  
        for i in range(len(solution)):
            weight,value = self.cal_weight(solution[i])
            if weight > self.bag_capacity:
                weight,value,solution[i] = self.repair_solution(weight,value,solution[i])
            solution[i] = (solution[i],value)
        return solution
    def cal_weight(self,solution):
        weight,value = 0,0
        for i in range(len(solution)):
            weight += self.weight[i] * solution[i]
            value += self.value[i] * solution[i]
        return weight,value
    def repair_solution(self,weight,value,solution):
        while weight > self.bag_capacity:
            r = np.random.randint(0,len(solution))
            if solution[r]:
                solution[r] = 0
                weight -= self.weight[r]
                value -= self.value[r]
        return weight,value,solution
    def generate_neighbour(self,qbit):
        neighbour = [self.measure(qbit) for i in range(self.population_size)] 
        return neighbour
    def find_best_worst(self,neighbour):
        neighbour.sort(key=lambda srt: srt[1],reverse=True)
        return (neighbour[0],neighbour[-1])
    def updateQ(self,worst_solution,best_solution,qbit):
        theta = 0.01 * pi
        for i in range(len(self.weight)):
            x = best_solution[i] - worst_solution[i]
            if (qbit[i,0] * qbit[i,1] < 0):
                x *= -1
            Ugate = np.array([[cos(x*theta), -sin(x*theta)],
                          [sin(x*theta),  cos(x*theta)]])
            qbit[i,:] = np.dot(Ugate,qbit[i,:])
        return qbit
if __name__ == '__main__':
    qts = QTS()
    solution = qts.measure(qts.qbit)
    gbest = qts.cal_fitness(solution)[0][1]
    i = 0
    while i < qts.iteration:
        i += 1
        neighbour = qts.generate_neighbour(qts.qbit)
        fitness = qts.cal_fitness(neighbour)
        (best_solution,worst_solution) = qts.find_best_worst(fitness)
        if best_solution[1] > gbest:
            gbest = best_solution[1]
        qts.qbit = qts.updateQ(worst_solution[0],best_solution[0],qts.qbit)
        print('第%s次迭代，最優解是%s' % (i,gbest))