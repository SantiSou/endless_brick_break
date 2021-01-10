
import pygame
import sys
import random
from pygame.locals import *
from pygame.sprite import Sprite, Group

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

pygame.init()

clock = pygame.time.Clock()

screen_width = 400  # Ancho
screen_height = 600  # Alto

screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))

bricks = Group()
brick_x = 0
brick_y = 0
brick_width = 30  # Ancho
brick_height = 10  # Alto
brick_separation = 1
amount_bricks = (screen_width / brick_width) - brick_separation
speed_factor = 1

players = Group()
player_x = 0
player_y = 0
player_width = 70
player_height = 3

balls = Group()
ball_x = 0
ball_y = 0
ball_width = 8
ball_height = 8


class Player(Sprite):

    def __init__(self, screen):

        super(Player, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.rect = pygame.Rect(
            player_x, player_y, player_width, player_height)

    def draw_player(self):

        pygame.draw.rect(self.screen, (0, 0, 0), self.rect)

    def update(self, mouse_x):

        self.rect.centerx = mouse_x
        self.rect.centery = 500

        for player in players.sprites():

            collision_bricks = pygame.sprite.spritecollide(player,bricks,False)

            # if collision_bricks:
            #     print('Has perdido')
            player.draw_player()


class Ball(Sprite):

    def __init__(self, screen, new_player, bricks):

        super(Ball, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.rect = pygame.Rect(ball_x, ball_y, ball_width, ball_height)

        self.rect.centery = new_player.rect.centery
        self.rect.centerx = new_player.rect.centerx

        self.direction_x = random.randint(0,1)
        self.direction_y = 0

    def draw_ball(self):

        pygame.draw.rect(self.screen, (0, 0, 0), self.rect)

    def update(self):

        if self.rect.centery <= 0:
            self.direction_y = 1 # True para que se desplaze hacia abajo        
        elif self.rect.centery >= screen_height:
            self.direction_y = 0 # False para que se desplaze hacia arriba 

        if self.rect.centerx <= 0:
            self.direction_x = 1 # True para que se desplaze hacia la derecha
        elif self.rect.centerx >= screen_width:
            self.direction_x = 0 # False para que se desplaze hacia la izquierda 

        for ball in balls.sprites():

            collision_bricks = pygame.sprite.spritecollide(ball,bricks,True)
            collision_player = pygame.sprite.spritecollide(ball,players,False)

            if collision_bricks:
                
                if self.direction_y and self.direction_x: # Abajo/Derecha

                    if (self.rect.bottomright[0] - collision_bricks[0].rect.topleft[0]) > (self.rect.bottomright[1] - collision_bricks[0].rect.topleft[1]):
                        self.direction_y = 0
                    else:
                        self.direction_x = 0

                elif not self.direction_y and self.direction_x: # Arriba/Derecha

                    if (self.rect.topright[0] - collision_bricks[0].rect.bottomleft[0]) > (collision_bricks[0].rect.bottomleft[1] - self.rect.topright[1]):
                        self.direction_y = 1
                    else:                     
                        self.direction_x = 0

                elif not self.direction_y and not self.direction_x: # Arriba/Izquierda

                    if (collision_bricks[0].rect.bottomright[0] - self.rect.topleft[0]) > (collision_bricks[0].rect.bottomright[1] - self.rect.topleft[1]):
                        self.direction_y = 1
                    else:
                        self.direction_x = 1

                elif self.direction_y and not self.direction_x: # Abajo/Izquierda

                    if (collision_bricks[0].rect.topright[0] - self.rect.bottomleft[0]) > (self.rect.bottomleft[1] - collision_bricks[0].rect.topright[1]):
                        self.direction_y = 0
                    else:
                        self.direction_x = 1

            if collision_player:
                self.direction_y = 0


        if self.direction_y and self.direction_x:
            self.rect.centery += speed_factor + 2
            self.rect.centerx += speed_factor + 2
        elif self.direction_y and not self.direction_x:
            self.rect.centery += speed_factor + 2
            self.rect.centerx -= speed_factor + 2
        elif not self.direction_y and self.direction_x:
            self.rect.centery -= speed_factor + 2
            self.rect.centerx += speed_factor + 2
        elif not self.direction_y and not self.direction_x:
            self.rect.centery -= speed_factor + 2
            self.rect.centerx -= speed_factor + 2

        for ball in balls.sprites():
            if len(balls) == 1:
                ball.draw_ball()
            else:
                balls.remove(ball)


class Brick(Sprite):

    def __init__(self, screen):

        super(Brick, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.rect = pygame.Rect(
            brick_x, brick_y, brick_width, brick_height)

    def draw_brick(self):

        pygame.draw.rect(self.screen, (0, 0, 0), self.rect)

    def update(self, speed_factor):

        self.rect.centery += speed_factor

        for brick in bricks.sprites():
            if brick.rect.bottom >= screen_height:
                bricks.remove(brick)

            brick.draw_brick()


new_player = Player(screen)
players.add(new_player)

while True:

    clock.tick(60)  # Frames Per Second

    # Evaluar el valor de clock.tick para utilizarlo de mecanismo de generación de bloques
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón
                new_ball = Ball(screen, new_player, bricks)
                balls.add(new_ball)

    if 1 == random.randint(1,50):
        new_brick = Brick(screen)
        bricks.add(new_brick)

        random_pos = random.randint(0, int(amount_bricks))

        brick_x = (brick_width + brick_separation) * random_pos
        if brick_x >= screen_width - brick_separation:
            brick_x = 0

    mouse_x, mouse_y = pygame.mouse.get_pos()
    speed_factor += 0.001

    screen.blit(background, (0, 0))
    balls.update()
    players.update(mouse_x)
    bricks.update(speed_factor)
    pygame.display.flip()
