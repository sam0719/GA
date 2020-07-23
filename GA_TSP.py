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
        self.filename = 'burma14'
        self.mutation_rate = 0.1#突變率
        self.dim,self.city_xy,self.EDGE_WEIGHT_TYPE = self.read_file(self.filename)
        self.city_num = len(self.city_xy)#城市數量
    def init_path(self):#初始化路徑
        temp = [x for x in range(1,self.city_num+1,1)]#初始化行走路徑
        random.shuffle(temp)#亂序
        return temp
    def select(self,fitness_list):#輪盤賭選擇
        sum_fit,random_num = 0,0
        parent_list,fit = [],[]
        for i in range(len(fitness_list)):
            fit.append(1/fitness_list[i][1])
        sum_fit = sum(fit)
        for i in range(int(self.population_size*self.survival_rate)):
            accumulator = 0.0
            random_num = numpy.random.random()*sum_fit
            for ind,val in enumerate(fit):
                accumulator += val
                if accumulator >= random_num:
                    parent_list.append(fitness_list[ind])
                    break
        return parent_list
        
    def read_file(self,filename):#讀取文件 返回維度和坐標列表
        dim = 0
        node = []
        EDGE_WEIGHT_TYPE = ''
        with open("data/"+filename+".tsp",mode='r',encoding='utf8') as f:
            for i in range(8):
                line = f.readline()
                if line.split(':')[0] == 'EDGE_WEIGHT_TYPE':
                    EDGE_WEIGHT_TYPE = line.split(':')[1][1:4]
                if line.split(':')[0] == 'DIMENSION':
                    dim = int(line.split(':')[1].split('\n')[0])
                if line == 'NODE_COORD_SECTION\n':
                    for j in range(dim):
                        line = f.readline()
                        node.append((float(line.split('       ')[0][6:]),float(line.split('       ')[1][:5])))
                    print(node)
        return dim,node,EDGE_WEIGHT_TYPE
            
    def cal_fitness(self,individual):#individual:路徑個體 返回那條路徑的fitness
        fitness = 0.0
        for i in range(len(individual)-1):
            fitness += self.cal_distance(individual[i]-1,individual[i+1]-1)
        fitness += self.cal_distance(individual[len(individual)-1]-1,individual[0]-1)
        return individual,fitness
    def cal_distance(self,index1,index2): #index:城市表的索引   
        latitude,longitude = [],[]
        if self.EDGE_WEIGHT_TYPE == 'GEO':
            PI = 3.141592
            for i in (index1,index2):
                deg = int(round(self.city_xy[i][0]))
                min = self.city_xy[i][0] - deg
                latitude.append(PI * (deg + 5.0 * min / 3) /180.0)
                deg = int(round(self.city_xy[i][1]))
                min = self.city_xy[i][1] - deg
                longitude.append(PI * (deg + 5.0 * min / 3) /180.0)
            '''
            deg = int(self.city_xy[index2][0])
            min = city_xy[index2][0] - deg
            latitude[1] = PI * (deg + 5.0 * min / 3) /180.0
            deg = int(self.city_xy[index2][1])
            min = city_xy[index2][1] - deg
            longitude[1] = PI * (deg + 5.0 * min / 3) /180.0
            '''
            RRR = 6378.388
            q1 = numpy.cos(longitude[0] - longitude[1])
            q2 = numpy.cos(latitude[0] - latitude[1])
            q3 = numpy.cos(latitude[0] + latitude[1])
            distance = int(RRR * numpy.arccos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)
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
        #self.read_file(self.filename)
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

        
        plt.subplot(2,2,3)
        X=[]
        Y=[]
        for i in range(self.city_num-1):
            x=survival_list[0][0][i]-1
            X.append(self.city_xy[x][0])
            Y.append(self.city_xy[x][1])
        plt.plot(X,Y)
        plt.axis([0,8000,0,8000])
        plt.title('result')
        plt.show()
        

if __name__ == "__main__":
    tsp = TSP(500,100)
    tsp.main()
