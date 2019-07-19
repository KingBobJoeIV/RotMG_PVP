import pygame
import time
import threading
import random
#import evdev
#from evdev import InputDevice, categorize, ecodes
#from select import select

#gamepad = InputDevice('/dev/input/event4')
#keyboard = InputDevice('/dev/input/event3')

aBtn = 288
bBtn = 289
xBtn = 290
yBtn = 291

up = 0
down = 32
left = 18
right = 33

start = 297
select = 296

lTrig = 292
rTrig = 293

pygame.init()

display_width = 1000
display_height = 800


#character locations
x1 = (display_width*.2)
y1 = (display_height*.8)
x2 = (display_width*.8)
y2 = (display_height*.8)


#class hp
wizzy_hp = 1000
necro_hp  = 1000
mystic_hp = 1000
knight_hp = 1000
trickster_hp = 1000
archer_hp = 1000
sin_hp = 1000

#class projectile initial directions
direction_p1 = ''
direction_p2 = ''   
#direction_p1 = ''
#direction_p2 = ''

#if player isn't moving
x1_change = 0
y1_change = 0
x2_change = 0
y2_change = 0



#start positions for each projectile
p1_startx = x1
p1_starty = y1


p2_startx = x2
p2_starty = y2

is_comp = False
counter = 0
comp_choice = 1

#Projectile specifics:

#wizard
spell_width = 50
spell_height = 50
spell_speed = 14

#necro
skull_width = 50
skull_height = 50
skull_speed = 9

#mystic
orb_width = 50
orb_height = 50
orb_speed = 7
stasis_p1 = False
stasis_p2 = False
stasis_effect1 = 0
stasis_effect2 = 0

#knight
sheild_width = 75
sheild_height = 75
sheild_speed = 7
sheild_p1 = False
sheild_p2 = False
sheild_effect1 = 0
sheild_effect2 = 0

#trickster
prism_width = 50
prism_height = 50
prism_speed = 10
prism_effect1 = False 
prism_effect2 = False
tp_p1 = 0
tp_p2 = 0

#archer
quiver_width = 50
quiver_height = 50
quiver_speed = 7
para_p1 = False
para_p2 = False
para_effect1 = 0
para_effect2 = 0

#sin
poison_width = 100
poison_height = 100
poison_speed = 6
poison_p1 = False
poison_p2 = False
poison_effect1 = 0
poison_effect2 = 0

p1_w = 0
p1_h = 0
p1_speed = 0

p2_w = 0
p2_h = 0
p2_speed = 0

#create window
gameDisplay = pygame.display.set_mode((display_width,display_height))


#title
pygame.display.set_caption('RotMG PVP')


#fps
clock = pygame.time.Clock()


#colors
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,100,200)
hover_red = (255,0,0)
hover_green = (0,255,0)
hover_blue = (0,0,255)
yellow = (200,200,0)
hover_yellow = (255,255,0)
cyan = (0,255,255)

pause = True


#chars
wizzy = pygame.image.load('wizzy.png')
necromancer = pygame.image.load('necro.png')
mystic = pygame.image.load('mystic.png')
knight = pygame.image.load('knight.png')
trickster = pygame.image.load('trickster.png')
archer = pygame.image.load('archer.png')
sin = pygame.image.load('sin.png')
#staff = pygame.image.load('staff.png')


#soundtracks
death_sound = pygame.mixer.Sound("oof.wav")
pygame.mixer.music.load("rotmg.mp3")


#char hitboxes
char1_width = 64
char2_width = 64
char1_height = 64
char2_height = 64


class Character:
    def __init__(self,sprite,hp,projectile,proj_w,proj_h,proj_speed):
        self.sprite = sprite
        self.hp = hp
        self.projectile = projectile
        self.proj_w = proj_w
        self.proj_h = proj_h
        self.proj_speed = proj_speed

        
#players
player1 = None
player2 = None



        


#projectile initializations
def spell(spellx, spelly, spellw, spellh, color):
    pygame.draw.rect(gameDisplay, color, [spellx, spelly, spellw, spellh])

def skull(skullx, skully, skullw, skullh, color):
    pygame.draw.rect(gameDisplay, color, [skullx, skully, skullw, skullh])

def orb(orbx, orby, orbw, orbh, color):
    pygame.draw.rect(gameDisplay, color, [orbx, orby, orbw, orbh])

def sheild(sheildx, sheildy, sheildw, sheildh, color):
    pygame.draw.rect(gameDisplay, color, [sheildx, sheildy, sheildw, sheildh])

def prism(prismx, prismy, prismw, prismh, color):
    pygame.draw.rect(gameDisplay, color, [prismx, prismy, prismw, prismh])
    
