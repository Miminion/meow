import pygame
import sys
from player import MusicPlayer

WIDTH, HEIGHT = 500, 300
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("zaicev.net")

font_big = pygame.font.SysFont("Arial", 28)
font_small = pygame.font.SysFont("Arial", 18)

player = MusicPlayer()
player.load_music_folder("/Users/medinameirambek/Desktop/meow/practice9/music_player/music") 

clock = pygame.time.Clock()

def draw_text(text, font, color, y):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(surf, rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s: 
                player.stop()
            elif event.key == pygame.K_n: 
                player.next_track()
            elif event.key == pygame.K_b: 
                player.prev_track()
            elif event.key == pygame.K_q: 
                pygame.quit()
                sys.exit()

    screen.fill((30, 30, 30))  

    status = "▶ Playing" if player.is_playing else "⏹ Stopped"
    draw_text("Zaicev.net", font_big, (255, 215, 0), 60)
    draw_text(f"Track: {player.get_track_name()}", font_small, (255, 255, 255), 120)
    draw_text(f"Status: {status}", font_small, (0, 255, 100), 160)
    draw_text(f"Position: {player.get_position()}s", font_small, (200, 200, 200), 195)
    draw_text("P=Play  S=Stop  N=Next  B=Prev  Q=Quit", font_small, (150, 150, 150), 250)

    pygame.display.flip()
    clock.tick(30)