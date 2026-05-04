import pygame

from db import init_db, get_top_scores
from game import WIDTH, HEIGHT, load_settings, save_settings, run_game
from game import BLACK, WHITE, GRAY, RED, GREEN, BLUE


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 22)
big_font = pygame.font.SysFont("Verdana", 44)
small_font = pygame.font.SysFont("Verdana", 18)

settings = load_settings()


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, (220, 220, 220), self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        image = font.render(self.text, True, BLACK)
        screen.blit(image, image.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def center_text(text, font_obj, color, y):
    image = font_obj.render(text, True, color)
    rect = image.get_rect(center=(WIDTH // 2, y))
    screen.blit(image, rect)


def ask_username():
    username = ""

    while True:
        screen.fill(WHITE)

        center_text("Enter username", big_font, BLACK, 180)
        center_text(username + "|", font, BLUE, 270)
        center_text("Press ENTER to continue", small_font, GRAY, 330)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username.strip() == "":
                        username = "Player"
                    return username

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                elif event.key == pygame.K_ESCAPE:
                    return None

                else:
                    if len(username) < 14:
                        username += event.unicode

        pygame.display.flip()
        clock.tick(60)


def main_menu():
    play = Button(210, 210, 180, 50, "Play")
    leaderboard = Button(210, 280, 180, 50, "Leaderboard")
    settings_btn = Button(210, 350, 180, 50, "Settings")
    quit_btn = Button(210, 420, 180, 50, "Quit")

    while True:
        screen.fill(WHITE)
        center_text("TSIS4 SNAKE", big_font, BLACK, 120)

        for btn in [play, leaderboard, settings_btn, quit_btn]:
            btn.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if play.clicked(event):
                return "play"
            if leaderboard.clicked(event):
                return "leaderboard"
            if settings_btn.clicked(event):
                return "settings"
            if quit_btn.clicked(event):
                return "quit"

        pygame.display.flip()
        clock.tick(60)


def leaderboard_screen():
    back = Button(220, 530, 160, 45, "Back")

    while True:
        screen.fill(WHITE)

        center_text("Top 10 Scores", big_font, BLACK, 60)

        try:
            rows = get_top_scores()
        except Exception as error:
            rows = []
            center_text("Database error", font, RED, 230)
            center_text(str(error)[:55], small_font, RED, 270)

        y = 125
        for index, row in enumerate(rows, start=1):
            username, score, level, played_at = row
            text = f"{index}. {username} | Score: {score} | Level: {level} | {played_at.strftime('%Y-%m-%d')}"
            image = small_font.render(text, True, BLACK)
            screen.blit(image, (35, y))
            y += 34

        back.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if back.clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def settings_screen():
    global settings

    grid_btn = Button(170, 170, 260, 45, "")
    sound_btn = Button(170, 240, 260, 45, "")
    color_btn = Button(170, 310, 260, 45, "")
    save_btn = Button(170, 430, 260, 45, "Save & Back")

    colors = [
        [255, 0, 0],
        [0, 180, 0],
        [0, 0, 255],
        [160, 0, 200],
        [0, 0, 0]
    ]

    while True:
        screen.fill(WHITE)

        center_text("Settings", big_font, BLACK, 90)

        grid_btn.text = f"Grid: {'ON' if settings['grid'] else 'OFF'}"
        sound_btn.text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        color_btn.text = f"Snake color:"

        color_preview_rect = pygame.Rect(440, 310, 40, 40)
        pygame.draw.rect(screen, settings["snake_color"], color_preview_rect)
        pygame.draw.rect(screen, BLACK, color_preview_rect, 2)
        
        for btn in [grid_btn, sound_btn, color_btn, save_btn]:
            btn.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if grid_btn.clicked(event):
                settings["grid"] = not settings["grid"]

            if sound_btn.clicked(event):
                settings["sound"] = not settings["sound"]

            if color_btn.clicked(event):
                if settings["snake_color"] in colors:
                    index = colors.index(settings["snake_color"])
                else:
                    index = 0
                settings["snake_color"] = colors[(index + 1) % len(colors)]

            if save_btn.clicked(event):
                save_settings(settings)
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(result):
    retry = Button(135, 440, 140, 45, "Retry")
    menu = Button(310, 440, 160, 45, "Main Menu")

    while True:
        screen.fill(BLUE)

        center_text("GAME OVER", big_font, WHITE, 150)
        center_text(f"Score: {result['score']}", font, WHITE, 230)
        center_text(f"Level: {result['level']}", font, WHITE, 270)
        center_text(f"Personal Best: {result['best']}", font, WHITE, 310)

        retry.draw()
        menu.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if retry.clicked(event):
                return "retry"

            if menu.clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def main():
    try:
        init_db()
    except Exception as error:
        print("Database connection error:")
        print(error)

    while True:
        action = main_menu()

        if action == "quit":
            break

        elif action == "leaderboard":
            if leaderboard_screen() == "quit":
                break

        elif action == "settings":
            if settings_screen() == "quit":
                break

        elif action == "play":
            username = ask_username()

            if username is None:
                continue

            while True:
                state, result = run_game(screen, username, settings)

                if state == "quit":
                    pygame.quit()
                    return

                next_action = game_over_screen(result)

                if next_action == "retry":
                    continue

                if next_action == "quit":
                    pygame.quit()
                    return

                break

    pygame.quit()


if __name__ == "__main__":
    main()