import src.map_gen as mg
import re

#def reverse(a,b):
#    d = (a ** 2 + b ** 2) ** (1/2)
#    e = ((500 - b) ** 2 + a ** 2 ) ** (1/2)
#    return (d,e)
#
#
#def main():
#    map = mg.map_gen(500)
#    coordinate = []
#    f = open('test.txt','r')
#    for data in f.readlines():
#        if data.strip() == '':
#            break
#        else:
#            data = data.strip()
#            co = re.findall(r'[\d.]+',data)
#            coordinate.append((float(co[0]) * 100,float(co[1]) * 100))
#    f.close()
#
#    for coor in coordinate:
#        dis = reverse(coor[0],coor[1])
#        map.add_loca(dis[0],dis[1])
#    dis = reverse(100,100)
#    map.add_obs(dis[0],dis[1])
#    dis = reverse(102,105)
#    map.add_obs(dis[0],dis[1])
#    
#    map.draw_map()


STEP_LENGTH = 0.15 # m

def dfs(map:mg.map_gen):
    rotate_angle = 0

    now_location = getLocation()
    map.add_loca(now_location)
    map.update_car_coordination(now_location)
    tmp_direction = ['front','left front','left','left back','back','right back','right','right front']

    ind = 0
    for direction in tmp_direction:
        if map.is_not_get_place(now_location,direction=direction,length=STEP_LENGTH):
            rotateCounterclockwise(ind*45 - rotate_angle)
            map.update_car_direction(ind*45 - rotate_angle)
            rotate_angle = ind*45
            walk_length = 0
            for i in range(STEP_LENGTH*100):
                if not faceObstacle():
                    moveForward(0.01)
                    walk_length += 0.01
                else:
                    map.add_obs(getLocation(),'front',0.01)
                    break
            dfs(map)

            for i in range(walk_length):
                moveBackward(0.01)
            map.update_car_coordination(getLocation())

        ind += 1

    if 360 - rotate_angle > rotate_angle:
        rotateCounterclockwise(-rotate_angle)
    else:
        rotateCounterclockwise(360 - rotate_angle)
        
    

def main():
    dis = getServersDistance()

    
    if not faceObstacle():
        back_location = getLocation()
        moveForward(STEP_LENGTH)
        front_location = getLocation()
    else:
        front_location = getLocation()
        moveBackward(STEP_LENGTH)
        back_location = getLocation()

    
    map = mg.map_gen(dis,back_location,front_location)

    dfs(map)

    map.draw_map()



if __name__ == '__main__':
    main()