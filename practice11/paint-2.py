import pygame
import sys
import math

pygame.init()


WIDTH  = 900   # Extended width to fit extra tool buttons
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()


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

font = pygame.font.SysFont("Arial", 15, bold=True)


current_color = BLACK
brush_size    = 8


tool = "pencil"

drawing   = False
start_pos = None   
preview   = None   




def draw_equilateral_triangle(surface, color, start, end, line_w):
    
    x1, y1 = start
    x2, y2 = end
    # Base of the triangle: bottom edge of the bounding box
    bx1, by1 = min(x1, x2), max(y1, y2)
    bx2, by2 = max(x1, x2), max(y1, y2)
    base_len = bx2 - bx1
    if base_len == 0:
        return
    
    tri_h = base_len * math.sqrt(3) / 2
    
    apex = ((bx1 + bx2) // 2, int(max(y1, y2) - tri_h))
    pts = [(bx1, by1), (bx2, by2), apex]
    pygame.draw.polygon(surface, color, pts, line_w)


def draw_right_triangle(surface, color, start, end, line_w):
    
    x1, y1 = start
    x2, y2 = end
    left   = min(x1, x2)
    right  = max(x1, x2)
    top    = min(y1, y2)
    bottom = max(y1, y2)
    pts = [
        (left, top),      # Right angle here
        (left, bottom),   # Bottom-left
        (right, bottom),  # Bottom-right
    ]
    pygame.draw.polygon(surface, color, pts, line_w)


def draw_square(surface, color, start, end, line_w):
    
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2 - x1), abs(y2 - y1))
    # Keep direction of the drag
    sx = x1 if x2 >= x1 else x1 - side
    sy = y1 if y2 >= y1 else y1 - side
    pygame.draw.rect(surface, color, (sx, sy, side, side), line_w)


def draw_rhombus(surface, color, start, end, line_w):
    
    x1, y1 = start
    x2, y2 = end
    left   = min(x1, x2)
    right  = max(x1, x2)
    top    = min(y1, y2)
    bottom = max(y1, y2)
    mid_x  = (left + right) // 2
    mid_y  = (top + bottom) // 2
    pts = [
        (mid_x, top),     # Top vertex
        (right, mid_y),   # Right vertex
        (mid_x, bottom),  # Bottom vertex
        (left, mid_y),    # Left vertex
    ]
    pygame.draw.polygon(surface, color, pts, line_w)