def quiver(quiverx,quivery,quiverw, quiverh, color):
    pygame.draw.rect(gameDisplay, color, [quiverx, quivery, quiverw, quiverh])

def poison(poisonx, poisony, poisonw, poisonh, color):
    pygame.draw.rect(gameDisplay, color, [poisonx, poisony, poisonw, poisonh])


#multithreading
def key_input():
    global direction_p1, x1_change,y1_change
    
    #print("current1:")
    #print(time.time())
    #print("t1: ")
    #print(t1_end)
    for event in pygame.event.get():
        t1_end = time.time()+.05
        while time.time()<t1_end:
            if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x1_change = -5
                    print("left")
                    direction_p1 = 'left'
                elif event.key == pygame.K_d:
                    x1_change = 5
                    print("right")
                    direction_p1 = 'right'
                elif event.key == pygame.K_s:
                    y1_change = 5
                    print("down")
                    direction_p1 = 'down'
                elif event.key == pygame.K_w:
                    y1_change = -5
                    print("up")
                    direction_p1 = 'up'
                if event.key == pygame.K_p:
                    pause = True
                    paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    x1_change = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    y1_change = 0
        break
        print("out_key")
def controller_input():
    global direction_p2, x2_change,y2_change
    #print("current2: ")
    #print(time.time())
    #print("t2: ")
    #print(t2_end)
    print(gamepad)
    print(type(gamepad))
    x,y,z = select([gamepad],[],[])
    for event in gamepad.read():
        t2_end = time.time()+.5
        while time.time()<t2_end:
            #print (time.time())
            if event.type == ecodes.EV_KEY:
                if event.value == 1:
                    print('hi')
                    if event.code == yBtn:
                        print("Y")
                        x2_change = -5
                        direction_p2 = 'left'
                elif event.code == aBtn:
                        print("A")
                        x2_change = 5
                        direction_p2 = 'right'
                elif event.code == bBtn:
                        print("B")
                        direction_p2 = 'down'
                        y2_change = 5
                elif event.code == xBtn:
                        print("X")
                        direction_p2 = 'up'
                        y2_change = -5
                if event.value == 0:
                    if event.code == yBtn:
                        print("Y_not pressed")
                        x2_change = 0
                if event.value == 0:
                    if event.code == aBtn:
                        print("a_not pressed")
                        x2_change = 0
                if event.value == 0:
                    if event.code == bBtn:
                        print("b_not pressed")
                        y2_change = 0
                if event.value == 0:
                    if event.code == xBtn:
                        print("x_not pressed")
                        y2_change = 0

        break
        print("out of controller")
#player1/2
def char1(x1,y1):
    global player1
    gameDisplay.blit(player1.sprite,(x1,y1))

def char2(x2,y2):
    global player2
    gameDisplay.blit(player2.sprite,(x2,y2))

    
#player1/2 health 
def char1_health(player1):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Player1 HP: "+str(player1.hp), True, black)
    gameDisplay.blit(text,(0,0))
    if player1.hp <= 0:
        death_p1()

def char2_health(player2):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Player2 HP: "+str(player2.hp), True, black)
    gameDisplay.blit(text,(600,0))
    if player2.hp <= 0:
        death_p2()


def text_objects(text, font):
    Text_Surface = font.render(text, True, black)
    return Text_Surface, Text_Surface.get_rect()


#death functions
def death_p1():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(death_sound)
    #reset all status effects
    global player1
    player1.hp = 1000
    global player2
    player2.hp = 1000
    global x1
    x1 = display_width*.2
    global y1
    y1 = display_height*.8
    global x2
    x2 = display_width*.8
    global y2
    y2 = display_height*.8
    global x1_change, y1_change, x2_change, y2_change
    x1_change = 0
    x2_change = 0
    y1_change = 0
    y2_change = 0
    global p1_startx, p1_starty, p2_startx, p2_starty
    p1_startx = x1
    p1_starty = y1
    p2_startx = x2
    p2_starty = y2
    #global prism_effect1, prism_effect2
    #prism_effect1 = False
    #prism_effect2 = False
    
    gameDisplay.blit((player1.sprite),(x1,y1))
    gameDisplay.blit((player2.sprite),(x2,y2))
    death = True
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, Text_Box = text_objects("Player 2 WINS", largeText) 
    Text_Box.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, Text_Box)
    while death:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #calls button function for go and quit
        button("Play Again",200,600,100,50,green,hover_green,game_loop)
        button("Classes",450,600,100,50,blue,hover_blue, player_menu)
        button("Quit",700,600,100,50,red,hover_red,quitgame)

        pygame.display.update()
        clock.tick(15)

