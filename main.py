import pygame
import sys
import random
import pygame_menu

pygame.init()

bgImg = pygame.image.load("just_white_background.jpg")

# colors
FRAME_COLOR = (216, 191, 222)  # pale purple
WHITE = (255, 255, 255)
HEADER_COLOR = (195, 155, 204)
PURPLE = (205, 147, 219)  # 205, 147, 219
SNAKE_COLOR = (139, 59, 155)
FOOD_COLOR = (139, 59, 155)
BLACK = (0, 0, 0)

# blocks
BLOCK_COUNT = 20
BLOCK_SIZE = 20

# margins
BLOCK_MARGIN = 2
HEADER_MARGIN = 70

size = [BLOCK_SIZE * BLOCK_COUNT + 2 * BLOCK_SIZE + BLOCK_MARGIN * BLOCK_COUNT,
        BLOCK_SIZE * BLOCK_COUNT + 2 * BLOCK_SIZE + BLOCK_MARGIN * BLOCK_SIZE + HEADER_MARGIN]

print(size)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake Game")
timer = pygame.time.Clock()
textFont = pygame.font.SysFont('courier', 24)

class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < BLOCK_SIZE and 0 <= self.y < BLOCK_SIZE

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y

def get_random_empty_block():
    x = random.randint(0, BLOCK_COUNT - 1)
    y = random.randint(0, BLOCK_COUNT - 1)
    empty_block = SnakeBlock(x, y)
    while empty_block in snake_blocks:
        empty_block.x = random.randint(0, BLOCK_COUNT - 1)
        empty_block.y = random.randint(0, BLOCK_COUNT - 1)
    return empty_block

def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [BLOCK_SIZE + column * BLOCK_SIZE + BLOCK_MARGIN * (column + 1),
                                     HEADER_MARGIN + BLOCK_SIZE + row * BLOCK_SIZE + BLOCK_MARGIN * (row + 1),
                                     BLOCK_SIZE,
                                     BLOCK_SIZE])

def start_the_game():

    def get_random_empty_block():
        x = random.randint(0, BLOCK_COUNT - 1)
        y = random.randint(0, BLOCK_COUNT - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, BLOCK_COUNT - 1)
            empty_block.y = random.randint(0, BLOCK_COUNT - 1)
        return empty_block

    snake_blocks = [SnakeBlock(9, 3), SnakeBlock(9, 4), SnakeBlock(9, 5)]
    food = get_random_empty_block()
    d_row = buf_row = 0
    d_column = buf_column = 1
    score = 0
    speed = 1

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exit")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_column != 0:
                    buf_row = -1
                    buf_column = 0
                elif event.key == pygame.K_DOWN and d_column != 0:
                    buf_row = 1
                    buf_column = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_column = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_column = 1

        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        score_total = textFont.render(f"Score: {score}", 0, BLACK)
        speed_label = textFont.render(f"Speed: {speed}", 0, BLACK)
        screen.blit(speed_label, (250, 20))
        screen.blit(score_total, (20, 20))

        for row in range(BLOCK_COUNT):
            for column in range(BLOCK_COUNT):
                if (row + column) % 2 == 0:
                    color = PURPLE
                else:
                    color = WHITE

                    draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            print("Game Over")
            break
            # pygame.quit()
            # sys.exit()

        draw_block(FOOD_COLOR, food.x, food.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)


        pygame.display.flip()

        if food == head:
            score += 1
            speed = score // 5 + 1
            snake_blocks.append(food)
            food = get_random_empty_block()

        d_row = buf_row
        d_column = buf_column
        new_head = SnakeBlock(head.x + d_row, head.y + d_column)

        if new_head in snake_blocks:
            print('crashed yourself')
            break
            # pygame.quit()
            # sys.exit()

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        timer.tick(3 + speed)

# game menu


menu = pygame_menu.Menu(220, 300, 'Snake Game',
                       theme=pygame_menu.themes.THEME_SOLARIZED)

menu.add_button('Play', start_the_game)

while True:

    screen.blit(bgImg, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()

