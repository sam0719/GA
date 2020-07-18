from time import *
import numpy
import random
import matplotlib.pyplot as plt

class TSP:
    def __init__(self,limit,num):
        self.city = []
        self.population = 300
        self.survival_rate = 0.2#生存率
        self.limit = limit
        self.city_num = num
        self.city_list = []
        self.mutation_rate = 0.1

        for i in range(self.city_num):
            self.city.append((numpy.random.random()*1000,numpy.random.random()*1000))
        self.city = list(self.city)
    def city_init(self):#城市初始化
        population_list=[]
        for i in range(self.population):
            city_list = [x for x in range(self.city_num)]
            random.shuffle(city_list)
            population_list.append(city_list)
        return population_list #全部种群打乱顺序
    def select(self,fitness_list):#輪盤賭選擇
        sum_fit = 0
        parent_list = []
        fit=[]
        for i in range(len(fitness_list)):
            fit.append(fitness_list[i][1])
        sum_fit = sum(fit)
        for i in range(int(self.population*self.survival_rate)):
            accumulator = 0.0
            random_num = numpy.random.randint(0,high=sum_fit)
            for ind,val in enumerate(fit):
                accumulator += val
                if accumulator >= random_num:
                    parent_list.append(fitness_list[ind][0])
                    break
        return parent_list
    def cal_distance(self,population_list,index):#計算距离
        distance = 0
        for i in range(len(population_list[index])-1):
            distance += ((self.city[population_list[index][i+1]][0]-self.city[population_list[index][i]][0])**2+(self.city[population_list[index][i+1]][1]-self.city[population_list[index][i]][1])**2)**(1/2)#
        return distance
    def cal_fitness(self,population_list):#計算fitness
        fitness_list = []
        distance = 0
        for i in range(len(population_list)):
            distance = self.cal_distance(population_list,i)
            fitness_list.append((population_list[i],distance))
        return fitness_list#[i][0]為到達城市順序 [i][1]為fitness
    def cross(self,parent_list):#交叉
        r1 = numpy.random.randint(self.population*self.survival_rate)
        r2 = numpy.random.randint(self.population*self.survival_rate)
        parent1 = parent_list[r1]
        parent2 = parent_list[r2]
        cycle = [] #交叉点集
        start = parent1[0]
        cycle.append(start)
        end = parent2[0]
        while end != start:
            cycle.append(end)
            end = parent2[parent1.index(end)]
        child = parent1[:]
        cross_points = cycle[:]
        if len(cross_points) < 2 :
            cross_points = random.sample(parent1,2)
        k = 0
        for i in range(len(parent1)):
            if child[i] in cross_points:
                continue
            else:
                for j in range(k,len(parent2)):
                    if parent2[j] in cross_points:
                        continue
                    else:
                        child[i] = parent2[j]
                        k = j + 1
                        break   
        return child
    def mutation(self,child_list):#變異
        mutation_list = child_list.copy()
        r1 = numpy.random.randint(0,high=self.city_num)
        r2 = numpy.random.randint(0,high=self.city_num)
        while r1 == r2:
            r2 = numpy.random.randint(0,high=self.city_num)
        mutation_list[r1],mutation_list[r2] = mutation_list[r2],mutation_list[r1]
        return mutation_list
    def survivial_select(self,mutation_list,fitness_list):
        child_fitness = self.cal_fitness(mutation_list)
        fitness = list(child_fitness+fitness_list)
        fitness.sort(key=lambda srt: srt[1],reverse=True)
        return fitness[:len(fitness_list)]
    def main(self):
        init_population = self.city_init()
        fitness_list = self.cal_fitness(init_population)
        count = 0
        while count < self.limit:
            parent_list = self.select(fitness_list)
            child_list = []
            while len(child_list) != self.population-(self.population*self.survival_rate):
                child_list.append(self.cross(parent_list))
            mutation_list = self.mutation(child_list)
            survival_list = self. survivial_select(mutation_list,fitness_list)
            fitness_list = survival_list
            count += 1
            print('*'+str(count)+' 第%s次迭代:' % count,end=' ')
            print('fitness最大值為',survival_list[0][1])
            print('種群為',survival_list[0][0])
        '''
        X=[]
        Y=[]
        for i in survival_list[0][0]:
            x = self.city[i][0]
            y = self.city[i][0]
            X.append(x)
            Y.append(y)
        plt.plot(X,Y,'-o')
        plt.title("satisfactory solution of TS:%d"%(int(survival_list[0][1])))
        plt.show()
        '''
if __name__ == "__main__":
    tsp = TSP(100,25)
    tsp.main()

    print(list(range(5)))