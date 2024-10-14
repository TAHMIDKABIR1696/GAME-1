from typing import Any

import pygame
from pygame.locals import *
import random

#from pygame.sprite import Group, _SpriteSupportsGroup

pygame.init()
width = 800
height = 900

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("FLAPPY BIRD")

background = pygame.image.load('images/bg.png')
ground = pygame.image.load('images/ground.png')
ground_scroll = 0
speed = 4
timer = pygame.time.Clock()
fps = 60
fly = False  #to fly the bird
dead = False  # to game over
gap = 200  #creating gap between pipes
pipe_freq = 2000  #milisecond
last_pipe = pygame.time.get_ticks() - pipe_freq  #to create the pipe right away
score = 0
pass_pipe = False
font = pygame.font.SysFont('Bauhaus 93', 60)
White = (255, 255, 255)
button = pygame.image.load('images/restart.png')


def draw_txt(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def restart_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(height / 2)
    score = 0
    return score


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bird1.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 0
        self.clicked = False

    #creating bird flooting system

    def update(self):
        if dead == False:
            if fly == True:
                self.velocity += 0.5
                if self.velocity > 9.8:  #adding limit(gravity)
                    # it will reset to the value if the function exceeds the value
                    self.velocity = 9.8
                if self.rect.bottom < 768:
                    self.rect.y += int(self.velocity)

            # jump function
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                # if mouse has been clicked or not
                self.velocity = -10
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False


#creating PIPEs
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/pipe.png")
        self.rect = self.image.get_rect()

        if position == 1:  #fliping y axis
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(gap / 2)]  # position 1 is top -1 is bottom

    def update(self):
        self.rect.x -= speed
        if self.rect.right < 0:
            self.kill()


class Restart():
    #Creating reset button
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):  #creating restart button
        pos = pygame.mouse.get_pos()
        action = False
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(height / 2))

bird_group.add(flappy)

restart = Restart(width // 2 - 50, height // 2 - 100, button)

#MAIN GAME LOOP
start = True
while start:
    timer.tick(fps)
    screen.blit(background, (0, 0))
    #drawing the Bird
    bird_group.draw(screen)
    bird_group.update()
    #Drawing the pipe
    pipe_group.draw(screen)

    #SCROLL THE GROUND
    screen.blit(ground, (ground_scroll, 768))

    #check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and pass_pipe == False:
            pass_pipe = True

        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    draw_txt(str(score), font, White, int(width / 2), 20)

    #bird hit the pipe
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        dead = True

    # bird hit the ground
    if flappy.rect.bottom >= 768:
        dead = True
        fly = False

    if dead == False and fly == True:

        #pipe time
        pipe_time = pygame.time.get_ticks()
        if pipe_time - last_pipe > pipe_freq:
            pipe_height = random.randint(-100, 100)
            bottom_pipes = Pipe(width, int(height / 2) + pipe_height, -1)
            top_pipes = Pipe(width, int(height / 2) + pipe_height, 1)
            pipe_group.add(bottom_pipes)
            pipe_group.add(top_pipes)
            last_pipe = pipe_time

        #making scrolling ground
        ground_scroll -= speed

        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()
    #game over and restart
    if dead == True:
        if restart.draw() == True:
            dead = False
            score = restart_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            fly = True

    pygame.display.update()  #update images
pygame.quit()
