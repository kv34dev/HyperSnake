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

#МЕНЮ НАСТРОЕК
snake_colors = {
    "Mint": (120, 255, 200),
    "Neon": (57, 255, 20),
    "Purple": (180, 90, 255),
    "Orange": (255, 150, 60)
}

difficulties = {
    "Easy": 7,
    "Normal": 12,
    "Hard": 17,
    "Ultra": 25
}

chosen_color = list(snake_colors.values())[0]
chosen_speed = list(difficulties.values())[1]


def draw_rounded_rect(surface, color, rect, radius=12):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_menu(selected_color, selected_speed):
    screen.fill((14, 14, 18))

    #Заголовок
    title = FONT_TITLE.render("HyperSnake", True, (240, 240, 255))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))

    #Карточка выбора цвета
    color_card = pygame.Rect(60, 150, 580, 180)
    draw_rounded_rect(screen, (25, 25, 32), color_card, 18)

    section_title = FONT_SECTION.render("Snake Color", True, (230, 230, 230))
    screen.blit(section_title, (color_card.x + 20, color_card.y + 10))

    y_offset = color_card.y + 70
    x_offset = color_card.x + 40

    for name, col in snake_colors.items():
        box = pygame.Rect(x_offset, y_offset, 35, 35)
        pygame.draw.rect(screen, col, box, border_radius=8)

        label = FONT_ITEM.render(name, True, (230, 230, 230))
        screen.blit(label, (x_offset + 50, y_offset + 5))

        if col == selected_color:
            pygame.draw.rect(screen, (255, 255, 255), box, 3, border_radius=8)

        y_offset += 50

    #Карточка выбора сложности
    diff_card = pygame.Rect(60, 360, 580, 180)
    draw_rounded_rect(screen, (25, 25, 32), diff_card, 18)

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

    #Кнопка Start
    start_rect = pygame.Rect(WIDTH//2 - 120, 580, 240, 65)
    draw_rounded_rect(screen, (70, 145, 255), start_rect, 20)
    start_txt = FONT_BTN.render("START", True, (255, 255, 255))
    screen.blit(start_txt, (start_rect.x + 70, start_rect.y + 14))

    return start_rect


#  ИГРА
def game_loop(snake_color, speed):
    clock = pygame.time.Clock()

    snake = [(WIDTH//2, HEIGHT//2)]
    dx, dy = CELL, 0
    food = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))

    game_over = False

    while True:  # остаёмся в цикле до выхода
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP and dy == 0:
                        dx, dy = 0, -CELL
                    elif event.key == pygame.K_DOWN and dy == 0:
                        dx, dy = 0, CELL
                    elif event.key == pygame.K_LEFT and dx == 0:
                        dx, dy = -CELL, 0
                    elif event.key == pygame.K_RIGHT and dx == 0:
                        dx, dy = CELL, 0

                if game_over and event.key == pygame.K_r:
                    return  # restart

        if not game_over:
            x, y = snake[0]
            new_head = (x + dx, y + dy)

            if (new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in snake):
                game_over = True

            snake.insert(0, new_head)

            if new_head == food:
                food = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
            else:
                snake.pop()

        #render
        screen.fill((20, 20, 28))

        pygame.draw.rect(screen, (255, 70, 70), (*food, CELL, CELL), border_radius=6)

        for x, y in snake:
            pygame.draw.rect(screen, snake_color, (x, y, CELL, CELL), border_radius=6)

        if game_over:
            txt = FONT_GAMEOVER.render("GAME OVER", True, (255, 100, 100))
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 70))

            restart_txt = FONT_MED.render("Press R to Restart", True, (235, 235, 235))
            screen.blit(restart_txt, (WIDTH//2 - restart_txt.get_width()//2, HEIGHT//2))

        pygame.display.flip()
        clock.tick(speed)


#ГЛАВНОЕ МЕНЮ
def main():
    global chosen_color, chosen_speed
    while True:
        start_button = draw_menu(chosen_color, chosen_speed)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # START
                if start_button.collidepoint(mx, my):
                    game_loop(chosen_color, chosen_speed)

                # Выбор цвета
                y = 150 + 70
                x = 60 + 40
                for name, col in snake_colors.items():
                    rect = pygame.Rect(x, y, 35, 35)
                    if rect.collidepoint(mx, my):
                        chosen_color = col
                    y += 50

                # Выбор сложности
                y = 360 + 70
                for name, spd in difficulties.items():
                    rect = pygame.Rect(60 + 40, y, 150, 35)
                    if rect.collidepoint(mx, my):
                        chosen_speed = spd
                    y += 45


main()
