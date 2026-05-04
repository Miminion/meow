import json
import random
from pathlib import Path

import pygame

from db import get_personal_best, save_result


WIDTH = 600
HEIGHT = 600
CELL = 30
GRID_W = WIDTH // CELL
GRID_H = HEIGHT // CELL

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (120, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 220, 0)
BLUE = (0, 100, 255)
PURPLE = (160, 0, 200)
ORANGE = (255, 140, 0)

SETTINGS_FILE = Path("settings.json")

DEFAULT_SETTINGS = {
    "snake_color": [255, 0, 0],
    "grid": True,
    "sound": True
}


def load_settings():
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    for k in DEFAULT_SETTINGS:
        if k not in cfg:
            cfg[k] = DEFAULT_SETTINGS[k]

    return cfg


def save_settings(cfg):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def same_pos(a, b):
    return a.x == b.x and a.y == b.y


def in_list(p, pts):
    for item in pts:
        if item.x == p.x and item.y == p.y:
            return True
    return False


def free_point(snake, obs, extras=None):
    if extras is None:
        extras = []

    while True:
        p = Point(random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))

        if in_list(p, snake.body):
            continue
        if in_list(p, obs):
            continue
        if in_list(p, extras):
            continue

        return p


class Snake:
    def __init__(self, color):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
        self.score = 0
        self.fed = 0
        self.level = 1
        self.color = color
        self.shield = False

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def border_collision(self):
        h = self.body[0]
        return h.x < 0 or h.x >= GRID_W or h.y < 0 or h.y >= GRID_H

    def self_collision(self):
        h = self.body[0]
        for seg in self.body[1:]:
            if same_pos(h, seg):
                return True
        return False

    def obstacle_collision(self, obs):
        return in_list(self.body[0], obs)

    def grow(self):
        h = self.body[0]
        self.body.append(Point(h.x, h.y))

    def shorten(self, n):
        for _ in range(n):
            if len(self.body) > 1:
                self.body.pop()

    def draw(self, screen):
        h = self.body[0]
        pygame.draw.rect(screen, self.color, (h.x * CELL, h.y * CELL, CELL, CELL))

        for seg in self.body[1:]:
            pygame.draw.rect(screen, YELLOW, (seg.x * CELL, seg.y * CELL, CELL, CELL))


class Food:
    def __init__(self, snake, obs, extras=None):
        self.pos = free_point(snake, obs, extras)
        self.weight = random.choice([1, 2, 3])
        self.born = pygame.time.get_ticks()
        self.ttl = 6000

    def expired(self):
        return pygame.time.get_ticks() - self.born > self.ttl

    def draw(self, screen):
        if self.weight == 1:
            color = GREEN
        elif self.weight == 2:
            color = ORANGE
        else:
            color = PURPLE

        pygame.draw.rect(screen, color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))


class PoisonFood:
    def __init__(self, snake, obs, extras=None):
        self.pos = free_point(snake, obs, extras)
        self.born = pygame.time.get_ticks()
        self.ttl = 8000

    def expired(self):
        return pygame.time.get_ticks() - self.born > self.ttl

    def draw(self, screen):
        pygame.draw.rect(screen, DARK_RED, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))


