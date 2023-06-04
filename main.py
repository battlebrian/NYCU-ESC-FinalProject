import src.map_gen as mg
import re

def reverse(a,b):
    d = (a ** 2 + b ** 2) ** (1/2)
    e = ((500 - b) ** 2 + a ** 2 ) ** (1/2)
    return (d,e)


def main():
    map = mg.map_gen(500)
    coordinate = []
    f = open('test.txt','r')
    for data in f.readlines():
        if data.strip() == '':
            break
        else:
            data = data.strip()
            co = re.findall(r'[\d.]+',data)
            coordinate.append((float(co[0]) * 100,float(co[1]) * 100))
    f.close()

    for coor in coordinate:
        dis = reverse(coor[0],coor[1])
        map.add_loca(dis[0],dis[1])
    dis = reverse(100,100)
    map.add_obs(dis[0],dis[1])
    dis = reverse(102,105)
    map.add_obs(dis[0],dis[1])
    
    map.draw_map()
        

if __name__ == '__main__':
    main()