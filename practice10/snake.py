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

font      = pygame.font.SysFont("Arial", 22, bold=True)
font_big  = pygame.font.SysFont("Arial", 52, bold=True)
font_med  = pygame.font.SysFont("Arial", 30, bold=True)


WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GREEN  = (0, 200, 0)
DGREEN = (0, 140, 0)
RED    = (220, 0, 0)
GREY   = (40, 40, 40)
YELLOW = (255, 215, 0)
BG  = (15, 15, 15)


UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)


SPEEDS = [8, 11, 15, 20, 26]


def new_food(snake):
   
    while True:
        x = random.randint(1, COLS - 2)
        y = random.randint(1, ROWS - 2)
        if (x, y) not in snake:
            return (x, y)


def draw_grid():
    for x in range(COLS):
        for y in range(ROWS):
            rect = pygame.Rect(x * CELL, y * CELL + 60, CELL, CELL)
            pygame.draw.rect(screen, (25, 25, 25), rect)
            pygame.draw.rect(screen, (35, 35, 35), rect, 1)


def draw_walls():
  
    for x in range(COLS):
        for y in [0, ROWS - 1]:
            pygame.draw.rect(screen, GREY,
                             (x * CELL, y * CELL + 60, CELL, CELL))
    for y in range(ROWS):
        for x in [0, COLS - 1]:
            pygame.draw.rect(screen, GREY,
                             (x * CELL, y * CELL + 60, CELL, CELL))


def draw_snake(snake):
    for i, (x, y) in enumerate(snake):
        color = GREEN if i == 0 else DGREEN
        rect = pygame.Rect(x * CELL + 1, y * CELL + 60 + 1, CELL - 2, CELL - 2)
        pygame.draw.rect(screen, color, rect, border_radius=4)


def draw_food(food):
    x, y = food
    cx = x * CELL + CELL // 2
    cy = y * CELL + 60 + CELL // 2
    pygame.draw.circle(screen, RED, (cx, cy), CELL // 2 - 2)


def draw_hud(score, level):
    pygame.draw.rect(screen, (20, 20, 30), (0, 0, WIDTH, 60))
    pygame.draw.line(screen, GREY, (0, 60), (WIDTH, 60), 2)
    s = font.render(f"score: {score}", True, WHITE)
    l = font.render(f"dengei: {level}", True, YELLOW)
    screen.blit(s, (15, 18))
    screen.blit(l, (WIDTH - l.get_width() - 15, 18))


def show_screen(title, sub="shashki ma ne"):
    screen.fill(BLACK)
    t = font_big.render(title, True, WHITE)
    screen.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 70))
    if sub:
        s = font_med.render(sub, True, YELLOW)
        screen.blit(s, (WIDTH // 2 - s.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.update()


def main():
    
    snake = [(COLS // 2, ROWS // 2),
             (COLS // 2 - 1, ROWS // 2),
             (COLS // 2 - 2, ROWS // 2)]

    direction = RIGHT
    next_dir  = RIGHT
    food      = new_food(snake)

    score            = 0
    level            = 1
    foods_eaten      = 0   
    FOODS_FOR_LEVEL  = 3   

    game_over = False
    move_timer = 0

  
    show_screen("ZHYLAN", "space — basta")
    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE: waiting = False
                if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

    while True:
        clock.tick(60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                if e.key == pygame.K_SPACE and game_over:
                    main(); return
            
                if e.key in (pygame.K_UP, pygame.K_w) and direction != DOWN:
                    next_dir = UP
                if e.key in (pygame.K_DOWN, pygame.K_s) and direction != UP:
                    next_dir = DOWN
                if e.key in (pygame.K_LEFT, pygame.K_a) and direction != RIGHT:
                    next_dir = LEFT
                if e.key in (pygame.K_RIGHT, pygame.K_d) and direction != LEFT:
                    next_dir = RIGHT

        if not game_over:
            move_timer += 1
            speed = SPEEDS[min(level - 1, len(SPEEDS) - 1)]

            if move_timer >= 60 // speed:
                move_timer = 0
                direction  = next_dir

                
                hx, hy   = snake[0]
                new_head = (hx + direction[0], hy + direction[1])

             
                if new_head[0] <= 0 or new_head[0] >= COLS - 1 or \
                   new_head[1] <= 0 or new_head[1] >= ROWS - 1:
                    game_over = True

              
                elif new_head in snake:
                    game_over = True

                else:
                    snake.insert(0, new_head)

                    if new_head == food:
                   
                        score       += 10 * level
                        foods_eaten += 1
                        food         = new_food(snake)

                        
                        if foods_eaten >= FOODS_FOR_LEVEL:
                            level       += 1
                            foods_eaten  = 0
                    else:
                        snake.pop()  

       
        screen.fill(BG)
        draw_grid()
        draw_walls()
        draw_food(food)
        draw_snake(snake)
        draw_hud(score, level)

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            t = font_big.render("", True, RED)
            screen.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 70))
            s = font_med.render(f"SCORE: {score}  DENGEI: {level}", True, YELLOW)
            screen.blit(s, (WIDTH // 2 - s.get_width() // 2, HEIGHT // 2 + 10))
            s2 = font.render("space — kaittan", True, WHITE)
            screen.blit(s2, (WIDTH // 2 - s2.get_width() // 2, HEIGHT // 2 + 55))

        pygame.display.update()


main()