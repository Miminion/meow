import pygame
import random
import sys

pygame.init()


CELL = 25
COLS = 28
ROWS = 24
WIDTH  = COLS * CELL
HEIGHT = ROWS * CELL + 60   

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

font     = pygame.font.SysFont("Arial", 22, bold=True)
font_big = pygame.font.SysFont("Arial", 52, bold=True)
font_med = pygame.font.SysFont("Arial", 30, bold=True)


WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GREEN  = (0, 200, 0)
DGREEN = (0, 140, 0)
RED    = (220, 0, 0)
GREY   = (40, 40, 40)
YELLOW = (255, 215, 0)
BG     = (15, 15, 15)
ORANGE = (255, 140, 0)
CYAN   = (0, 220, 220)
PINK   = (255, 100, 180)

# направления
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)

#таблица спидов
SPEEDS = [8, 11, 15, 20, 26]


# виды хавчика

FOOD_TYPES = [
    {
        "name":   "apple",
        "weight": 50,           # база
        "score":  10,           # база+счет
        "color":  RED,
        "border": (160, 0, 0),
        "timer":  None,         #бесконечуакыт
    },
    {
        "name":   "berry",
        "weight": 30,           # редко
        "score":  20,
        "color":  PINK,
        "border": (180, 0, 100),
        "timer":  15,            # 15секлимит
    },
    {
        "name":   "melon",
        "weight": 15,           # ультрамегасупердуперредко
        "score":  40,
        "color":  ORANGE,
        "border": (180, 80, 0),
        "timer":  8,            # 8секлимит
    },
    {
        "name":   "diamond",
        "weight": 5,            #хаваем алмазы
        "score":  100,
        "color":  CYAN,
        "border": (0, 140, 180),
        "timer":  3,            #всего3сек
    },
]

# Total weight for weighted random selection
TOTAL_WEIGHT = sum(t["weight"] for t in FOOD_TYPES)


def pick_food_type():
    
    r = random.randint(1, TOTAL_WEIGHT)
    cumulative = 0
    for t in FOOD_TYPES:
        cumulative += t["weight"]
        if r <= cumulative:
            return t
    return FOOD_TYPES[0]  # fallback


class Food:
   

    def __init__(self, snake):
        self.food_type = pick_food_type()
        self.pos = self._random_pos(snake)
        # Timer: how many milliseconds until this food disappears (None = forever)
        if self.food_type["timer"] is not None:
            self.time_left = self.food_type["timer"] * 1000  # convert to ms
        else:
            self.time_left = None
        self.alive = True

    def _random_pos(self, snake):
      
        while True:
            x = random.randint(1, COLS - 2)
            y = random.randint(1, ROWS - 2)
            if (x, y) not in snake:
                return (x, y)

    def update(self, dt):
        
        if self.time_left is not None:
            self.time_left -= dt
            if self.time_left <= 0:
                self.alive = False

    def draw(self, surface):
       
        x, y = self.pos
        cx = x * CELL + CELL // 2
        cy = y * CELL + 60 + CELL // 2
        r  = CELL // 2 - 2

        pygame.draw.circle(surface, self.food_type["color"],  (cx, cy), r)
        pygame.draw.circle(surface, self.food_type["border"], (cx, cy), r, 2)

   
        if self.time_left is not None:
            total_ms   = self.food_type["timer"] * 1000
            ratio      = max(0.0, self.time_left / total_ms)
            bar_w      = CELL - 4
            bar_h      = 4
            bx         = x * CELL + 2
            by         = y * CELL + 60 + CELL - bar_h - 1
   
            pygame.draw.rect(surface, (60, 60, 60), (bx, by, bar_w, bar_h))
          
            fill_color = (
                int(255 * (1 - ratio)),   # R increases as time runs out
                int(255 * ratio),         # G decreases as time runs out
                0
            )
            pygame.draw.rect(surface, fill_color, (bx, by, int(bar_w * ratio), bar_h))




def draw_grid():
    #сетОчка
    for x in range(COLS):
        for y in range(ROWS):
            rect = pygame.Rect(x * CELL, y * CELL + 60, CELL, CELL)
            pygame.draw.rect(screen, (25, 25, 25), rect)
            pygame.draw.rect(screen, (35, 35, 35), rect, 1)


def draw_walls():
    #walls
    for x in range(COLS):
        for y in [0, ROWS - 1]:
            pygame.draw.rect(screen, GREY,
                             (x * CELL, y * CELL + 60, CELL, CELL))
    for y in range(ROWS):
        for x in [0, COLS - 1]:
            pygame.draw.rect(screen, GREY,
                             (x * CELL, y * CELL + 60, CELL, CELL))


def draw_snake(snake):
    #draw_zhylaaan
    for i, (x, y) in enumerate(snake):
        color = GREEN if i == 0 else DGREEN
        rect = pygame.Rect(x * CELL + 1, y * CELL + 60 + 1, CELL - 2, CELL - 2)
        pygame.draw.rect(screen, color, rect, border_radius=4)


