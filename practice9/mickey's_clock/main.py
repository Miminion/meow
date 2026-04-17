import pygame
import sys
from clock import MickeysClock

WIDTH, HEIGHT = 400, 400
FPS = 1 

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")
clock_obj = MickeysClock(screen, WIDTH, HEIGHT)
tick = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))
    clock_obj.draw()
    pygame.display.flip()
    tick.tick(FPS)