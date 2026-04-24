import pygame

class Ball:
    def __init__(self, screen_width, screen_height):
        self.radius = 25
        self.default_color = (255, 0, 0)
        self.wall_color = (0, 255, 0)
        self.color = self.default_color
        self.step = 20
        self.screen_w = screen_width
        self.screen_h = screen_height
        self.x = screen_width // 2
        self.y = screen_height // 2

    def move(self, direction):
        if direction == "UP":
            self.y -= self.step
        elif direction == "DOWN":
            self.y += self.step
        elif direction == "LEFT":
            self.x -= self.step
        elif direction == "RIGHT":
            self.x += self.step

        #айналып журед
        if self.x > self.screen_w + self.radius:
            self.x = -self.radius
        elif self.x < -self.radius:
            self.x = self.screen_w + self.radius

        if self.y > self.screen_h + self.radius:
            self.y = -self.radius
        elif self.y < -self.radius:
            self.y = self.screen_h + self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)