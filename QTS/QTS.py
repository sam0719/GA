import numpy as np
from math import sqrt,pi,sin,cos
import matplotlib.pyplot as plt
import mail


class QTS:
    def __init__(self):
        self.population_size = 10
        self.iteration = 2000
        self.weight = [1,2,3,4,5,6,7,8,9,10]*10
        self.value = [6,7,8,9,10,11,12,13,14,15]*10
        self.bag_capacity = sum(self.weight)/2
        self.qbit = np.zeros((len(self.weight), 2))
        self.qbit.fill(1/sqrt(2))
        self.theta = 0.01 * pi
    def measure(self,qbit):
        return np.vectorize(lambda x,y : 1 if (x < np.power(y,2)) else 0)\
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
        array = np.array(solution).nonzero()[0]
        while weight > self.bag_capacity:        
            r = np.random.randint(0,len(array))
            solution[array[r]] = 0
            array = np.delete(array,r)
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
        for i in range(len(self.weight)):
            # if T.setdefault(i,0) != 0:
            #     continue
            x = best_solution[i] - worst_solution[i]
            if not x:
                continue
            if (qbit[i,0] * qbit[i,1] < 0):
                x *= -1
            Ugate = np.array([[cos(x*self.theta), -sin(x*self.theta)],
                          [sin(x*self.theta),  cos(x*self.theta)]])
            qbit[i,:] = np.dot(Ugate,qbit[i,:])
            # T[i] = tabu_itt
        return qbit
    def qts(self,itt_not_change):
        count = 0
        solution = self.measure(self.qbit)
        gbest = self.cal_fitness(solution)[0][1]
        X = []
        Y = []
        i = 0
        while i < self.iteration and gbest!=620:
            i += 1
            neighbour = self.generate_neighbour(self.qbit)
            fitness = self.cal_fitness(neighbour)
            (best_solution,worst_solution) = self.find_best_worst(fitness)          
            if best_solution[1] > gbest:
                gbest = best_solution[1]
                count = i
                itt_not_change = 0
            else:
                itt_not_change += 1
            Y.append(gbest)
            X.append(i)
            self.qbit = self.updateQ(worst_solution[0],best_solution[0],self.qbit)
            if itt_not_change == 200:
                self.theta = self.theta / 2
                self.qbit = np.zeros((len(self.weight), 2))
                self.qbit.fill(1/sqrt(2))
            #print('第%s次迭代，最優解是%s' % (i,gbest)) 
        print('一共跑了%i世代,第%s世代找出最优解:%s' % (i,count,gbest))
        return X,Y,gbest,i
  
if __name__ == '__main__':
    qts_time = 100
    count = 0
    itt_not_change = 0
    avg = []
    try:
        for i in range(qts_time):
            qts = QTS()
            X,Y,gbest,i = qts.qts(itt_not_change)
            if i != 5000:
                avg.append(i)
            if gbest == 620:
                count += 1
        print('平均第%s世代找到最优解' % str(sum(avg)/len(avg)))
        avg = []
        print('%s次QTS一共找到%s次最優解' % (str(qts_time),str(count)))
        mail.sendMail('您的程序已经运行完成，请去查看日志结果')
    #plt.figure(figsize=(5,5))
    #plt.plot(X,Y,'r-')
    #plt.show()
    except:
        mail.sendMail('您的程序出现错误，请去查看日志结果')