def death_p2():
    #reset all status effects
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(death_sound)
    global player1
    player1.hp = 1000
    global player2
    player2.hp = 1000
    global x1
    x1 = display_width*.2
    global y1
    y1 = display_height*.8
    global x2
    x2 = display_width*.8
    global y2
    y2 = display_height*.8
    global x1_change, y1_change, x2_change, y2_change
    x1_change = 0
    x2_change = 0
    y1_change = 0
    y2_change = 0
    global p1_startx, p1_starty, p2_startx, p2_starty
    p1_startx = x1
    p1_starty = y1
    p2_startx = x2
    p2_starty = y2
    #global prism_effect1, prism_effect2
    #prism_effect1 = False
    #prism_effect2 = False
    
    gameDisplay.blit((player1.sprite),(x1,y1))
    gameDisplay.blit((player2.sprite),(x2,y2))
    death = True
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, Text_Box = text_objects("Player 1 WINS", largeText) 
    Text_Box.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, Text_Box)
    while death:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        

        #calls button function for go and quit
        button("Play Again",200,600,100,50,green,hover_green,game_loop)
        button("Classes",450,600,100,50,blue,hover_blue, player_menu)
        button("Quit",700,600,100,50,red,hover_red,quitgame)

        pygame.display.update()
        clock.tick(15)

def message_display(text):
    #what the text is(font,size)
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, Text_Box = text_objects(text, largeText)
    #where the text box is 
    Text_Box.center = ((display_width/2),(display_height/2))
    #keeps box in background
    gameDisplay.blit(TextSurf, Text_Box)

    pygame.display.update()
    #pause the game(displays the text for 2 sec)
    time.sleep(2)
    #restarts the game
    game_loop()
    
def button(msg,x,y,width,height,in_color,act_color,action=None):
    #where the mouse is
    mouse = pygame.mouse.get_pos()
    #mouse_click
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(gameDisplay, in_color, (x,y,width,height))
    #if mouse is over button, "light it up"
    if (x+width)>mouse[0] > x and (y+height) > mouse[1] > y:
        pygame.draw.rect(gameDisplay, act_color, (x,y,width,height))
        if click[0] == 1 and action != None:
            action()   

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, text_Box = text_objects(msg, smallText)
    text_Box.center = ( (x+(width/2)),(y+(height/2)) )
    gameDisplay.blit(textSurf, text_Box)

