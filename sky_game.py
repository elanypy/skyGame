import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



#setup the clock for a decent framerate 
clock = pygame.time.Clock()



#define a player object by extending pygame.sprite.Sprite
#The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):  #create a rectangle white with size 75,25
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(r'C:\Users\Happycode3D-07\Documents\Pessoais\PythonProjects\gameWithPython\PyGame\image\jet.png').convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()

    #move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)

        #keep player on the screen
        if self.rect.left<0:
            self.rect.left =0
        if self.rect.right>SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >=SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


#Define the enemy object by extending pygame.sprite.Sprite
#the surface you drawn on the screen is now an attribute of enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(r'C:\Users\Happycode3D-07\Documents\Pessoais\PythonProjects\gameWithPython\PyGame\image\missile.png').convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center =(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5,20)

    #move the sprite based on speed
    #remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right <0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super (Cloud, self).__init__()
        self.surf = pygame.image.load(r'C:\Users\Happycode3D-07\Documents\Pessoais\PythonProjects\gameWithPython\PyGame\image\cloud.png').convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        #the starting position is randomly generated 
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
    #move the cloud based on constant speed
    #remove the cloud when it passes left edge of the screen
    def update(self):
        self.rect.move_ip(-5,0)
        if self.rect.right<0:
            self.kill()

#setup for music and sound 
pygame.mixer.init()

 #initialize pyhgame
pygame.init()   


#create the screen object 
#the size is determined by the constants
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  #main screen

#Instantiate player ; Right now, this is a just a rectangle 
player = Player()

#create a custom event for adding a new enemy and clouds 
TIME_ENEMYAPPEAR = 1000
ADDENEMY  = pygame.USEREVENT+1
pygame.time.set_timer(ADDENEMY, TIME_ENEMYAPPEAR)

ADDCLOUD = pygame.USEREVENT+2
pygame.time.set_timer(ADDCLOUD, 1500)

#load and play background music 
pygame.mixer.music.load(r'C:\Users\Happycode3D-07\Documents\Pessoais\PythonProjects\gameWithPython\PyGame\music\Apoxode_-_Electric_1.mp3')
pygame.mixer.music.play(loops =-1)
pygame.mixer.music.set_volume(0.5)

#load all sound files 
move_up_sound = pygame.mixer.Sound(r'C:\Users\Happycode3D-07\Documents\Pessoais\PythonProjects\gameWithPython\PyGame\music\Rising_putter.ogg')
move_down_sound = pygame.mixer.Sound(r'C:\Users\Happycode3D-07\Documents\Pessoais\PythonProjects\gameWithPython\PyGame\music\Falling_putter.ogg')
collision_sound = pygame.mixer.Sound(r'C:\Users\Happycode3D-07\Documents\Pessoais\PythonProjects\gameWithPython\PyGame\music\Collision.ogg')

move_up_sound.set_volume(0.3)
move_down_sound.set_volume(0.3)
collision_sound.set_volume(1.0)


#create groups to hold enemy sprites and all sprites 
#- enemies is used for collision detection and position updates
#- all sprites is used for rendering 
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


#Variable to keep the main loop running
running = True

#Main loop
while running:

    #look at every event in queue
    for event in pygame.event.get():

        #did the user hit a key?
        if event.type == KEYDOWN:
            #print(f"{event.key}") #print keys values was pressed 
            #was it the escape key? if so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        #did the user click the window close button? if so, stop the loop
        elif event.type == QUIT:
            running= False

        #add a new enemy 
        elif event.type == ADDENEMY:
            #Ccreate the new enemy and add it to sprite groups 
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        #add a new cloud 
        elif event.type == ADDCLOUD:
            new_clouds = Cloud()
            clouds.add(new_clouds)
            all_sprites.add(new_clouds)

    #get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    #update the player sprite based keypresses
    player.update(pressed_keys)

    #update enemy position 
    enemies.update()

    #update the clouds
    clouds.update()

    #fill the screen with white
    screen.fill((135,206,250))

    #draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #CHECK if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()

        #stop any moving sound and play
        move_down_sound.stop()
        move_up_sound.stop()
        pygame.time.delay(50)
        collision_sound.stop()
        pygame.time.delay(500)

        #stop loop
        running = False


    #update the display
    pygame.display.flip()

    #ensure program maintains a maximum rate of 30 frame per second 
    clock.tick(60)

pygame.mixer.quit()
