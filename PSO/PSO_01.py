import numpy as np
import random
import matplotlib.pyplot as plt
import math

class PSO:
    def __init__(self,c1,c2,w,limit,population_size):
        self.c1 = c1#個人經驗權重
        self.c2 = c2#群體經驗權重
        self.w = w#慣性權重
        self.price = np.array([825594,1677009,1676628,1523970,943972,97426,69666,1296457,1679693,1902996,1844992,1049289,1252836,1319836,953277,2067538,675367,853655,1826027,65731,901489,577243,466257,369261])
        self.weight = np.array([382745,799601,909247,729069,467902,44328,34610,698150,823460,903959,853665,551830,610856,670702,488960,951111,323046,446298,931161,31385,496951,264724,224916,169684])
        self.limit = limit #迭代次數
        #self.length = len(self.weight) #長度
        self.population_size = population_size #種群數量
        self.bag_capacity = 6404180 #背包容量
        #self.x_bound = [0,2**(self.length)-1]#上下界
        self.dim = len(self.weight)#維度#物品數量
        #初始化粒子群位置#
        self.x =  np.random.randint(0,2,(self.population_size,self.dim)) #0,1組成的矩陣
        self.v = np.random.rand(self.population_size,self.dim)#初始化粒子群速度
        fitness = [self.cal_fitness(self.x[i]) for i in range(np.shape(self.x)[0])]#計算初始粒子群適應度
        self.p_best = self.x#粒子最佳解
        self.p_best_fitness = fitness
        self.g_best =  self.x[np.argmax(fitness)]#群體最佳位置
        self.g_best_fitness = np.max(fitness)#群體最佳適應值
    def cal_fitness(self,x):#計算fitness
        x_bin = []
        import math
        temp = np.array(x)
        weight_sum = np.sum(temp*self.weight)
        if weight_sum > self.bag_capacity:
            return 0
        else:
            return np.sum(temp*self.price)
    def envolve(self):
        #f = open("data/PSO_01.epin",mode='w')#創建EPanel配置,UTF-8會亂碼
        #f.write('Particle:\n')
        for i in range(self.limit):
            r1 = np.random.rand(self.population_size,self.dim)#一個[0,1)組成的矩陣
            r2 = np.random.rand(self.population_size,self.dim)
            self.v = self.v*self.w+self.c1*r1*(self.p_best-self.x)+self.c2*r2*(self.g_best-self.x)
            for j in range(self.population_size):
                for k in range(self.dim):
                    self.x[j][k] = self.cal_x(self.v[j][k])#計算x
            #self.x = self.x+self.v
            fitness = [self.cal_fitness(self.x[i]) for i in range(np.shape(self.x)[0])]
            for j in range(self.population_size):
                if self.p_best_fitness[j] < fitness[j]:
                    self.p_best = np.copy(self.x[j])
                    self.p_best_fitness[j] = fitness[j]
                if np.max(fitness) > self.g_best_fitness:
                    self.g_best = self.x[np.argmax(fitness[j])]
                    self.g_best_fitness = np.max(fitness[j])
            print('第%s次迭代'%(i+1))
            print('最好的fitness為:%d,平均fitness為:%d:'%(self.g_best_fitness,np.mean(fitness)))
        #f.close()
    def cal_x(self,v):
        if random.random() < 1/(1+math.exp(-v)):
            return 1
        else:
            return 0
if __name__ == '__main__':
    pso = PSO(1.4,1.4,0.6,100,6)
    pso.envolve()