import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
LIGHT_GRAY = (220, 220, 220)
BLUE = (40, 90, 220)
RED = (220, 40, 40)
GREEN = (0, 170, 70)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font):
        pygame.draw.rect(screen, LIGHT_GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        text_img = font.render(self.text, True, BLACK)
        text_rect = text_img.get_rect(center=self.rect.center)
        screen.blit(text_img, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_center_text(screen, text, font, color, y):
    image = font.render(text, True, color)
    rect = image.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(image, rect)


def draw_text(screen, text, font, color, x, y):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))