def apply_shape(surface, tool_name, start, end, color, line_w):
    
    if tool_name == "line":
        pygame.draw.line(surface, color, start, end, max(1, line_w))
    elif tool_name == "rect":
        x = min(start[0], end[0])
        y = min(start[1], end[1])
        w = abs(end[0] - start[0])
        h = abs(end[1] - start[1])
        pygame.draw.rect(surface, color, (x, y, w, h), line_w)
    elif tool_name == "circle":
        cx = (start[0] + end[0]) // 2
        cy = (start[1] + end[1]) // 2
        r  = int(((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5 // 2)
        if r > 0:
            pygame.draw.circle(surface, color, (cx, cy), r, line_w)
    elif tool_name == "square":
        draw_square(surface, color, start, end, line_w)
    elif tool_name == "right_tri":
        draw_right_triangle(surface, color, start, end, line_w)
    elif tool_name == "equi_tri":
        draw_equilateral_triangle(surface, color, start, end, line_w)
    elif tool_name == "rhombus":
        draw_rhombus(surface, color, start, end, line_w)




# менюшка
TOOL_ROW1 = [
    ("pencil",   "Pencil"),
    ("line",     "Line"),
    ("rect",     "Rect"),
    ("circle",   "Circle"),
    ("eraser",   "Eraser"),
]
TOOL_ROW2 = [
    ("square",   "Square"),
    ("right_tri","R.Tri"),
    ("equi_tri", "E.Tri"),
    ("rhombus",  "Rhombus"),
]


def draw_ui():
    
    # --- Toolbar background ---
    pygame.draw.rect(screen, GREY, (0, HEIGHT - 80, WIDTH, 80))
    pygame.draw.line(screen, BLACK, (0, HEIGHT - 80), (WIDTH, HEIGHT - 80), 2)

   
    colors = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE]
    for i, c in enumerate(colors):
        x = 10 + i * 40
        y = HEIGHT - 72
        pygame.draw.rect(screen, c, (x, y, 30, 30))
        pygame.draw.rect(screen, BLACK, (x, y, 30, 30), 2)
        
        if c == current_color:
            pygame.draw.rect(screen, (255, 205, 0), (x - 3, y - 3, 36, 36), 3)

    
    BTN_W1 = 62
    for i, (t, label) in enumerate(TOOL_ROW1):
        x = 340 + i * (BTN_W1 + 2)
        y = HEIGHT - 76
        color = (100, 200, 100) if tool == t else (220, 220, 220)
        pygame.draw.rect(screen, color, (x, y, BTN_W1, 26), border_radius=4)
        pygame.draw.rect(screen, BLACK,  (x, y, BTN_W1, 26), 2, border_radius=4)
        txt = font.render(label, True, BLACK)
        screen.blit(txt, (x + BTN_W1 // 2 - txt.get_width() // 2, y + 5))

    BTN_W2 = 68
    for i, (t, label) in enumerate(TOOL_ROW2):
        x = 340 + i * (BTN_W2 + 2)
        y = HEIGHT - 46
        color = (100, 200, 100) if tool == t else (220, 220, 220)
        pygame.draw.rect(screen, color, (x, y, BTN_W2, 26), border_radius=4)
        pygame.draw.rect(screen, BLACK,  (x, y, BTN_W2, 26), 2, border_radius=4)
        txt = font.render(label, True, BLACK)
        screen.blit(txt, (x + BTN_W2 // 2 - txt.get_width() // 2, y + 5))


    txt = font.render(f"Size: {brush_size}", True, BLACK)
    screen.blit(txt, (10, HEIGHT - 30))
    txt2 = font.render("↑/↓", True, BLACK)
    screen.blit(txt2, (90, HEIGHT - 30))

    active_label = next((l for t, l in TOOL_ROW1 + TOOL_ROW2 if t == tool), tool)
    txt3 = font.render(f"Tool: {active_label}", True, (50, 50, 150))
    screen.blit(txt3, (10, HEIGHT - 50))


def on_canvas(my):
    return my < HEIGHT - 80


def check_tool_click(mx, my):
    BTN_W1 = 62
    for i, (t, _) in enumerate(TOOL_ROW1):
        x = 340 + i * (BTN_W1 + 2)
        y = HEIGHT - 76
        if x <= mx <= x + BTN_W1 and y <= my <= y + 26:
            return t
    BTN_W2 = 68
    for i, (t, _) in enumerate(TOOL_ROW2):
        x = 340 + i * (BTN_W2 + 2)
        y = HEIGHT - 46
        if x <= mx <= x + BTN_W2 and y <= my <= y + 26:
            return t
    return None



def is_shape_tool(t):
    return t in ("line", "rect", "circle", "square", "right_tri", "equi_tri", "rhombus")


#лупик

while True:
    clock.tick(60)
    mx, my = pygame.mouse.get_pos()
    in_canvas = on_canvas(my)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_c:
                canvas.fill(WHITE)    # Clear canvas
            if event.key == pygame.K_UP:
                brush_size = min(brush_size + 2, 50)
            if event.key == pygame.K_DOWN:
                brush_size = max(brush_size - 2, 2)

       
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not in_canvas:
                
                colors = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE]
                for i, c in enumerate(colors):
                    x = 10 + i * 40
                    y = HEIGHT - 72
                    if x <= mx <= x + 30 and y <= my <= y + 30:
                        current_color = c

               
                clicked_tool = check_tool_click(mx, my)
                if clicked_tool:
                    tool = clicked_tool

            else:
       
                if is_shape_tool(tool):
                
                    drawing   = True
                    start_pos = (mx, my)
                    preview   = canvas.copy()
                elif tool == "pencil":
                    drawing = True
                    pygame.draw.circle(canvas, current_color, (mx, my), brush_size)
                elif tool == "eraser":
                    drawing = True
                    pygame.draw.circle(canvas, WHITE, (mx, my), brush_size * 2)

        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == "pencil" and in_canvas:
             
                pygame.draw.circle(canvas, current_color, (mx, my), brush_size)
            elif tool == "eraser" and in_canvas:
                
                pygame.draw.circle(canvas, WHITE, (mx, my), brush_size * 2)
           

        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if is_shape_tool(tool) and start_pos and drawing:
                # Restore clean snapshot, then draw the final shape exactly once
                canvas.blit(preview, (0, 0))
                apply_shape(canvas, tool, start_pos, (mx, my), current_color, brush_size)
       
            drawing   = False
            start_pos = None
            preview   = None


    screen.blit(canvas, (0, 0))

   
   
    if drawing and is_shape_tool(tool) and start_pos and preview:
        preview_surf = preview.copy()
        apply_shape(preview_surf, tool, start_pos, (mx, my), current_color, brush_size)
        screen.blit(preview_surf, (0, 0))


    if tool == "eraser" and in_canvas:
        pygame.draw.circle(screen, GREY, (mx, my), brush_size * 2, 2)

    draw_ui()
    pygame.display.update()
