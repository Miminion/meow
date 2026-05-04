import math
import pygame


def calculate_rect(start, end):
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    return pygame.Rect(left, top, width, height)


def calculate_square(start, end):
    x1, y1 = start
    x2, y2 = end

    size = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        left = x1 - size
    else:
        left = x1

    if y2 < y1:
        top = y1 - size
    else:
        top = y1

    return pygame.Rect(left, top, size, size)


def draw_rhombus(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end

    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    half_width = abs(x2 - x1) // 2
    half_height = abs(y2 - y1) // 2

    points = [
        (center_x, center_y - half_height),
        (center_x + half_width, center_y),
        (center_x, center_y + half_height),
        (center_x - half_width, center_y)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_right_triangle(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end

    points = [
        (x1, y1),
        (x2, y1),
        (x1, y2)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_equilateral_triangle(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end

    side = abs(x2 - x1)
    height = int(side * math.sqrt(3) / 2)

    if y2 < y1:
        height = -height

    points = [
        (x1, y1),
        (x1 - side // 2, y1 + height),
        (x1 + side // 2, y1 + height)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_circle_by_points(surface, color, start, end, width=0):
    cx, cy = start
    ex, ey = end

    radius = int(math.hypot(ex - cx, ey - cy))

    if radius > 0:
        pygame.draw.circle(surface, color, (cx, cy), radius, width)


def flood_fill(surface, start_pos, fill_color):
    width, height = surface.get_size()
    x, y = start_pos

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = surface.get_at((x, y))
    new_color = pygame.Color(fill_color)

    if target_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        px, py = stack.pop()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        stack.append((px + 1, py))
        stack.append((px - 1, py))
        stack.append((px, py + 1))
        stack.append((px, py - 1))