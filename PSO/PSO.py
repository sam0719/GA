import numpy as np
import random
import matplotlib.pyplot as plt
import math

class particle:
    def __init__(self,c1,c2,w,size,limit):
        self.c1 = c1#個人經驗權重
        self.c2 = c2#群體經驗權重
        self.w = w#慣性權重
        #self.length = 8
        self.dim = 1#維度
        self.population_size = size#粒子大小
        self.limit = limit#迭代次數
        self.x_bound = [-10,10]#解空間範圍
        self.v_max = 0.5*(self.x_bound[1]-self.x_bound[0])#速度最大值 0.5*(x上界-x下界)
        #初始化粒子群位置
        self.x = np.random.uniform(self.x_bound[0],self.x_bound[1],(self.population_size,self.dim))
        #f(x)
        self.y = np.zeros(shape=[self.population_size,self.dim])
        self.v = np.random.rand(self.population_size,self.dim)#初始化粒子群速度
        fitness = self.cal_fitness(self.x)#計算初始粒子群適應度
        self.p = self.x #個體最佳位置
        self.p_best_fitness = fitness#個體最佳適應值
        self.g = self.x[np.argmax(fitness)]#群體最佳位置
        self.g_best_fitness = np.max(fitness)#群體最佳適應值
        #print(self.x)
    def cal_fitness(self,x):#計算fitness
        self.y = x*np.sin(10*math.pi*x)+2#xsin(10πx)+2
        return np.sum(x*np.sin(10*math.pi*x)+2,axis=1)
    def evolve(self):
        plotx=[]
        ploty=[]
        f = open("data/PSO.epin",mode='w')#創建EPanel配置,UTF-8會亂碼
        f.write('Dimension : '+str(self.dim)+'\nFormula : 2+Xi*sin(10*Pi*Xi)\nRange : '+str(self.x_bound[0])+' ~ '+str(self.x_bound[1])+'\nPosition :\n')
        for i in range(self.limit):
            r1 = np.random.rand(self.population_size,self.dim)#一個[0,1)組成的矩陣
            r2 = np.random.rand(self.population_size,self.dim)
            self.v = self.v*self.w+self.c1*r1*(self.p-self.x)+self.c2*r2*(self.g-self.x)
            for j in range(self.population_size):
                #如果速度越界則設置成0到v_max的隨機數
                if self.v[j] > self.v_max or self.v[j] < -self.v_max:
                    self.v[i] = np.random.uniform(0.0,self.v_max)
            self.x = self.x+self.v
            for j in range(self.population_size):
                #如果粒子位置越界則設置成隨機數
                if self.x[j] > self.x_bound[1] or self.x[j] < self.x_bound[0]:
                    self.x[j] = np.random.uniform(self.x_bound[0],self.x_bound[1])
            '''
            plt.clf()
            plt.scatter(self.x[:, 0], self.y[:, 0], s=30, color='k')
            plt.xlim(self.x_bound[0], self.x_bound[1])
            plt.ylim(-self.v_max, self.v_max)
            plt.pause(0.01)
            #散佈圖
            '''
            fitness = self.cal_fitness(self.x)
            evolve_obj = np.less(self.p_best_fitness,fitness) #前者比後者小時返回True
            self.p[evolve_obj] = self.x[evolve_obj] #更新個體最優解
            self.p_best_fitness[evolve_obj] = fitness[evolve_obj]
            if np.max(fitness) > self.g_best_fitness:
                self.g = self.x[np.argmax(fitness)]
                self.g_best_fitness = np.max(fitness)
            print('第%s次迭代'%(i+1))
            print('最好的fitness為:%.8f,平均fitness為:%.5f,x為%.5f:'%(self.g_best_fitness,np.mean(fitness),self.g))
            ploty.append(self.g_best_fitness)
            plotx.append(i)
            f.write('*'+str(i+1)+',第'+str(i+1)+'世代 '+str('{:.6f}'.format(self.g_best_fitness)+':'))
            for j in range(self.population_size):
                f.write(str(self.x[j][0])+',8,0,2 ')
            f.write('\n')
        f.close()
        plt.plot(plotx,ploty)
        
if __name__ == '__main__':
    pso = particle(1.4,1.4,0.6,100,100)
    pso.evolve()
    plt.show()#散佈圖

    