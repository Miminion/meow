import pygame

from persistence import load_leaderboard, load_settings, save_settings
from racer import oyyn, ENI, BIK
from ui import Button, draw_center_text, draw_text, BLACK, WHITE, BLUE, GRAY, GREEN, RED


pygame.init()

screen = pygame.display.set_mode((ENI, BIK))
pygame.display.set_caption("TSIS3 Racer")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 22)
big_font = pygame.font.SysFont("Verdana", 42)
small_font = pygame.font.SysFont("Verdana", 18)

settings = load_settings()


def ask_username():
    name = ""

    while True:
        screen.fill(WHITE)

        draw_center_text(screen, "Enter your name", big_font, BLACK, 210)
        draw_center_text(screen, name + "|", font, BLUE, 290)
        draw_center_text(screen, "Press ENTER to start", small_font, GRAY, 350)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip() == "":
                        name = "Player"
                    return name

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                elif event.key == pygame.K_ESCAPE:
                    return None

                else:
                    if len(name) < 12:
                        name += event.unicode

        pygame.display.flip()
        clock.tick(60)


def main_menu():
    play_btn = Button(170, 210, 160, 50, "Play")
    leader_btn = Button(170, 280, 160, 50, "Leaderboard")
    settings_btn = Button(170, 350, 160, 50, "Settings")
    quit_btn = Button(170, 420, 160, 50, "Quit")

    while True:
        screen.fill(WHITE)

        draw_center_text(screen, "TSIS3 RACER", big_font, BLACK, 120)

        play_btn.draw(screen, font)
        leader_btn.draw(screen, font)
        settings_btn.draw(screen, font)
        quit_btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if play_btn.clicked(event):
                return "play"

            if leader_btn.clicked(event):
                return "leaderboard"

            if settings_btn.clicked(event):
                return "settings"

            if quit_btn.clicked(event):
                return "quit"

        pygame.display.flip()
        clock.tick(60)


def leaderboard_screen():
    back_btn = Button(170, 610, 160, 45, "Back")

    while True:
        screen.fill(WHITE)

        draw_center_text(screen, "Leaderboard TOP 10", big_font, BLACK, 70)

        scores = load_leaderboard()

        if not scores:
            draw_center_text(screen, "No scores yet", font, GRAY, 220)

        y = 135
        for index, item in enumerate(scores[:10], start=1):
            text = f"{index}. {item['name']} | Score: {item['score']} | Distance: {item['distance']}m"
            draw_text(screen, text, small_font, BLACK, 50, y)
            y += 36

        back_btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if back_btn.clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def settings_screen():
    sound_btn = Button(120, 170, 260, 45, "")
    color_btn = Button(120, 240, 260, 45, "")
    difficulty_btn = Button(120, 310, 260, 45, "")
    back_btn = Button(120, 420, 260, 45, "Back")

    colors = ["blue", "red", "green", "yellow"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill(WHITE)

        draw_center_text(screen, "Settings", big_font, BLACK, 90)

        sound_btn.text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        color_btn.text = f"Car color: {settings['car_color']}"
        difficulty_btn.text = f"Difficulty: {settings['difficulty']}"

        sound_btn.draw(screen, font)
        color_btn.draw(screen, font)
        difficulty_btn.draw(screen, font)
        back_btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if sound_btn.clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            if color_btn.clicked(event):
                index = colors.index(settings["car_color"])
                settings["car_color"] = colors[(index + 1) % len(colors)]
                save_settings(settings)

            if difficulty_btn.clicked(event):
                index = difficulties.index(settings["difficulty"])
                settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
                save_settings(settings)

            if back_btn.clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(result):
    retry_btn = Button(110, 470, 130, 45, "Retry")
    menu_btn = Button(260, 470, 160, 45, "Main Menu")

    while True:
        screen.fill(WHITE)

        title = "FINISH!" if result.get("won") else "GAME OVER"
        color = GREEN if result.get("won") else RED

        draw_center_text(screen, title, big_font, color, 150)
        draw_center_text(screen, f"Score: {result['score']}", font, BLACK, 230)
        draw_center_text(screen, f"Distance: {result['distance']}m", font, BLACK, 280)
        draw_center_text(screen, f"Coins: {result['coins']}", font, BLACK, 330)

        retry_btn.draw(screen, font)
        menu_btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if retry_btn.clicked(event):
                return "retry"

            if menu_btn.clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def main():
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
                state, result = oyyn(screen, username, settings)

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