def draw_hud(score, level):
   #менюшка с инфо
    pygame.draw.rect(screen, (20, 20, 30), (0, 0, WIDTH, 60))
    pygame.draw.line(screen, GREY, (0, 60), (WIDTH, 60), 2)
    s = font.render(f"score: {score}", True, WHITE)
    l = font.render(f"dengei: {level}", True, YELLOW)
    screen.blit(s, (15, 18))
    screen.blit(l, (WIDTH - l.get_width() - 15, 18))


def show_screen(title, sub="shashki ma ne"):
    #title
    screen.fill(BLACK)
    t = font_big.render(title, True, WHITE)
    screen.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 70))
    if sub:
        s = font_med.render(sub, True, YELLOW)
        screen.blit(s, (WIDTH // 2 - s.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.update()


def draw_legend(foods):
    #виды еды
    lx = WIDTH - 160
    ly = 2
    for food in foods:
        ft = food.food_type
        pygame.draw.circle(screen, ft["color"], (lx + 8, ly + 8), 6)
        label = font.render(f"+{ft['score']}", True, ft["color"])
        screen.blit(label, (lx + 18, ly))
        ly += 18


def main():
   

    snake     = [(COLS // 2, ROWS // 2),
                 (COLS // 2 - 1, ROWS // 2),
                 (COLS // 2 - 2, ROWS // 2)]
    direction = RIGHT
    next_dir  = RIGHT

    #начать с базы
    foods = [Food(snake)]

    score           = 0
    level           = 1
    foods_eaten     = 0
    FOODS_FOR_LEVEL = 3    # Eat 3 to level up

    game_over  = False
    move_timer = 0

    #таймеры для легенд
    food_spawn_timer    = 0
    FOOD_SPAWN_INTERVAL = 5000   # Spawn extra food every 5 seconds
    MAX_FOODS           = 3      # No more than 3 foods at once on the grid

    # интро
    show_screen("ZHYLAN", "space — basta")
    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:   pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:  waiting = False
                if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

    #лупик
    while True:
        dt = clock.tick(60)  # ms since last frame

       
        for e in pygame.event.get():
            if e.type == pygame.QUIT:   pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                if e.key == pygame.K_SPACE and game_over:
                    main(); return   # Restart

               #направления
                if e.key in (pygame.K_UP, pygame.K_w) and direction != DOWN:
                    next_dir = UP
                if e.key in (pygame.K_DOWN, pygame.K_s) and direction != UP:
                    next_dir = DOWN
                if e.key in (pygame.K_LEFT, pygame.K_a) and direction != RIGHT:
                    next_dir = LEFT
                if e.key in (pygame.K_RIGHT, pygame.K_d) and direction != LEFT:
                    next_dir = RIGHT

        if not game_over:
   
            for food in foods:
                food.update(dt)
            foods = [f for f in foods if f.alive]

            food_spawn_timer += dt
            if food_spawn_timer >= FOOD_SPAWN_INTERVAL:
                food_spawn_timer = 0
                if len(foods) < MAX_FOODS:
                    foods.append(Food(snake))

   
            if not foods:
                foods.append(Food(snake))

       
            move_timer += 1
            speed = SPEEDS[min(level - 1, len(SPEEDS) - 1)]

            if move_timer >= 60 // speed:
                move_timer = 0
                direction  = next_dir

              
                hx, hy   = snake[0]
                new_head = (hx + direction[0], hy + direction[1])

                #стены голова бить
                if new_head[0] <= 0 or new_head[0] >= COLS - 1 or \
                   new_head[1] <= 0 or new_head[1] >= ROWS - 1:
                    game_over = True

                # суицид
                elif new_head in snake:
                    game_over = True

                else:
                    snake.insert(0, new_head)  # Move head forward

                    # Check if any food is eaten
                    eaten_food = None
                    for food in foods:
                        if new_head == food.pos:
                            eaten_food = food
                            break

                    if eaten_food:
                        # добавсчет
                        score       += eaten_food.food_type["score"] * level
                        foods_eaten += 1
                        foods.remove(eaten_food)  # Remove eaten food
                        # Snake grows (we don't pop the tail)

                        # левелап
                        if foods_eaten >= FOODS_FOR_LEVEL:
                            level       += 1
                            foods_eaten  = 0
                    else:
                        snake.pop()  # Remove tail (snake moves forward without growing)

      
        screen.fill(BG)
        draw_grid()
        draw_walls()

    
        for food in foods:
            food.draw(screen)

        draw_snake(snake)
        draw_hud(score, level)
        draw_legend(foods) 

        # проиграллох
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            t = font_big.render("GAME OVER", True, RED)
            screen.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 70))
            s = font_med.render(f"SCORE: {score}  DENGEI: {level}", True, YELLOW)
            screen.blit(s, (WIDTH // 2 - s.get_width() // 2, HEIGHT // 2 + 10))
            s2 = font.render("space — kaittan", True, WHITE)
            screen.blit(s2, (WIDTH // 2 - s2.get_width() // 2, HEIGHT // 2 + 55))

        pygame.display.update()


main()
