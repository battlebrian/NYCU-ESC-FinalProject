import numpy as np
from PIL import Image


MAP_NOT_GET_HERE = [192,192,192]
MAP_NONWALKABLE = [255,69,0]
MAP_WALKABLE = [173,255,47]
MAP_GATEWAY_DEVICE = [255,140,0]

GO_RIGHT_UP = 2
GO_RIGHT = 3
GO_RIGHT_DOWN = 4
GO_UP = 5
GO_STOP = 6
GO_DOWN = 7
GO_LEFT_UP = 8
GO_LEFT = 9
GO_LEFT_DOWN = 10

CAR_SIZE = 15
BLOCK_SIZE = CAR_SIZE    # cm
SPEED = 40


class map_gen:

    def __init__(self,dis:float) -> None:
        self.servers_distance = dis
        distance_coor = int(dis / BLOCK_SIZE)
        if distance_coor % 2 == 1:
            self.server_a_coor = (0,int(distance_coor / 2) + 1)
            self.server_b_coor = (0,distance_coor + int(distance_coor / 2) + 1)
            self.map_length = distance_coor * 2 + 1
            self.map_width = distance_coor * 2 + 1
        else:
            self.server_a_coor = (0,distance_coor)
            self.server_b_coor = (0,int(distance_coor/2*3))
            self.map_length = distance_coor * 2
            self.map_width = distance_coor * 2

        self.map = np.zeros((self.map_width,self.map_length,3),dtype=np.uint8)
        for i in range(self.map_length):
            for j in range(self.map_width):
                self.map[i][j] = MAP_NOT_GET_HERE
        self.map[self.server_a_coor[0]][self.server_a_coor[1]] = MAP_GATEWAY_DEVICE
        self.map[self.server_b_coor[0]][self.server_b_coor[1]] = MAP_GATEWAY_DEVICE

        self.car_now_coor = None

    def add_loca(self,dis_a:float,dis_b:float) -> None:
        coor = self.__get_coordination(dis_a,dis_b)
        if coor[0] >= self.map_width:
            tmp_np = np.zeros((2*(coor[0] - self.map_width + 1),self.map_length,3),dtype=np.uint8)
            for i in range(2*(coor[0] - self.map_width + 1)):
                for j in range(self.map_length):
                    tmp_np[i][j] = MAP_NOT_GET_HERE
            self.map = np.row_stack((self.map,tmp_np))
            self.map_width += 2 * (coor[0] - self.map_width + 1)
        elif coor[1] >= self.map_length:
            tmp_np = np.zeros((self.map_width,2 * (coor[1] - self.map_length + 1),3),dtype=np.uint8)
            for i in range(self.map_width):
                for j in range(2 * (coor[1] - self.map_length + 1)):
                    tmp_np[i][j] = MAP_NOT_GET_HERE
            self.map = np.column_stack((self.map,tmp_np))
            self.map_length += 2 * (coor[1] - self.map_length + 1)

        if coor[0] < 0:
            tmp_np = np.zeros((2*(0 - coor[0]),self.map_length,3),dtype=np.uint8)
            for i in range(2*(0 - coor[0])):
                for j in range(self.map_length):
                    tmp_np[i][j] = MAP_NOT_GET_HERE
            self.map = np.row_stack((tmp_np, self.map))
            self.map_width += 2*(0 - coor[0])
            self.server_a_coor[0] += 2*(0 - coor[0])
            self.server_b_coor[0] += 2*(0 - coor[0])
        elif coor[1] < 0:
            tmp_np = np.zeros((self.map_width,2 * (0 - coor[1]),3),dtype=np.uint8)
            for i in range(self.map_width):
                for j in range(2 * (0 - coor[1])):
                    tmp_np[i][j] = MAP_NOT_GET_HERE
            self.map = np.column_stack((tmp_np,self.map))
            self.map_length += 2 * (0 - coor[1])
            self.server_a_coor[1] += 2 * (0 - coor[1])
            self.server_b_coor[1] += 2 * (0 - coor[1])


        if self.car_now_coor:
            coor_last = self.car_now_coor
        else:
            coor_last = coor
        # get coordiate from distance
        self.car_now_coor = coor

        times = int(((coor[0] - coor_last[0]) ** 2 + (coor[1] - coor_last[1]) ** 2) ** (1/2) / (BLOCK_SIZE/100))
        if times == 0:
            if list(self.map[coor[0]][coor[1]]) == MAP_NOT_GET_HERE:
                self.map[coor[0]][coor[1]] = MAP_WALKABLE
            return
        x_len = (coor[0] - coor_last[0])/times
        y_len = (coor[1] - coor_last[1])/times
        for i in range(times+1):
            if list(self.map[int(coor_last[0] + x_len * i)][int(coor_last[1] + y_len * i)]) == MAP_NOT_GET_HERE:
                self.map[int(coor_last[0] + x_len * i)][int(coor_last[1] + y_len*i)] = MAP_WALKABLE


    def add_obs(self,dis_a:float,dis_b:float):
        coor = self.__get_coordination(dis_a,dis_b)
        # get coordiate from distance
        self.map[coor[0]][coor[1]] = MAP_NONWALKABLE

    def draw_map(self):
        im = Image.fromarray(np.flip(self.map.transpose((1,0,2)),(0)))
        im.save("test.png")

    
    def __get_coordination(self,dis_a:float,dis_b:float) -> list[int]:
        coor = self.__cal_location(dis_a,dis_b)
        y = int(coor[1]/BLOCK_SIZE) + self.server_a_coor[1]
        x = int(coor[0]/BLOCK_SIZE) + self.server_a_coor[0]

        return (x,y)

    def __cal_location(self,dis_a:float,dis_b:float):
        y = (self.servers_distance ** 2 + dis_a ** 2 - dis_b ** 2) / ( 2 * self.servers_distance )
        x = (dis_a ** 2 - y ** 2) ** (1/2)
        return (x,y)

    #def is_cross_obs(self,dis_a,dis_b) -> bool:
    #    coor = self.__get_coordination(dis_a,dis_b)
    #    for i in range(len(self.obstacle[0])):
    #        if (coor[0] - self.obstacle[0][i]) ** 2 + (coor[1] - self.obstacle[1][i]) ** 2 <= 225:
    #            return True
    #        
    #    return False
    #
    #def get_path(self,start_point,end_point):
    #    start_coor = self.__get_coordination(start_point[0],start_point[1])
    #    end_coor = self.__get_coordination(end_point[0],end_point[1])
