# F1 high(BLOCK1) START / RELAX END
# F2 HIGH(BLOCK1) END / RELAX START
# F1 LOW (BLOCK2) START / RELAX END
# F3 LOW (BLOCK2) END / RELAX START
import pygame, sys ,os,csv,serial
from pygame import *
import pandas as pd


pygame.init()

#串口
#ser = serial.Serial("COM3",9600,timeout=0.5)


#输入患者信息
def get_subj_info():
    subj_id = input("subject ID:")
    subj_name = input("subject Name:")
    subj_gender = input("subject Gender:")
    subj_age = input("subject Age:")
    return [subj_id , subj_name , subj_gender , subj_age]

subj = get_subj_info()
'''
if not os.path.exists('data_file'):
    os.mkdir('data_file')
data_file = open('data_file/'+'_'.join(subj[:2])+'.csv','w',encoding='UTF-8')
writer = csv.writer(data_file)
writer.writerow(["ID","NAME","GENDER","AGE","TRAIL","LEFT","TOP","WIDTH","HEIGHT",
                 "FAULT" ,"DELAY" , "TIME_DOWN" , "TIME_UP" ,"POINT_X" ,"POINT_Y" , "CORRECT"])
'''

clock = pygame.time.Clock()
TIME_EVERYFRAMW = 0
STATUS = []

#状态机文件
if not os.path.exists('data_file'):
    os.mkdir('data_file')
data_file = open('data_file/'+'_'.join(subj[:2])+'.csv','w',encoding='UTF-8',newline='')
writer = csv.writer(data_file)
writer.writerow(["BLOCK","TIME","STATUS","X","Y"])


#测试输出文件
if not os.path.exists('data_file_test'):
    os.mkdir('data_file_test')
data_file_test = open('data_file_test/'+'_'.join(subj[:2])+'.csv','w',encoding='UTF-8',newline='')
writer_test = csv.writer(data_file_test)
writer_test.writerow(["BLOCK","TIME_MOVE","ID","SUCESS"])

#定义颜色
WHITE = pygame.color.Color(255,255,255)
BLACK = pygame.color.Color(0,0,0,)
GRAY = pygame.color.Color(220,220,220)
BLUE = pygame.color.Color(240,248,255)

#定义pygame程序框大小
w = 65                                                                         #目标正方形宽度（像素）
BACK_COLOR = BLACK
SCREEN_WIDTH = 17.2 * w
SCREEN_HEIGHT = 13 * w
win = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), DOUBLEBUF|HWSURFACE)
win.fill(BACK_COLOR)


#从number文件导入目标方块
def import_csv(file):
    TARGET = []
    i = 0
    numberFile = pd.read_csv(file)

    while i < 31:
        TARGET.append([numberFile.iloc[i]["X"] * w, numberFile.iloc[i]["Y"] * w, numberFile.iloc[i]["WIDTH"] * w, numberFile.iloc[i]["WIDTH"] * w])
        i += 1
    return TARGET,numberFile



def text_msg(msg, loc):
    txt_font = pygame.font.SysFont('Microsoft YaHei',50)
    txt_msg = txt_font.render(msg,True,WHITE)
    pygame.Surface.fill(win, BACK_COLOR)
    win.blit(txt_msg,((loc[0]-txt_msg.get_width())/2,(loc[1]-txt_msg.get_height())/2))
    pygame.display.flip()
    pygame.event.pump()


#text_msg("点击白色目标并保持，下个目标出现快速点击",(SCREEN_WIDTH,SCREEN_HEIGHT))
#pygame.time.wait(3000)


