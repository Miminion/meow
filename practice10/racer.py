

import pygame
from pygame.locals import *
import random
import sys
import os

pygame.init()


FPS        = 60
ENI        = 600    
UZYN       = 900    


ROAD_LEFT  = 100
ROAD_RIGHT = 500


CAR_W, CAR_H   = 80, 140
COIN_W, COIN_H = 55, 55


SARY      = (255, 215,   0)
AK        = (255, 255, 255)
ZHAS      = ( 34, 139,  34)
DARK_GREY = ( 30,  30,  30)


Disp        = pygame.display.set_mode((ENI, UZYN))
FramePerSec = pygame.time.Clock()
pygame.display.set_caption("Гонки")

font_small  = pygame.font.SysFont("Arial", 28, bold=True)
font_medium = pygame.font.SysFont("Arial", 40, bold=True)
font_large  = pygame.font.SysFont("Arial", 72, bold=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_img(filename, size):
    path = os.path.join(BASE_DIR, filename)
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)
    return img

IMG_PLAYER = load_img("images.png", (CAR_W, CAR_H))
IMG_ENEMY  = load_img("enemy.png",  (CAR_W, CAR_H))
IMG_COIN   = load_img("tg.png",   (COIN_W, COIN_H))





class Player(pygame.sprite.Sprite):
    SPEED = 7

    def __init__(self):
        super().__init__()
        self.image = IMG_PLAYER
        self.rect  = self.image.get_rect()
       
        self.rect.centerx = (ROAD_LEFT + ROAD_RIGHT) // 2
        self.rect.bottom  = UZYN - 30

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]  and self.rect.left  > ROAD_LEFT:
            self.rect.move_ip(-self.SPEED, 0)
        if keys[K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.move_ip( self.SPEED, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        super().__init__()
        self.speed = speed
        self.image = IMG_ENEMY
        self.rect  = self.image.get_rect()
        # Спавним внутри дороги с учётом ширины машины
        self.rect.centerx = random.randint(ROAD_LEFT + CAR_W // 2,
                                           ROAD_RIGHT - CAR_W // 2)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > UZYN:
            self.rect.bottom  = 0
            self.rect.centerx = random.randint(ROAD_LEFT + CAR_W // 2,
                                               ROAD_RIGHT - CAR_W // 2)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed=4):
        super().__init__()
        self.speed = speed
        self.image = IMG_COIN
        self.rect  = self.image.get_rect()
        self.rect.centerx = random.randint(ROAD_LEFT  + COIN_W // 2,
                                           ROAD_RIGHT - COIN_W // 2)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > UZYN:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)




class RoadMarkings:
    DASH_H = 60
    GAP_H  = 60
    DASH_W = 12

    DASH_X = (ROAD_LEFT + ROAD_RIGHT) // 2 - 6

    def __init__(self):
        self.offset = 0

    def update(self, speed):
        self.offset = (self.offset + speed) % (self.DASH_H + self.GAP_H)

    def draw(self, surface):
        y = -self.DASH_H + self.offset
        while y < UZYN:
            pygame.draw.rect(surface, AK,
                             (self.DASH_X, y, self.DASH_W, self.DASH_H))
            y += self.DASH_H + self.GAP_H


def draw_road(surface):
 
    surface.fill(ZHAS)

    pygame.draw.rect(surface, DARK_GREY,
                     (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, UZYN))
    # Бордюры
    pygame.draw.rect(surface, AK, (ROAD_LEFT,      0, 6, UZYN))
    pygame.draw.rect(surface, AK, (ROAD_RIGHT - 6, 0, 6, UZYN))


def draw_hud(surface, score, coins):
    
    surface.blit(font_small.render(f"Очки:", True, AK),        (10, 10))
    surface.blit(font_small.render(str(score), True, AK),      (10, 40))

    cs = font_small.render(f"Монеты:", True, SARY)
    surface.blit(cs, (ENI - cs.get_width() - 10, 10))
    cv = font_small.render(str(coins), True, SARY)
    surface.blit(cv, (ENI - cv.get_width() - 10, 40))


def show_overlay(surface, title, subtitle=""):
    ov = pygame.Surface((ENI, UZYN), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 160))
    surface.blit(ov, (0, 0))
    t = font_large.render(title, True, AK)
    surface.blit(t, (ENI//2 - t.get_width()//2, UZYN//2 - 80))
    if subtitle:
        s = font_medium.render(subtitle, True, SARY)
        surface.blit(s, (ENI//2 - s.get_width()//2, UZYN//2 + 20))



def main():
    road        = RoadMarkings()
    P1          = Player()
    enemies     = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    enemies.add(Enemy(speed=5))

    score = 0; coin_count = 0; enemy_speed = 5
    enemy_timer = 0; enemy_itvl = 1500
    coin_timer  = 0; coin_itvl  = 2000
    game_over   = False

    
    draw_road(Disp)
    show_overlay(Disp, "Shashki ma ne", "space-basta")
    pygame.display.update()
    while True:
        for ev in pygame.event.get():
            if ev.type == QUIT: pygame.quit(); sys.exit()
            if ev.type == KEYDOWN:
                if ev.key == K_SPACE:  break
                if ev.key == K_ESCAPE: pygame.quit(); sys.exit()
        else:
            continue
        break

    
    while True:
        dt = FramePerSec.tick(FPS)

        for ev in pygame.event.get():
            if ev.type == QUIT: pygame.quit(); sys.exit()
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE: pygame.quit(); sys.exit()
                if ev.key == K_SPACE and game_over: main(); return

        if not game_over:
            enemy_speed = 5 + score // 200
            enemy_itvl  = max(600, 1500 - score // 5)

            enemy_timer += dt
            if enemy_timer >= enemy_itvl:
                enemies.add(Enemy(speed=enemy_speed))
                enemy_timer = 0

            coin_timer += dt
            if coin_timer >= coin_itvl:
                coins_group.add(Coin(speed=max(4, enemy_speed - 1)))
                coin_timer = 0

            P1.update()
            for e in enemies:     e.move()
            for c in coins_group: c.move()
            road.update(enemy_speed)
            score += 1

            if pygame.sprite.spritecollideany(P1, enemies):
                game_over = True
            coin_count += len(pygame.sprite.spritecollide(P1, coins_group, True))

        draw_road(Disp)
        road.draw(Disp)
        for e in enemies:     e.draw(Disp)
        for c in coins_group: c.draw(Disp)
        P1.draw(Disp)
        draw_hud(Disp, score, coin_count)

        if game_over:
            show_overlay(Disp, "THE END",
                         f"SCore: {score}  Kaspi: {coin_count}  |  Space")

        pygame.display.update()


if __name__ == "__main__":
    main()