class PowerUp:
    def __init__(self):
        self.kind = None
        self.pos = Point(0, 0)
        self.born = 0
        self.ttl = 8000
        self.on_field = False

    def spawn(self, snake, obs, extras):
        if self.on_field:
            return

        self.kind = random.choice(["speed", "slow", "shield"])
        self.pos = free_point(snake, obs, extras)
        self.born = pygame.time.get_ticks()
        self.on_field = True

    def expired(self):
        return self.on_field and pygame.time.get_ticks() - self.born > self.ttl

    def collect(self):
        self.on_field = False
        return self.kind

    def draw(self, screen):
        if not self.on_field:
            return

        if self.kind == "speed":
            color, label = BLUE, "S"
        elif self.kind == "slow":
            color, label = PURPLE, "L"
        else:
            color, label = ORANGE, "H"

        pygame.draw.rect(screen, color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

        font = pygame.font.SysFont("Verdana", 16, bold=True)
        txt = font.render(label, True, WHITE)
        r = txt.get_rect(center=(self.pos.x * CELL + CELL // 2, self.pos.y * CELL + CELL // 2))
        screen.blit(txt, r)


def draw_grid_chess(screen):
    colors = [WHITE, GRAY]
    for i in range(GRID_W):
        for j in range(GRID_H):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))


def draw_grid_lines(screen):
    for i in range(GRID_W):
        for j in range(GRID_H):
            pygame.draw.rect(screen, GRAY, (i * CELL, j * CELL, CELL, CELL), 1)


def draw_obstacles(screen, obs):
    for b in obs:
        pygame.draw.rect(screen, BLACK, (b.x * CELL, b.y * CELL, CELL, CELL))


def gen_obstacles(snake, level):
    if level < 3:
        return []

    obs = []
    count = min(4 + level, 12)
    h = snake.body[0]

    banned = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            banned.append(Point(h.x + dx, h.y + dy))

    tries = 0
    while len(obs) < count and tries < 300:
        tries += 1
        p = Point(random.randint(1, GRID_W - 2), random.randint(1, GRID_H - 2))

        if in_list(p, snake.body):
            continue
        if in_list(p, banned):
            continue
        if in_list(p, obs):
            continue

        obs.append(p)

    return obs


def run_game(screen, username, settings):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 18)

    snake = Snake(tuple(settings["snake_color"]))
    best = get_personal_best(username)

    obs = []
    food = Food(snake, obs)
    poison = PoisonFood(snake, obs, [food.pos])
    pu = PowerUp()

    running = True
    dead = False

    cur_power = None
    power_end = 0
    last_pu = pygame.time.get_ticks()

    while running:
        now = pygame.time.get_ticks()
        fps = 5 + snake.level

        if cur_power == "speed":
            fps += 5
            if now > power_end:
                cur_power = None
        elif cur_power == "slow":
            fps = max(3, fps - 3)
            if now > power_end:
                cur_power = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and snake.dx != -1:
                    snake.dx, snake.dy = 1, 0
                elif event.key == pygame.K_LEFT and snake.dx != 1:
                    snake.dx, snake.dy = -1, 0
                elif event.key == pygame.K_DOWN and snake.dy != -1:
                    snake.dx, snake.dy = 0, 1
                elif event.key == pygame.K_UP and snake.dy != 1:
                    snake.dx, snake.dy = 0, -1

        snake.move()

        hit = snake.border_collision() or snake.self_collision() or snake.obstacle_collision(obs)

        if hit:
            if snake.shield:
                snake.shield = False
                snake.body[0].x = GRID_W // 2
                snake.body[0].y = GRID_H // 2
            else:
                dead = True
                running = False

        if not dead:
            h = snake.body[0]

            if same_pos(h, food.pos):
                snake.grow()
                snake.score += food.weight
                snake.fed += 1

                old_lvl = snake.level
                snake.level = snake.fed // 4 + 1

                if snake.level != old_lvl:
                    obs = gen_obstacles(snake, snake.level)

                food = Food(snake, obs, [poison.pos])

            if food.expired():
                food = Food(snake, obs, [poison.pos])

            if same_pos(h, poison.pos):
                snake.shorten(2)

                if len(snake.body) <= 1:
                    dead = True
                    running = False
                else:
                    poison = PoisonFood(snake, obs, [food.pos])

            if poison.expired():
                poison = PoisonFood(snake, obs, [food.pos])

            if not pu.on_field and now - last_pu > 9000:
                pu.spawn(snake, obs, [food.pos, poison.pos])
                last_pu = now

            if pu.expired():
                pu.on_field = False

            if pu.on_field and same_pos(h, pu.pos):
                kind = pu.collect()

                if kind == "speed":
                    cur_power = "speed"
                    power_end = now + 5000
                elif kind == "slow":
                    cur_power = "slow"
                    power_end = now + 5000
                elif kind == "shield":
                    snake.shield = True

        draw_grid_chess(screen)

        if settings["grid"]:
            draw_grid_lines(screen)

        draw_obstacles(screen, obs)
        food.draw(screen)
        poison.draw(screen)
        pu.draw(screen)
        snake.draw(screen)

        screen.blit(font.render(f"Score: {snake.score}", True, BLACK), (10, 10))
        screen.blit(font.render(f"Level: {snake.level}", True, BLACK), (10, 32))
        screen.blit(font.render(f"Best: {best}", True, BLACK), (10, 54))
        screen.blit(font.render(f"Power: {cur_power if cur_power else 'None'}", True, BLACK), (10, 76))
        screen.blit(font.render(f"Shield: {'ON' if snake.shield else 'OFF'}", True, BLACK), (10, 98))

        pygame.display.flip()
        clock.tick(fps)

    save_result(username, snake.score, snake.level)

    return "game_over", {
        "score": snake.score,
        "level": snake.level,
        "best": max(best, snake.score)
    }