import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 700, 700
CELL = 25
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HyperSnake")

FONT_TITLE = pygame.font.SysFont("Arial", 64, bold=True)
FONT_SECTION = pygame.font.SysFont("Arial", 32, bold=True)
FONT_ITEM = pygame.font.SysFont("Arial", 26)
FONT_BTN = pygame.font.SysFont("Arial", 30, bold=True)
FONT_GAMEOVER = pygame.font.SysFont("Arial", 52, bold=True)
FONT_MED = pygame.font.SysFont("Arial", 28)
FONT_SCORE = pygame.font.SysFont("Arial", 32, bold=True)

# Цвета
snake_colors = {
    "Red": (255, 70, 70),
    "Orange": (255, 150, 60),
    "Yellow": (255, 225, 80),
    "Green": (57, 255, 20),
    "Cyan": (0, 255, 255),
    "Blue": (0, 120, 255),
    "Purple": (180, 90, 255),
    "Pink": (255, 100, 200),
    "White": (240, 240, 240)
}

difficulties = {
    "Easy": 5,
    "Normal": 7,
    "Hard": 15
}

chosen_color = list(snake_colors.values())[0]
chosen_speed = list(difficulties.values())[1]


def draw_rounded_rect(surface, color, rect, radius=12):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_menu(selected_color, selected_speed):
    screen.fill((14, 14, 18))

    # Заголовок
    title = FONT_TITLE.render("HyperSnake", True, (240, 240, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    # Карточка цветов
    color_card = pygame.Rect(60, 150, 580, 180)
    section_title = FONT_SECTION.render("Snake Color", True, (230, 230, 230))
    screen.blit(section_title, (color_card.x + 20, color_card.y + 10))

    # Сетка 3 на 4
    cols = 4
    rows = 3
    cell_w = 140
    cell_h = 50

    start_x = color_card.x + 40
    start_y = color_card.y + 60

    items = list(snake_colors.items())

    for i, (name, col) in enumerate(items):
        col_i = i // rows
        row_i = i % rows

        x = start_x + col_i * cell_w
        y = start_y + row_i * cell_h

        box = pygame.Rect(x, y, 35, 35)
        pygame.draw.rect(screen, col, box, border_radius=8)

        label = FONT_ITEM.render(name, True, (230, 230, 230))
        screen.blit(label, (x + 45, y + 5))

        if col == selected_color:
            pygame.draw.rect(screen, (255, 255, 255), box, 3, border_radius=8)

    # Карточка сложности
    diff_card = pygame.Rect(60, 360, 580, 180)
    section_title = FONT_SECTION.render("Difficulty", True, (230, 230, 230))
    screen.blit(section_title, (diff_card.x + 20, diff_card.y + 10))

    y_offset = diff_card.y + 70
    x_offset = diff_card.x + 40

    for name, spd in difficulties.items():
        label = FONT_ITEM.render(name, True, (230, 230, 230))
        screen.blit(label, (x_offset, y_offset))

        if spd == selected_speed:
            underline = pygame.Rect(x_offset, y_offset + 28, label.get_width(), 3)
            pygame.draw.rect(screen, (255, 255, 255), underline)

        y_offset += 45

    # Кнопка Start
    start_rect = pygame.Rect(WIDTH // 2 - 120, 580, 240, 65)
    draw_rounded_rect(screen, (70, 145, 255), start_rect, 20)
    start_txt = FONT_BTN.render("START", True, (255, 255, 255))
    screen.blit(start_txt, (start_rect.x + 70, start_rect.y + 14))

    return start_rect


# Игровой цикл
def game_loop(snake_color, speed):
    clock = pygame.time.Clock()

    snake = [(WIDTH // 2, HEIGHT // 2)]
    dx, dy = CELL, 0
    food = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))

    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # Управление
                if not game_over:
                    if event.key == pygame.K_UP and dy == 0:
                        dx, dy = 0, -CELL
                    elif event.key == pygame.K_DOWN and dy == 0:
                        dx, dy = 0, CELL
                    elif event.key == pygame.K_LEFT and dx == 0:
                        dx, dy = -CELL, 0
                    elif event.key == pygame.K_RIGHT and dx == 0:
                        dx, dy = CELL, 0

                # Рестарт по R
                if game_over and event.key == pygame.K_r:
                    return

        if not game_over:
            x, y = snake[0]
            new_head = (x + dx, y + dy)

            # Столкновение
            if (
                new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in snake
            ):
                game_over = True

            snake.insert(0, new_head)

            # Еда
            if new_head == food:
                score += 1
                food = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
            else:
                snake.pop()

        # Рендер
        screen.fill((20, 20, 28))

        # Еда
        pygame.draw.rect(screen, (255, 70, 70), (*food, CELL, CELL), border_radius=6)

        # Змейка
        for x, y in snake:
            pygame.draw.rect(screen, snake_color, (x, y, CELL, CELL), border_radius=6)

        # Счёт
        score_txt = FONT_SCORE.render(f"Score: {score}", True, (240, 240, 240))
        screen.blit(score_txt, (20, 20))

        # Game Over
        if game_over:
            txt = FONT_GAMEOVER.render("GAME OVER", True, (255, 100, 100))
            screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 70))

            restart_txt = FONT_MED.render("Press R to Restart", True, (235, 235, 235))
            screen.blit(restart_txt, (WIDTH // 2 - restart_txt.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(speed)


# Главное меню
def main():
    global chosen_color, chosen_speed
    while True:
        start_button = draw_menu(chosen_color, chosen_speed)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Нажатие мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # START
                if start_button.collidepoint(mx, my):
                    game_loop(chosen_color, chosen_speed)

                # Выбор цвета
                cols = 4
                rows = 3
                cell_w = 140
                cell_h = 50
                start_x = 60 + 40
                start_y = 150 + 60

                items = list(snake_colors.items())

                for i, (name, col) in enumerate(items):
                    col_i = i // rows
                    row_i = i % rows

                    x = start_x + col_i * cell_w
                    y = start_y + row_i * cell_h

                    rect = pygame.Rect(x, y, 35, 35)
                    if rect.collidepoint(mx, my):
                        chosen_color = col

                # Выбор сложности
                y = 360 + 70
                for name, spd in difficulties.items():
                    rect = pygame.Rect(100, y, 150, 35)
                    if rect.collidepoint(mx, my):
                        chosen_speed = spd
                    y += 45

            # ENTER = START
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop(chosen_color, chosen_speed)


main()