def block(choice):
    if choice == "high" :
        TARGET = import_csv("number_file/number_high.csv")[0]
        numberFile = import_csv("number_file/number_high.csv")[1]
    else:
        TARGET = import_csv("number_file/number_low.csv")[0]
        numberFile = import_csv("number_file/number_low.csv")[1]


    text_msg("点击屏幕开始", (SCREEN_WIDTH, SCREEN_HEIGHT))
    START = False
    pygame.event.clear()
    while not START:
        for ev_START in pygame.event.get():
            if ev_START.type == FINGERUP:
                #ser.write("F1".encode())
                START = True
                TIME_BEGIN = time.get_ticks()
                print("BEGIN_BLOCK")
                print(TIME_BEGIN)
                writer.writerow([choice,TIME_BEGIN,"BEGIN_BLOCK","-1","-1"])

    win.fill(BACK_COLOR)
    pygame.display.flip()

    TIME_DOWN_LASTTRAIL = 0                                                                          #设置第一次trail的TIME_DOWN_LASTTRAIL
    TIME_NEXT_BUTTON_UNTOUCH = 0
    TRAIL = 1
    i = 0
    while TRAIL <= 31:

        pars_loc = [TARGET[i][0],TARGET[i][1]]
        pars_size = [TARGET[i][2], TARGET[i][3]]
        RECT_CURRENT_TARGET = pygame.Rect(TARGET[i][0],TARGET[i][1],TARGET[i][2],TARGET[i][3])
        RECT_CURRENT_TARGET.center = (TARGET[i][0],TARGET[i][1])
        if i < 30:
            RECT_NEXT_TARGET = pygame.Rect(TARGET[i + 1][0], TARGET[i + 1][1], TARGET[i + 1][2], TARGET[i + 1][3])
            RECT_NEXT_TARGET.center = (TARGET[i + 1][0], TARGET[i + 1][1])


        rect_current = pygame.draw.rect(win,WHITE,RECT_CURRENT_TARGET)
        pygame.display.flip()
        TIME_BEGIN_TRAIL = time.get_ticks()                                        #就是前一次up的时间
        print("BEGIN_TRAIL_UNTOUCH")
        #print(TIME_BEGIN_TRAIL)
        #writer.writerow(["",TIME_BEGIN_TRAIL, "BEGIN_TRAIL_UNTOUCH", "-1", "-1"])

        if TRAIL > 1:                                                            #  current target 出现在前一次，的时间
            TIME_CURRENT_BUTTON_APPEAR = TIME_DOWN_LASTTRAIL + 1
        else:
            TIME_CURRENT_BUTTON_APPEAR = TIME_BEGIN_TRAIL


        print("CURRENT_BUTTON_appear")
        print(TIME_CURRENT_BUTTON_APPEAR)

        TOUCH_DOWN_EFFECT = False
        TIME_OVER5S = False
        CURRENT_DISPLAY_DISAPPREAR = False
        FAULT = 0
        CORRECT = 0
        DELAY = 0

        while not TOUCH_DOWN_EFFECT:
            clock.tick(60)
            TIME_NOW = pygame.time.get_ticks()
            STATUS = "CUUUENT_BUTTON_UNTOUCH"
            POINT_X = -1
            POINT_Y = -1
            writer.writerow([choice, TIME_NOW, STATUS, POINT_X, POINT_Y])

            if TIME_NOW - TIME_CURRENT_BUTTON_APPEAR >= 5000:                               #BUTTON出现5s,不点击
                print("超时啦")
                STATUS = "NEXT_BUTTON_UNTOUCH"
                writer.writerow([choice, TIME_NOW, STATUS, "-1", "-1"])
                TIME_DOWN_LASTTRAIL = TIME_NOW
                rect_current = pygame.draw.rect(win, BACK_COLOR, RECT_CURRENT_TARGET)      # 隐藏当前图片
                pygame.display.flip()
                break                                                                       #跳出上面的while循环

            else:
                for ev_DOWN in pygame.event.get():                                          #5S内点击
                    if ev_DOWN.type == FINGERDOWN:
                        POINT_X = ev_DOWN.x * SCREEN_WIDTH
                        POINT_Y = ev_DOWN.y * SCREEN_HEIGHT
                        TIME_TOUCH_DOWN_FIRST = time.get_ticks()

                        print("finger down")
                        PASS_1S = False
                        while not PASS_1S:
                            clock.tick(60)
                            TIME_NOW = pygame.time.get_ticks()
                            STATUS = "TOUCH_DOWN"
                            writer.writerow([choice, TIME_NOW, STATUS, POINT_X, POINT_Y])

                            if TIME_NOW - TIME_TOUCH_DOWN_FIRST < 1000:
                                for ev_UP in pygame.event.get():
                                    if ev_UP.type == FINGERUP:
                                        print("miss-fingerup")
                                        STATUS = "TOUCH_UP"
                                        writer.writerow([choice, TIME_NOW, STATUS, POINT_X, POINT_Y])
                                        PASS_1S = True
                                        TOUCH_DOWN_EFFECT = False
                                        FAULT += 1
                                    else:
                                        pass

                            elif TIME_NOW - TIME_TOUCH_DOWN_FIRST >= 1000 :
                                TIME_DOWN_LASTTRAIL = TIME_TOUCH_DOWN_FIRST                                          # 这次的TIME_DOWM+1即时是下次trail的起始时间
                                TIME_MOVE = TIME_TOUCH_DOWN_FIRST -TIME_NEXT_BUTTON_UNTOUCH

                                if pygame.Rect.collidepoint(rect_current,POINT_X,POINT_Y):
                                    CORRECT = 1                                                                      # 如果点到了
                                    print("CORRECT")
                                else:
                                    CORRECT = 0
                                    print("WRONG")
                                #测试输出
                                writer_test.writerow([choice,TIME_MOVE,numberFile.iloc[i]["ID"], CORRECT])

                                if TRAIL < 31:
                                    rect_next = pygame.draw.rect(win,WHITE,RECT_NEXT_TARGET)                         #展示下一张图片
                                    pygame.display.flip()
                                if TRAIL == 31:
                                    text_msg("松开手指，休息一下", (SCREEN_WIDTH, SCREEN_HEIGHT))


                                if TRAIL <= 31:
                                    rect_current = pygame.draw.rect(win, BACK_COLOR, RECT_CURRENT_TARGET)            # 隐藏当前图片
                                    pygame.display.flip()

                                PASS_1S = True
                                TOUCH_DOWN_EFFECT = True






        while TOUCH_DOWN_EFFECT:
            clock.tick(60)
            TIME_NOW = pygame.time.get_ticks()
            STATUS ="TOUCH_DOWN"
            writer.writerow([choice, TIME_NOW, STATUS, POINT_X, POINT_Y])


            if TIME_NOW - TIME_CURRENT_BUTTON_APPEAR > 5000 and not TIME_OVER5S:                                         # 图片展示超过5s
                #DELAY += 1
                TIME_OVER5S = True
                print("走神了")
                break

            for ev_UP in pygame.event.get():
                if ev_UP.type == FINGERUP:
                    TIME_NOW = pygame.time.get_ticks()
                    STATUS = "TOUCH_UP"
                    writer.writerow([choice, TIME_NOW, STATUS, POINT_X, POINT_Y])
                    STATUS = "NEXT_BUTTON_UNTOUCH"
                    writer.writerow([choice, TIME_NOW, STATUS, "-1", "-1"])
                    TIME_NEXT_BUTTON_UNTOUCH = TIME_NOW
                    print("finger up")
                    # 插入 output
                    TOUCH_DOWN_EFFECT =False

        '''
        trail_data =subj + [TRAIL]  + pars_loc + pars_size + [FAULT] +[DELAY] + [TIME_DOWN] + [TIME_UP] +[POINT_X] +[POINT_Y] + [CORRECT]
        trail_data = map(str,trail_data)
        trail_data = ",".join(trail_data) + "\n"
        data_file.write(trail_data)
        '''

        TRAIL += 1
        i += 1

#休息时间
def relax(time):
    TIME_BEGIN_RELAX = pygame.time.get_ticks()
    RUN = True
    while RUN:
        TIME_NOW = pygame.time.get_ticks()
        if TIME_NOW < TIME_BEGIN_RELAX + time:
            image = pygame.image.load(r"cross.png")
            pygame.Surface.fill(win, BACK_COLOR)
            win.blit(image, ((SCREEN_WIDTH - image.get_width()) / 2, (SCREEN_HEIGHT - image.get_height()) / 2))
            pygame.display.flip()
            pygame.event.pump()
        else:
            RUN = False

#writer.writerow(["Blook1"])

block("low")
#ser.write("F2".encode())

relax(30000)

block("high")
#ser.write("F3".encode())

relax(30000)

block("high")
#ser.write("F3".encode())

relax(30000)

block("low")
#ser.write("F2".encode())

relax(30000)

block("high")
#ser.write("F3".encode())

relax(30000)

block("low")
#ser.write("F2".encode())

relax(30000)


data_file.close()
#ser.close()
sys.exit()