#
    #    color = np.zeros((self.map_width,self.map_length),dtype=np.uint8)
    #    color[start_coor[0]][start_coor[1]] = 1
    #    q = [start_coor]
#
    #    while q != []:
    #        now_coor = q.pop(0)
    #        if now_coor == end_coor:
    #            break
    #        for i in range(-1,2):
    #            for j in range(-1,2):
#
    #                if now_coor[0] + i >= 0 and now_coor[1] + j >= 0 and color[now_coor[0] + i][now_coor[1] + j] == 0 and self.map[now_coor[0]+i][now_coor[1]+j] == MAP_WALKABLE:
    #                    if i == -1:
    #                        if j == -1:
    #                            color[now_coor[0] + i][now_coor[1] + j] = 2
    #                        elif j == 0:
    #                            color[now_coor[0] + i][now_coor[1] + j] = 3
    #                        elif j == 1:
    #                            color[now_coor[0] + i][now_coor[1] + j] = 4
    #                    elif i == 0:
    #                        if j == -1:
    #                            color[now_coor[0] + i][now_coor[1] + j] = 5
    #                        elif j == 0:
    #                            color[now_coor[0] + i][now_coor[1] + j] = 6
    #                        elif j == 1:
    #                            color[now_coor[0] + i][now_coor[1] + j] = 7
    #                    elif i == 1:
    #                        if j == -1:
    #                            color[now_coor[0] + i][now_coor[1] + j] = 8
    #                        elif j == 0:
    #                            color[now_coor[0] + i][now_coor[1] + j] = 9
    #                        elif j == 1:
    #                            color[now_coor[0] + i][now_coor[1] + j] = 10
    #                    q.append(color[now_coor[0] + i][now_coor[1] + j])
    #    if q == []:
    #        return None
    #    
    #    now_coor = end_coor
    #    path = []
#
    #    while now_coor != start_coor:
    #        path.append(color[now_coor[0]][now_coor[1]])
    #        if color[now_coor[0]][now_coor[1]] == 2:
    #            now_coor = (now_coor[0] + 1,now_coor[1] + 1)
    #        elif color[now_coor[0]][now_coor[1]] == 3:
    #            now_coor = (now_coor[0] + 1,now_coor[1])
    #        elif color[now_coor[0]][now_coor[1]] == 4:
    #            now_coor = (now_coor[0] + 1,now_coor[1] - 1)
    #        elif color[now_coor[0]][now_coor[1]] == 5:
    #            now_coor = (now_coor[0],now_coor[1] + 1)
    #        elif color[now_coor[0]][now_coor[1]] == 6:
    #            now_coor = (now_coor[0],now_coor[1])
    #        elif color[now_coor[0]][now_coor[1]] == 7:
    #            now_coor = (now_coor[0],now_coor[1] - 1)
    #        elif color[now_coor[0]][now_coor[1]] == 8:
    #            now_coor = (now_coor[0] - 1,now_coor[1] + 1)
    #        elif color[now_coor[0]][now_coor[1]] == 9:
    #            now_coor = (now_coor[0] - 1,now_coor[1])
    #        elif color[now_coor[0]][now_coor[1]] == 10:
    #            now_coor = (now_coor[0] - 1,now_coor[1] - 1)
