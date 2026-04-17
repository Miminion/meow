import pygame

class Ball:
    def __init__(self, screen_width, screen_height):
        self.radius = 25
        self.color = (255, 0, 0)        
        self.step = 20                  
        self.screen_w = screen_width
        self.screen_h = screen_height

       
        self.x = screen_width // 2
        self.y = screen_height // 2

    def move(self, direction):
      
        new_x, new_y = self.x, self.y

        if direction == "UP":
            new_y -= self.step
        elif direction == "DOWN":
            new_y += self.step
        elif direction == "LEFT":
            new_x -= self.step
        elif direction == "RIGHT":
            new_x += self.step

        
        if self.radius <= new_x <= self.screen_w - self.radius:
            self.x = new_x
        if self.radius <= new_y <= self.screen_h - self.radius:
            self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)