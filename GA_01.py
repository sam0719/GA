import numpy
from time import *
import math
class GA:
    def __init__(self,number,limit):
        self.price = [825594,1677009,1676628,1523970,943972,97426,69666,1296457,1679693,1902996,1844992,1049289,1252836,1319836,953277,2067538,675367,853655,1826027,65731,901489,577243,466257,369261]
        #self.weight = [23,31,29,44,53,38,63,85,89,82]
        self.weight = [382745,799601,909247,729069,467902,44328,34610,698150,823460,903959,853665,551830,610856,670702,488960,951111,323046,446298,931161,31385,496951,264724,224916,169684]
        #self.price = [92,57,49,68,60,43,67,84,87,72]
        self.limit = limit #迭代次數
        self.length = len(self.weight) #長度
        self.number = number #種群數量
        self.bag_capacity = 6404180 #背包容量
        self.survival_rate = 0.2 #选择率
        self.mutation_rate =0.1 #突變率
        #self.tournament = 5 #tournament select
    def takeSecond(self,elem):
        return elem[1]    
    def initial(self):#種群初始化
        init_population = ''
        population_list = []
        for i in range(self.number):
            for j in range(self.length):
                if numpy.random.random()<0.5:
                    init_population += '0'
                else:
                    init_population += '1'
            population_list.append(init_population)
            init_population = ''
        return population_list
    def cal_weight_price(self,population_list,index):#計算總重量和價值
        sum_weight = 0
        sum_price = 0
        for j in range(len(population_list[index])):
            sum_weight = sum_weight + (int(population_list[index][j])*self.weight[j])
            sum_price  = sum_price+(int(population_list[index][j])*self.price[j])
        return sum_weight,sum_price
    def cal_fitness(self,population_list):
        """
        計算fitness,如果重量超過背包大小,適應度為0
        """
        fitness_list = []
        for i in range(len(population_list)):
            weight,price = self.cal_weight_price(population_list,i)
            if(weight > self.bag_capacity):
                fitness_list.append((population_list[i],0))
            else:
               fitness_list.append((population_list[i],price))
        return fitness_list
    def select(self,fitness_list):#輪盤賭選擇
        sum_fit = 0.0
        parent_list=[]
        fit=[]
        for i in range(len(fitness_list)):
            fit.append(fitness_list[i][1])
        sum_fit = sum(fit)
        for j in range(int(self.number*self.survival_rate)):
            accumulator = 0.0
            random_num = numpy.random.randint(0,high=sum_fit/100)
            for ind,val in enumerate(fit):
                accumulator += val
                if accumulator/100 >= random_num:
                    parent_list.append(fitness_list[ind][0])
                    break
        return parent_list
        """
        # tournament selection 
        parent_list = []
        temp=fitness_list
        temp.sort(key=self.takeSecond,reverse=True)
        for j in range(int(self.number*self.survival_rate)):
            parent_list.append(temp[j])
        return parent_list
        """
    def cross(self,parent_list):
        children_list = []
        while len(children_list) < self.number-int(self.number*self.survival_rate):
            father = numpy.random.randint(0,high=len(parent_list))
            mother = numpy.random.randint(0,high=len(parent_list))
            if father != mother:
                random_cross_point = numpy.random.randint(0,high=self.length-1)
                father = parent_list[father]
                mother = parent_list[mother]
                children_list.append(father[:random_cross_point]+mother[random_cross_point:])
                children_list.append(mother[:random_cross_point]+father[random_cross_point:])
        return children_list
    def mutation(self,children_list):
        mutation_list = []
        for i in range(len(children_list)):
            for j in range(len(self.weight)):
                if(numpy.random.random(size=None)<self.mutation_rate):
                    if(children_list[i][j] == "0"):
                        temp = list(children_list[i])
                        temp[j] = "1"
                        children_list[i] = "".join(temp)
                    else:
                        temp = list(children_list[i])
                        temp[j] = "0"
                        children_list[i] = "".join(temp)
            mutation_list.append(children_list[i])
        return mutation_list
    def survivalselect(self,children_list,parent_list):
        child_fitness = self.cal_fitness(children_list)
        fitness = list(child_fitness+parent_list)
        fitness.sort(key=lambda srt: srt[1],reverse=True)
        return fitness[:len(parent_list)]
    def main(self):
        init_population = self.initial()
        fitness_list = self.cal_fitness(init_population)
        count = 0
        f = open("data/GA.epin",mode='a',encoding='utf8')
        f.write('Particle:\n')
        while count<self.limit:
            parent = self.select(fitness_list)
            children = self.cross(parent)
            mutation_list = self.mutation(children)
            survival_list = self.survivalselect(mutation_list,fitness_list)
            #print(children)
            fitness_list = survival_list
            count += 1
            f.write('*'+str(count)+' '+str(survival_list[0][1])+': ')
            for i in range(len(survival_list)):
                f.write(str(survival_list[i][1])+' Bag'+str((i+1))+' ')
                for j in range(self.length):
                    f.write(str(survival_list[i][0][j])+',1,bit'+str((j+1)))
                    if j != self.length-1:
                        f.write(' ')
                f.write('/')
            f.write('\n')
            print('*'+str(i)+' 第%s次迭代:' % count,end=' ')
            #print(survival_list[0][1],end=' ')
            #for i in range(len(survival_list)):
            #    print('Bag%s'%(i+1),end=' ')
            #    for j in range(self.length):
            #        print('%s,0,bit%i'%(survival_list[i][0][j],j+1),end=' ')
            #        print('/',end='')
            #    print('')
            print('\rfitness最大值為',survival_list[0][1])
            print('\r種群為',survival_list[0][0])
        f.close()
            

if __name__ == '__main__':
    start_time = time()
    print(start_time)
    ga = GA(200,300)
    ga.main()
    end_time = time()
    print(end_time)
    print("時間:",end_time-start_time,'秒')