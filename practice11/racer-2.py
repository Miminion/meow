import pygame
from pygame.locals import *
import random
import sys
import os

pygame.init()


FPS = 60
ENI = 600       
UZYN = 900      

ROAD_LEFT = 100
ROAD_RIGHT = 500

CAR_W, CAR_H = 80, 140


SARY = (255, 215, 0)     
AK = (255, 255, 255)       
ZHAS = (34, 139, 34)       
DARK_GREY = (30, 30, 30)    

Disp = pygame.display.set_mode((ENI, UZYN))
FramePerSec = pygame.time.Clock()
pygame.display.set_caption("шашочки")

font_small = pygame.font.SysFont("Arial", 28, bold=True)
font_medium = pygame.font.SysFont("Arial", 40, bold=True)
font_large = pygame.font.SysFont("Arial", 72, bold=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_img(filename, size):
    
    path = os.path.join(BASE_DIR, filename)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)

IMG_PLAYER = load_img("/Users/medinameirambek/Desktop/meow/practice10/images.png", (CAR_W, CAR_H))
IMG_ENEMY = load_img("/Users/medinameirambek/Desktop/meow/practice10/enemy.png", (CAR_W, CAR_H))


COIN_TYPES = [
    {"weight": 60, "value": 1,  "color": (200, 160, 0),   "border": (140, 100, 0), "label": "1"},   # Bronze (common)
    {"weight": 30, "value": 3,  "color": (192, 192, 192), "border": (130, 130, 130), "label": "3"}, # Silver (uncommon)
    {"weight": 10, "value": 5,  "color": (255, 215, 0),   "border": (180, 140, 0), "label": "5"},   # Gold (rare)
]

# увелечение скорости кчау от скока монет
SPEED_BOOST_THRESHOLD = 10  
SPEED_BOOST_AMOUNT    = 1  


def pick_coin_type():

    total = sum(t["weight"] for t in COIN_TYPES)
    r = random.randint(1, total)
    cumulative = 0
    for t in COIN_TYPES:
        cumulative += t["weight"]
        if r <= cumulative:
            return t
    return COIN_TYPES[0] 


