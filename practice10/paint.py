import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

# цвета
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 0, 160)
GREY   = (180, 180, 180)


canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

font = pygame.font.SysFont("Arial", 18, bold=True)


current_color = BLACK
brush_size = 8
tool = "pencil"  # pencil / rect / circle / eraser

drawing = False
start_pos = None  
preview = None    





def draw_ui():

    pygame.draw.rect(screen, GREY, (0, HEIGHT - 60, WIDTH, 60))
    pygame.draw.line(screen, BLACK, (0, HEIGHT - 60), (WIDTH, HEIGHT - 60), 2)

 
    colors = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE]
    for i, c in enumerate(colors):
        x = 10 + i * 45
        y = HEIGHT - 45
        pygame.draw.rect(screen, c, (x, y, 35, 35))
        pygame.draw.rect(screen, BLACK, (x, y, 35, 35), 2)
        if c == current_color:
            pygame.draw.rect(screen, (255, 215, 0), (x - 3, y - 3, 41, 41), 3)


    tools = [("pencil", "Карандаш"), ("rect", "Прямоуг"), ("circle", "Круг"),
             ("eraser", "Ластик")]
    for i, (t, label) in enumerate(tools):
        x = 390 + i * 85
        y = HEIGHT - 50
        color = (100, 200, 100) if tool == t else (220, 220, 220)
        pygame.draw.rect(screen, color, (x, y, 80, 30), border_radius=5)
        pygame.draw.rect(screen, BLACK, (x, y, 80, 30), 2, border_radius=5)
        txt = font.render(label, True, BLACK)
        screen.blit(txt, (x + 40 - txt.get_width() // 2, y + 7))

    
    txt = font.render(f"Размер: {brush_size}", True, BLACK)
    screen.blit(txt, (10, HEIGHT - 58))
    txt2 = font.render("↑↓", True, BLACK)
    screen.blit(txt2, (120, HEIGHT - 58))


while True:
    clock.tick(60)
    mx, my = pygame.mouse.get_pos()
    on_canvas = my < HEIGHT - 60

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_c:
                canvas.fill(WHITE)
            if event.key == pygame.K_UP:
                brush_size = min(brush_size + 2, 50)
            if event.key == pygame.K_DOWN:
                brush_size = max(brush_size - 2, 2)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # клик по панели инструментов
            if not on_canvas:
                # палитра
                colors = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE]
                for i, c in enumerate(colors):
                    x = 10 + i * 45
                    y = HEIGHT - 45
                    if x <= mx <= x + 35 and y <= my <= y + 35:
                        current_color = c

                # инструменты
                tools_list = ["pencil", "rect", "circle", "eraser"]
                for i, t in enumerate(tools_list):
                    x = 390 + i * 85
                    y = HEIGHT - 50
                    if x <= mx <= x + 80 and y <= my <= y + 30:
                        tool = t

            else:
           
                
                if tool in ("rect", "circle"):
                    drawing = True
                    start_pos = (mx, my)
                    preview = canvas.copy()
                elif tool in ("pencil", "eraser"):
                    drawing = True
                    c = WHITE if tool == "eraser" else current_color
                    pygame.draw.circle(canvas, c, (mx, my), brush_size)

        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == "pencil" and on_canvas:
                pygame.draw.circle(canvas, current_color, (mx, my), brush_size)
            elif tool == "eraser" and on_canvas:
                pygame.draw.circle(canvas, WHITE, (mx, my), brush_size * 2)
            elif tool in ("rect", "circle") and start_pos:
              
                canvas.blit(preview, (0, 0))
                if tool == "rect":
                    x = min(start_pos[0], mx)
                    y = min(start_pos[1], my)
                    w = abs(mx - start_pos[0])
                    h = abs(my - start_pos[1])
                    pygame.draw.rect(canvas, current_color, (x, y, w, h), brush_size)
                elif tool == "circle":
                    cx = (start_pos[0] + mx) // 2
                    cy = (start_pos[1] + my) // 2
                    r = int(((mx - start_pos[0])**2 + (my - start_pos[1])**2)**0.5 // 2)
                    if r > 0:
                        pygame.draw.circle(canvas, current_color, (cx, cy), r, brush_size)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if tool in ("rect", "circle") and start_pos and drawing:
               
                canvas.blit(preview, (0, 0))
                if tool == "rect":
                    x = min(start_pos[0], mx)
                    y = min(start_pos[1], my)
                    w = abs(mx - start_pos[0])
                    h = abs(my - start_pos[1])
                    pygame.draw.rect(canvas, current_color, (x, y, w, h), brush_size)
                elif tool == "circle":
                    cx = (start_pos[0] + mx) // 2
                    cy = (start_pos[1] + my) // 2
                    r = int(((mx - start_pos[0])**2 + (my - start_pos[1])**2)**0.5 // 2)
                    if r > 0:
                        pygame.draw.circle(canvas, current_color, (cx, cy), r, brush_size)
            drawing = False
            start_pos = None
            preview = None


    screen.blit(canvas, (0, 0))

  
    if tool == "eraser" and on_canvas:
        pygame.draw.circle(screen, GREY, (mx, my), brush_size * 2, 2)

    draw_ui()
    pygame.display.update()