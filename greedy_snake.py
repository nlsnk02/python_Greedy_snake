import os
import time
import random
from pynput.keyboard import Listener

def bp (s): #用于输出一个屏幕的内容
    os.system('cls') #本程序只适用于Windows
    if s == 'normal':
        print('#'*(L+2))
        for i in range(L//2):
            print('#',end='')
            for j in range(L):
                if Map[i][j].status == 0:
                    print(' ',end='')
                elif Map[i][j].status == 1:
                    print('*',end='')
                elif Map[i][j].status == 2:
                    print('O',end='')
                elif Map[i][j].status == 3:
                    print('@',end='')
                elif Map[i][j].status == 4:
                    print('$',end='')
            print('#')
        print('#'*(L+2))

    elif s == 'over':
        print(
            '''
##############################################################
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#     ____    _    __  __ _____    _____     _______ ____    #
#    / ___|  / \  |  \/  | ____|  / _ \ \   / / ____|  _ \   #
#   | |  _  / _ \ | |\/| |  _|   | | | \ \ / /|  _| | |_) |  #
#   | |_| |/ ___ \| |  | | |___  | |_| |\ V / | |___|  _ <   #
#    \____/_/   \_\_|  |_|_____|  \___/  \_/  |_____|_| \_\  #
#                                                            #
#                                                            #
'''
+'#              你吃到了'+str(speed-30)+'\t个苹果，下次加油             #'+
'''
#                                                            #
#                                                            #
#                                                            #
##############################################################                                          
            ''')
    elif s == 'welcome':
        print(
            '''
##############################################################
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#                                                            #
#     __        _______ _     ____ ___  __  __ _____         #
#     \ \      / / ____| |   / ___/ _ \|  \/  | ____|        #
#      \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _|          #
#       \ V  V / | |___| |__| |__| |_| | |  | | |___         #
#        \_/\_/  |_____|_____\____\___/|_|  |_|_____|        #
#                                                            #
#                                                            #
#                                                            #
#     游戏中只能通过按wasd移动，按下其他非字母键游戏直接等死 #
#     游戏难度 a 地狱 s简单 d普通 w困难                      #
#                                                            #
#     按下他们开始游戏                                       #
#                                                            #
#                                                            #
##############################################################                                              
            ''')


def on_press(key):
    global di
    try:
        di = key.char
    except:
        return False

class block ():
    def __init__ (self, status, direction):
        self.status = status
        self.chD(direction)
    def chD (self,b):
        if b == 'w':
            self.direction = (-1,0)
        elif b == 'a':
            self.direction = (0,-1)
        elif b == 's':
            self.direction = (1,0)
        elif b == 'd':
            self.direction = (0,1)
        else:
            self.direction = -1
            return 0
        return 1
    
def gn (a,b):
    temp = Map[a][b].direction
    return a+temp[0],b+temp[1]

di,L,S,Map = 30,30,30,30
if __name__ == '__main__':
    with Listener(on_press=on_press) as listener:
        bp('welcome')
        while not di in {'w','a','s','d'}:
            time.sleep(0.5)

        #初始化数据
        if di == 'w':
            L,S = 20,2
        elif di == 'a':
            L,S = 30,15
        elif di == 's':
            L,S = 30,15
        elif di == 'd':
            L,S = 20,4
        speed = 30
        head = (7,15)
        tail = (7,12)
        Map = [[block(0,0) for __ in range(L)] for _ in range(L//2)]
        print(len(Map),len(Map[0]))
        Map[7][12] = block(1,'d')
        Map[7][13] = block(2,'d')
        Map[7][14] = block(2,'d')
        Map[7][15] = block(3,'d')
        apple = False
        os.system('cls')

        while 1:
            #apple!
            while not apple:
                a = random.randint(0,L//2-1)
                b = random.randint(0,L-1)
                if Map[a][b].status == 0:
                    Map[a][b].status = 4
                    apple = 1
                    break

            time.sleep(S/speed)
            fh = gn(*head)
            if fh[0]>=L//2 or fh[0]<0 or fh[1]>=L or fh[1]<0 or Map[fh[0]][fh[1]].status in {2,1}:
                bp('over')
                listener.join()
                break
            elif Map[fh[0]][fh[1]].status == 4:
                apple = False
                speed+=1

                Map[head[0]][head[1]].status = 2
                head = fh
                Map[head[0]][head[1]].status = 3
                Map[head[0]][head[1]].chD(di)

            elif Map[fh[0]][fh[1]].status == 0:
                Map[head[0]][head[1]].status = 2
                head = fh
                Map[head[0]][head[1]].status = 3
                Map[head[0]][head[1]].chD(di)
                
                Map[tail[0]][tail[1]].status = 0
                temp = gn(*tail)
                Map[tail[0]][tail[1]].direction = 0
                Map[temp[0]][temp[1]].status = 1
                tail = temp

            bp('normal')