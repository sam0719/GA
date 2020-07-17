import numpy
from time import *
import math
class GA:
    def __init__(self,length,number,limit):
        self.limit = limit #迭代次數
        self.length = length #長度
        self.number = number #種群數量
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
    def convert(self,population_list,index):
        sum=0
        for i in range(len(population_list[index])-1,0,-1):
            sum += int(population_list[index][i])*(2**i)
        return sum
    def cal_fitness(self,population_list):
        """
        計算fitness
        """
        fitness_list = []
        
        for i in range(len(population_list)):
            num = self.convert(population_list,i)
            num = abs(num)
            fitness_list.append((population_list[i],num))
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
            for j in range(self.length):
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
        f = open("data/test.epin",mode='a',encoding='utf8')
        while count<self.limit:
            parent = self.select(fitness_list)
            children = self.cross(parent)
            mutation_list = self.mutation(children)
            survival_list = self.survivalselect(mutation_list,fitness_list)
            #print(children)
            fitness_list = survival_list
            count += 1
            f.write('Dimension : 1\nFormula : sum(|Xi|)\nRange : -100 ~ 100\nPosition :\n*'+str(count)+',世代'+str(count)+' '+str(survival_list[count-1][1]))
            for i in range(len(survival_list)):
                f.write(str(self.convert(init_population,i))+'8,0,2 ')             
            f.write('\n')
            print('*'+str(i)+' 第%s次迭代:' % count,end=' ')
            #print(survival_list[0][1],end=' ')
            #for i in range(len(survival_list)):
            #    print('Bag%s'%(i+1),end=' ')
            #    for j in range(self.length):
            #        print('%s,0,bit%i'%(survival_list[i][0][j],j+1),end=' ')
            #        print('/',end='')
            #    print('')
        f.close()
            #print('\rfitness最大值為',survival_list[0][1])
            #print('\r種群為',survival_list[0][0])

if __name__ == '__main__':
    start_time = time()
    print(start_time)
    ga = GA(8,30,30)
    ga.main()
    end_time = time()
    print(end_time)
    print("時間:",end_time-start_time,'秒')