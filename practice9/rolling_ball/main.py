import pygame
import sys
from sharik import Ball

WIDTH, HEIGHT = 600, 400
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")
clock = pygame.time.Clock()

ball = Ball(WIDTH, HEIGHT)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move("UP")
            elif event.key == pygame.K_DOWN:
                ball.move("DOWN")
            elif event.key == pygame.K_LEFT:
                ball.move("LEFT")
            elif event.key == pygame.K_RIGHT:
                ball.move("RIGHT")

    screen.fill((255, 255, 255))  
    ball.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)