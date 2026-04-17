import pygame
import math
import datetime

class MickeysClock:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.cx = width // 2
        self.cy = height // 2
        self.width = width
        self.height = height
        self.hand_img = pygame.image.load("/Users/medinameirambek/Desktop/meow/practice9/mickey\'s_clock/miki_hand.png").convert_alpha()
        self.hand_img = pygame.transform.scale(self.hand_img, (100, 180))
        self.face_img = pygame.image.load("/Users/medinameirambek/Desktop/meow/practice9/mickey\'s_clock/images.png").convert_alpha()
        self.face_img = pygame.transform.scale(self.face_img, (240, 240)) 

    def get_angle(self, value, max_value):
        return (value / max_value) * 360

    def draw_rotated_hand(self, image, angle_deg):
        rotated = pygame.transform.rotate(image, -angle_deg)
        rect = rotated.get_rect(center=(self.cx, self.cy))
        self.screen.blit(rotated, rect)

    def draw_clock_face(self):
        pygame.draw.circle(self.screen, (50, 50, 50), (self.cx, self.cy), 190, 4)
        pygame.draw.circle(self.screen, (255, 255, 255), (self.cx, self.cy), 186)  

        rect = self.face_img.get_rect(center=(self.cx, self.cy))
        self.screen.blit(self.face_img, rect)


        for i in range(60):
            angle = math.radians(i * 6 - 90)
            if i % 5 == 0:
                inner_r = 160
                outer_r = 180
                width = 3
                color = (30, 30, 30)
            else:
                inner_r = 170
                outer_r = 180
                width = 1
                color = (150, 150, 150)

            x1 = int(self.cx + inner_r * math.cos(angle))
            y1 = int(self.cy + inner_r * math.sin(angle))
            x2 = int(self.cx + outer_r * math.cos(angle))
            y2 = int(self.cy + outer_r * math.sin(angle))
            pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), width)

        pygame.draw.circle(self.screen, (20, 20, 20), (self.cx, self.cy), 8)

    def draw(self):
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        min_angle = self.get_angle(minutes, 60)
        sec_angle = self.get_angle(seconds, 60)

        self.draw_clock_face()
        self.draw_rotated_hand(self.hand_img, min_angle)

        sec_hand = pygame.transform.flip(self.hand_img, True, False)
        self.draw_rotated_hand(sec_hand, sec_angle)

        pygame.draw.circle(self.screen, (20, 20, 20), (self.cx, self.cy), 8) 