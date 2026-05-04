import pygame
import datetime
from pathlib import Path

from tools import (
    calculate_rect,
    calculate_square,
    draw_rhombus,
    draw_right_triangle,
    draw_equilateral_triangle,
    draw_circle_by_points,
    flood_fill,
)

pygame.init()

W, H, FPS = 800, 600, 60
BG = (255, 255, 255)

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("TSIS2 Paint")
clock = pygame.time.Clock()

f_ui    = pygame.font.SysFont("Verdana", 20)
f_small = pygame.font.SysFont("Verdana", 16)
f_text  = pygame.font.SysFont("Verdana", 28)

COLORS = {
    pygame.K_0: ((0,   0,   0),   "BLACK"),
    pygame.K_1: ((255, 0,   0),   "RED"),
    pygame.K_2: ((0,   180, 0),   "GREEN"),
    pygame.K_3: ((0,   0,   255), "BLUE"),
    pygame.K_4: ((255, 255, 0),   "YELLOW"),
    pygame.K_5: ((255, 165, 0),   "ORANGE"),
    pygame.K_6: ((128, 0,   128), "PURPLE"),
    pygame.K_7: ((255, 105, 180), "PINK"),
    pygame.K_8: ((139, 69,  19),  "BROWN"),
    pygame.K_9: ((160, 160, 160), "GRAY"),
}

SHAPE_TOOLS = ("line", "rect", "circle", "square", "rhombus", "equilateral_triangle", "right_triangle")

tool       = "pen"
color      = (0, 0, 0)
color_name = "BLACK"
thick      = 5
drawing    = False
p0 = p1 = p_prev = None

typing    = False
txt_input = ""
txt_pos   = None

canvas = pygame.Surface((W, H))
canvas.fill(BG)


def draw_color():
    return BG if tool == "eraser" else color


def save():
    d = Path("assets")
    d.mkdir(exist_ok=True)
    name = d / f"canvas_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    pygame.image.save(canvas, name)
    print(f"Saved: {name}")


def draw_ui():
    panel = pygame.Rect(W - 250, 10, 235, 150)
    pygame.draw.rect(screen, (235, 235, 235), panel)
    pygame.draw.rect(screen, (0, 0, 0), panel, 2)
    screen.blit(f_ui.render(f"Tool: {tool.upper()}", True, (0, 0, 0)),  (W - 235, 20))
    screen.blit(f_ui.render(f"Brush: {thick}px",     True, (0, 0, 0)),  (W - 235, 50))
    screen.blit(f_ui.render(f"Color: {color_name}",  True, (0, 0, 0)),  (W - 235, 80))
    pygame.draw.rect(screen, (160, 160, 160), pygame.Rect(W - 75, 78, 40, 40))
    pygame.draw.rect(screen, color,           pygame.Rect(W - 70, 83, 30, 30))
    screen.blit(f_small.render("W/L/R/C/E/S/T/F/D/B/X  ↑↓size", True, (0, 0, 0)), (W - 235, 120))

def finalize():
    c = draw_color()
    if tool == "line"                   and p0 and p1: pygame.draw.line(canvas, c, p0, p1, thick)
    elif tool == "rect"                 and p0 and p1: pygame.draw.rect(canvas, c, calculate_rect(p0, p1), thick)
    elif tool == "square"               and p0 and p1: pygame.draw.rect(canvas, c, calculate_square(p0, p1), thick)
    elif tool == "circle"               and p0 and p1: draw_circle_by_points(canvas, c, p0, p1, thick)
    elif tool == "right_triangle"       and p0 and p1: draw_right_triangle(canvas, c, p0, p1, thick)
    elif tool == "equilateral_triangle" and p0 and p1: draw_equilateral_triangle(canvas, c, p0, p1, thick)
    elif tool == "rhombus"              and p0 and p1: draw_rhombus(canvas, c, p0, p1, thick)


def preview():
    c = draw_color()
    if tool == "line":                   pygame.draw.line(screen, c, p0, p1, thick)
    elif tool == "rect":                 pygame.draw.rect(screen, c, calculate_rect(p0, p1), thick)
    elif tool == "circle":               draw_circle_by_points(screen, c, p0, p1, thick)
    elif tool == "square":               pygame.draw.rect(screen, c, calculate_square(p0, p1), thick)
    elif tool == "right_triangle":       draw_right_triangle(screen, c, p0, p1, thick)
    elif tool == "equilateral_triangle": draw_equilateral_triangle(screen, c, p0, p1, thick)
    elif tool == "rhombus":              draw_rhombus(screen, c, p0, p1, thick)


running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        elif e.type == pygame.KEYDOWN:
            if typing:
                if   e.key == pygame.K_RETURN:
                    canvas.blit(f_text.render(txt_input, True, color), txt_pos)
                    typing, txt_input, txt_pos = False, "", None
                elif e.key == pygame.K_ESCAPE:
                    typing, txt_input, txt_pos = False, "", None
                elif e.key == pygame.K_BACKSPACE:
                    txt_input = txt_input[:-1]
                else:
                    txt_input += e.unicode
            else:
                if e.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save()
                elif e.key == pygame.K_w: tool = "pen"
                elif e.key == pygame.K_l: tool = "line"
                elif e.key == pygame.K_r: tool = "rect"
                elif e.key == pygame.K_c: tool = "circle"
                elif e.key == pygame.K_e: tool = "eraser"
                elif e.key == pygame.K_s: tool = "square"
                elif e.key == pygame.K_t: tool = "right_triangle"
                elif e.key == pygame.K_f: tool = "equilateral_triangle"
                elif e.key == pygame.K_d: tool = "rhombus"
                elif e.key == pygame.K_b: tool = "fill"
                elif e.key == pygame.K_x: tool = "text"
                elif e.key == pygame.K_UP:   thick = min(thick + 1, 50)
                elif e.key == pygame.K_DOWN: thick = max(thick - 1, 1)
                elif e.key == pygame.K_SPACE: canvas.fill(BG)
                elif e.key in COLORS:
                    color, color_name = COLORS[e.key]

        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if tool == "fill":
                flood_fill(canvas, e.pos, color)
            elif tool == "text":
                typing, txt_input, txt_pos = True, "", e.pos
            else:
                drawing = True
                p0 = p_prev = p1 = e.pos
                if tool in ("pen", "eraser"):
                    pygame.draw.circle(canvas, draw_color(), e.pos, max(1, thick // 2))

        elif e.type == pygame.MOUSEMOTION and drawing:
            p1 = e.pos
            if tool in ("pen", "eraser"):
                pygame.draw.line(canvas, draw_color(), p_prev, p1, thick)
                p_prev = p1

        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and drawing:
            p1 = e.pos
            if tool in SHAPE_TOOLS:
                finalize()
            drawing = False
            p0 = p1 = p_prev = None

    screen.blit(canvas, (0, 0))

    if drawing and tool in SHAPE_TOOLS and p0 and p1:
        preview()

    if typing and txt_pos:
        screen.blit(f_text.render(txt_input, True, color), txt_pos)

    draw_ui()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()