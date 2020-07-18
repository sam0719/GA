from time import *
import numpy
import random
import matplotlib.pyplot as plt

class TSP:
    def __init__(self,limit,population_size):
        self.population_size = population_size
        self.survival_rate = 0.2#生存率
        self.limit = limit
        self.city_list = []
        self.mutation_rate = 0.1#突變率
        #48個城市坐標
        self.city_xy = [[6734,1453],[2233,10],[5530,1424],[401,841],[3082,1644],[7608,4458],[7573,3716],[7265,1268],[6898,1885],[1112,2049],[5468,2606],[5989,2873],[4706,2674],[4612,2035],[6347,2683],[6107,669],[7611,5184],[7462,3590],[7732,4723],[5900,3561],[4483,3369],[6101 ,1110],[5199 ,2182],[1633 ,2809],[4307 ,2322], [675 ,1006],[7555 ,4819],[7541 ,3981],[3177 ,756],[7352 ,4506],[7545 ,2801],[3245 ,3305],[6426 ,3173],[4608 ,1198],  [23 ,2216],[7248 ,3779],[7762 ,4595],[7392 ,2244],[3484 ,2829],[6271 ,2135],[4985 ,140],[1916 ,1569],[7280 ,4899],[7509 ,3239],  [10 ,2676],[6807 ,2993],[5185 ,3258],[3023 ,1942]]
        self.city_num = len(self.city_xy)#城市數量
    def init_path(self):#初始化路徑
        temp = [x for x in range(1,self.city_num,1)]#初始化行走路徑
        random.shuffle(temp)#亂序
        return temp
    def select(self,fitness_list):#輪盤賭選擇
        sum_fit = 0
        parent_list = []
        fit=[]
        for i in range(len(fitness_list)):
            fit.append(fitness_list[i][1])
        sum_fit = sum(fit)
        for i in range(int(self.population_size*self.survival_rate)):
            accumulator = 0.0
            random_num = numpy.random.randint(0,high=sum_fit)
            for ind,val in enumerate(fit):
                accumulator += val
                if accumulator >= random_num:
                    parent_list.append(fitness_list[ind])
                    break
        return parent_list
    def cal_fitness(self,path_list):#path_list:路徑列表
        sum = self.cal_distance(path_list[0],path_list[-1])#第一個到最後一個城市的距離
        sum += self.cal_distance(0,path_list[0])#起始城市到第一個城市的距離
        for i in range(len(path_list)-1):
            sum += self.cal_distance(path_list[i],path_list[i+1])#路徑表第二個城市到最後一個的總距離
        return path_list,sum
    def cal_distance(self,index1,index2): #index:城市表的索引   
        distance = ((self.city_xy[index2][0]-self.city_xy[index2][1])**2+(self.city_xy[index1][0]-self.city_xy[index1][1])**2)**0.5
        return distance
    def cross(self,parent_list):#交叉
        r1 = numpy.random.randint(self.population_size*self.survival_rate)
        r2 = numpy.random.randint(self.population_size*self.survival_rate)
        parent1 = parent_list[r1][0]
        parent2 = parent_list[r2][0]
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
        r1 = numpy.random.randint(0,high=self.city_num-1)
        r2 = numpy.random.randint(0,high=self.city_num-1)
        while r1 == r2:
            r2 = numpy.random.randint(0,high=self.city_num-1)
        mutation_list[r1],mutation_list[r2] = mutation_list[r2],mutation_list[r1]
        return mutation_list
    def survivial_select(self,mutation_list,fitness_list):
        child_fitness = []
        for i in range(len(mutation_list)):
            child_fitness.append(self.cal_fitness(mutation_list[i]))
        fitness = list(child_fitness+fitness_list)
        fitness.sort(key=lambda srt: srt[1],reverse=False)
        return fitness[:len(fitness_list)]
    def main(self):
        path_list = []
        fitness_list = []
        for i in range(self.population_size):
            path_list.append(self.init_path())
        for i in range(self.population_size):
            fitness_list.append(self.cal_fitness(path_list[i]))
        count = 0
        while count < self.limit:
            parent_list = self.select(fitness_list)
            child_list = []
            while len(child_list) != self.population_size-(self.population_size*self.survival_rate):
                child_list.append(self.cross(parent_list))
            mutation_list = child_list.copy()
            for i in range(len(child_list)):
                if numpy.random.random() < self.mutation_rate:
                    mutation_list[i] = self.mutation(child_list[i])
            survival_list = self. survivial_select(mutation_list,fitness_list)
            fitness_list = survival_list
            count += 1
            print('*'+str(count)+' 第%s次迭代:' % count,end=' ')
            print('fitness最大值為',survival_list[0][1])
            print('種群為',survival_list[0][0])

        X=[]
        Y=[]
        
        for i in survival_list[0][0]:
            x = self.city_xy[i][0]
            y = self.city_xy[i][1]
            X.append(x)
            Y.append(y)
        plt.plot(X,Y,'-o')
        plt.title("satisfactory solution of TS:%d"%(int(survival_list[0][1])))
        plt.show()
        

if __name__ == "__main__":
    tsp = TSP(100,200)
    tsp.main()
