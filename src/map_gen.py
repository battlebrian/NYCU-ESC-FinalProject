import numpy as np
from PIL import Image


MAP_NOT_GET_HERE = [192,192,192]
MAP_NONWALKABLE = [255,69,0]
MAP_WALKABLE = [173,255,47]
MAP_GATEWAY_DEVICE = [255,140,0]

CAR_SIZE = 15
GAP_SIZE = CAR_SIZE/5
SPEED = 40


class map_gen:

    def __init__(self,dis:float) -> None:
        self.dis = dis
        self.map = np.zeros((100,100,3),dtype=np.uint8)
        for i in range(100):
            for j in range(100):
                self.map[i][j] = MAP_NOT_GET_HERE
        self.map[0][20] = MAP_GATEWAY_DEVICE
        self.map[0][20 + int(dis / CAR_SIZE)] = MAP_GATEWAY_DEVICE

    def add_loca(self,dis_a:float,dis_b:float,dis_a_last:float,dis_b_last:float) -> None:
        coor = self.__cal_location(dis_a,dis_b)
        coor_last = self.__cal_location(dis_a_last,dis_b_last)
        # get coordiate from distance

        times = int(((coor[0] - coor_last[0]) ** 2 + (coor[1] - coor_last[1]) ** 2) ** (1/2) / GAP_SIZE)
        if times == 0:
            if list(self.map[int(coor[0]/15)][int(coor[1]/15 + 20)]) == MAP_NOT_GET_HERE:
                self.map[int(coor[0]/15)][int(coor[1]/15 + 20)] = MAP_WALKABLE
            return
        x_len = (coor[0] - coor_last[0])/times
        y_len = (coor[1] - coor_last[1])/times
        for i in range(times+1):
            if list(self.map[int((coor_last[0] + x_len * i)/15)][int((coor_last[1] + y_len*i)/15 + 20)]) == MAP_NOT_GET_HERE:
                self.map[int((coor_last[0] + x_len * i)/15)][int((coor_last[1] + y_len*i)/15 + 20)] = MAP_WALKABLE




    def add_obs(self,dis_a:float,dis_b:float):
        coor = self.__cal_location(dis_a,dis_b)
        # get coordiate from distance
        self.map[int(coor[0]/15)][int(coor[1]/15 + 20)] = MAP_NONWALKABLE

    def draw_map(self):
        im = Image.fromarray(np.flip(self.map.transpose((1,0,2)),(0)))
        im.save("test.png")


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