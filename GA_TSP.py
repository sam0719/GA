from time import *
import numpy
import random
import matplotlib.pyplot as plt
import re

class TSP:
    def __init__(self,iterator,population_size):
        self.population_size = population_size
        self.survival_rate = 0.2#生存率
        self.iterator = iterator
        self.city_list = []
        self.filename = 'burma14'
        self.mutation_rate = 0.1#突變率
        self.dim,self.city_xy,self.EDGE_WEIGHT_TYPE = self.read_file(self.filename)
        self.city_num = len(self.city_xy)#城市數量
        #繪圖
        self.iter_x = []
        self.iter_y = []
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
        line = ''
        pattern = re.compile(r'-?[0-9]{1,5}[\.]?[0-9]{0,2}')
        pattern2 = re.compile(r'EOF')
        with open("data/"+filename+".tsp",mode='r',encoding='utf8') as f:
            while 'EOF' not in line:
                line = f.readline()
                if line[:16] == 'EDGE_WEIGHT_TYPE':
                    EDGE_WEIGHT_TYPE = line.split(':')[1][1:4]
                if line[:9] == 'DIMENSION':
                    dim = int(line.split(':')[1].split('\n')[0])
                if line == 'NODE_COORD_SECTION\n':
                    for j in range(dim):
                        line = f.readline()
                        result = pattern.findall(line)
                        node.append((float(result[-2]),float(result[-1])))
        return dim,node,EDGE_WEIGHT_TYPE
            
    def cal_fitness(self,individual):#individual:路徑個體 返回那條路徑的distance
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
                deg = int(self.city_xy[i][0])
                min = self.city_xy[i][0] - deg
                latitude.append(PI * (deg + 5.0 * min / 3) /180.0)
                deg = int(self.city_xy[i][1])
                min = self.city_xy[i][1] - deg
                longitude.append(PI * (deg + 5.0 * min / 3) /180.0)
            RRR = 6378.388
            q1 = numpy.cos(longitude[0] - longitude[1])
            q2 = numpy.cos(latitude[0] - latitude[1])
            q3 = numpy.cos(latitude[0] + latitude[1])
            distance = int(RRR * numpy.arccos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)
        elif self.EDGE_WEIGHT_TYPE == 'ATT':
            xd = self.city_xy[index1][0] - self.city_xy[index2][0]
            yd = self.city_xy[index1][1] - self.city_xy[index2][1]
            r = ((xd ** 2 + yd ** 2) / 10) ** 0.5
            t = int(r)
            if (t < r):
                distance = t + 1
            else:
                distance = t
        return distance
    def cross(self,parent_list):#交叉
        index1 = numpy.random.randint(self.population_size*self.survival_rate)
        index2 = numpy.random.randint(self.population_size*self.survival_rate)
        parent1 = parent_list[index1][0]
        parent2 = parent_list[index2][0]
        r1 = numpy.random.randint(0,high=round(self.city_num/2))
        r2 = numpy.random.randint(round(self.city_num/2),high=self.city_num)
        g1 = parent2[r1:r2] + parent1
        newGene = []
        for i in g1:
                if i not in newGene:
                    newGene.append(i)
        return newGene
    def mutation(self,gene):#變異
        path_list = [t for t in range(len(gene))]
        order = list(random.sample(path_list, 2))
        start, end = min(order), max(order)
        tmp = gene[start:end]
        tmp = tmp[::-1]
        gene[start:end] = tmp
        return list(gene)
    def combinate(self,mutation_list,fitness_list):
        child_fitness = []
        for i in range(len(mutation_list)):
            child_fitness.append(self.cal_fitness(mutation_list[i]))
        fitness = list(child_fitness+fitness_list)
        fitness.sort(key=lambda srt: srt[1],reverse=False)
        return fitness[:len(fitness_list)]
    def main(self):
        plt.rcParams['font.sans-serif']=['SimHei']
        plt.rcParams['lines.linewidth'] = 0.5 
        path_list = []
        fitness_list = []
        g_best = 0
        for i in range(self.population_size):
            path_list.append(self.init_path())
        for i in range(self.population_size):
            fitness_list.append(self.cal_fitness(path_list[i]))
        count = 0
        while count < self.iterator:
            plt.clf()
            parent_list = self.select(fitness_list)
            child_list = []
            while len(child_list) != self.population_size-(self.population_size*self.survival_rate):
                child_list.append(self.cross(parent_list))
            mutation_list = child_list.copy()
            for i in range(len(child_list)):
                if numpy.random.random() < self.mutation_rate:
                    mutation_list[i] = self.mutation(child_list[i])
            survival_list = self.combinate(mutation_list,fitness_list)
            fitness_list = survival_list
            count += 1
            if survival_list[0][1] != g_best:
                g_best = survival_list[0][1]
                g_best_count = count
            print('第%s次迭代:' % count,end=' ')
            print('fitness最大值為',survival_list[0][1])
            print('族群為',survival_list[0][0])
            self.iter_x.append(count)
            self.iter_y.append(survival_list[0][1])
            '''
            #動態圖
            plt.ion()
            plt.figure(figsize=(10,5))
            plt.subplot(1, 2, 2)
            plt.title('收斂圖')
            plt.plot(self.iter_x,self.iter_y,'b-',self.iter_x,self.iter_y,'b.') 
            plt.annotate((count,survival_list[0][1]),xy=(count,survival_list[0][1]),xycoords='data',xytext=(+9,+4),textcoords='offset points')
            #plt.annotate((count,survival_list[0][1]),xy=(5,5),xycoords='figure fraction')

            plt.subplot(1, 2, 1)
            X=[]
            Y=[]
            for i in range(self.city_num):
                x=survival_list[0][0][i]-1
                X.append(self.city_xy[x][0])
                Y.append(self.city_xy[x][1])
            X.append(X[0])
            Y.append(Y[0])
            plt.plot(X,Y,'ro',X,Y,'r-')
            plt.axis([13,27,90,100])
            plt.title('運行結果')
            plt.pause(0.05)
        survival_list[0][0].append(survival_list[0][0][0])
        for i in range(len(X)-1):
            x = survival_list[0][0][i]-1
            y = survival_list[0][0][i+1]-1
            plt.annotate(self.cal_distance(x,y),xy=((X[i]+X[i+1])/2,(Y[i]+Y[i+1])/2),xycoords='data',xytext=(+0,+4),textcoords='offset points')
        plt.ioff()
        plt.show()
        '''
        plt.subplot(1, 2, 2)
        plt.title('收斂圖')
        plt.plot(self.iter_x,self.iter_y,'b-')    
        plt.plot(g_best_count,g_best,'b.')
        plt.annotate((g_best_count,g_best),xy=(g_best_count,g_best),xycoords='data',xytext=(-15,-10),textcoords='offset points') 
        plt.subplot(1, 2, 1)
        X=[]
        Y=[]
        for i in range(self.city_num):
            x=survival_list[0][0][i]-1
            X.append(self.city_xy[x][0])
            Y.append(self.city_xy[x][1])
        X.append(X[0])
        Y.append(Y[0])
        survival_list[0][0].append(survival_list[0][0][0])
        for i in range(len(X)-1):
            x = survival_list[0][0][i]-1
            y = survival_list[0][0][i+1]-1
            plt.annotate(self.cal_distance(x,y),xy=((X[i]+X[i+1])/2,(Y[i]+Y[i+1])/2),xycoords='data',xytext=(+0,+4),textcoords='offset points')
        plt.plot(X,Y,'ro',X,Y,'r-')
        #plt.axis([13,27,90,100])
        plt.title('運行結果')
        plt.show()

if __name__ == "__main__":
    tsp = TSP(200,50)
    tsp.main()