#игрок
class Player(pygame.sprite.Sprite):
    SPEED = 7

    def __init__(self):
        super().__init__()
        self.image = IMG_PLAYER
        self.rect = self.image.get_rect()
       
        self.rect.centerx = (ROAD_LEFT + ROAD_RIGHT) // 2
        self.rect.bottom = UZYN - 30

    def update(self):
       
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.move_ip(-self.SPEED, 0)
        if keys[K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.move_ip(self.SPEED, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# красная машинакчау
class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        super().__init__()
        self.speed = speed
        self.image = IMG_ENEMY
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        
        self.rect.centerx = random.randint(ROAD_LEFT + CAR_W//2, ROAD_RIGHT - CAR_W//2)
        self.rect.bottom = 0

    def move(self):
  
        self.rect.move_ip(0, self.speed)
        if self.rect.top > UZYN:
            self.kill()  # Remove from all groups

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# монеткииии
class Coin(pygame.sprite.Sprite):
    def __init__(self, speed=4, coin_type=None):
        super().__init__()
        # Select coin type if not provided
        if coin_type is None:
            coin_type = pick_coin_type()
        self.coin_type = coin_type
        self.value = coin_type["value"]  

        
        self.radius = 14
        size = self.radius * 2
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, coin_type["color"], (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, coin_type["border"], (self.radius, self.radius), self.radius, 3)

       
        label_font = pygame.font.SysFont("Arial", 13, bold=True)
        label_surf = label_font.render(coin_type["label"], True, (30, 30, 30))
        lx = self.radius - label_surf.get_width() // 2
        ly = self.radius - label_surf.get_height() // 2
        self.image.blit(label_surf, (lx, ly))

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(ROAD_LEFT + 20, ROAD_RIGHT - 20)
        self.rect.y = -20

        self.speed = speed
        # Float position for smooth magnet movement
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def move(self, player_rect):
       
        MAGNET_RADIUS = 300
        MAGNET_SPEED  = 8


        self.y += self.speed  

        # Calculate distance to player center
        px, py = player_rect.center
        dx, dy = px - self.x, py - self.y
        dist = (dx**2 + dy**2) ** 0.5

       
        if 0 < dist < MAGNET_RADIUS:
            strength = (1 - dist / MAGNET_RADIUS) * MAGNET_SPEED
            self.x += (dx / dist) * strength
            self.y += (dy / dist) * strength

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Remove coin if it exits the screen
        if self.rect.top > UZYN:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# рисунок дороги
class RoadMarkings:
    DASH_H = 60
    GAP_H  = 60
    DASH_W = 12

    def __init__(self):
        self.offset = 0

    def update(self, speed):
        
        self.offset = (self.offset + speed) % (self.DASH_H + self.GAP_H)

    def draw(self, surface):
        
        y = -self.DASH_H + self.offset
        while y < UZYN:
            pygame.draw.rect(surface, AK,
                             ((ROAD_LEFT + ROAD_RIGHT)//2 - 6, y, self.DASH_W, self.DASH_H))
            y += self.DASH_H + self.GAP_H


def draw_road(surface):

    surface.fill(ZHAS)
    pygame.draw.rect(surface, DARK_GREY,
                     (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, UZYN))
    pygame.draw.rect(surface, AK, (ROAD_LEFT, 0, 6, UZYN))
    pygame.draw.rect(surface, AK, (ROAD_RIGHT - 6, 0, 6, UZYN))


def draw_hud(surface, score, coins, enemy_speed_level):
   
    surface.blit(font_small.render(f"score: {score}", True, AK), (10, 10))
    surface.blit(font_small.render(f"coins: {coins}", True, SARY), (10, 50))
    # Show current enemy speed boost level
    surface.blit(font_small.render(f"level: {enemy_speed_level}", True, (200, 100, 100)), (10, 90))


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

    while True:
       
        road = RoadMarkings()
        player = Player()
        enemies = pygame.sprite.Group()
        coins = pygame.sprite.Group()

        score = 0
        coin_count = 0       
        game_over = False

        enemy_timer = 0
        coin_timer  = 0

        # Track how many speed thresholds have been crossed
        enemy_speed_level = 0

        #интро
        draw_road(Disp)
        show_overlay(Disp, "Shashki ma ne", "SPACE to start")
        pygame.display.update()

        waiting = True
        while waiting:
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == KEYDOWN:
                    if ev.key == K_SPACE:
                        waiting = False

        # лупик игры
        while True:
            dt = FramePerSec.tick(FPS)

            for ev in pygame.event.get():
                if ev.type == QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == KEYDOWN:
                    if ev.key == K_SPACE and game_over:
                        return  # Restart via outer while True

            if not game_over:
                enemy_timer += dt
                coin_timer  += dt

              
                current_enemy_speed = 5 + score // 200 + enemy_speed_level * SPEED_BOOST_AMOUNT

                
                if enemy_timer > 1200:
                    enemies.add(Enemy(speed=current_enemy_speed))
                    enemy_timer = 0

              
                if coin_timer > 2000:
                    coins.add(Coin(speed=4, coin_type=pick_coin_type()))
                    coin_timer = 0

                player.update()

                # Move all enemies and coins
                for e in enemies:
                    e.move()
                for c in coins:
                    c.move(player.rect)

                road.update(6)
                score += 1

                if pygame.sprite.spritecollideany(player, enemies):
                    game_over = True

      
                collected = pygame.sprite.spritecollide(player, coins, True)
                for c in collected:
                    coin_count += c.value  # Add coin's value (1, 3, or 5)

                
                new_speed_level = coin_count // SPEED_BOOST_THRESHOLD
                if new_speed_level > enemy_speed_level:
                    enemy_speed_level = new_speed_level
         
                    for e in enemies:
                        e.speed = 5 + score // 200 + enemy_speed_level * SPEED_BOOST_AMOUNT

          
            draw_road(Disp)
            road.draw(Disp)

            for e in enemies:
                e.draw(Disp)
            for c in coins:
                c.draw(Disp)

            player.draw(Disp)
            draw_hud(Disp, score, coin_count, enemy_speed_level)

            if game_over:
                show_overlay(Disp, "THE END",
                             f"Score: {score} | Coins: {coin_count} | Lvl: {enemy_speed_level}")

            pygame.display.update()


if __name__ == "__main__":
    while True:
        main()