def choose_button(msg,x,y,width,height,in_color,act_color,action=None):
    global player1
    global player2
    global p1_w
    global p1_h
    global p1_speed
    global p2_w
    global p2_h
    global p2_speed
    global prism_effect1
    global prism_effect2
    global is_comp
    #prism_effect1 = False
    #prism_effect2 = False
    #where the mouse is
    mouse = pygame.mouse.get_pos()
    #mouse_click
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(gameDisplay, in_color, (x,y,width,height))
    #if mouse is over button, "light it up"
    if (x+width)>mouse[0] > x and (y+height) > mouse[1] > y:
        pygame.draw.rect(gameDisplay, act_color, (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == 'player1_wiz':
                player1 = Character(wizzy,wizzy_hp,spell,spell_width,spell_height,spell_speed)
                p1_w = spell_width
                p1_h = spell_height
                p1_speed = spell_speed
                prism_effect1 = False
            if action == 'player1_necro':
                player1 = Character(necromancer,necro_hp,skull,skull_width,skull_height,skull_speed)
                p1_w = skull_width
                p1_h = skull_height
                p1_speed = skull_speed
                prism_effect1 = False
            if action == 'player1_mystic':
                player1 = Character(mystic,mystic_hp,orb,orb_width,orb_height,orb_speed)
                p1_w = orb_width
                p1_h = orb_height
                p1_speed = orb_speed
                prism_effect1 = False
            if action == 'player1_knight':
                player1 = Character(knight,knight_hp,sheild,sheild_width,sheild_height,sheild_speed)
                p1_w = sheild_width
                p1_h = sheild_height
                p1_speed = sheild_speed
                prism_effect1 = False
            if action == 'player1_trickster':
                player1 = Character(trickster,trickster_hp,prism,prism_width,prism_height,prism_speed)
                p1_w = prism_width
                p1_h = prism_height
                p1_speed = prism_speed
                prism_effect1 = True
            if action == 'player1_archer':
                player1 = Character(archer,archer_hp,quiver,quiver_width,quiver_height,quiver_speed)
                p1_w = quiver_width
                p1_h = quiver_height
                p1_speed = quiver_speed
                prism_effect1 = False
            if action == 'player1_sin':
                player1 = Character(sin,sin_hp,poison,poison_width,poison_height,poison_speed)
                p1_w = poison_width
                p1_h = poison_height
                p1_speed = poison_speed
                prism_effect1 = False
            if action == 'player2_wiz':
                player2 = Character(wizzy,wizzy_hp,spell,spell_width,spell_height,spell_speed)
                p2_w = spell_width
                p2_h = spell_height
                p2_speed = spell_speed
                prism_effect2 = False
            if action == 'player2_necro':
                player2 = Character(necromancer,necro_hp,skull,skull_width,skull_height,skull_speed)
                p2_w = skull_width
                p2_h = skull_height
                p2_speed = skull_speed
                prism_effect2 = False
            if action == 'player2_mystic':
                player2 = Character(mystic,mystic_hp,orb,orb_width,orb_height,orb_speed)
                p2_w = orb_width
                p2_h = orb_height
                p2_speed = orb_speed
                prism_effect2 = False
            if action == 'player2_knight':
                player2 = Character(knight,knight_hp,sheild,sheild_width,sheild_height,sheild_speed)
                p2_w = sheild_width
                p2_h = sheild_height
                p2_speed = sheild_speed
                prism_effect2 = False
            if action == 'player2_trickster':
                player2 = Character(trickster,trickster_hp,prism,prism_width,prism_height,prism_speed)
                p2_w = prism_width
                p2_h = prism_height
                p2_speed = prism_speed
                prism_effect2 = True
            if action == 'player2_archer':
                player2 = Character(archer,archer_hp,quiver,quiver_width,quiver_height,quiver_speed)
                p2_w = quiver_width
                p2_h = quiver_height
                p2_speed = quiver_speed
                prism_effect2 = False
            if action == 'player2_sin':
                player2 = Character(sin,sin_hp,poison,poison_width,poison_height,poison_speed)
                p2_w = poison_width
                p2_h = poison_height
                p2_speed = poison_speed
                prism_effect2 = False
            if action == 'computer':
                player2 = Character(wizzy,wizzy_hp,spell,spell_width,spell_height,spell_speed)
                p2_w = spell_width
                p2_h = spell_height
                p2_speed = spell_speed
                prism_effect2 = False
                is_comp = True
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, text_Box = text_objects(msg, smallText)
    text_Box.center = ( (x+(width/2)),(y+(height/2)) )
    gameDisplay.blit(textSurf, text_Box)


def quitgame():
    pygame.quit()
    quit()
        
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, Text_Box = text_objects("RotMG PVP", largeText) 
        Text_Box.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, Text_Box)

        #calls button function for go and quit
        button("GO!",200,600,100,50,green,hover_green,player_menu)
        button("Quit",700,600,100,50,red,hover_red,quitgame)

        pygame.display.update()
        clock.tick(15)

def player_menu():
    p_menu = True
    while p_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, Text_Box = text_objects("Character Select", largeText) 
        Text_Box.center = ((display_width/2),((display_height/2)-200))
        gameDisplay.blit(TextSurf, Text_Box)

        #calls button function for go and quit
        choose_button("Player 1: Wizard",200,260,110,50,blue,hover_blue,'player1_wiz')
        choose_button("Player 1: Necro",200,320,110,50,blue,hover_blue,'player1_necro')
        choose_button("Player 1: Mystic",200,380,110,50,blue,hover_blue,'player1_mystic')
        choose_button("Player 1: Knight",200,440,110,50,blue,hover_blue,'player1_knight')
        choose_button("Player 1: Trickster",200,500,110,50,blue,hover_blue,'player1_trickster')
        choose_button("Player 1: Archer",200,560,110,50,blue,hover_blue,'player1_archer')
        choose_button("Player 1: Assassin",200,620,110,50,blue,hover_blue,'player1_sin')
        choose_button("Player 2: Wizard",700,260,110,50,red,hover_red,'player2_wiz')
        choose_button("Player 2: Necro",700,320,110,50,red,hover_red,'player2_necro')
        choose_button("Player 2: Mystic",700,380,110,50,red,hover_red,'player2_mystic')
        choose_button("Player 2: Knight",700,440,110,50,red,hover_red,'player2_knight')
        choose_button("Player 2: Trickster",700,500,110,50,red,hover_red,'player2_trickster')
        choose_button("Player 2: Archer",700,560,110,50,red,hover_red,'player2_archer')
        choose_button("Player 2: Assassin",700,620,110,50,red,hover_red,'player2_sin')
        button(" ", 450,600,110,50,yellow,hover_yellow,game_loop_comp)
        choose_button("Player 2: Computer", 450,600,110,50,yellow,hover_yellow,'computer')
        button("GO!",450,500,100,50,green,hover_green,game_loop)
        pygame.display.update()
        clock.tick(15)

        
def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False

def paused():

    pygame.mixer.music.pause()
    
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, Text_Box = text_objects("PAUSED", largeText) 
    Text_Box.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, Text_Box)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #gameDisplay.fill(white)
        

        #calls button function for go and quit
        button("Continue?",200,600,100,50,green,hover_green,unpause)
        button("Change Classes",450,600,100,50,blue,hover_blue, player_menu)
        button("Quit",700,600,100,50,red,hover_red,quitgame)

        pygame.display.update()
        clock.tick(15)
        
