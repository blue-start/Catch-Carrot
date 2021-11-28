import pygame
import random
import time
from datetime import datetime
#1.게임 초기화
pygame.init()

#2.게임창 옵션 설정
size = [1280,720]
screen = pygame.display.set_mode(size)

title = "Catch carrot"
pygame.display.set_caption(title)

#3.게임 내 필요한 설정
clock = pygame.time.Clock()


class obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
    def put_img(self,address):
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()
        else :
            self.img = pygame.image.load(address)
            self.bx, self.by = self.img.get_size()
    def change_size(self,bx,by):
        self.img = pygame.transform.scale(self.img, (bx,by))
        self.bx, self.by = self.img.get_size()
    def show(self):
        screen.blit(self.img,(self.x,self.y))
              
def crash(a,b):
    if (a.x-b.bx <= b.x) and (b.x <= a.x+a.bx):
        if (a.y-b.by <= b.y)  and (b.y <= a.y+a.by):
            return True
        else :
            return False
    else : 
        return False
            
bu = obj()
bu.put_img("D:/team/bunny.png")
bu.change_size(150,200)
bu.x = round(size [0]/2 - bu.bx/2.5)
bu.y = size[1] -bu.by- 15
bu.move = 5

left_go = False
right_go = False
space_go = False

s_list =[]
c_list =[]

color = (255,204,230)
k = 0

GO = 0
kill = 0
loss = 0

#4-0. 게임 시작 대기 화면
SB = 0
while SB == 0:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                SB = 1
    screen.fill(color)
    font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf",80)
    text = font.render("Catch Carrot", True, (255,255,255))
    screen.blit(text,(400, round(size[1]/2-90)))
    
    font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf",20)
    text_go = font.render("If you want to start game, press the space key!", True, (255,255,255))
    screen.blit(text_go,(430,round(size[1]/2-1)))
    pygame.display.flip()
    
    
#4.메인 이벤트
start_time = datetime.now()
SB = 0
while SB ==0:
    

    #4-1.FPS 설정
    clock.tick(60)
    
    #4-2.각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SB = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_go = True
            elif event.key == pygame.K_RIGHT:
                right_go = True
            elif event.key == pygame.K_SPACE:
                space_go = True
                k = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_go = False
            elif event.key == pygame.K_RIGHT:
                right_go = False
            elif event.key == pygame.K_SPACE:
                space_go = False
           

    #4-3.입력, 시간에 따른 변화
    now_time = datetime.now()
    delta_time = round((now_time - start_time).total_seconds())
    
    
    
    if left_go == True:
        bu.x -= bu.move
        if bu.x<=0:
            bu.x = 0
    elif right_go == True:
        bu.x += bu.move
        if bu.x >= size[0] - bu.bx:
            bu.x = size[0] - bu.bx
            
    if space_go == True and k % 6 == 0:
        sh = obj()
        sh.put_img("D:/team/ball.png")
        sh.change_size(30,30)
        sh.x = round(bu.x + bu.bx/2 - sh.bx/2)
        sh.y = bu.y - sh.by - 10
        sh.move = 13
        s_list.append(sh)
    k += 1
    d_list = []
    for i in range(len(s_list)):
        s = s_list[i]
        s.y -= s.move
        if s.y <= -s.by:
            d_list.append(i)
    d_list.reverse()
    for d in d_list:
        del s_list[d]
             
    if random.random()> 0.99:
        ca = obj()
        ca.put_img("D:/team/carrot.png")
        ca.change_size(40,70)
        ca.x = random.randrange(0, size[0]-ca.bx-round(bu.bx/2))
        ca.y = 10
        ca.move = 1
        c_list.append(ca)

    d_list = []
    for i in range(len(c_list)):
        c = c_list[i]
        c.y += c.move
        if c.y >= size[1]:
            d_list.append(i)
    for d in d_list:
        del c_list[d]
        loss += 1
    
    ds_list =[]
    dc_list =[]
    for i in range(len(s_list)):
        for j in range(len(c_list)):
            s=s_list[i]
            c=c_list[j]
            if crash(s,c) == True:
                ds_list.append(i)
                dc_list.append(j)
    ds_list = list(set(ds_list))
    dc_list = list(set(dc_list))
    ds_list.reverse()
    dc_list.reverse()
    try:
    
        for ds in ds_list:
            del s_list[ds]
        for dc in dc_list:
            del c_list[dc]
            kill += 1
    except:
        pass
   
    for i in range(len(c_list)):
        c = c_list[i]
        if crash(c,bu) == True:
            SB = 1
            GO = 1
            
                
    #4-4. 그리기
    screen.fill(color)
    bu.show()
    for s in s_list:
        s.show()
    for c in c_list:
        c.show()
        
        
    font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf", 25)
    text_kill = font.render("killed : {} loss : {}".format(kill, loss), True, (255,255,255))
    screen.blit(text_kill,(10,5))
    
    text_time = font.render("time : {}".format(delta_time), True, (255,255,255))
    screen.blit(text_time,(size[0]-150,5))
    

    #4-5.업데이트
    pygame.display.flip()

#5.게임종료
while GO == 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GO = 0
    font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf",80)
    text = font.render("Game Over", True, (255,0,0))
    screen.blit(text,(400, round(size[1]/2-80)))
    pygame.display.flip()
    
pygame.quit()
