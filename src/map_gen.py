import matplotlib.pyplot as plt
import numpy as np

MAP_NOT_GET_HERE = 0
MAP_NONWALKABLE = -1
MAP_WALKABLE = 1
MAP_GATEWAY_DEVICE = 2



class map_gen:

    def __init__(self,dis:float) -> None:
        self.dis = dis
        self.map = np.zeros((1000,1000),dtype='i')
        self.map[0][200] = MAP_GATEWAY_DEVICE
        self.map[0][200 + int(int(dis) / 15)] = MAP_GATEWAY_DEVICE

    def add_loca(self,dis_a:float,dis_b:float) -> None:
        coor = self.__cal_location(dis_a,dis_b)
        self.car_loca[0].append(coor[0])
        self.car_loca[1].append(coor[1])

    def add_obs(self,dis_a:float,dis_b:float):
        coor = self.__cal_location(dis_a,dis_b)
        self.obstacle[0].append(coor[0])
        self.obstacle[1].append(coor[1])

    def draw_map(self):
        plt.scatter(self.car_loca[0], self.car_loca[1])
        plt.plot(self.car_loca[0], self.car_loca[1],linewidth = 15)

        plt.scatter(self.obstacle[0], self.obstacle[1],linewidths = 15)

        plt.scatter([0,0], [0,self.dis])
        plt.savefig('test.png')
        plt.show()
        

    def is_cross_obs(self,dis_a,dis_b) -> bool:
        coor = self.__cal_location(dis_a,dis_b)
        for i in range(len(self.obstacle[0])):
            if (coor[0] - self.obstacle[0][i]) ** 2 + (coor[1] - self.obstacle[1][i]) ** 2 <= 225:
                return True
            
        return False


    def __cal_location(self,dis_a:float,dis_b:float):
        y = (self.dis ** 2 + dis_a ** 2 - dis_b ** 2) / ( 2 * self.dis )
        x = (dis_a ** 2 - y ** 2) ** (1/2)
        return (x,y)