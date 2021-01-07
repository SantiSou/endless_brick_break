
import pygame, sys, random
from pygame.locals import *
from pygame.sprite import Sprite, Group

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

pygame.init()

clock = pygame.time.Clock()

screen_width = 400 # Ancho 
screen_height = 600 # Alto

screen = pygame.display.set_mode((screen_width,screen_height))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255,255,255))

bricks = Group()
players = Group()
brick_x = 0
brick_y = 0
brick_width = 30 # Ancho 
brick_height = 10 # Alto

brick_separation = 1
amount_bricks = (screen_width / brick_width) - brick_separation

speed_factor = 1

player_x = 0
player_y = 0
player_width = 45
player_height = 3

class Player(Sprite):

    def __init__(self,screen):

        super(Player, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.player_rect = pygame.Rect(player_x,player_y,player_width,player_height)

    def draw_player(self):

        pygame.draw.rect(self.screen,(0,0,0),self.player_rect)

    def update(self,mouse_x):
        
        self.player_rect.centerx = mouse_x
        self.player_rect.centery = 500
        
        for player in players.sprites():
            player.draw_player() 


class Brick(Sprite):

    def __init__(self,screen):

        super(Brick, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.brick_rect = pygame.Rect(brick_x,brick_y,brick_width,brick_height)
        # self.brick_rect.y = float(self.brick_rect.y)
        # self.brick_rect.centerx = self.screen_rect.centerx
        # self.brick_rect.centery = self.screen_rect.centery


    def draw_brick(self):

        pygame.draw.rect(self.screen,(0,0,0),self.brick_rect)

    def update(self, speed_factor):

        self.brick_rect.centery += speed_factor

        for brick in bricks.sprites():

            if brick.brick_rect.bottom >= screen_height:
                bricks.remove(brick)

            brick.draw_brick()     

new_player = Player(screen)
players.add(new_player)
  
while True:

    clock.tick(60) # Frames Per Second
    # Evaluar el valor de clock.tick para utilizarlo de mecanismo de generación de bloques
    for event in pygame.event.get():

        # if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_SPACE:
                       
        if event.type == pygame.QUIT:
            sys.exit()

    if 1 == random.randint(1,100):
        new_brick = Brick(screen)
        bricks.add(new_brick)

        random_pos = random.randint(0,int(amount_bricks))

        brick_x = (brick_width + brick_separation) * random_pos
        if brick_x >= screen_width - brick_separation:
            brick_x = 0         

    mouse_x, mouse_y = pygame.mouse.get_pos()
    speed_factor += 0.001

    screen.blit(background, (0, 0))
    players.update(mouse_x)
    bricks.update(speed_factor)
    pygame.display.flip()