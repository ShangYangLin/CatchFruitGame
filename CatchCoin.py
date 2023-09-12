import pygame,sys,os,random
pygame.init()

class rect():#画出小人
    def __init__(self,filename,initial_position):
        self.image=pygame.image.load("basket.png")
        self.rect=self.image.get_rect()
        self.rect.topleft=initial_position
        
class goldrect(pygame.sprite.Sprite):#绘出金币
    def __init__(self,gold_position,speed,random_num):
        pygame.sprite.Sprite.__init__(self)

        if random_num==0:
            self.image=pygame.image.load("strawberry.png")
        elif random_num==1:
            self.image=pygame.image.load("orange.png")
        elif random_num==2:
            self.image=pygame.image.load("pea.png")
        elif random_num==3:
            self.image=pygame.image.load("mango.png")
        elif random_num==4:
            self.image=pygame.image.load("pineapple.png")
        elif random_num==5:
            self.image=pygame.image.load("lemon.png")
        elif random_num==6:
            self.image=pygame.image.load("apple.png")
        else:
            self.image=pygame.image.load("watermelon.png")
        self.rect=self.image.get_rect()
        self.rect.topleft=gold_position
        self.speed=speed

    def move(self):
        self.rect=self.rect.move(self.speed)


def drawback(): #绘出背景图片
    my_back=pygame.image.load('qi3.jpg') 
    bakscreen.blit(my_back,[0,0])

        
def loadtext(levelnum,score,highscore,miss):#绘出成绩、level、最高分等
    my_font=pygame.font.SysFont(None,48)
    levelstr='Level:'+str(levelnum)
    text_screen=my_font.render(levelstr, True, (255, 0, 0))
    bakscreen.blit(text_screen, (850,50))
    highscorestr='Higescore:'+str(highscore)
    text_screen=my_font.render(highscorestr, True, (255, 0, 0))
    bakscreen.blit(text_screen, (850,85))
    scorestr='Score:'+str(score)
    text_screen=my_font.render(scorestr, True, (255, 0, 0))
    bakscreen.blit(text_screen, (850,120)) 
    missstr='Miss:'+str(miss)
    text_screen=my_font.render(missstr, True, (255, 0, 0))
    bakscreen.blit(text_screen, (850,155))   

def loadgameover(scorenum,highscore):#绘出GAME OVER
    my_font=pygame.font.SysFont(None,50)
    levelstr='GAME OVER'
    over_screen=my_font.render(levelstr, True, (255, 0, 0))
    bakscreen.blit(over_screen, (470,240))
    highscorestr='YOUR SCORE IS '+str(scorenum)
    over_screen=my_font.render(highscorestr, True, (255, 0, 0))
    bakscreen.blit(over_screen, (450,290))
    if scorenum>int(highscore):#写入最高分
        highscorestr='YOUR HAVE GOT THE HIGHEST SCORE!'
        text_screen=my_font.render(highscorestr, True, (255, 0, 0))
        bakscreen.blit(text_screen, (270,340))
        highfile=open('highscore','w')
        highfile.writelines(str(scorenum))  
        highfile.close()  
    
def gethighscore(): #读取最高分
    if os.path.isfile('highscore'):
        highfile=open('highscore','r')
        highscore=highfile.readline() 
        highfile.close() 
    else:
        highscore=0
    return highscore
                  
bakscreen=pygame.display.set_mode([1100,780])
bakscreen.fill([0,160,233])
pygame.display.set_caption('I like fruit!')
drawback()



levelnum=1 #level
scorenum=0 #得分
highscore=gethighscore()#最高分
miss=0#失誤次數，可容許3次
ileft=1  #记录向左移动步数，用来控制图片
iright=10 #记录向右移动步数，用来控制图片
x=100
y=580
filename='image\\1.png'
backimg_ren=rect(filename,[x,y])
bakscreen.blit(backimg_ren.image,backimg_ren.rect)
loadtext(levelnum,scorenum,highscore,miss)
goldx=random.randint(150,1000)
speed=[0,levelnum+4]
random_num=random.randint(0,7)
mygold=goldrect([goldx,100],speed,random_num) 
pygame.display.update()


while True:
    if scorenum>0:#当得分是50的倍数时修改level
        levelnum=int(scorenum/50)+1
        speed=[0,levelnum+4]
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
    #make gold    

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT]:#按下左键

        drawback()  
        loadtext(levelnum,scorenum,highscore,miss)

        if iright > 14 :iright=10
        iright=iright+1
        filename='image\\'+str(iright)+'.png'
        if x<60 :
            x=60
        else:
            x=x-10

        backimg_surface=rect(filename,[x,y])
        bakscreen.blit(backimg_surface.image,backimg_surface.rect)

        
    if pressed_keys[pygame.K_RIGHT]:#按下右键

        drawback()
        loadtext(levelnum,scorenum,highscore,miss)

        if ileft > 4 :ileft=0
        ileft=ileft+1
        filename='image\\'+str(ileft)+'.png'
        if x>860:
            x=860
        else:
            x=x+10

        backimg_surface=rect(filename,[x,y])
        bakscreen.blit(backimg_surface.image,backimg_surface.rect)

    drawback()
    loadtext(levelnum,scorenum,highscore,miss)
    mygold.move()
    bakscreen.blit(mygold.image,mygold.rect) 
    
    backimg_surface=rect(filename,[x,y])
    bakscreen.blit(backimg_surface.image,backimg_surface.rect)
    if mygold.rect.top>700 and miss>=2:
        loadgameover(scorenum,highscore)
    else:
        if mygold.rect.top>700:#判断金币是否着地，一但着地，游戏结束    
            miss+=1
            loadtext(levelnum,scorenum,highscore,miss)
            goldx=random.randint(50,580)
            random_num=random.randint(0,7)
            mygold=goldrect([goldx,100],speed,random_num) 
    
    if mygold.rect.colliderect(backimg_surface.rect):#判断金币是否与小人碰撞，如果碰撞表示小人接到金币
        if random_num<2:
            scorenum+=5
        elif random_num<4:
            scorenum+=15
        elif random_num<6:
            scorenum+=30
        else:
            scorenum+=50
        loadtext(levelnum,scorenum,highscore,miss)
        goldx=random.randint(50,580)
        random_num=random.randint(0,7)
        mygold=goldrect([goldx,100],speed,random_num) 
    pygame.display.update()