def game_loop_comp():
    global pause
    pygame.mixer.music.play(-1)
    
    global x1, y1, x2, y2
    
    global p1_hp, p2_hp
    
    global x1_change, x2_change, y1_change, y2_change
    
    global p1_startx, p1_starty, p1_w, p1_h,p1_speed
    global p2_startx, p2_starty, p2_w, p2_h,p2_speed
    
    global direction_p1, direction_p2
    global player1, player2
    global sheild_p1, sheild_p2
    global stasis_p1, stasis_p2
    global sheild_effect1, sheild_effect2, stasis_effect1, stasis_effect2
    global tp_p1, tp_p2, prism_effect1, prism_effect2
    global para_p1, para_p2, para_effect1, para_effect2
    global poison_p1, poison_p2, poison_effect1, poison_effect2
    global comp_choice
    global counter
    gameExit = False

    while not gameExit:
        '''
        if counter == 30:
            comp_choice = random.randint(1,4)
            #print(comp_choice)
            counter = 0
        else:
            counter+=1'''

        if(p2_startx<x1):
            comp_choice = 1
        elif(p2_startx>x1):
            comp_choice = 2
        elif(p2_starty>y1):
            comp_choice = 3
        elif(p2_starty<y1):
            comp_choice = 4
        '''
        if (x2+50)>display_width:
            comp_choice = 1
        elif (x2-50)<0:
            comp_chice = 2
        elif (y2-50)<0:
            comp_choice = 3
        elif (y2+50)>display_width:
            comp_choice = 4'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x1_change = -5
                    direction_p1 = 'left'
                elif event.key == pygame.K_d:
                    x1_change = 5
                    direction_p1 = 'right'
                elif event.key == pygame.K_s:
                    y1_change = 5
                    direction_p1 = 'down'
                elif event.key == pygame.K_w:
                    y1_change = -5
                    direction_p1 = 'up'           
                if event.key == pygame.K_p:
                    pause = True
                    paused() 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    x1_change = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    y1_change = 0
        if comp_choice == 1:
            x2_change = -5
            direction_p2 = 'left'
        elif comp_choice == 2:
            x2_change = 5
            direction_p2 = 'right'
        elif comp_choice == 3:
            y2_change = 5
            direction_p2 = 'down'
            print('hi')
        elif comp_choice == 4:
            y2_change = -5
            direction_p2 = 'up'
        #stasis(para+stun)
        if stasis_p1 == True:
            x1_change = 0
            y1_change = 0
            p1_startx = -10000
            p1_starty = -10000
            stasis_effect1 += 1
            tp_p1 = 0
        if stasis_effect1 == 150:
            stasis_effect1 = 0
            stasis_p1 = False
            
        if stasis_p2 == True:
            x2_change = 0
            y2_change = 0
            p2_startx = -10000
            p2_starty = -10000
            stasis_effect2 += 1
            tp_p2 = 0
        if stasis_effect2 == 150:
            stasis_effect2 = 0
            stasis_p2 = False
            
        #para
        if para_p1 == True:
            x1_change = 0
            y1_change = 0
            para_effect1 += 1
        if para_effect1 == 225:
            para_effect1 = 0
            para_p1 = False
            
        if para_p2 == True:
            x2_change = 0
            y2_change = 0
            para_effect2 += 1
        if para_effect2 == 225:
            para_effect2 = 0
            para_p2 = False
            
        #stun
        if sheild_p1 == True:
            p1_startx = -10000
            p1_starty = -10000
            sheild_effect1 += 1
            tp_p1 = 0
        if sheild_effect1 == 225:
            sheild_effect1 = 0
            sheild_p1 = False
            
        if sheild_p2 == True:
            p2_startx = -10000
            p2_starty = -10000
            sheild_effect2 += 1
            tp_p2 = 0
        if sheild_effect2 == 225:
            sheild_effect2 = 0
            sheild_p2 = False

        
        #prism(teleport)
        if prism_effect1 == True:   
            if tp_p1 == 300 and (sheild_p1 == False and stasis_p1 == False):
                x1 = p1_startx
                y1 = p1_starty
                tp_p1 = 0
            else:
                tp_p1 += 1
        if prism_effect2 == True:
            if tp_p2 == 300 and (sheild_p2 == False and stasis_p2 == False):
                x2 = p2_startx
                y2 = p2_starty
                tp_p2 = 0
            else:
                tp_p2 += 1

        #poison
        if poison_p1 == True:
            player1.hp -=1
            poison_effect1 +=1
        if poison_effect1 == 200:
            poison_effect1 = 0
            poison_p1 = False
        if poison_p2 == True:
            player2.hp -=1
            poison_effect2 +=1
        if poison_effect2 == 200:
            poison_effect2 = 0
            poison_p2 = False

        #print(x2_change)
        #print(y2_change)
        x1 += x1_change
        y1 += y1_change
        x2 += x2_change
        y2 += y2_change
        
        gameDisplay.fill(white)        
        player1.projectile(p1_startx, p1_starty, p1_w, p1_h, blue)

        player2.projectile(p2_startx, p2_starty, p2_w, p2_h, red)
        
        if direction_p1 == 'up': 
            p1_starty += p1_speed
            #print("direction1up")
        elif direction_p1 == 'down':
            p1_starty -= p1_speed
        elif direction_p1 == 'left':
            p1_startx += p1_speed
        elif direction_p1 == 'right':
            p1_startx -= p1_speed
        if direction_p2 == 'up':
            p2_starty += p2_speed
            #print("direction2up")
        elif direction_p2 == 'down':
            p2_starty -= p2_speed
        elif direction_p2 == 'left':
            p2_startx += p2_speed
        elif direction_p2 == 'right':
            p2_startx -= p2_speed
        char1(x1,y1)
        char2(x2,y2)
        char1_health(player1)
        char2_health(player2)
        if x1 > display_width-char1_width or x1 < 0:
            player1.hp -= 1
        if x2 >display_width-char2_width or x2 < 0:
            player2.hp -= 1
        if y1 > display_height-char1_height or y1 < 0:
            player1.hp -= 1
        if y2 >display_height-char2_height or y2 < 0:
            player2.hp -= 1
        if p1_startx > display_width or p1_startx < 0 or p1_starty > display_height or p1_starty < 0:
            p1_startx = x1
            p1_starty = y1
        if p2_startx < 0 or p2_startx > display_width or p2_starty < 0 or p2_starty >display_height:
            p2_startx = x2
            p2_starty = y2


        if x1 in range(int((p2_startx-char1_width)),int((p2_startx+p2_w))):
            if y1 in range(int((p2_starty-char1_height)), int((p2_starty+p2_h))):
                if player2.projectile == spell:
                    player1.hp -=3
                    #p2_startx = x2
                    #p2_starty = y2
                elif player2.projectile == skull:
                    player1.hp -=3
                    player2.hp +=1
                    #p2_startx = x2
                    #p2_starty = y2
                elif player2.projectile == orb:
                    player1.hp -=20
                    p2_startx = x2
                    p2_starty = y2
                    stasis_p1 = True
                elif player2.projectile == sheild:
                    player1.hp -=3
                    #p2_startx = x2
                    #p2_starty = y2
                    sheild_p1 = True
                elif player2.projectile == prism:
                    player1.hp -=7
                    #p2_startx = x2
                    #p2_starty = y2
                elif player2.projectile == quiver:
                    player1.hp -=20
                    p2_startx = x2
                    p2_starty = y2
                    para_p1 = True
                elif player2.projectile == poison:
                    player1.hp -=1
                    #p2_startx = x2
                    #p2_starty = y2
                    poison_p1 = True
                char1_health(player1)
        if x2 in range(int((p1_startx-char2_width)),int((p1_startx+p1_w))):
            if y2 in range(int((p1_starty-char2_height)), int((p1_starty+p1_h))):
                if player1.projectile == spell:
                    player2.hp -=3
                    #p1_startx = x1
                    #p1_starty = y1
                elif player1.projectile == skull:
                    player2.hp -=3
                    player1.hp +=1
                    #p1_startx = x1
                    #p1_starty = y1
                elif player1.projectile == orb:
                    player2.hp -=20
                    p1_startx = x1
                    p1_starty = y1
                    stasis_p2 = True
                elif player1.projectile == sheild:
                    player2.hp -=3
                    #p1_startx = x1
                    #p1_starty = y1
                    sheild_p2 = True
                elif player1.projectile == prism:
                    player2.hp -=7
                    #p1_startx = x1
                    #p1_starty = y1
                elif player1.projectile == quiver:
                    player2.hp -=20
                    p1_startx = x1
                    p1_starty = y1
                    para_p2 = True
                elif player1.projectile == poison:
                    player2.hp -=1
                    #p1_startx = x1
                    #p1_starty = y1
                    poison_p2 = True
                char2_health(player2)
        pygame.display.update()
        clock.tick(60)
        
def game_loop():
    global pause
    pygame.mixer.music.play(-1)
    
    global x1, y1, x2, y2
    
    global p1_hp, p2_hp
    
    global x1_change, x2_change, y1_change, y2_change
    
    global p1_startx, p1_starty, p1_w, p1_h,p1_speed
    global p2_startx, p2_starty, p2_w, p2_h,p2_speed
    
    global direction_p1, direction_p2
    global player1, player2
    global sheild_p1, sheild_p2
    global stasis_p1, stasis_p2
    global sheild_effect1, sheild_effect2, stasis_effect1, stasis_effect2
    global tp_p1, tp_p2, prism_effect1, prism_effect2
    global para_p1, para_p2, para_effect1, para_effect2
    global poison_p1, poison_p2, poison_effect1, poison_effect2
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
        #t1 = threading.Thread(target=key_input, args=())
        #t2 = threading.Thread(target=controller_input, args = ())
        #t1.start()
        #t2.start()
        #t1.join()
        #t2.join()
        #a,b = select([keyboard],[gamepad])
        #for event in gamepad.read():
        #    print(event)
        #print("DONE")
        #print(gamepad)
        #print(type(gamepad))
        #x = select([gamepad],[],[])
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x1_change = -5
                    direction_p1 = 'left'
                elif event.key == pygame.K_d:
                    x1_change = 5
                    direction_p1 = 'right'
                elif event.key == pygame.K_s:
                    y1_change = 5
                    direction_p1 = 'down'
                elif event.key == pygame.K_w:
                    y1_change = -5
                    direction_p1 = 'up'           
                if event.key == pygame.K_LEFT:
                    x2_change = -5
                    direction_p2 = 'left'
                elif event.key == pygame.K_RIGHT:
                    x2_change = 5
                    direction_p2 = 'right'
                elif event.key == pygame.K_DOWN:
                    y2_change = 5
                    direction_p2 = 'down'
                elif event.key == pygame.K_UP:
                    y2_change = -5
                    direction_p2 = 'up'
                if event.key == pygame.K_p:
                    pause = True
                    paused() 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    x1_change = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    y1_change = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x2_change = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y2_change = 0
                    
        #stasis(para+stun)
        if stasis_p1 == True:
            x1_change = 0
            y1_change = 0
            p1_startx = -10000
            p1_starty = -10000
            stasis_effect1 += 1
            tp_p1 = 0
        if stasis_effect1 == 150:
            stasis_effect1 = 0
            stasis_p1 = False
            
        if stasis_p2 == True:
            x2_change = 0
            y2_change = 0
            p2_startx = -10000
            p2_starty = -10000
            stasis_effect2 += 1
            tp_p2 = 0
        if stasis_effect2 == 150:
            stasis_effect2 = 0
            stasis_p2 = False
            
        #para
        if para_p1 == True:
            x1_change = 0
            y1_change = 0
            para_effect1 += 1
        if para_effect1 == 225:
            para_effect1 = 0
            para_p1 = False
            
        if para_p2 == True:
            x2_change = 0
            y2_change = 0
            para_effect2 += 1
        if para_effect2 == 225:
            para_effect2 = 0
            para_p2 = False
            
        #stun
        if sheild_p1 == True:
            p1_startx = -10000
            p1_starty = -10000
            sheild_effect1 += 1
            tp_p1 = 0
        if sheild_effect1 == 225:
            sheild_effect1 = 0
            sheild_p1 = False
            
        if sheild_p2 == True:
            p2_startx = -10000
            p2_starty = -10000
            sheild_effect2 += 1
            tp_p2 = 0
        if sheild_effect2 == 225:
            sheild_effect2 = 0
            sheild_p2 = False

        
        #prism(teleport)
        if prism_effect1 == True:   
            if tp_p1 == 300 and (sheild_p1 == False and stasis_p1 == False):
                x1 = p1_startx
                y1 = p1_starty
                tp_p1 = 0
            else:
                tp_p1 += 1
        if prism_effect2 == True:
            if tp_p2 == 300 and (sheild_p2 == False and stasis_p2 == False):
                x2 = p2_startx
                y2 = p2_starty
                tp_p2 = 0
            else:
                tp_p2 += 1

        #poison
        if poison_p1 == True:
            player1.hp -=1
            poison_effect1 +=1
        if poison_effect1 == 200:
            poison_effect1 = 0
            poison_p1 = False
        if poison_p2 == True:
            player2.hp -=1
            poison_effect2 +=1
        if poison_effect2 == 200:
            poison_effect2 = 0
            poison_p2 = False

        #print(x2_change)
        #print(y2_change)
        x1 += x1_change
        y1 += y1_change
        x2 += x2_change
        y2 += y2_change
        
        gameDisplay.fill(white)        
        player1.projectile(p1_startx, p1_starty, p1_w, p1_h, blue)

        player2.projectile(p2_startx, p2_starty, p2_w, p2_h, red)
        
        if direction_p1 == 'up': 
            p1_starty += p1_speed
            #print("direction1up")
        elif direction_p1 == 'down':
            p1_starty -= p1_speed
        elif direction_p1 == 'left':
            p1_startx += p1_speed
        elif direction_p1 == 'right':
            p1_startx -= p1_speed
        if direction_p2 == 'up':
            p2_starty += p2_speed
            #print("direction2up")
        elif direction_p2 == 'down':
            p2_starty -= p2_speed
        elif direction_p2 == 'left':
            p2_startx += p2_speed
        elif direction_p2 == 'right':
            p2_startx -= p2_speed
        char1(x1,y1)
        char2(x2,y2)
        char1_health(player1)
        char2_health(player2)
        if x1 > display_width-char1_width or x1 < 0:
            player1.hp -= 1
        if x2 >display_width-char2_width or x2 < 0:
            player2.hp -= 1
        if y1 > display_height-char1_height or y1 < 0:
            player1.hp -= 1
        if y2 >display_height-char2_height or y2 < 0:
            player2.hp -= 1
        if p1_startx > display_width or p1_startx < 0 or p1_starty > display_height or p1_starty < 0:
            p1_startx = x1
            p1_starty = y1
        if p2_startx < 0 or p2_startx > display_width or p2_starty < 0 or p2_starty >display_height:
            p2_startx = x2
            p2_starty = y2


        if x1 in range(int((p2_startx-char1_width)),int((p2_startx+p2_w))):
            if y1 in range(int((p2_starty-char1_height)), int((p2_starty+p2_h))):
                if player2.projectile == spell:
                    player1.hp -=3
                    #p2_startx = x2
                    #p2_starty = y2
                elif player2.projectile == skull:
                    player1.hp -=3
                    player2.hp +=1
                    #p2_startx = x2
                    #p2_starty = y2
                elif player2.projectile == orb:
                    player1.hp -=20
                    p2_startx = x2
                    p2_starty = y2
                    stasis_p1 = True
                elif player2.projectile == sheild:
                    player1.hp -=3
                    #p2_startx = x2
                    #p2_starty = y2
                    sheild_p1 = True
                elif player2.projectile == prism:
                    player1.hp -=7
                    #p2_startx = x2
                    #p2_starty = y2
                elif player2.projectile == quiver:
                    player1.hp -=20
                    p2_startx = x2
                    p2_starty = y2
                    para_p1 = True
                elif player2.projectile == poison:
                    player1.hp -=1
                    #p2_startx = x2
                    #p2_starty = y2
                    poison_p1 = True
                char1_health(player1)
        if x2 in range(int((p1_startx-char2_width)),int((p1_startx+p1_w))):
            if y2 in range(int((p1_starty-char2_height)), int((p1_starty+p1_h))):
                if player1.projectile == spell:
                    player2.hp -=3
                    #p1_startx = x1
                    #p1_starty = y1
                elif player1.projectile == skull:
                    player2.hp -=3
                    player1.hp +=1
                    #p1_startx = x1
                    #p1_starty = y1
                elif player1.projectile == orb:
                    player2.hp -=20
                    p1_startx = x1
                    p1_starty = y1
                    stasis_p2 = True
                elif player1.projectile == sheild:
                    player2.hp -=3
                    #p1_startx = x1
                    #p1_starty = y1
                    sheild_p2 = True
                elif player1.projectile == prism:
                    player2.hp -=7
                    #p1_startx = x1
                    #p1_starty = y1
                elif player1.projectile == quiver:
                    player2.hp -=20
                    p1_startx = x1
                    p1_starty = y1
                    para_p2 = True
                elif player1.projectile == poison:
                    player2.hp -=1
                    #p1_startx = x1
                    #p1_starty = y1
                    poison_p2 = True
                char2_health(player2)
        pygame.display.update()
        clock.tick(60)


player1 = Character(wizzy,wizzy_hp,spell,spell_width,spell_height,spell_speed)
p1_w = spell_width
p1_h = spell_height
p1_speed = spell_speed
player2 = Character(wizzy,wizzy_hp,spell,spell_width,spell_height,spell_speed)
p2_w = spell_width
p2_h = spell_height
p2_speed = spell_speed
game_intro()
pygame.quit()
quit()
