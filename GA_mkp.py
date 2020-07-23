import numpy
from time import *
import math
class GA:
    def __init__(self,number,limit):
        self.Segmentation_index = 0
        self.old_price = []
        self.weight = [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10),(7,10),(8,10),(10,10),(9,10)]
        self.new_weight = self.weight
        self.price = [6,7,8,9,10,11,12,13,15,14]
        self.sum_price = 0
        self.cp_value =[]
        self.limit = limit #迭代次數
        self.length = len(self.weight) #長度
        for i in range(self.length):
            self.cp_value.append(self.price[i] / self.weight[i][0])
        #self.cp_value.sort(reverse=True)#cp值排序
        self.number = number #種群數量
        self.bag_capacity = 275 #背包容量
        self.survival_rate = 0.2 #选择率
        self.mutation_rate =0.5 #突變率
        #self.tournament = 5 #tournament select
    def transform(self):
        new_weight = []
        new_price = []
        for i in range(len(self.new_weight)):
            k=0
            sum =1
            while self.new_weight[i][1] - sum > 0:
                k += 1
                sum += 2**k
            for j in range(k):
                new_weight.append(self.new_weight[i][0]*(2**j))
                new_price.append(self.price[i]*(2**j))
            new_weight.append(self.new_weight[i][0]*(self.new_weight[i][1]-(sum-2**k)))
            new_price.append(self.price[i]*(self.new_weight[i][1]-(sum-2**k)))
        return new_weight,new_price
    def decode(self,population): #將縮短后的種群還原為原來長度
        new_population=''
        for i in range(len(self.weight)-self.Segmentation_index):
            sum = 0
            key = int(math.log(self.weight[i+self.Segmentation_index][1],2))
            for j in range(key):
                new_population += population[j+i*(key+1)] * (2 ** j)
                sum += (2 ** j)
            new_population += population[j+1+i*(key+1)] * (self.weight[i][1] - sum)
        new_population = '1' * 10 * self.Segmentation_index + new_population
        return new_population
    def takeSecond(self,elem):#好像沒用
        return elem[1]    
    def initial(self):#種群初始化
        #對cp值和對應的weight,price進行大到小的排序
        points = zip(self.cp_value,self.weight,self.price)
        sorted_points = sorted(points,reverse=True)
        self.cp_value = [point[0] for point in sorted_points]
        self.weight = [point[1] for point in sorted_points]
        self.new_weight = self.weight
        self.price = [point[2] for point in sorted_points]
        i = 0
        while self.bag_capacity - self.weight[i][0] * self.weight[i][1] > 0: #直到背包承受不下時
            self.bag_capacity = self.bag_capacity - self.weight[i][0] * self.weight[i][1]
            self.sum_price += self.price[i] * self.weight[i][1]
            i += 1
        #if self.bag_capacity % self.weight[i][0] == 0:
        if self.bag_capacity % self.weight[i][0] != 0: 
           #self.bag_capacity = self.bag_capacity + self.weight[i][0] * self.weight[i][1]
            #self.sum_price = self.sum_price - self.price[i] * self.weight[i][1]
            #分割重量和價值列表
            self.Segmentation_index = i#記錄分割時的位置
            #self.old_weight = self.weight[:i-1]
            self.new_weight = self.weight[i:]
            self.old_price = self.price[:i]
            self.price = self.price[i:]
        else:
            self.Segmentation_index = i-1#記錄分割時的位置
            self.bag_capacity = self.bag_capacity + self.weight[i-1][0] * self.weight[i-1][1] + self.weight[i-2][0] * 10
            self.sum_price = self.sum_price - self.price[i-1] * self.weight[i-1][1] - self.price[i-2] * 10
            #self.old_weight = self.weight[:i-2]
            self.new_weight = self.weight[i-1:]
            self.old_price = self.price[:i-1]
            self.price = self.price[i-1:]
        
        '''
        cp值高的先選，去掉對應的內容
        '''
        self.new_weight,self.price = self.transform()
        init_population = ''
        population_list = []
        for k in range(self.number):
            for j in range(len(self.new_weight)):#
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
            sum_weight = sum_weight + (int(population_list[index][j])*self.new_weight[j])
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
            if sum_fit == 0:
                parent_list.append(fitness_list[0][0])
            else:
                accumulator = 0.0
                random_num = numpy.random.randint(0,high=sum_fit)
                for ind,val in enumerate(fit):
                    accumulator += val
                    if accumulator >= random_num:
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
        '''
        for i in range(len(children_list)):        
            if(numpy.random.random() < self.mutation_rate):
                r1 = numpy.random.randint(len(children_list[i]))
                r2 = numpy.random.randint(len(children_list[i]))
                children_list[r1],children_list[r2] = children_list[r2],children_list[r1]
                mutation_list.append(children_list[i])
        '''  
        #隨機選一個染色體 隨機選1位 0變1 1變0
        for i in range(len(children_list)):
            for j in range(len(self.new_weight)):
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
        f = open("data/GA_mkp.epin",mode='w',encoding='utf8')
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
            new_fitness = survival_list[0][1]
            for i in range(len(self.old_price)):
                new_fitness += self.old_price[i] * 10
            print('\rfitness最大值為',new_fitness)
            print('\r種群為',survival_list[0][0])
        new_population = self.decode(survival_list[0][0])
        print('最終種群為',new_population)    
        c = 2
        multi_solution = {}
        multi_solution[survival_list[0][0]] = survival_list[0][1]#dict
        for i in range(1,len(survival_list),1):
            if survival_list[i][1]  == survival_list[0][1] and survival_list[i][0] not in multi_solution:
                print("第"+str(c)+"種解為:",self.decode(survival_list[i][0]))#求多種解
                c+=1
                multi_solution[survival_list[i][0]] = survival_list[i][1]
        f.close()
            

if __name__ == '__main__':
    start_time = time()
    print(start_time)
    ga = GA(200,500)
    ga.main()
    end_time = time()
    print(end_time)
    print("時間:",end_time-start_time,'秒')