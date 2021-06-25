import sys
import pygame
import random

pygame.init()

size = width, height = 700, 700
screen = pygame.display.set_mode(size)

main_character_speed = [5, 5]


# enemies randomly spawn every 10 seconds or so idk
# player has 3 lives
# maybe use a counter for that

# player can shoot at enemies
# WASD to move
# updownleftright to shoot
# set speed, doesn't change


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("main_character.jpg")
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.rect = self.image.get_rect()
        self.rect.center = (350, 350)
        self.totalLives = 3
        self.lastHit = 0
    
    def hit_main_character(self):
        self.lastHit = pygame.time.get_ticks()
        self.totalLives -= 1

        if self.totalLives <= 0:
            # print a "You lose!" message
            # yes it's impossible to win
            print("FAILED")
            sys.exit() # placeholder


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # pick one of three enemy sprites
        num = random.randint(0, 2)
        if num == 0:
            self.image = pygame.image.load("enemy1.jpg")
        elif num == 1:
            self.image = pygame.image.load("enemy2.jpg")
        elif num == 2:
            self.image = pygame.image.load("enemy3.jpg")
        
        self.image = pygame.transform.scale(self.image, (20, 20))

        self.rect = self.image.get_rect()
        
        # randomly choose a side to start on: left, right, top, or bottom
        rand = random.randint(0, 3)
        if rand == 0:
            self.rect.center = (5, random.randint(0, 700))
        elif rand == 1:
            self.rect.center = (695, random.randint(0, 700))
        elif rand == 2:
            self.rect.center = (random.randint(0, 700), 5)
        elif rand == 3:
            self.rect.center = (random.randint(0, 700), 695)
        
        badSpeed = [1, 1]

    def update(self):
        self.rect = self.rect.move(badSpeed)
    
    def kill_enemy(self):
        # remove it
        # self.rect_sprite.kill()
        pygame.sprite.Sprite.kill(self)


main = MainCharacter()

main_sprite = pygame.sprite.Group()
main_sprite.add(main)

enemy_sprites = pygame.sprite.Group()

courier_font = pygame.font.SysFont("Courier New", 20)

# add to these every X ticks
countdown_to_enemy_add = 10 # adjust number if necessary


clock = pygame.time.Clock()
while True:
    clock.tick(60)

    key = pygame.key.get_pressed()
    # wasd moves character; NOT elif, all should be checked each run
    if key[pygame.K_w]:
        # up
        print("move")
    if key[pygame.K_a]:
        # left
        print("move up")
    if key[pygame.K_s]:
        # down
        print("move up")
    if key[pygame.K_d]:
        # right
        print("move up")
    
    # only shoot one at a time, so elif
    if key[pygame.K_UP]:
        # up
        print("move up")
    elif key[pygame.K_RIGHT]:
        # right
        print("move up")
    elif key[pygame.K_DOWN]:
        # down
        print("move up")
    elif key[pygame.K_LEFT]:
        # left
        print("move up")
    
    # need to make sure that this doesn't let players or enemies go off the screen either

    if main.rect.left < 0 or main.rect.right > width:
        main_character_speed[0] = -main_character_speed[0]
    if main.rect.top < 0 or main.rect.bottom > height:
        main_character_speed[1] = -main_character_speed[1]
    
    main.rect = main.rect.move(main_character_speed)
    enemy_sprites.update()

    screen.fill((36, 0, 0)) # black
    main_sprite.draw(screen)
    enemy_sprites.draw(screen)

    nums_lives_draw = courier_font.render(str(main.totalLives), True, (51, 156, 255))
    screen.blit(nums_lives_draw, (30, 30))

    pygame.display.flip()

