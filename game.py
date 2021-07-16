import sys
import pygame
import random

pygame.init()

size = width, height = 700, 700
screen = pygame.display.set_mode(size)

main_sprite = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group() # empty at the start


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("bullet.jpg")
        self.image = pygame.transform.scale(self.image, (20, 20))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.bullet_speed = [4, 4]
        if direction == "up":
            self.bullet_speed = [0, -15]
        elif direction == "down":
            self.bullet_speed = [0, 15]
        elif direction == "left":
            self.bullet_speed = [-15, 0]
        elif direction == "right":
            self.bullet_speed = [15, 0]
    
    def update(self):
        self.rect = self.rect.move(self.bullet_speed)
        if self.rect.left < 0 or self.rect.right > width or self.rect.top < 0 or self.rect.bottom > height:
            bullet_sprites.remove(self)
    
    def collide_with_enemy(self):
        pass
        pygame.sprite.Sprite.kill(self)
        bullet_sprites.remove(self)


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("main_character.png")
        self.image = pygame.transform.scale(self.image, (60, 60))

        self.rect = self.image.get_rect()
        self.rect.center = (350, 350)
        self.total_lives = 3
        # self.lastHit = 0

        self.collision_immune = False
        self.collision_immune_time = 0 # for invincibility frames
    
    def hit_main_character(self):
        if self.collision_immune:
            return
        # self.lastHit = pygame.time.get_ticks()

        self.total_lives -= 1
        # different code to handle death in the loop but here
        if self.total_lives <= 0:
            sys.exit() # placeholder


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # pick one of three enemy sprites
        num = random.randint(0, 2)
        if num == 0:
            self.image = pygame.image.load("enemy1.png")
        elif num == 1:
            self.image = pygame.image.load("enemy2.png")
        elif num == 2:
            self.image = pygame.image.load("enemy3.png")
        
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.rect = self.image.get_rect()
        
        # randomly choose a side to start on: left, right, top, or bottom
        rand = random.randint(0, 3)
        if rand == 0:
            self.rect.center = (20, random.randint(0, 700))
        elif rand == 1:
            self.rect.center = (680, random.randint(0, 700))
        elif rand == 2:
            self.rect.center = (random.randint(0, 700), 20)
        elif rand == 3:
            self.rect.center = (random.randint(0, 700), 680)
        
        self.enemy_speed = [5, 5]

    def update(self):
        self.rect = self.rect.move(self.enemy_speed)

        if self.rect.left < 0 or self.rect.right > width:
            self.enemy_speed[0] = -self.enemy_speed[0]
            self.enemy_speed[1] = self.enemy_speed[1]
        if self.rect.top < 0 or self.rect.bottom > height:
            self.enemy_speed[1] = -self.enemy_speed[1]
            self.enemy_speed[0] = self.enemy_speed[0]
    
    def kill_enemy(self):
        pygame.sprite.Sprite.kill(self)
        enemy_sprites.remove(self)


# Some helper functions

def make_bullet(direction: str) -> Bullet:
    return Bullet(main.rect.x, main.rect.y, direction)

def check_main_collisions(collisions):
    if main_collisions != None:
        main.hit_main_character()
        main.collision_immune_time = 30 # immunity frames post-hit
        main.collision_immune = True


main_character_speed = [0, 0]
main = MainCharacter()
main_sprite.add(main)
for i in range(0, 3):
    enemy_sprites.add(Enemy())

# add to these every X ticks
enemy_add_countdown = 200 # how often enemies spawn
bullet_countdown = 0 # how often someone can fire a bullet, starts at 0 because you can fire bullets immediately

lives_font = pygame.font.SysFont("Courier New", 40, bold=pygame.font.Font.bold)
clock = pygame.time.Clock()

while True:    
    clock.tick(60)

    # spawn a new enemy if necessary
    enemy_add_countdown -= 1
    bullet_countdown -= 1 # time to fire a bullet
    main.collision_immune_time -= 1 # reduce immunity frames, if applicable
    if main.collision_immune_time <= 0:
        main.collision_immune = False

    if enemy_add_countdown == 0:
        max_idx = random.randint(0, 5) # spawn some number of enemies from 0 to 5
        for i in range(0, max_idx):
            enemy_sprites.add(Enemy())
        enemy_add_countdown += random.randint(100, 200)
    

    key = pygame.key.get_pressed()
    # wasd moves character; NOT elif, all should be checked each run
    if (key[pygame.K_w]):
        # up
        main_character_speed[1] = -5
    if (key[pygame.K_s]):
        # down
        main_character_speed[1] = 5
    if (key[pygame.K_a]):
        # left
        main_character_speed[0] = -5
    if (key[pygame.K_d]):
        # right
        main_character_speed[0] = 5
    
    # only shoot one at a time, so elif
    if bullet_countdown <= 0:
        position = main.image.get_rect()
        if key[pygame.K_UP]:
            bullet = make_bullet("up")
            bullet_sprites.add(bullet)
            bullet_countdown = 30
        elif key[pygame.K_RIGHT]:
            bullet = make_bullet("right")
            bullet_sprites.add(bullet)
            bullet_countdown = 30
        elif key[pygame.K_DOWN]:
            bullet = make_bullet("down")
            bullet_sprites.add(bullet)
            bullet_countdown = 30
        elif key[pygame.K_LEFT]:
            bullet = make_bullet("left")
            bullet_sprites.add(bullet)
            bullet_countdown = 30
    
    # need to make sure that this doesn't let players or enemies go off the screen either

    if main.rect.left < 0 or main.rect.right > width:
        main_character_speed[0] = -main_character_speed[0]
    if main.rect.top < 0 or main.rect.bottom > height:
        main_character_speed[1] = -main_character_speed[1]
    
    main.rect = main.rect.move(main_character_speed)
    main_character_speed = [0, 0] # stop moving after one click, just move one position at a time then stop
    enemy_sprites.update()
    bullet_sprites.update()

    main_collisions = pygame.sprite.spritecollideany(main, enemy_sprites)
    check_main_collisions(main_collisions)


    # checks for collisions and removes any enemies and bullets that collided
    bullet_collisions = pygame.sprite.groupcollide(bullet_sprites, enemy_sprites, True, True)


    screen.fill((36, 0, 0)) # reddish brown
    main_sprite.draw(screen)
    enemy_sprites.draw(screen)
    bullet_sprites.draw(screen)

    # # check if you've lost
    # if main.total_lives <= 0:
    #     # draw_you_lose = lives_font.render("You lose! " + str("x") + " points", True, (50, 156, 255)) # points don't work yet
    #     draw_you_lose = lives_font.render("You lose!", True, (50, 156, 255))
    #     screen.blit(draw_you_lose, (200, 100))
    #     break
    
    draw_lives = lives_font.render("Lives: " + str(main.total_lives), True, (51, 156, 255)) # light blue
    screen.blit(draw_lives, (0, 0))
    # draw_points = lives_font.render("Points: " + str("placeholder"), True, (51, 156, 255)) # points don't work yet
    # screen.blit(draw_points, (0, 30))

    pygame.display.flip()
    pygame.event.pump()
