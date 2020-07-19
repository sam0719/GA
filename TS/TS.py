import numpy as np
import random
class TS:
    def __init__(self,limit):
        self.limit = limit#迭代次數
        #self.population_size = population_size#種群數量
        self.neighbourhoodNum = 0
        #48個城市的坐標
        self.spe = 5#特攝值
        self.city_xy = [[6734,1453],[2233,10],[5530,1424],[401,841],[3082,1644],[7608,4458],[7573,3716],[7265,1268],[6898,1885],[1112,2049],[5468,2606],[5989,2873],[4706,2674],[4612,2035],[6347,2683],[6107,669],[7611,5184],[7462,3590],[7732,4723],[5900,3561],[4483,3369],[6101 ,1110],[5199 ,2182],[1633 ,2809],[4307 ,2322], [675 ,1006],[7555 ,4819],[7541 ,3981],[3177 ,756],[7352 ,4506],[7545 ,2801],[3245 ,3305],[6426 ,3173],[4608 ,1198],  [23 ,2216],[7248 ,3779],[7762 ,4595],[7392 ,2244],[3484 ,2829],[6271 ,2135],[4985 ,140],[1916 ,1569],[7280 ,4899],[7509 ,3239],  [10 ,2676],[6807 ,2993],[5185 ,3258],[3023 ,1942]]
        self.city_num = len(self.city_xy)
        self.tabu_list = np.zeros(shape=(self.city_num,self.city_num),dtype=int)
        self.tabu_size = 5
        self.path = [np.zeros(shape=(1,self.city_num-1),dtype=int)]
        self.path = self.init_path()#亂序
        self.current_path = self.path#當前路徑
        self.best_path = self.path#最佳路徑
        self.best_path_length = self.cal_fitness(self.best_path)

        
    def init_path(self):
        temp = [x for x in range(self.city_num)]#初始化行走路徑
        random.shuffle(temp)#亂序
        return temp
    def cal_fitness(self,path):#path_list:路徑列表
        sum = self.cal_distance(path[0],path[-1])#第一個到最後一個城市的距離
        for i in range(len(path)-1):
            sum += self.cal_distance(path[i],path[i+1])#路徑表第二個城市到最後一個的總距離
        return sum
    def cal_distance(self,index1,index2): #index:城市表的索引   
        distance = ((self.city_xy[index2][0]-self.city_xy[index2][1])**2+(self.city_xy[index1][0]-self.city_xy[index1][1])**2)**0.5
        return distance
    def compute_path(self,paths):
        result = []
        for one in paths:
            length = self.cal_fitness(one)
            result.append(length)
        return result
    def TS_random(self,x):
        new_path = []
        moves = []
        #城市兩兩移動后的新路徑和對應的移動的城市
        for i in range(len(x)-1):
            for j in range(i+1,len(x)):
                temp = x.copy()
                temp[i],temp[j] = temp[j],temp[i]
                new_path.append(temp)
                moves.append([i,j])
        return new_path,moves
if  __name__ == "__main__":
    ts = TS(200)
    for i in range(ts.limit):
        new_path,moves = ts.TS_random(ts.current_path)
        new_length = ts.compute_path(new_path)
        sort_index = np.argsort(new_length)
        min_l = new_length[sort_index[0]]#最短路徑長度
        min_path = new_path[sort_index[0]]#最短路徑
        min_move = moves[sort_index[0]]#交換的兩個城市
        #更新當前最優路徑
        if min_l < ts.best_path_length:
            ts.best_path_length = min_l
            ts.best_path = min_path
            ts.current_path = min_path
            #更新禁忌表
            if min_move in ts.tabu_list:
                list(ts.tabu_list).remove(min_move)
            list(ts.tabu_list).append(min_move)
            '''
        else:
            # 找到不在禁忌表中的操作
            while min_move in ts.tabu_list:
                sort_index = sort_index[1:]
                min_l = new_length[sort_index[0]]
                min_path = new_path[sort_index[0]]
                min_move = moves[sort_index[0]]
            ts.current_path = min_path
            assert ts.current_path != ts.best_path
            list(ts.tabu_list).append(min_move)
        # 禁忌表超长了
        '''
        if len(ts.tabu_list) > ts.tabu_size:
            ts.tabu_list = ts.tabu_list[1:]
        #ts.iter_x.append(i)
        #ts.iter_y.append(ts.best_path_length)
        print(i, ts.best_path_length)
        print(ts.best_path)
    
    

    